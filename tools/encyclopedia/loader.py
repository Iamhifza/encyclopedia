"""Read ``content/`` into a :class:`Corpus`.

Entries are Markdown files with YAML front matter: structured metadata for the
machine, prose for the reader. Nothing here validates -- see ``validate.py``.
"""

from __future__ import annotations

import datetime as _datetime
import re
from pathlib import Path
from typing import Any

import yaml

from .model import Corpus, Entry

FRONT_MATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?(.*)\Z", re.DOTALL)
HEADING_RE = re.compile(r"^##\s+(?!#)(.+?)\s*$", re.MULTILINE)


class ContentError(Exception):
    """Raised when a file cannot be parsed at all."""


def parse_front_matter(text: str, source: str) -> tuple[dict[str, Any], str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ContentError(f"{source}: missing YAML front matter delimited by '---'")
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:  # pragma: no cover - message passthrough
        raise ContentError(f"{source}: front matter is not valid YAML: {exc}") from exc
    if not isinstance(meta, dict):
        raise ContentError(f"{source}: front matter must be a mapping")
    return _normalise(meta), match.group(2)


def _normalise(value):
    """YAML turns bare dates into date objects; the schema wants ISO strings."""
    if isinstance(value, _datetime.date):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _normalise(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalise(v) for v in value]
    return value


def split_sections(body: str) -> tuple[dict[str, str], list[str]]:
    """Split a body on ``##`` headings, preserving author order."""
    sections: dict[str, str] = {}
    order: list[str] = []
    matches = list(HEADING_RE.finditer(body))
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[heading] = body[start:end].strip()
        order.append(heading)
    return sections, order


def load_entry(path: Path) -> Entry:
    text = path.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text, path.name)
    sections, order = split_sections(body)
    return Entry(
        slug=path.stem,
        path=str(path),
        meta=meta,
        sections=sections,
        section_order=order,
        raw_body=body.strip(),
    )


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ContentError(f"{path.name}: expected a mapping at the top level")
    return data


def load_comparison(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text, path.name)
    meta["id"] = path.stem
    meta["path"] = str(path)
    meta["body"] = body.strip()
    return meta


def load_corpus(content_dir: str | Path) -> Corpus:
    content = Path(content_dir)
    corpus = Corpus()

    entry_dir = content / "entries"
    for path in sorted(entry_dir.glob("*.md")):
        if path.name.startswith("_"):
            continue
        entry = load_entry(path)
        if entry.slug in corpus.entries:
            raise ContentError(f"duplicate entry slug: {entry.slug}")
        corpus.entries[entry.slug] = entry

    corpus.taxonomy = _load_yaml(content / "taxonomy.yaml")
    corpus.paths = _load_yaml(content / "learning-paths.yaml")
    corpus.timeline = _load_yaml(content / "timeline.yaml")

    comparison_dir = content / "comparisons"
    if comparison_dir.exists():
        for path in sorted(comparison_dir.glob("*.md")):
            if path.name.startswith("_"):
                continue
            corpus.comparisons.append(load_comparison(path))

    return corpus
