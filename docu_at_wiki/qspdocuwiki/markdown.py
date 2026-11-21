from __future__ import annotations

from dataclasses import dataclass, field
import re
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.footnote import footnote_plugin

from .config import ConverterConfig
from .errors import ConversionError


_ANCHOR_RE = re.compile(r"\s+\{#([^{}\s]+)\}\s*$")
_SUPPORTED_CODE_LANGUAGES = {"qsp", "text", "html", "js"}
_WIKI_TEXT_ESCAPES = (
    ("**", "&#42;&#42;"),
    ("//", "&#47;&#47;"),
    ("__", "&#95;&#95;"),
    ("''", "&#39;&#39;"),
    ("[[", "&#91;["),
    ("{{", "&#123;{"),
    ("%%", "&#37;&#37;"),
    ("|", "&#124;"),
)


@dataclass
class _Node:
    token: Token | None
    children: list[_Node] = field(default_factory=list)


@dataclass
class _Document:
    tree: _Node
    anchors: dict[str, str]
    footnotes: dict[int, list[Token]]
    source_lines: list[str]


def _strip_front_matter(source: str, source_key: str) -> str:
    lines = source.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return source
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "".join(lines[index + 1 :])
    raise ConversionError(f"{source_key}: opening YAML front matter has no closing `---`.")


def _build_tree(tokens: list[Token], source_key: str) -> _Node:
    root = _Node(token=None)
    stack = [root]
    for token in tokens:
        if token.nesting == 1:
            node = _Node(token=token)
            stack[-1].children.append(node)
            stack.append(node)
        elif token.nesting == -1:
            if len(stack) == 1:
                raise ConversionError(f"{source_key}: unexpected closing Markdown token {token.type!r}.")
            open_type = stack[-1].token.type if stack[-1].token else ""
            expected = open_type.removesuffix("_open") + "_close"
            if token.type != expected:
                raise ConversionError(
                    f"{source_key}: mismatched Markdown tokens {open_type!r} and {token.type!r}."
                )
            stack.pop()
        else:
            stack[-1].children.append(_Node(token=token))
    if len(stack) != 1:
        dangling = stack[-1].token.type if stack[-1].token else "unknown"
        raise ConversionError(f"{source_key}: unclosed Markdown token {dangling!r}.")
    return root


def _inline_child(node: _Node) -> Token | None:
    return next(
        (child.token for child in node.children if child.token and child.token.type == "inline"),
        None,
    )


class DokuWikiRenderer:
    def __init__(self, config: ConverterConfig) -> None:
        self.config = config
        self.parser = MarkdownIt("default", {"html": True}).use(footnote_plugin).enable("table")
        self._documents: dict[str, _Document] = {}
        self._current_document: _Document | None = None
        self._current_source = ""
        self._current_footnotes: dict[int, str] = {}

    def render(self, source_key: str, source: str) -> str:
        document = self._parse_document(source_key, source)
        self._documents[source_key] = document
        self._current_document = document
        self._current_source = source_key
        self._current_footnotes = self._render_footnotes(document)
        rendered = self._render_blocks(document.tree.children)
        return rendered.strip() + "\n"

    def _parse_document(self, source_key: str, source: str) -> _Document:
        body = _strip_front_matter(source, source_key)
        tree = _build_tree(self.parser.parse(body), source_key)
        anchors: dict[str, str] = {}
        footnotes: dict[int, list[Token]] = {}
        for node in self._walk(tree):
            token = node.token
            if token is None:
                continue
            if token.type == "heading_open":
                inline = _inline_child(node)
                if inline is not None:
                    anchor_id, heading_text = self._heading_details(inline, source_key)
                    if anchor_id:
                        if anchor_id in anchors:
                            raise ConversionError(
                                f"{source_key}: duplicate heading anchor {anchor_id!r}."
                            )
                        anchors[anchor_id] = heading_text
            elif token.type == "footnote_open":
                footnote_id = token.meta.get("id")
                if isinstance(footnote_id, int):
                    footnotes[footnote_id] = [
                        child
                        for item in self._walk(node)
                        if item.token and item.token.type == "inline"
                        for child in (item.token.children or [])
                    ]
        return _Document(
            tree=tree,
            anchors=anchors,
            footnotes=footnotes,
            source_lines=body.splitlines(),
        )

    @staticmethod
    def _walk(node: _Node) -> Iterable[_Node]:
        yield node
        for child in node.children:
            yield from DokuWikiRenderer._walk(child)

    def _heading_details(self, inline: Token, source_key: str) -> tuple[str | None, str]:
        match = _ANCHOR_RE.search(inline.content)
        content = inline.content[: match.start()].rstrip() if match else inline.content.strip()
        parsed = self.parser.parseInline(content, {})
        children = parsed[0].children or [] if parsed else []
        return (match.group(1) if match else None, self._plain_inline(children, source_key))

    def _render_footnotes(self, document: _Document) -> dict[int, str]:
        result: dict[int, str] = {}
        for footnote_id, tokens in document.footnotes.items():
            result[footnote_id] = self._render_inline(tokens)
        return result

    def _plain_inline(self, tokens: list[Token], source_key: str) -> str:
        parts: list[str] = []
        for token in tokens:
            if token.type in {"text", "code_inline"}:
                parts.append(token.content)
            elif token.type == "image":
                parts.append(token.content)
            elif token.type in {"softbreak", "hardbreak"}:
                parts.append(" ")
            elif token.type == "html_inline":
                raise ConversionError(f"{source_key}: raw HTML in a heading is unsupported.")
        return re.sub(r"\s+", " ", "".join(parts)).strip()

    def _render_blocks(self, nodes: list[_Node]) -> str:
        blocks: list[str] = []
        previous_was_list = False
        for node in nodes:
            token = node.token
            if token is None:
                continue
            kind = token.type
            if kind == "heading_open":
                inline = _inline_child(node)
                if inline is None:
                    raise ConversionError(f"{self._current_source}: heading has no inline content.")
                match = _ANCHOR_RE.search(inline.content)
                content = inline.content[: match.start()].rstrip() if match else inline.content
                parsed = self.parser.parseInline(content, {})
                children = parsed[0].children or [] if parsed else []
                level = int(token.tag[1:])
                if level > 5:
                    raise ConversionError(
                        f"{self._current_source}: DokuWiki does not support Markdown H{level} headings."
                    )
                marker = "=" * (7 - level)
                blocks.append(f"{marker} {self._render_inline(children)} {marker}")
            elif kind == "paragraph_open":
                if token.hidden:
                    continue
                inline = _inline_child(node)
                if inline is not None:
                    blocks.append(self._render_inline(inline.children or []))
            elif kind in {"bullet_list_open", "ordered_list_open"}:
                depth = 1 if previous_was_list and self._list_indent(token) > 0 else 0
                rendered_list = self._render_list(node, depth=depth)
                if depth and blocks:
                    blocks[-1] = f"{blocks[-1]}\n{rendered_list}"
                else:
                    blocks.append(rendered_list)
                previous_was_list = True
            elif kind == "blockquote_open":
                quoted = self._render_blocks(node.children)
                blocks.append("\n".join(f"> {line}" if line else ">" for line in quoted.splitlines()))
            elif kind == "fence":
                blocks.append(self._render_fence(token))
            elif kind == "code_block":
                blocks.append(self._render_code(token.content, ""))
            elif kind == "table_open":
                blocks.append(self._render_table(node))
            elif kind == "hr":
                blocks.append("----")
            elif kind == "footnote_block_open":
                continue
            elif kind in {"inline", "footnote_anchor"}:
                continue
            elif kind == "html_block":
                raise ConversionError(f"{self._current_source}: raw HTML blocks are unsupported.")
            elif kind.endswith("_close") or kind in {"list_item_open", "table_row_open"}:
                continue
            else:
                raise ConversionError(
                    f"{self._current_source}: unsupported Markdown block token {kind!r}."
                )
            if kind not in {"bullet_list_open", "ordered_list_open"}:
                previous_was_list = False
        return "\n\n".join(block for block in blocks if block)

    def _list_indent(self, token: Token) -> int:
        if (
            self._current_document is None
            or token.map is None
            or token.map[0] >= len(self._current_document.source_lines)
        ):
            return 0
        line = self._current_document.source_lines[token.map[0]]
        return len(line) - len(line.lstrip(" "))

    def _render_list(self, node: _Node, depth: int) -> str:
        marker = "*" if node.token and node.token.type == "bullet_list_open" else "-"
        lines: list[str] = []
        for item in node.children:
            if not item.token or item.token.type != "list_item_open":
                continue
            item_lines: list[str] = []
            nested_lines: list[str] = []
            for child in item.children:
                child_token = child.token
                if child_token is None:
                    continue
                if child_token.type == "paragraph_open":
                    inline = _inline_child(child)
                    if inline is not None:
                        item_lines.append(self._render_inline(inline.children or []))
                elif child_token.type in {"bullet_list_open", "ordered_list_open"}:
                    nested_lines.extend(self._render_list(child, depth + 1).splitlines())
                else:
                    rendered = self._render_blocks([child])
                    if rendered:
                        item_lines.extend(rendered.splitlines())
            indent = "  " * (depth + 1)
            continuation = "  " * (depth + 2)
            if item_lines:
                lines.append(f"{indent}{marker} {item_lines[0]}")
                lines.extend(f"{continuation}{line}" for line in item_lines[1:])
            else:
                lines.append(f"{indent}{marker}")
            lines.extend(nested_lines)
        return "\n".join(lines)

    def _render_table(self, node: _Node) -> str:
        rows: list[tuple[bool, list[tuple[str, str]]]] = []
        for row in self._walk(node):
            if row.token is None or row.token.type != "tr_open":
                continue
            cells = [
                cell
                for cell in row.children
                if cell.token and cell.token.type in {"th_open", "td_open"}
            ]
            cells_for_output: list[tuple[str, str]] = []
            for cell in cells:
                inline = _inline_child(cell)
                raw_content = inline.content.strip() if inline else ""
                if raw_content == "^":
                    cells_for_output.append(("up", ""))
                elif raw_content == ">":
                    cells_for_output.append(("right", ""))
                else:
                    rendered = self._render_inline(inline.children or []) if inline else ""
                    cells_for_output.append(("text", rendered))
            is_header = any(cell.token and cell.token.type == "th_open" for cell in cells)
            rows.append((is_header, cells_for_output))

        rendered_rows: list[str] = []
        for row_number, (is_header, cells) in enumerate(rows, start=1):
            output_cells: list[tuple[str, int]] = []
            cell_index = 0
            while cell_index < len(cells):
                kind, content = cells[cell_index]
                if kind == "up":
                    if row_number == 1:
                        raise ConversionError(
                            f"{self._current_source}: table row {row_number}, cell {cell_index + 1} "
                            "uses `^` without a cell above."
                        )
                    output_cells.append((":::", 1))
                    cell_index += 1
                elif kind == "right":
                    if cell_index + 1 == len(cells):
                        raise ConversionError(
                            f"{self._current_source}: table row {row_number}, cell {cell_index + 1} "
                            "uses `>` without a cell to the right."
                        )
                    right_kind, right_content = cells[cell_index + 1]
                    if right_kind != "text":
                        raise ConversionError(
                            f"{self._current_source}: table row {row_number}, cell {cell_index + 1} "
                            "uses `>` before another span marker."
                        )
                    output_cells.append((right_content, 2))
                    cell_index += 2
                else:
                    output_cells.append((content, 1))
                    cell_index += 1

            delimiter = "^" if is_header else "|"
            row = delimiter
            for content, colspan in output_cells:
                row += f" {content} " + delimiter * colspan
            rendered_rows.append(row)
        return "\n".join(rendered_rows)

    def _render_fence(self, token: Token) -> str:
        info = token.info.strip().split()
        language = info[0].lower() if info else ""
        if language and language not in _SUPPORTED_CODE_LANGUAGES:
            raise ConversionError(
                f"{self._current_source}: unsupported fenced code language {language!r}."
            )
        return self._render_code(token.content, language)

    @staticmethod
    def _render_code(content: str, language: str) -> str:
        tag = f" {language}" if language else ""
        body = content.rstrip("\r\n").replace("</sxh", "&lt;/sxh")
        return f"<sxh{tag}>\n{body}\n</sxh>"

    def _render_inline(self, tokens: list[Token]) -> str:
        output: list[str] = []
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token.type in {"strong_open", "em_open", "s_open", "link_open"}:
                close_index = self._find_inline_close(tokens, index)
                if close_index is None:
                    raise ConversionError(f"{self._current_source}: unclosed inline token {token.type!r}.")
                inner = self._render_inline(tokens[index + 1 : close_index])
                if token.type == "strong_open":
                    output.append(f"**{inner}**")
                elif token.type == "em_open":
                    output.append(f"//{inner}//")
                elif token.type == "s_open":
                    output.append(f"<del>{inner}</del>")
                else:
                    href = token.attrs.get("href", "")
                    output.append(self._render_link(href, inner))
                index = close_index + 1
                continue
            if token.type in {"strong_close", "em_close", "s_close", "link_close"}:
                index += 1
                continue
            if token.type == "text":
                output.append(self._escape_text(token.content))
            elif token.type == "code_inline":
                inline_code = token.content.replace("''", "&#39;&#39;").replace("%%", "&#37;&#37;")
                output.append(f"''%%{inline_code}%%''")
            elif token.type == "image":
                output.append(self._render_image(token.attrs.get("src", ""), token.content))
            elif token.type == "softbreak":
                output.append(" ")
            elif token.type == "hardbreak":
                output.append("\\\\\n")
            elif token.type == "footnote_ref":
                footnote_id = token.meta.get("id")
                if not isinstance(footnote_id, int) or footnote_id not in self._current_footnotes:
                    raise ConversionError(f"{self._current_source}: footnote reference has no definition.")
                output.append(f"(({self._current_footnotes[footnote_id]}))")
            elif token.type == "html_inline" and re.fullmatch(
                r"<br\s*/?>", token.content, flags=re.IGNORECASE
            ):
                output.append("\\\\ ")
            elif token.type in {"html_inline", "html_block"}:
                raise ConversionError(f"{self._current_source}: raw HTML is unsupported.")
            elif token.type in {"footnote_anchor"}:
                index += 1
                continue
            else:
                raise ConversionError(
                    f"{self._current_source}: unsupported inline Markdown token {token.type!r}."
                )
            index += 1
        return "".join(output)

    @staticmethod
    def _find_inline_close(tokens: list[Token], start: int) -> int | None:
        opening = tokens[start]
        closing_type = opening.type.removesuffix("_open") + "_close"
        depth = 0
        for index in range(start + 1, len(tokens)):
            token = tokens[index]
            if token.type == opening.type:
                depth += 1
            elif token.type == closing_type:
                if depth == 0:
                    return index
                depth -= 1
        return None

    def _render_link(self, href: str, label: str) -> str:
        if href.startswith("DOCLINK::index::"):
            anchor_id = href.split("::", 2)[2]
            title = self._get_document(self._current_source).anchors.get(anchor_id)
            if title is None:
                raise ConversionError(
                    f"{self._current_source}: DOCLINK anchor {anchor_id!r} does not match a heading."
                )
            return self._doku_link(f"#{title}", label)

        parsed = urlsplit(href)
        if parsed.scheme in {"http", "https", "mailto"}:
            return self._doku_link(href, label)
        if parsed.scheme:
            raise ConversionError(f"{self._current_source}: unsupported link scheme {parsed.scheme!r}.")

        path_part = unquote(parsed.path)
        if path_part:
            current_path = self.config.source_path(self._current_source)
            destination = (current_path.parent / path_part).resolve()
            if not destination.is_relative_to(self.config.source_root):
                raise ConversionError(f"{self._current_source}: link escapes source_root: {href!r}.")
            destination_key = destination.relative_to(self.config.source_root).as_posix()
        else:
            destination_key = self._current_source

        target = self.config.link_targets.get(destination_key)
        if target is None:
            raise ConversionError(
                f"{self._current_source}: link target is not in `pages` or `excluded_pages`: {href!r}."
            )
        if ":" not in target and not target.startswith(":"):
            target = f":{target}"
        if parsed.fragment:
            anchor_id = unquote(parsed.fragment)
            title = self._get_document(destination_key).anchors.get(anchor_id)
            if title is None:
                raise ConversionError(
                    f"{self._current_source}: link fragment {anchor_id!r} does not match a heading in "
                    f"{destination_key}."
                )
            target = f"{target}#{title}"
        return self._doku_link(target, label)

    def _render_image(self, source: str, alt: str) -> str:
        parsed = urlsplit(source)
        if parsed.scheme:
            raise ConversionError(
                f"{self._current_source}: remote Markdown image must be explicitly mapped in config: {source!r}."
            )
        current_path = self.config.source_path(self._current_source)
        image_path = (current_path.parent / unquote(parsed.path)).resolve()
        if not image_path.is_relative_to(self.config.source_root):
            raise ConversionError(f"{self._current_source}: image path escapes source_root: {source!r}.")
        image_key = image_path.relative_to(self.config.source_root).as_posix()
        rule = self.config.images.get(image_key)
        if rule is None:
            raise ConversionError(
                f"{self._current_source}: image has no explicit mapping in config: {image_key}."
            )
        image_caption = rule.caption if rule.caption is not None else alt
        filename = Path(unquote(parsed.path)).name
        caption = (
            self._escape_text(image_caption)
            if image_caption and image_caption.strip().casefold() != filename.casefold()
            else ""
        )
        if rule.kind == "dokuwiki":
            width = f"?{rule.width}" if rule.width else ""
            suffix = f"|{caption}" if caption else ""
            return f"{{{{{rule.target}{width}{suffix}}}}}"
        if rule.kind == "external":
            sized_url = f"{rule.url}?{rule.width}" if rule.width else rule.url
            inner = f"{{{{{sized_url}{'|' + caption if caption else ''}}}}}"
            return f"[[{rule.url}|{inner}]]"
        raise ConversionError(f"{self._current_source}: unsupported image mapping kind {rule.kind!r}.")

    def _get_document(self, source_key: str) -> _Document:
        document = self._documents.get(source_key)
        if document is not None:
            return document
        path = self.config.source_path(source_key)
        try:
            source = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ConversionError(f"{source_key}: cannot read linked source: {exc}") from exc
        except UnicodeError as exc:
            raise ConversionError(f"{source_key}: linked source is not valid UTF-8: {exc}") from exc
        document = self._parse_document(source_key, source)
        self._documents[source_key] = document
        return document

    @staticmethod
    def _escape_text(value: str) -> str:
        escaped = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        for marker, replacement in _WIKI_TEXT_ESCAPES:
            escaped = escaped.replace(marker, replacement)
        return escaped

    @staticmethod
    def _doku_link(target: str, label: str) -> str:
        safe_target = target.replace("|", "%7C")
        safe_label = label.replace("|", "&#124;")
        return f"[[{safe_target}|{safe_label}]]" if safe_label else f"[[{safe_target}]]"
