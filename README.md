# 國高中自然科命題規範與自動化產卷技能 (jhsh-science-exam-generator)

本技能 (Skill) 專門用於指導 Google Antigravity 等 AI 代理人進行國高中自然科（生物、理化、地球科學、物理、化學）段考自動化命題，生成完全符合「新北市立錦和高級中學」教務處規範、素養導向評量與 PISA 2025 標準的試題卷、答案解析卷與命題審題檢核表。

---

## 🏛️ 專案模組架構 (Architecture)

本技能遵循 Antigravity 漸進揭示 (Progressive Disclosure) 設計規範，採用精簡化三層架構：

```text
jhsh-science-exam-generator/
├── SKILL.md                          # 核心引導文檔 (<200行)：規範、提詞模板、排版守則與檢查清單
├── README.md                         # 專案介紹與安裝說明文檔
├── requirements.txt                  # Python 相依套件 (python-docx, matplotlib, numpy, sympy)
├── LICENSE                           # MIT 開源授權條款
├── scripts/                          # 自動化輔助程式碼庫
│   ├── docx_science_builder.py       # Word 試卷建構器：1cm 邊界、全卷 11Pt、浮動文繞圖、動態頁碼
│   ├── science_chem_math_omml.py     # Word 原生可編輯 OMML：化學式、物態、同位素、單位與方程式
│   ├── science_plotter.py            # 300 DPI 向量繪圖引擎：+8Pt 特大字級、黑白灰階與斜線填充
│   └── science_verifier.py           # 試卷品質校驗器：總分 100/連續題號/選項平衡/防超綱過濾
└── references/                       # 課綱與素養評量參考庫
    ├── curriculum_science_inquiry.md # 108 自然課綱指標、探究六歷程 (I1~I6) 與 Bloom 認知層次
    └── science_anti_out_of_bounds.md # 嚴格防超綱紅線清單 (嚴禁用「斜率」、禁複雜合金密度計算等)
```

---

## 📦 如何匯入 / 安裝本技能

他人取得此技能後，可依需求選擇「**全域安裝（推薦）**」或「**單一專案安裝**」：

### 方式 A：全域安裝（推薦，所有專案與新對話皆可隨時調用）

#### 1. 在 Antigravity 對話框貼上一句話自動安裝（最推薦）：
```text
請幫我把這個 GitHub 倉庫安裝成全域 Skill：
https://github.com/geniefu/jhsh-science-exam-generator
並幫我檢查安裝所需的 Python 套件 (python-docx, matplotlib, numpy, sympy)
```

#### 2. 透過 Git 一鍵安裝（未來更新只需 `git pull`）：
- **Windows (PowerShell)**:
  ```powershell
  git clone https://github.com/geniefu/jhsh-science-exam-generator.git "$HOME\.gemini\config\skills\jhsh-science-exam-generator"
  ```
- **macOS / Linux**:
  ```bash
  git clone https://github.com/geniefu/jhsh-science-exam-generator.git ~/.gemini/config/skills/jhsh-science-exam-generator
  ```

#### 3. 手動解壓縮安裝：
將下載的 `jhsh-science-exam-generator` 資料夾複製至使用者的個人全域設定目錄：
- **Windows**: `C:\Users\<使用者名稱>\.gemini\config\skills\jhsh-science-exam-generator\`
- **macOS / Linux**: `~/.gemini/config/skills/jhsh-science-exam-generator/`

---

## 🚀 快速開始：提詞範例 (Prompt)

安裝完成後，在對話框中輸入 `/jhsh-science-exam-generator` 並依當次命題範圍修改以下參數：

```text
請使用 /jhsh-science-exam-generator 技能為我生成一份自然科段考試卷，規格參數如下：
1、標題：【例如：新北市立錦和高級中學115學年度第一學期 國中部八年級 自然科第一次段考試題卷】（年級請依出題範圍調整為七年級、八年級或九年級）。
2、範圍：【請填寫章節，例如：緒論到 3-1】。
3、題型：【例如：單一選擇題，每題有四個選項 (A)(B)(C)(D)】。
4、題數：【例如：35 題（含單題與素養閱讀題組）】。
5、配分：總分 100 分【例如：第 1～25 題每題 3 分共 75 分；第 26～30 題題組每題 3 分共 15 分；第 31～35 題題組每題 2 分共 10 分】。
6、難易程度：【例如：中等偏難（預估平均通過率約 55%～65%）】。
7、其它：【選填，例如：以「皮克敏的故事世界」之虛擬情境串連試卷題組】。
```

---

## 🛠️ 環境依賴需求 (Dependencies)

```bash
pip install -r requirements.txt
```
或直接安裝：
```bash
pip install python-docx matplotlib numpy sympy
```

---

## ✨ 核心特色

1. **嚴格符合錦和高中格式**：包含完整試卷抬頭、必放警語（未寫座號扣5分等）、全卷 11Pt 標楷體/Times New Roman、1cm 窄邊界、題號凸排、右側浮動文繞圖與動態頁碼（第X頁共X頁）。
2. **雙份獨立 Word 文件自動產出（免 PDF 與檢核表）**：同步產出正式試題卷 (`.docx`) 與含題題詳解的答案卷 (`.docx`)，免除繁瑣 PDF 與檢核表產生負擔，直接開啟即刻送印。
3. **Word 原生 OMML 數學與化學方程式**：零外部編譯器依賴，化學式上下標、反應箭頭與科學單位在 Word 中雙擊即可直接編輯。
4. **高品質向量繪圖與 +8 Pt 特大字級**：透過 Matplotlib 自動繪製 300 DPI 考卷插圖，特大字級（16.5~21 Pt）、高對比黑白灰階與斜線填充，避免油印模糊與文字壓線。
5. **素養導向與認知階層**：深度融合 Bloom 六大認知階層、探究六步驟 (I1~I6)、原創素養長文題組與生活化情境。
6. **全自動防錯驗證**：自動校驗總分 100 分、連續題號、選項配比平衡與嚴格防超綱禁忌詞清單。
7. **100% 零 LaTeX $ 符號殘留**：內建變數與符號全域自動清洗機制，物理變數（如 V、M、f、λ）與化學式（如 H₂O、CO₂、→）以中學考卷最乾淨純文字與 Unicode 呈現，徹底杜絕 $ 排版標籤外露。
