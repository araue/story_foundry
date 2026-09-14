#!/usr/bin/env python3
"""Dependency-free utilities for a literary-project repository."""

from __future__ import annotations

import argparse
import posixpath
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import date
from pathlib import Path
from xml.etree import ElementTree


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_EPUB = PROJECT_ROOT / "dist" / "project.epub"
RESET_DIRECTORIES: dict[str, tuple[str, ...]] = {
    "arcs": (),
    "assumptions": (),
    "cast": (),
    "dist": (),
    "story": (),
    "world": (),
    "manuscript": ("edition_notice.md",),
}
RESEARCH_DIRECTORIES = ("analysis", "characters", "questions")
RESET_FILES = ("epub/map.md",)


def _assert_project_root(root: Path) -> None:
    """Refuse to operate unless *root* contains the required template files."""

    required = (
        root / "AGENTS.md",
        root / "README.md",
        root / "phase_instructions" / "README.md",
        *(root / "phase_instructions" / f"phase_{number:02d}_{name}.md" for number, name in (
            (1, "literary_analysis"),
            (2, "character_analysis"),
            (3, "open_questions"),
            (4, "assumptions"),
            (5, "story_architecture"),
            (6, "character_arcs_and_cast"),
            (7, "world_building"),
            (8, "writing"),
        )),
        root / "epub" / "metadata.yaml",
        root / "epub" / "reader.css",
        root / "manuscript" / "edition_notice.md",
    )
    missing = [path for path in required if not path.is_file()]
    if missing:
        joined = ", ".join(str(path) for path in missing)
        raise RuntimeError(f"Refusing to operate outside a literary project; missing: {joined}")


def _reset_targets(root: Path, *, include_research: bool) -> list[Path]:
    targets: list[Path] = []
    if include_research:
        targets.extend(root / name for name in RESEARCH_DIRECTORIES if (root / name).exists())
    for name, preserved_children in RESET_DIRECTORIES.items():
        directory = root / name
        if not directory.exists():
            continue
        if not preserved_children:
            targets.append(directory)
        else:
            preserved = set(preserved_children)
            targets.extend(child for child in directory.iterdir() if child.name not in preserved)
    targets.extend(root / name for name in RESET_FILES if (root / name).exists())
    return sorted(set(targets), key=lambda path: str(path.relative_to(root)))


def _initial_status(*, include_research: bool) -> str:
    if include_research:
        stage = "The authored solution and research have been reset. Phase 1 is next."
        next_step = "Read `phase_instructions/phase_01_literary_analysis.md` before work."
    else:
        stage = "The authored solution has been reset. Phase 1–3 research remains; Phase 4 is next."
        next_step = "Review the retained research, then begin approved assumptions in Phase 4."
    return f"""# Literary Project — Status

## Status date

{date.today().isoformat()}

## Current stage

{stage}

## Active review gate

No chapter is drafted or under review.

## Current edition

No generated edition exists.

## Next permitted work

{next_step}
"""


def reset_project(
    *, confirm: bool = False, include_research: bool = False, root: Path = PROJECT_ROOT
) -> list[Path]:
    """List or, with confirmation, remove authored content and reset project state."""

    root = root.resolve()
    _assert_project_root(root)
    targets = _reset_targets(root, include_research=include_research)
    if not confirm:
        return targets
    for target in targets:
        resolved = target.resolve()
        if root not in resolved.parents:
            raise RuntimeError(f"Refusing to remove path outside project root: {resolved}")
        if resolved.is_dir() and not resolved.is_symlink():
            shutil.rmtree(resolved)
        else:
            resolved.unlink(missing_ok=True)
    (root / "status.md").write_text(_initial_status(include_research=include_research), encoding="utf-8")
    return targets


def _numbered_chapters(root: Path) -> list[Path]:
    chapters = sorted((root / "manuscript").glob("chapter_[0-9][0-9].md"))
    if not chapters:
        raise RuntimeError("No numbered manuscript chapters exist; nothing to build.")
    return chapters


def build_epub(*, output: Path = DEFAULT_EPUB, root: Path = PROJECT_ROOT, validate: bool = True) -> Path:
    """Build an EPUB from the notice, optional map, and numbered chapters."""

    root = root.resolve()
    _assert_project_root(root)
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        raise RuntimeError("pandoc is required to build the EPUB.")
    notice = root / "manuscript" / "edition_notice.md"
    sources = [notice]
    map_source = root / "epub" / "map.md"
    if map_source.is_file():
        sources.append(map_source)
    sources.extend(_numbered_chapters(root))
    output = output if output.is_absolute() else root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        pandoc, "--from", "markdown+smart", "--metadata-file=epub/metadata.yaml",
        "--css=epub/reader.css", "--toc", "--split-level=1",
        *(str(path.relative_to(root)) for path in sources), "-o", str(output),
    ]
    subprocess.run(command, cwd=root, check=True)
    if validate:
        validate_epub(output=output, root=root)
    return output


def _css_assigns_background(css: str) -> bool:
    without_comments = re.sub(r"/\\*.*?\\*/", "", css, flags=re.DOTALL)
    return bool(re.search(r"(?im)(?:^|[;{])\\s*background(?:-color)?\\s*:", without_comments))


def validate_epub(*, output: Path = DEFAULT_EPUB, root: Path = PROJECT_ROOT) -> list[str]:
    """Validate archive integrity, reading order, map placement, and CSS policy."""

    root = root.resolve()
    _assert_project_root(root)
    output = output if output.is_absolute() else root / output
    if not output.is_file():
        raise RuntimeError(f"EPUB does not exist: {output}")
    if _css_assigns_background((root / "epub" / "reader.css").read_text(encoding="utf-8")):
        raise RuntimeError("epub/reader.css must not assign background or background-color.")
    with zipfile.ZipFile(output) as archive:
        if bad_member := archive.testzip():
            raise RuntimeError(f"Corrupt EPUB member: {bad_member}")
        names = set(archive.namelist())
        required = {"mimetype", "EPUB/content.opf", "EPUB/nav.xhtml"}
        if missing := sorted(required - names):
            raise RuntimeError(f"EPUB is missing required members: {', '.join(missing)}")
        package = ElementTree.fromstring(archive.read("EPUB/content.opf"))
        namespace = {"opf": "http://www.idpf.org/2007/opf"}
        manifest = {item.attrib["id"]: item.attrib["href"] for item in package.findall("opf:manifest/opf:item", namespace)}
        spine = [manifest[item.attrib["idref"]] for item in package.findall("opf:spine/opf:itemref", namespace)]
        if len(spine) < 3 or spine[:2] != ["text/title_page.xhtml", "nav.xhtml"]:
            raise RuntimeError(f"Unexpected EPUB opening spine order: {spine[:3]}")
        title_page = archive.read("EPUB/text/title_page.xhtml").decode("utf-8")
        marker = "PRIVATE DRAFT — NOT FOR DISTRIBUTION"
        if marker not in title_page or title_page.find(marker) < title_page.find('class="title"'):
            raise RuntimeError("The edition notice is missing or not below the title page heading.")
        if 'class="abstract"' not in title_page:
            raise RuntimeError("The title-page notice lacks its small-print container.")
        map_source = root / "epub" / "map.md"
        expected_pages = len(_numbered_chapters(root)) + int(map_source.is_file())
        text_pages = [href for href in spine if href.startswith("text/ch")]
        if len(text_pages) != expected_pages:
            raise RuntimeError("EPUB spine page count does not match map and chapter inputs.")
        if map_source.is_file():
            map_markup = archive.read(f"EPUB/{spine[2]}").decode("utf-8")
            match = re.search(r'<img[^>]+src="([^"]+)"[^>]+alt="([^"]+)"', map_markup)
            if "map-page" not in map_markup or match is None or not match.group(2).strip():
                raise RuntimeError("The map page lacks a map marker or meaningful image alternative text.")
            image_href = posixpath.normpath(posixpath.join(posixpath.dirname(f"EPUB/{spine[2]}"), match.group(1)))
            if image_href not in names:
                raise RuntimeError(f"Broken map image reference: {image_href}")
    return ["edition notice embedded below title", "archive integrity verified", "reader stylesheet does not force a background"]


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    reset = commands.add_parser("reset-project", help="list reset targets; pass --yes to remove them")
    reset.add_argument("--yes", action="store_true", help="confirm deletion of listed content")
    reset.add_argument("--include-research", action="store_true", help="also remove Phase 1–3 research")
    for name, help_text in (("build-epub", "build and validate the EPUB"), ("validate-epub", "validate the current EPUB")):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("--output", type=Path, default=DEFAULT_EPUB)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        if args.command == "reset-project":
            targets = reset_project(confirm=args.yes, include_research=args.include_research)
            print("\n".join(str(path.relative_to(PROJECT_ROOT)) for path in targets) or "Nothing would be removed.")
            print("\nDry run only. Re-run with --yes to delete these paths." if not args.yes else "\nProject content reset.")
        elif args.command == "build-epub":
            print(build_epub(output=args.output).relative_to(PROJECT_ROOT))
        else:
            for message in validate_epub(output=args.output):
                print(f"OK: {message}")
        return 0
    except (OSError, RuntimeError, subprocess.CalledProcessError, zipfile.BadZipFile) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
