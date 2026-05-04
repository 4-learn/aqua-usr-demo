"""LLM 可以呼叫的「工具」 — 每個工具都是一個讀 DB 的 function。

這檔的設計：
- TOOL_SCHEMAS：給 LLM 看的 tool 定義（函數名、參數、描述）
- dispatch()：LLM 說要呼叫某 tool 時，這裡負責真的執行

🚧 Session 2 學員會在這裡加新 function（搜「TODO」）
"""

from datetime import timedelta

from django.utils import timezone

from water.models import Pond, SensorReading


# ============================================================
# 工具實作（真的去查 DB）
# ============================================================


def get_latest_water_quality(pond_name: str) -> dict:
    """指定池塘最新一筆水質讀值。"""
    try:
        pond = Pond.objects.get(name=pond_name)
    except Pond.DoesNotExist:
        return {"error": f"找不到池塘 `{pond_name}`，可用：{list(Pond.objects.values_list('name', flat=True))}"}

    latest = pond.readings.first()
    if not latest:
        return {"error": f"`{pond_name}` 還沒任何感測讀值"}

    return {
        "pond": pond.name,
        "species": pond.species,
        "measured_at": latest.measured_at.isoformat(),
        "temperature_c": latest.temperature,
        "ph": latest.ph,
        "dissolved_oxygen_mg_l": latest.dissolved_oxygen,
        "salinity_ppt": latest.salinity,
    }


# 🚧 TODO Session 2 練習 #1：加 get_water_quality_history(pond_name, days)
#    回傳指定池塘最近 N 天的讀值清單（讓 LLM 看趨勢）。
#
# def get_water_quality_history(pond_name: str, days: int = 7) -> dict:
#     ...


# 🚧 TODO Session 2 練習 #2：加 check_thresholds(pond_name)
#    對指定池塘最新讀值做閾值判斷，回傳哪些指標異常（DO < 4、pH > 9 等）。
#
# def check_thresholds(pond_name: str) -> dict:
#     ...


# 🚧 TODO Session 2 練習 #3：加 list_ponds()
#    列出所有池塘 + species，讓 LLM 知道有哪些池可問。
#
# def list_ponds() -> dict:
#     ...


# ============================================================
# 給 LLM 看的 tool schemas（OpenAI function calling 格式）
# ============================================================

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_latest_water_quality",
            "description": "查詢指定養殖池最新一筆水質讀值（溫度、pH、溶氧、鹽度）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "pond_name": {
                        "type": "string",
                        "description": "池塘名稱，例如：1 號池、2 號池、3 號池",
                    }
                },
                "required": ["pond_name"],
            },
        },
    },
    # 🚧 TODO Session 2：學員加完上面的 function 之後，這裡也要加對應的 schema。
    # 範本：
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "get_water_quality_history",
    #         "description": "查指定池最近 N 天的所有讀值，看趨勢。",
    #         "parameters": {...},
    #     },
    # },
]


# ============================================================
# Dispatcher — LLM 說 "call X(args)" 時，這裡執行
# ============================================================

# 把 tool name 對應到實際函數
_TOOL_REGISTRY = {
    "get_latest_water_quality": get_latest_water_quality,
    # 🚧 TODO Session 2：加新 function 後也要在這裡註冊。
}


def dispatch(name: str, arguments: dict) -> dict:
    """LLM 要求呼叫 `name`、傳 `arguments`。執行後把結果回傳給 LLM。"""
    fn = _TOOL_REGISTRY.get(name)
    if fn is None:
        return {"error": f"unknown tool: {name}"}
    try:
        return fn(**arguments)
    except TypeError as e:
        return {"error": f"參數不對：{e}"}
    except Exception as e:  # noqa: BLE001
        return {"error": f"工具執行失敗：{type(e).__name__}: {e}"}
