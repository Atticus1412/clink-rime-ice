# clink-rime-ice

把[雾凇拼音（Rime-Ice）](https://github.com/iDvel/rime-ice)的 `base` 詞庫轉換成 Clink 語言包的實驗性社群專案。這不是 Rime 引擎移植，也不是 Clink 或 Rime-Ice 官方發布、合作或背書的產品。

**GPL-3.0-only。** 原詞庫、可讀轉換資料、轉換腳本、來源提交號及 SHA-256 回執均隨倉庫提供；完整授權原文見 [LICENSE](LICENSE)，來源與修改說明見 [PROVENANCE.md](PROVENANCE.md)。

## 包含什麼

- `Lexicons/zh.clex`：Clink CLEX v1 詞典，由雾凇 `cn_dicts/base.dict.yaml` 轉換。可讀輸出有 **542,039 個去重詞條**；原詞庫解析了 543,118 行。
- `Lexicons/zh.cime`：只有 **5 組完整拼音**的候選補充表：`nihao`、`pinyin`、`wusongpinyin`、`zhongguo`、`zhongwen`。每組最多 16 個候選，全部選自同一份來源詞庫。這不是完整的雾凇拼音輸入方案。
- `source/zh-words.txt`、`source/zh-ime.tsv`：對應的可讀轉換資料。
- `source/rime-ice/`：未改動的 `base.dict.yaml`、上游許可證及來源回執。
- `scripts/build_clink_rime_ice.py`：可重建上述資料的轉換腳本；`source/BUILD-RECEIPT.txt` 記錄來源哈希和計數。

本倉庫不包含其他第三方詞庫、Rime schema、Lua、神經模型或 emoji 資料。

## 在 Clink 新增

1. 在 Clink 開啟 **General → Repositories**。
2. 新增 `Atticus1412/clink-rime-ice`，或完整 URL：`https://github.com/Atticus1412/clink-rime-ice`。
3. 開啟 **Languages**，重新整理，在 **Community** 中選擇此倉庫的中文（`zh`）語言包並下載。
4. 下載通過 Clink 的檔案大小與 SHA-256 驗證後，使用 **簡體中文／QWERTY 拼音**測試 `nihao`、`zhongwen` 等完整讀音。可切離鍵盤再返回，確認重新載入。

[最新 Release](https://github.com/Atticus1412/clink-rime-ice/releases/latest) 同時提供由最終資產自動產生的 `manifest.json` 與兩個詞典檔案。Clink 透過 `releases/latest/download/manifest.json` 讀取索引。每個資產 URL 都指向同一倉庫、同一個 Release，並附精確位元組數與 SHA-256。Release 的原始碼封存包含本包的來源資料與腳本。

官方操作說明：[社群倉庫](https://anti.ltd/docs/clink/reference/repositories)與[語言包](https://www.anti.ltd/docs/clink/languages)。

## 重建與校驗

需要 Python 3，以及[Clink 官方語言包倉庫](https://github.com/anti-ltd/clink-language-packs)的本地副本。官方建置工具未複製進本倉庫。

```sh
python3 scripts/build_clink_rime_ice.py --clink-repo /path/to/clink-language-packs
```

省略 `--clink-repo` 時只匯出可讀資料，不編譯詞典。可明確選擇相同的完整拼音集合：

```sh
python3 scripts/build_clink_rime_ice.py --clink-repo /path/to/clink-language-packs \
  --cime-readings nihao zhongguo zhongwen pinyin wusongpinyin
```

## 相容範圍與限制

`.clex` 和 `.cime` 是 Clink 專用格式。本包使用官方建置器產生，並通過官方格式驗證器；發布資產的大小、哈希及來源回執另作核對。

**尚未在 Clink 手機鍵盤完成安裝與輸入的執行期實測。** 格式與下載驗證通過不等於所有裝置上的行為已驗證。Clink 的拼音轉換仍由應用內建模型處理；此處 `zh.cime` 只為簡體中文／QWERTY 拼音的五組完整讀音補充候選，不支援 Rime Lua、Rime 語法模型、雙拼方案或 Rime 引擎。不要把它當作可直接匯入的通用手機詞表。

此包採 GPL-3.0-only，獨立發布於使用者自有社群倉庫，未提交到 Clink 官方社群資源倉庫，也不主張與其他倉庫附加條款之間的法律相容性結論。
