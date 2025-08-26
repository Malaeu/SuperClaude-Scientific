import os, json, urllib.request

CORE_MEMORY_URL = os.getenv("CORE_MEMORY_URL")  # e.g. https://core.heysol.ai/api/v1/mcp
CORE_MEMORY_TOKEN = os.getenv("CORE_MEMORY_TOKEN")

def _call(method: str, params: dict):
    req = urllib.request.Request(
        CORE_MEMORY_URL,
        data=json.dumps({"method": method, "params": params}).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {CORE_MEMORY_TOKEN}"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def upsert_journal_guideline(payload: dict) -> bool:
    """
    Expected server method (пример): core.memory.upsert_node
    Node type: JournalGuideline
    Unique key: journal
    """
    # TODO: адаптировать под реальный API методов MCP core-memory
    res = _call("core.memory.upsert_node", {
        "type": "JournalGuideline",
        "match": {"journal": payload["journal"]},
        "set": payload
    })
    return bool(res.get("changed", True))