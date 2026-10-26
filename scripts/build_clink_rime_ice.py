#!/usr/bin/env python3
"""Convert the Rime-Ice base dictionary into Clink-compatible local sources.

This script only extracts word/frequency and selected complete Pinyin readings.
It does not load librime, Rime schemas, or Lua.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_DICT = ROOT / "source/rime-ice/cn_dicts/base.dict.yaml"
DEFAULT_READINGS = ["nihao", "zhongguo", "zhongwen", "pinyin", "wusongpinyin"]


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rime-dict", type=pathlib.Path, default=DEFAULT_DICT,
                        help="Rime-Ice cn_dicts/base.dict.yaml")
    parser.add_argument("--clink-repo", type=pathlib.Path,
                        help="Local clone of anti-ltd/clink-language-packs; builds and validates .clex/.cime")
    parser.add_argument("--cime-readings", nargs="+", default=DEFAULT_READINGS,
                        help="Only emit these whole Pinyin readings in the demo CIME table")
    args = parser.parse_args()

    source = args.rime_dict.resolve()
    if not source.is_file():
        parser.error(f"Rime dictionary not found: {source}")

    wanted = {re.sub(r"[\s']+", "", item).lower() for item in args.cime_readings}
    words: dict[str, float] = defaultdict(float)
    candidates: dict[str, list[tuple[float, int, str]]] = defaultdict(list)
    in_data = False
    data_rows = 0
    skipped = 0

    with source.open("r", encoding="utf-8") as stream:
        for line_no, raw in enumerate(stream, 1):
            line = raw.rstrip("\r\n")
            if line.strip() == "...":
                in_data = True
                continue
            if not in_data or not line.strip() or line.lstrip().startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) < 3:
                skipped += 1
                continue
            word, spelling, raw_weight = fields[0].strip(), fields[1].strip(), fields[2].strip()
            try:
                weight = float(raw_weight)
            except ValueError:
                skipped += 1
                continue
            if not word or any(ch.isspace() for ch in word) or weight <= 0:
                skipped += 1
                continue
            data_rows += 1
            words[word] += weight
            reading = re.sub(r"[\s']+", "", spelling).lower()
            if reading in wanted and reading:
                candidates[reading].append((weight, line_no, word))

    if not words:
        raise SystemExit("No usable Rime-Ice entries found. Expected the base dictionary's tab-separated text, reading, weight rows.")

    word_list = ROOT / "source/zh-words.txt"
    word_list.parent.mkdir(parents=True, exist_ok=True)
    with word_list.open("w", encoding="utf-8", newline="\n") as out:
        for word in sorted(words):
            out.write(f"{word}\t{words[word]:.0f}\n")

    ime_tsv = ROOT / "source/zh-ime.tsv"
    emitted = 0
    with ime_tsv.open("w", encoding="utf-8", newline="\n") as out:
        for reading in sorted(wanted):
            ranked: list[str] = []
            seen: set[str] = set()
            for _weight, _line_no, word in sorted(candidates.get(reading, []), key=lambda item: (-item[0], item[1], item[2])):
                if word not in seen:
                    seen.add(word)
                    ranked.append(word)
                if len(ranked) == 16:
                    break
            if ranked:
                out.write("\t".join([reading, *ranked]) + "\n")
                emitted += 1

    print(f"Parsed {data_rows:,} Rime-Ice base rows ({skipped:,} skipped).")
    print(f"Wrote {len(words):,} unique words to {word_list.relative_to(ROOT)} ({word_list.stat().st_size:,} bytes).")
    print(f"Wrote {emitted} selected CIME reading rows to {ime_tsv.relative_to(ROOT)}.")
    missing = sorted(wanted - candidates.keys())
    if missing:
        print("No source match for: " + ", ".join(missing), file=sys.stderr)

    receipt = ROOT / "source/BUILD-RECEIPT.txt"
    receipt.write_text(
        "Local Clink prototype build receipt\n"
        f"source={source.relative_to(ROOT) if source.is_relative_to(ROOT) else source}\n"
        f"source_sha256={sha256(source)}\n"
        f"source_rows_parsed={data_rows}\n"
        f"unique_words={len(words)}\n"
        f"cime_readings_requested={','.join(sorted(wanted))}\n"
        f"cime_rows_emitted={emitted}\n"
        "derived_assets_license=GPL-3.0-only (per Rime-Ice upstream)\n",
        encoding="utf-8",
    )

    if args.clink_repo:
        repo = args.clink_repo.resolve()
        build_pack = repo / "build-pack.py"
        build_ime = repo / "tools/build-ime-table.py"
        validate = repo / "tools/validate-pack.py"
        for tool in (build_pack, build_ime, validate):
            if not tool.is_file():
                parser.error(f"Clink language-pack tool not found: {tool}")
        subprocess.run([sys.executable, str(build_pack), "zh", str(word_list)], cwd=ROOT, check=True)
        subprocess.run([sys.executable, str(build_ime), "zh", str(ime_tsv)], cwd=ROOT, check=True)
        subprocess.run([sys.executable, str(validate), "zh"], cwd=ROOT, check=True)
        print("Official Clink pack validator passed for zh.clex and zh.cime.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
