# aqua-usr-demo — 水井USR 智慧養殖 AI 專家系統（學生 base repo）

> 配合課程：**[水井USR] 用本地端實作水井USR智慧養殖AI專家系統** — 9 hr / 3 堂課
> 配合教師：林正敏 教授（南開科大）+ 敏哥（虎科大電資 / 水井USR）
> Python 3.10+ / Django 4.2 / OpenAI Function Calling

把水質感測數據（溫度、pH、溶氧、鹽度）丟給 LLM，讓 AI 講人話告訴你「池子現在怎麼樣、要不要注意」。

---

## 5 分鐘跑起來

```bash
# 1. clone + 進去
git clone https://github.com/4-learn/aqua-usr-demo.git
cd aqua-usr-demo

# 2. 裝套件
python -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. 環境變數（老師會發 OpenAI key）
cp .env.example .env
# 編輯 .env，把 OPENAI_API_KEY 填上

# 4. 建 DB + 灌假資料
python manage.py migrate
python manage.py seed

# 5. 跑！
python manage.py runserver
```

開瀏覽器到 [http://localhost:8000/](http://localhost:8000/) 開始聊天。

試試看：
- `1 號池現在水質怎樣？`
- `2 號池跟 3 號池哪個比較好？`（這題目前會卡，留給 Session 2）

---

## 它在做什麼

```
你   ───>   Django chat view   ───>   OpenAI API
                  ↓                          ↓
              呼叫 tool                "請呼叫 get_latest_water_quality(pond=1)"
                  ↓                          ↓
              查 DB（水質）   ───>   LLM 拿結果再產出回答
                                            ↓
你   <───────────────────────  「1 號池目前水溫 28°C…」
```

→ **LLM 不直接讀你的 DB**。是你的 Django 主動去呼叫 LLM、執行 tool、把結果丟回去。
這個模式叫 **Function Calling**，是這門課的核心。

---

## 目錄結構

```
.
├── aquausr/             ← Django project（settings、urls、wsgi）
├── chat/                ← Chat 介面 + Function Calling 邏輯
│   ├── llm.py           ← OpenAI 呼叫 loop
│   ├── tools.py         ← LLM 可用的工具定義 + 執行
│   ├── views.py         ← /api/chat/ endpoint
│   └── templates/chat/chat.html  ← 簡易前端
├── water/               ← 水質資料層
│   ├── models.py        ← Pond / SensorReading
│   └── management/commands/seed.py  ← 灌假資料
├── manage.py
├── requirements.txt
└── .env.example
```

---

## 🚧 課程進度 — base repo 故意留洞

這個 repo 是「**80% 完成**」的，**有些功能故意沒做**，等你 Session 2 用 Codex CLI 把它補完。

搜尋整個 repo 的 `🚧 TODO`：

| TODO | 檔案 | 哪堂課 |
|------|------|--------|
| 加 `get_water_quality_history(pond, days)` | `chat/tools.py` | Session 2 |
| 加 `check_thresholds(pond)` 異常偵測 | `chat/tools.py` | Session 2 |
| 加 `list_ponds()` 池塘清單 | `chat/tools.py` | Session 2 |
| 把 chat history 接上來（多輪對話）| `chat/views.py` | Session 2 |
| CSRF 保護打開 | `chat/views.py` | Session 3 部署前 |
| OpenAI 換成 Ollama base URL | `chat/llm.py` | Session 3 |

---

## Session 對應

- **Session 1** — clone、跑起來、看 chat 會講話、學 Function Calling 概念
- **Session 2** — 用 Codex CLI 把上面 TODO 寫完、整合進你自己的 Django
- **Session 3** — 部署到 PythonAnywhere、看老師示範把 LLM 從 OpenAI 換成 Ollama

---

## 給老師

完整解答 + 課堂備課 prompt 在 private repo：[`4-learn/aqua-usr-workshop`](https://github.com/4-learn/aqua-usr-workshop)（teacher only）。
