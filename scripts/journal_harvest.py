import argparse, hashlib, json, os, time
from pathlib import Path
from core_memory_adapter import upsert_journal_guideline
from parsers import parse_html_or_pdf  # TODO: implement

def sha256(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode("utf-8")).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", required=True)
    args = ap.parse_args()

    src = json.loads(Path(args.sources).read_text().replace("'", '"')) \
          if args.sources.endswith(".json") else None
    if src is None:
        # naive YAML→dict (для примера; замени на pyyaml)
        lines = Path(args.sources).read_text().splitlines()
        pairs = []
        cur = {}
        arr = []
        for ln in lines:
            if ln.strip().startswith("- journal:"):
                if cur: arr.append(cur); cur={}
                cur["journal"] = ln.split(":")[1].strip().strip('"')
            elif "publisher:" in ln: cur["publisher"] = ln.split(":")[1].strip().strip('"')
            elif "source_url:" in ln: cur["source_url"] = ln.split(":")[1].strip().strip('"')
            elif "format:" in ln: cur["format"] = ln.split(":")[1].strip().strip('"')
        if cur: arr.append(cur)
        src = {"journals": arr}

    updated, unchanged, missing = [], [], []
    for j in src["journals"]:
        raw = parse_html_or_pdf(j["source_url"])  # TODO
        if not raw:
            missing.append(j["journal"]); continue
        norm = normalize_guidelines(raw)  # TODO: implement from regex/patterns
        norm["journal"] = j["journal"]
        norm["publisher"] = j.get("publisher")
        norm["source_url"] = j["source_url"]
        norm["retrieved_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        norm["source_hash"] = sha256(raw)
        changed = upsert_journal_guideline(norm)  # returns True if new/changed
        (updated if changed else unchanged).append(j["journal"])

    print(json.dumps({"updated": updated, "unchanged": unchanged, "missing": missing}, indent=2))

if __name__ == "__main__":
    main()