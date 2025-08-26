from scripts.core_memory_adapter import upsert_journal_guideline

class FakeHTTP:
    def __init__(self, changed=True): 
        self.changed = changed
    def call(self, method, params): 
        return {"changed": self.changed}

def test_upsert_changes(monkeypatch):
    def _fake_call(method, params): 
        return {"changed": True}
    monkeypatch.setattr("scripts.core_memory_adapter._call", _fake_call)
    assert upsert_journal_guideline({"journal": "Demo"}) is True

def test_upsert_no_changes(monkeypatch):
    def _fake_call(method, params): 
        return {"changed": False}
    monkeypatch.setattr("scripts.core_memory_adapter._call", _fake_call)
    assert upsert_journal_guideline({"journal": "Demo"}) is False

def test_upsert_payload_structure(monkeypatch):
    captured_params = {}
    
    def _fake_call(method, params):
        captured_params.update(params)
        return {"changed": True}
    
    monkeypatch.setattr("scripts.core_memory_adapter._call", _fake_call)
    
    payload = {
        "journal": "NEJM",
        "word_counts": {"main": 3000, "abstract": 150},
        "refs_style": "Vancouver superscript"
    }
    
    upsert_journal_guideline(payload)
    
    # Check that the correct API method was called with proper structure
    assert captured_params["type"] == "JournalGuideline"
    assert captured_params["match"]["journal"] == "NEJM"
    assert captured_params["set"]["word_counts"]["main"] == 3000