# Provenance and notices

## Rime-Ice data

- Project: [iDvel/rime-ice](https://github.com/iDvel/rime-ice).
- Upstream revision: `da1fbe602e38f26db846fa10120ee64c2b0324c0` (also recorded in `source/rime-ice/SOURCE-RECEIPT.txt`).
- Input: `cn_dicts/base.dict.yaml` only. The source copy is unmodified.
- Input SHA-256: `0418d5103d8e40c8fff4b686a873ad03e9836cd0419ecae0b7e1e2526312dba0`.
- Upstream licence: **GPL-3.0-only**. The exact upstream licence text is retained at `source/rime-ice/LICENSE` and copied to the repository-root `LICENSE`.
- The generated dictionaries and readable exports are adapted from that input and are conveyed under GPL-3.0-only. The conversion script and accompanying project material are also provided under GPL-3.0-only. Keep the source attribution and licence when redistributing them.

## Modifications made on 2026-10-27

The converter extracts text and frequency, sums frequencies for duplicate words, and exports a sorted readable list. It selects candidates for only five complete Pinyin readings (`nihao`, `pinyin`, `wusongpinyin`, `zhongguo`, `zhongwen`), removes duplicate candidates, preserves source-based ranking, and limits each reading to 16 candidates. The official Clink builders then produce `zh.clex` and `zh.cime`.

`source/BUILD-RECEIPT.txt` records the input hash, 543,118 parsed source rows, 542,039 unique exported words, and five emitted CIME rows. No Rime schema, Lua module, engine, additional dictionary, emoji data or neural model was copied into this project.

## Clink build tools and release metadata

The assets are built and checked with the official tools from [anti-ltd/clink-language-packs](https://github.com/anti-ltd/clink-language-packs): `build-pack.py`, `tools/build-ime-table.py`, and `tools/validate-pack.py`. Publication revalidation uses upstream revision `2cc15342f1824622ba3d2b9f9379c89ff3bbdb59`. Those tools are used locally and are not copied into this repository.

The Release's `manifest.json` is generated from the final `zh.clex` and `zh.cime` bytes using the official release manifest format. It contains only version, language/platform identifiers, same-Release asset addresses, SHA-256 hashes, and exact byte counts. No optional language assets are added.

This is an independent, experimental community conversion. It is not endorsed by Clink or Rime-Ice. Format validation and public download checks are not a claim of a completed Clink keyboard runtime installation test.
