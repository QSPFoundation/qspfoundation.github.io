from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath
import re
import tomllib
from typing import Any
from urllib.parse import urlsplit

from .errors import ConfigError


@dataclass(frozen=True)
class ExcludedPage:
    target: str
    reason: str


@dataclass(frozen=True)
class ImageRule:
    kind: str
    target: str | None = None
    url: str | None = None
    width: int | None = None
    caption: str | None = None


@dataclass(frozen=True)
class ConverterConfig:
    config_path: Path
    source_root: Path
    source_sections: tuple[str, ...]
    output_dir: Path
    state_file: Path
    pages: dict[str, str]
    excluded_pages: dict[str, ExcludedPage]
    images: dict[str, ImageRule]

    @property
    def link_targets(self) -> dict[str, str]:
        targets = dict(self.pages)
        targets.update({key: value.target for key, value in self.excluded_pages.items()})
        return targets

    def source_path(self, source_key: str) -> Path:
        return _resolve_source_key(self.source_root, source_key)


_PAGE_ID_RE = re.compile(r"^:?[^\s:/\\?#]+(?::[^\s:/\\?#]+)*$")
_MARKDOWN_SOURCE_SUFFIXES = {".md", ".mdx"}


def _required_string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ConfigError(f"Expected a non-empty string for `{key}`.")
    return value


def _validate_relative_key(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value:
        raise ConfigError(f"{label} must be a non-empty POSIX relative path.")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ConfigError(f"{label} must stay within its configured root: {value!r}.")
    if path.as_posix() != value:
        raise ConfigError(f"{label} is not normalized: {value!r}.")
    return value


def _resolve_config_path(config_dir: Path, value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ConfigError(f"Expected a relative path for `{label}`.")
    path = Path(value)
    if path.is_absolute():
        raise ConfigError(f"`{label}` must be relative to the config directory.")
    resolved = (config_dir / path).resolve()
    if not resolved.is_relative_to(config_dir):
        raise ConfigError(f"`{label}` must stay within the config directory.")
    return resolved


def _validate_page_id(value: Any, label: str) -> str:
    if not isinstance(value, str) or not _PAGE_ID_RE.fullmatch(value):
        raise ConfigError(f"Invalid DokuWiki page/media ID for {label}: {value!r}.")
    parts = value.lstrip(":").split(":")
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise ConfigError(f"Invalid DokuWiki page/media ID for {label}: {value!r}.")
    return value


def _parse_pages(raw: Any) -> dict[str, str]:
    if not isinstance(raw, dict):
        raise ConfigError("`pages` must be a TOML table.")
    pages: dict[str, str] = {}
    for source, target in raw.items():
        key = _validate_markdown_source_key(source, "Page source")
        pages[key] = _validate_page_id(target, f"page {key!r}")
    return pages


def _parse_excluded_pages(raw: Any) -> dict[str, ExcludedPage]:
    if not isinstance(raw, dict):
        raise ConfigError("`excluded_pages` must be a TOML table.")
    excluded: dict[str, ExcludedPage] = {}
    for source, details in raw.items():
        key = _validate_markdown_source_key(source, "Excluded page source")
        if not isinstance(details, dict):
            raise ConfigError(f"`excluded_pages.{key}` must be a TOML table.")
        target = _validate_page_id(details.get("target"), f"excluded page {key!r}")
        reason = details.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise ConfigError(f"`excluded_pages.{key}.reason` must be a non-empty string.")
        excluded[key] = ExcludedPage(target=target, reason=reason)
    return excluded


def _parse_images(raw: Any) -> dict[str, ImageRule]:
    if not isinstance(raw, dict):
        raise ConfigError("`images` must be a TOML table.")
    images: dict[str, ImageRule] = {}
    for source, details in raw.items():
        key = _validate_relative_key(source, "Image source")
        if not isinstance(details, dict):
            raise ConfigError(f"`images.{key}` must be a TOML table.")
        kind = details.get("kind")
        width = details.get("width")
        caption = details.get("caption")
        if caption is not None and not isinstance(caption, str):
            raise ConfigError(f"`images.{key}.caption` must be a string.")
        if width is not None and (not isinstance(width, int) or isinstance(width, bool) or width <= 0):
            raise ConfigError(f"`images.{key}.width` must be a positive integer.")
        if kind == "dokuwiki":
            target = _validate_page_id(details.get("target"), f"image {key!r}")
            images[key] = ImageRule(kind=kind, target=target, width=width, caption=caption)
        elif kind == "external":
            url = details.get("url")
            if not isinstance(url, str):
                raise ConfigError(f"`images.{key}.url` must be a URL.")
            parsed = urlsplit(url)
            if parsed.scheme != "https" or not parsed.netloc:
                raise ConfigError(f"`images.{key}.url` must be an absolute HTTPS URL.")
            images[key] = ImageRule(kind=kind, url=url, width=width, caption=caption)
        else:
            raise ConfigError(f"Unsupported image kind for {key!r}: {kind!r}.")
    return images


def load_config(path: Path) -> ConverterConfig:
    config_path = path.resolve()
    try:
        raw = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ConfigError(f"Cannot read config {config_path}: {exc}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"Invalid TOML in {config_path}: {exc}") from exc

    config_dir = config_path.parent.resolve()
    source_root_value = raw.get("source_root")
    if not isinstance(source_root_value, str) or not source_root_value:
        raise ConfigError("Expected a relative path for `source_root`.")
    source_root_path = Path(source_root_value)
    if source_root_path.is_absolute():
        raise ConfigError("`source_root` must be relative to the config directory.")
    source_root = (config_dir / source_root_path).resolve()
    sections = raw.get("source_sections")
    if (
        not isinstance(sections, list)
        or not sections
        or any(not isinstance(item, str) or not item or "/" in item or "\\" in item for item in sections)
        or len(set(sections)) != len(sections)
    ):
        raise ConfigError("`source_sections` must be a non-empty array of unique directory names.")

    output_dir = _resolve_config_path(config_dir, raw.get("output_dir"), "output_dir")
    state_file = _resolve_config_path(config_dir, raw.get("state_file"), "state_file")
    pages = _parse_pages(raw.get("pages"))
    excluded_pages = _parse_excluded_pages(raw.get("excluded_pages", {}))
    images = _parse_images(raw.get("images"))

    if set(pages) & set(excluded_pages):
        raise ConfigError("A source cannot be both active and excluded.")
    targets = list(pages.values()) + [page.target for page in excluded_pages.values()]
    if len(targets) != len(set(targets)):
        raise ConfigError("DokuWiki page IDs must be unique across active and excluded sources.")

    return ConverterConfig(
        config_path=config_path,
        source_root=source_root,
        source_sections=tuple(sections),
        output_dir=output_dir,
        state_file=state_file,
        pages=pages,
        excluded_pages=excluded_pages,
        images=images,
    )


def validate_config(config: ConverterConfig) -> list[str]:
    warnings: list[str] = []
    configured_sources = set(config.pages) | set(config.excluded_pages)
    discovered_sources: set[str] = set()

    for section in config.source_sections:
        section_path = (config.source_root / section).resolve()
        if not section_path.is_relative_to(config.source_root):
            raise ConfigError(f"Source section escapes source_root: {section!r}.")
        if not section_path.is_dir():
            warnings.append(f"Source section does not exist: {section_path}")
            continue
        discovered_sources.update(
            path.relative_to(config.source_root).as_posix()
            for path in section_path.rglob("*")
            if path.is_file() and path.suffix.casefold() in _MARKDOWN_SOURCE_SUFFIXES
        )

    for source in sorted(configured_sources - discovered_sources):
        warnings.append(f"Configured source is missing; existing output will be kept: {source}")
    for source in sorted(discovered_sources - configured_sources):
        warnings.append(f"Unmapped source is skipped until configured or excluded: {source}")

    for source in sorted(config.images):
        if not config.source_path(source).is_file():
            warnings.append(f"Configured image is missing: {source}")
    if config.output_dir == config.source_root or config.output_dir.is_relative_to(config.source_root):
        raise ConfigError("`output_dir` must not be inside the source documentation tree.")
    return warnings


def _resolve_source_key(source_root: Path, source_key: str) -> Path:
    key = _validate_relative_key(source_key, "Source path")
    resolved = (source_root / Path(*PurePosixPath(key).parts)).resolve()
    if not resolved.is_relative_to(source_root):
        raise ConfigError(f"Source path escapes source_root: {source_key!r}.")
    return resolved


def _validate_markdown_source_key(value: Any, label: str) -> str:
    key = _validate_relative_key(value, label)
    if PurePosixPath(key).suffix.casefold() not in _MARKDOWN_SOURCE_SUFFIXES:
        raise ConfigError(f"{label} must have a `.md` or `.mdx` extension.")
    return key
