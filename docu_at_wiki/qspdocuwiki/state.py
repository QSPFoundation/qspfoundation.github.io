from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import tempfile
from typing import Any

from .errors import StateError


@dataclass(frozen=True)
class StateEntry:
    source_sha256: str
    conversion_signature: str
    target: str
    output: str


@dataclass
class ConverterState:
    entries: dict[str, StateEntry]


def load_state(path: Path) -> ConverterState:
    if not path.exists():
        return ConverterState(entries={})
    try:
        raw: Any = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise StateError(f"Cannot read hash manifest {path}: {exc}") from exc
    if not isinstance(raw, dict) or raw.get("version") != 1 or not isinstance(raw.get("entries"), dict):
        raise StateError(f"Hash manifest {path} has an unsupported structure.")

    entries: dict[str, StateEntry] = {}
    for source, value in raw["entries"].items():
        if not isinstance(source, str) or not isinstance(value, dict):
            raise StateError(f"Hash manifest {path} contains an invalid entry.")
        try:
            entry = StateEntry(
                source_sha256=value["source_sha256"],
                conversion_signature=value["conversion_signature"],
                target=value["target"],
                output=value["output"],
            )
        except KeyError as exc:
            raise StateError(f"Hash manifest {path} is missing {exc.args[0]!r}.") from exc
        if not all(isinstance(item, str) for item in asdict(entry).values()):
            raise StateError(f"Hash manifest {path} contains a non-string entry value.")
        entries[source] = entry
    return ConverterState(entries=entries)


def save_state(path: Path, state: ConverterState) -> None:
    payload = {
        "version": 1,
        "entries": {
            source: asdict(entry)
            for source, entry in sorted(state.entries.items())
        },
    }
    _atomic_write(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def atomic_write_text(path: Path, content: str) -> None:
    _atomic_write(path, content)


def _atomic_write(path: Path, content: str) -> None:
    temporary_path: Path | None = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(content)
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, path)
    except OSError as exc:
        cleanup_error: OSError | None = None
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError as cleanup_exc:
                cleanup_error = cleanup_exc
        message = f"Cannot atomically write {path}: {exc}"
        if cleanup_error is not None:
            message += f" (temporary file cleanup also failed: {cleanup_error})"
        raise StateError(message) from exc
