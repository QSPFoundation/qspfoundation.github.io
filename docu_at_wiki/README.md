# Markdown to DokuWiki converter

The converter generates local DokuWiki pages from explicitly mapped Markdown
and MDX sources in `../docs/`. It does not publish to the wiki. Page IDs and image
mappings are maintained in [`config.toml`](config.toml); review the generated
files in `output/`.

For the workflow, source constraints, and instructions for adding pages and
media, see the [usage guide](USAGE.md).

## Requirements

- Python 3.11 or newer
- Internet access for the initial dependency installation

## Setup and use

Run these commands from `docu_at_wiki/`:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m qspdocuwiki validate
.\.venv\Scripts\python.exe -m qspdocuwiki convert
```

`validate` checks configured sources and reports unsupported markup without
writing pages. `convert` writes or updates changed pages in `output/`. The
second run skips unchanged pages. Use `--config path\to\config.toml` before
the subcommand to select a different configuration.

The local SHA-256 manifest is `.state/hashes.json`. Output and state are
intentionally ignored by Git. A failed conversion leaves that page's previous
output and recorded hash unchanged. If a source disappears or is removed from
the active map, its output is retained and a warning is printed.

## Mapping and supported content

Every source-to-page mapping belongs in `[pages]`; placeholder pages belong in
`[excluded_pages]` so links can still resolve without generating them. Images
must have an explicit entry in `[images]`, pointing to an existing DokuWiki
media ID or a confirmed external URL. Image mappings can set `width` and
override the source alt text with `caption` (an empty caption omits the label).

The renderer supports headings, paragraphs, lists, block quotes, inline
formatting, links, mapped images, fenced code (`qsp`, `text`, `html`, `js`),
tables, and footnotes. Fenced code uses the `<sxh>` syntax from the wiki
examples. Front matter and `{#anchor}` suffixes are omitted from
the generated article; the anchor IDs remain available for resolving internal
links. Unsupported raw HTML and code languages fail that page rather than
silently dropping content; inline `<br>` is converted to a DokuWiki line break.

Markdown tables are emitted with DokuWiki header/body delimiters and standard
cell spacing. A cell containing only `^` is converted to a vertical merge with
the cell above (`:::`). A cell containing only `>` merges with the cell on its
right; that right-hand cell's contents are placed in the merged DokuWiki cell.

Run the focused tests from this directory with:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
