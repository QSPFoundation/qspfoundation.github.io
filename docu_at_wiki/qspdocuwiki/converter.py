from __future__ import annotations

from dataclasses import dataclass, field, asdict
import hashlib
import json
from pathlib import Path

from . import __version__
from .config import ConverterConfig, validate_config
from .errors import ConfigError, ConversionError, StateError
from .markdown import DokuWikiRenderer
from .state import ConverterState, StateEntry, atomic_write_text, load_state, save_state


@dataclass
class ConversionReport:
    converted: int = 0
    skipped: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class Converter:
    def __init__(self, config: ConverterConfig) -> None:
        self.config = config
        self.renderer = DokuWikiRenderer(config)

    def validate(self) -> ConversionReport:
        report = ConversionReport(warnings=validate_config(self.config))
        for source_key in sorted(self.config.pages):
            source_path = self.config.source_path(source_key)
            if not source_path.is_file():
                continue
            try:
                source = source_path.read_text(encoding="utf-8")
                self.renderer.render(source_key, source)
            except (OSError, UnicodeError, ConversionError) as exc:
                report.errors.append(str(exc))
        return report

    def convert(self) -> ConversionReport:
        report = ConversionReport(warnings=validate_config(self.config))
        try:
            state = load_state(self.config.state_file)
        except StateError as exc:
            report.errors.append(str(exc))
            return report

        active_sources = set(self.config.pages)
        state_changed = False
        for source_key in sorted(set(state.entries) - active_sources):
            previous = state.entries.pop(source_key)
            reason = self.config.excluded_pages.get(source_key)
            status = f"excluded: {reason.reason}" if reason else "no longer configured"
            report.warnings.append(
                f"{source_key}: {status}; keeping {previous.output} and removing its hash entry."
            )
            state_changed = True

        if state_changed:
            try:
                save_state(self.config.state_file, state)
            except StateError as exc:
                report.errors.append(str(exc))
                return report

        signature = self._conversion_signature()
        for source_key, target in sorted(self.config.pages.items()):
            source_path = self.config.source_path(source_key)
            previous = state.entries.get(source_key)
            if not source_path.is_file():
                report.warnings.append(
                    f"{source_key}: source is missing; keeping the existing output and dropping its hash."
                )
                if state.entries.pop(source_key, None) is not None:
                    try:
                        save_state(self.config.state_file, state)
                    except StateError as exc:
                        report.errors.append(str(exc))
                        return report
                continue
            try:
                source_bytes = source_path.read_bytes()
                source_hash = hashlib.sha256(source_bytes).hexdigest()
                source_text = source_bytes.decode("utf-8")
            except (OSError, UnicodeError) as exc:
                report.errors.append(f"{source_key}: cannot read UTF-8 source: {exc}")
                continue

            output_path = self._output_path(target)
            output_relative = output_path.relative_to(self.config.output_dir).as_posix()
            if (
                previous is not None
                and previous.source_sha256 == source_hash
                and previous.conversion_signature == signature
                and previous.target == target
                and previous.output == output_relative
                and output_path.is_file()
            ):
                report.skipped += 1
                continue

            if previous is not None and previous.target != target:
                report.warnings.append(
                    f"{source_key}: target changed from {previous.target!r} to {target!r}; "
                    f"keeping the old output {previous.output}."
                )

            try:
                rendered = self.renderer.render(source_key, source_text)
                atomic_write_text(output_path, rendered)
            except (ConversionError, StateError) as exc:
                report.errors.append(str(exc))
                continue

            state.entries[source_key] = StateEntry(
                source_sha256=source_hash,
                conversion_signature=signature,
                target=target,
                output=output_relative,
            )
            try:
                save_state(self.config.state_file, state)
            except StateError as exc:
                if previous is None:
                    state.entries.pop(source_key, None)
                else:
                    state.entries[source_key] = previous
                report.errors.append(str(exc))
                continue
            report.converted += 1

        return report

    def _conversion_signature(self) -> str:
        payload = {
            "converter_version": __version__,
            "pages": self.config.link_targets,
            "images": {
                source: asdict(rule)
                for source, rule in sorted(self.config.images.items())
            },
        }
        serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def _output_path(self, page_id: str) -> Path:
        parts = page_id.lstrip(":").split(":")
        if not parts or any(part in {"", ".", ".."} for part in parts):
            raise ConfigError(f"Cannot create an output path for page ID {page_id!r}.")
        relative = Path(*parts[:-1], parts[-1] + ".dokuwiki")
        output_path = (self.config.output_dir / relative).resolve()
        if not output_path.is_relative_to(self.config.output_dir):
            raise ConfigError(f"Page ID {page_id!r} escapes the output directory.")
        return output_path
