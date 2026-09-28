# 國高中自然科命題規範與自動化產卷技能 (jhsh-science-exam-generator)

本技能 (Skill) 專門用於指導 Google Antigravity 等 AI 代理人進行國高中自然科（生物、理化、地球科學、物理、化學）段考自動化命題，生成符合「新北市立錦和高級中學」教務處規範、素養導向評量與 PISA 2025 標準的試題卷與答案解析卷。

---

## 📦 如何匯入 / 安裝本技能

他人取得此技能後，可依需求選擇「**全域安裝（推薦）**」或「**單一專案安裝**」：

### 方式 A：全域安裝（推薦，所有專案與新對話皆可隨時調用）

#### 1. 在 Antigravity 對話框貼上一句話自動安裝（最推薦）：
```text
請幫我把這個 GitHub 倉庫安裝成全域 Skill：
https://github.com/geniefu/jhsh-science-exam-generator
並幫我檢查安裝所需的 Python 套件 (python-docx, matplotlib, numpy)
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

*(若目錄不存在，可手動建立 `skills` 資料夾)*

---

### 方式 B：單一專案安裝（僅在特定工作區目錄下生效）
將 `jhsh-science-exam-generator` 資料夾放入欲使用的專案根目錄中的 `.agents/skills/`：
- 目錄結構：
  ```text
  你的專案根目錄/
  └── .agents/
      └── skills/
          └── jhsh-science-exam-generator/
              ├── SKILL.md
              └── README.md
  ```

---

## 🚀 快速開始：提詞範例 (Prompt)

安裝完成後，在對話框中輸入 `/jhsh-science-exam-generator` 並依當次命題範圍修改以下參數：

```text
請使用 /jhsh-science-exam-generator 技能為我生成一份自然科段考試卷，規格參數如下：
1、範圍：【請填寫章節，例如：第 4 章「光與透鏡成像」到 第 5 章「溫度與熱量傳播」】。
2、題型：【例如：單一選擇題，每題有四個選項 (A)(B)(C)(D)】。
3、題數：【例如：40 題（含單題與素養閱讀題組）】。
4、配分：總分 100 分【例如：第 1～20 題每題 3 分共 60 分；第 21～40 題每題 2 分共 40 分】。
5、難易程度：【例如：難易適中（預估平均通過率約 65%～70%）】。
6、其它：【選填，例如：以「火星生態基地探測任務」或「智慧綠建築日常節能」之虛擬情境串連試卷題組】。
```

---

## 🛠️ 環境依賴需求 (Dependencies)

本技能包含自動繪製 300 DPI 考卷黑白插圖與建立 Word 文件功能，需具備以下 Python 套件：
```bash
pip install python-docx matplotlib numpy
```

---

## ✨ 核心特色

1. **嚴格符合錦和高中格式**：包含完整試卷抬頭、必放警語（未寫座號扣5分等）、全卷 11Pt 標楷體/Times New Roman、1cm 窄邊界、題號凸排、右側浮動文繞圖與動態頁碼（第X頁共X頁）。
2. **三份 Word 自動產出**：同步產出正式試題卷 (`.docx`)、含題題詳解的答案卷 (`.docx`) 與命題審題檢核表 (`.docx`)。
3. **高品質向量繪圖**：透過 Matplotlib 自動繪製 300 DPI 考卷插圖，特大字級（+8 Pt）、高對比黑白灰階與斜線填充，避免油印模糊。
4. **素養導向與認知階層**：深度融合 Bloom 六大認知階層、探究六步驟 (I1~I6)、原創素養長文題組與生活化情境。
