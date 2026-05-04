# aqua-usr-demo — 水井USR 智慧養殖 AI 專家系統（學生版）

> 🚧 **本 repo 仍在建構中** — 課程開課前完成
> 配合課程：[水井USR 智慧養殖 AI 專家系統](https://github.com/4-learn) — NFU 虎科大 9 小時課程
> 配合教師：林正敏教授

## 這是什麼

把水質感測數據（溫度、溶氧、pH、鹽度）丟給 LLM，得到自然語言的養殖管理建議。

學生會：
1. 在自己筆電 clone 起來、跑得起來、看到 chat 會講話
2. 用 Codex CLI 把這 repo 整合到自己的 Django，加新功能
3. 部署到 PythonAnywhere

## 技術棧

- Django（學生已會）
- OpenAI Function Calling
- SQLite（本機）/ MySQL（PA）
- 簡易 HTML chat 前端

## 給學生

```bash
git clone https://github.com/4-learn/aqua-usr-demo.git
cd aqua-usr-demo
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver
```

開瀏覽器到 http://localhost:8000/ 開始聊天。

## 給老師

詳細解答在 private repo `4-learn/aqua-usr-workshop`（teacher only）。
