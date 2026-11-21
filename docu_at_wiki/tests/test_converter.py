from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from qspdocuwiki.config import ConverterConfig, ImageRule, load_config
from qspdocuwiki.converter import Converter
from qspdocuwiki.errors import ConversionError
from qspdocuwiki.markdown import DokuWikiRenderer
from qspdocuwiki.state import load_state


def _config(root: Path) -> ConverterConfig:
    source_root = root / "docs"
    (source_root / "section").mkdir(parents=True)
    return ConverterConfig(
        config_path=root / "config.toml",
        source_root=source_root,
        source_sections=("section",),
        output_dir=root / "output",
        state_file=root / ".state" / "hashes.json",
        pages={
            "section/guide.mdx": "help:guide",
            "section/peer.mdx": "help:peer",
        },
        excluded_pages={},
        images={},
    )


class RendererTests(unittest.TestCase):
    def test_renders_structures_and_mapped_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = _config(root)
            (config.source_root / "section" / "peer.mdx").write_text(
                "# Peer page {#peer}\n", encoding="utf-8"
            )
            config.pages["section/start.mdx"] = "start"
            source = """---
title: Guide
---
# Guide {#guide}

Text with **bold**, `inline code`, [peer](peer.mdx#peer), and [root](start.mdx).

- first
  - nested

1. ordered
2. parent:
  - indented child

```qsp
pl 'hello'
```

| Name | Value |
| ---- | ----- |
| one  | two   |

Footnote[^note].

[^note]: Footnote text.
"""
            rendered = DokuWikiRenderer(config).render("section/guide.mdx", source)

            self.assertIn("====== Guide ======", rendered)
            self.assertIn("**bold**", rendered)
            self.assertIn("''%%inline code%%''", rendered)
            self.assertIn("[[help:peer#Peer page|peer]]", rendered)
            self.assertIn("[[:start|root]]", rendered)
            self.assertIn("  * first\n    * nested", rendered)
            self.assertIn("  - ordered\n  - parent:\n    * indented child", rendered)
            self.assertIn("<sxh qsp>\npl 'hello'\n</sxh>", rendered)
            self.assertIn("^ Name ^ Value ^", rendered)
            self.assertIn("| one | two |", rendered)
            self.assertIn("Footnote((Footnote text.))", rendered)

    def test_rejects_unmapped_image(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = _config(root)
            with self.assertRaises(ConversionError):
                DokuWikiRenderer(config).render(
                    "section/guide.mdx",
                    "# Guide\n\n![missing](missing.png)\n",
                )

    def test_renders_explicit_image_mappings_and_widths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = _config(root)
            config.images["section/image.png"] = ImageRule(kind="dokuwiki", target="help:image.png", width=300)
            rendered = DokuWikiRenderer(config).render(
                "section/guide.mdx",
                "![Error image](image.png)\n",
            )

            self.assertIn("{{help:image.png?300|Error image}}", rendered)
            filename_alt = DokuWikiRenderer(config).render(
                "section/guide.mdx",
                "![image.png](image.png)\n",
            )
            self.assertIn("{{help:image.png?300}}", filename_alt)
            config.images["section/image.png"] = ImageRule(
                kind="external",
                url="https://images.example.test/error.png",
                width=500,
            )
            external_image = DokuWikiRenderer(config).render(
                "section/guide.mdx",
                "![Error image](image.png)\n",
            )
            self.assertIn(
                "[[https://images.example.test/error.png|"
                "{{https://images.example.test/error.png?500|Error image}}]]",
                external_image,
            )

    def test_renders_vertical_and_horizontal_table_spans(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            config = _config(Path(temporary))
            rendered = DokuWikiRenderer(config).render(
                "section/guide.mdx",
                """| First | Second | Third |
| --- | --- | --- |
| A | ^ | C |
| Left | > | Right |
| Break | Before<br>after | End |
""",
            )

            self.assertIn("| A | ::: | C |", rendered)
            self.assertIn("| Left | Right ||", rendered)
            self.assertIn("| Break | Before\\\\ after | End |", rendered)

    def test_rejects_horizontal_span_without_a_right_cell(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            config = _config(Path(temporary))
            with self.assertRaisesRegex(ConversionError, "without a cell to the right"):
                DokuWikiRenderer(config).render(
                    "section/guide.mdx",
                    "| First | Second |\n| --- | --- |\n| A | > |\n",
                )


class IncrementalConversionTests(unittest.TestCase):
    def test_validates_and_converts_markdown_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root = root / "docs"
            source_path = source_root / "section" / "guide.md"
            source_path.parent.mkdir(parents=True)
            source_path.write_text("# Guide\n\nMarkdown source.\n", encoding="utf-8")
            config_path = root / "config.toml"
            config_path.write_text(
                'source_root = "docs"\n'
                'source_sections = ["section"]\n'
                'output_dir = "output"\n'
                'state_file = ".state/hashes.json"\n'
                '\n[pages]\n'
                '"section/guide.md" = "help:guide"\n'
                '\n[images]\n',
                encoding="utf-8",
            )
            config = load_config(config_path)
            converter = Converter(config)

            validation = converter.validate()
            conversion = converter.convert()

            self.assertEqual(validation.warnings, [])
            self.assertEqual(validation.errors, [])
            self.assertEqual(conversion.warnings, [])
            self.assertEqual(conversion.errors, [])
            self.assertEqual(conversion.converted, 1)
            self.assertIn(
                "Markdown source.",
                (config.output_dir / "help" / "guide.dokuwiki").read_text(encoding="utf-8"),
            )

    def test_skips_unchanged_sources_and_reconverts_edits(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = _config(root)
            source_path = config.source_root / "section" / "guide.mdx"
            source_path.write_text("# Guide\n\nOriginal text.\n", encoding="utf-8")
            (config.source_root / "section" / "peer.mdx").write_text(
                "# Peer\n", encoding="utf-8"
            )
            converter = Converter(config)

            first = converter.convert()
            second = converter.convert()
            source_path.write_text("# Guide\n\nUpdated text.\n", encoding="utf-8")
            third = converter.convert()

            self.assertEqual((first.converted, first.skipped), (2, 0))
            self.assertEqual((second.converted, second.skipped), (0, 2))
            self.assertEqual((third.converted, third.skipped), (1, 1))
            self.assertIn("Updated text.", (config.output_dir / "help" / "guide.dokuwiki").read_text(encoding="utf-8"))

    def test_failed_conversion_preserves_previous_output_and_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = _config(root)
            source_path = config.source_root / "section" / "guide.mdx"
            source_path.write_text("# Guide\n\nOriginal text.\n", encoding="utf-8")
            (config.source_root / "section" / "peer.mdx").write_text("# Peer\n", encoding="utf-8")
            converter = Converter(config)
            converter.convert()
            output_path = config.output_dir / "help" / "guide.dokuwiki"
            original_output = output_path.read_text(encoding="utf-8")
            original_entry = load_state(config.state_file).entries["section/guide.mdx"]

            source_path.write_text("<div>raw HTML</div>\n", encoding="utf-8")
            report = converter.convert()

            self.assertTrue(report.errors)
            self.assertEqual(output_path.read_text(encoding="utf-8"), original_output)
            self.assertEqual(
                load_state(config.state_file).entries["section/guide.mdx"],
                original_entry,
            )


if __name__ == "__main__":
    unittest.main()
