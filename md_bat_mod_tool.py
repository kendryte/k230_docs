#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def heading(line: str) -> str:
    pattern = r'^(\s*#+\s*)\d+[\.\d]*(?:\s+|$)(.+)$'
    if re.match(pattern, line):
        return re.sub(pattern, lambda m: f"{m.group(1)}{m.group(2).strip()}", line)
    return line.rstrip()


def process_file(filepath: Path, fn, dry_run: bool, verbose: bool) -> list[tuple[int, str, str]]:
    changes = []
    lines = filepath.read_text(encoding="utf-8").splitlines()
    new_lines = []
    for i, line in enumerate(lines, start=1):
        old = line
        new = fn(line)
        new_lines.append(new)
        if new != old:
            changes.append((i, old, new))
    if not dry_run and changes:
        filepath.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    if verbose and changes:
        print(f"\n{filepath}:")
        for lineno, old, new in changes:
            print(f"  L{lineno}: \"{old}\" -> \"{new}\"")
    return changes


def run_on_files(files: list[Path], fn, dry_run: bool, verbose: bool) -> int:
    total = 0
    for f in files:
        total += len(process_file(f, fn, dry_run, verbose))
    return total


def collect_files(paths: list[Path], recursive: bool, include: str) -> list[Path]:
    files = []
    for p in paths:
        if p.is_file() and p.suffix == ".md":
            files.append(p)
        elif p.is_dir():
            files.extend(p.rglob(include) if recursive else p.glob(include))
    return sorted(set(files))


def cmd_heading(args) -> None:
    fn = heading
    files = collect_files(args.paths, args.recursive, args.include)
    if not files:
        print("No markdown files found.")
        return
    total = run_on_files(files, fn, args.dry_run, args.verbose)
    print(f"\nProcessed {len(files)} file(s), {total} heading(s) cleaned.")


def cmd_domain(args) -> None:
    files = collect_files(args.paths, args.recursive, args.include)
    if not files:
        print("No markdown files found.")
        return
    total = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        new_text = text
        for old, new in args.replacements:
            if old in text:
                count = text.count(old)
                total += count
                new_text = new_text.replace(old, new)
                if args.verbose:
                    print(f"  [{f}] {count}x \"{old}\" -> \"{new}\"")
        if not args.dry_run and new_text != text:
            f.write_text(new_text, encoding="utf-8")
    print(f"\nProcessed {len(files)} file(s), {total} replacement(s) made.")


def fixlink(content: str) -> str:
    pattern = re.compile(r"(.*?\()#(?:\d+\.)*\d+-([^\)]+\))")
    return pattern.sub(r"\1#\2", content)


def cmd_fixlink(args) -> None:
    files = collect_files(args.paths, args.recursive, args.include)
    if not files:
        print("No markdown files found.")
        return
    total = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        new_text = fixlink(text)
        if new_text != text:
            pat = r"(.*?\()#(?:\d+\.)*\d+-([^\)]+\))"
            changes = len(re.findall(pat, text))
            total += changes
            if args.verbose:
                print(f"\n{f}:")
                for m in re.finditer(pat, text):
                    print(f"  \"{m.group()}\" -> \"{m.group(1)}#{m.group(2)}\"")
            if not args.dry_run:
                f.write_text(new_text, encoding="utf-8")
    print(f"\nProcessed {len(files)} file(s), {total} link anchor(s) fixed.")


def cmd_cover(args) -> None:
    files = collect_files(args.paths, args.recursive, args.include)
    if not files:
        print("No markdown files found.")
        return

    en_sections = [
        r"^## Disclaimer",
        r"^## Trademark Statement",
        r"^## Trademark Notice",
        r"^## Table of Contents",
        r"^## Preface",
        r"^## Menu",
    ]
    zh_sections = [
        r"^## 免责声明",
        r"^## 商标声明",
        r"^## 目录",
        r"^## 前言",
    ]

    removed = []
    for f in files:
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()
        out = []
        skip = False
        i = 0

        in_cover = False
        while i < len(lines):
            line = lines[i]

            if not skip and not in_cover and "![cover" in line:
                in_cover = True
                removed.append((f, line))
                i += 1
                while i < len(lines) and not re.match(r"^## ", lines[i]):
                    i += 1
                continue

            if re.match(r"^## ", line):
                skip = False
                in_cover = False
                for pat in en_sections + zh_sections:
                    if re.match(pat, line):
                        skip = True
                        removed.append((f, line))
                        break
                if skip:
                    i += 1
                    continue

            if not skip:
                out.append(line)
            i += 1

        new_text = "\n".join(out) + "\n"
        if new_text != text:
            if args.verbose:
                for _, title in removed:
                    print(f"  [{f}] removed: \"{title}\"")
            if not args.dry_run:
                f.write_text(new_text, encoding="utf-8")

    print(f"\nProcessed {len(files)} file(s), {len(removed)} section(s) removed.")


def main():
    parser = argparse.ArgumentParser(description="Markdown file utility.")
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        default=True,
        help="Recurse into subdirectories (default: enabled)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Preview changes without writing",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show diffs of changes",
    )
    parser.add_argument(
        "--include",
        default="*.md",
        help="File pattern to include (default: *.md)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_heading = sub.add_parser("heading", help="Remove manual chapter numbers from headings")
    p_heading.add_argument("paths", nargs="*", default=[Path(".")], type=Path)
    p_heading.set_defaults(func=cmd_heading)

    p_domain = sub.add_parser("domain", help="Replace domain names in URLs")
    p_domain.add_argument("paths", nargs="*", default=[Path(".")], type=Path)
    p_domain.add_argument(
        "--replace",
        nargs=2,
        action="append",
        dest="replacements",
        metavar=("OLD", "NEW"),
        help="Domain replacement pair (can be specified multiple times)",
    )
    p_domain.set_defaults(
        func=cmd_domain,
        replacements=[
            ("developer.canaan-creative.com", "www.kendryte.com"),
        ],
    )

    p_cover = sub.add_parser("cover", help="Remove template boilerplate sections")
    p_cover.add_argument("paths", nargs="*", default=[Path(".")], type=Path)
    p_cover.set_defaults(func=cmd_cover)

    p_fixlink = sub.add_parser("fixlink", help="Remove number prefixes from link anchors")
    p_fixlink.add_argument("paths", nargs="*", default=[Path(".")], type=Path)
    p_fixlink.set_defaults(func=cmd_fixlink)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
