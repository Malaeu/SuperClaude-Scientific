import argparse, hashlib, json, os, time
from pathlib import Path
import yaml
from core_memory_adapter import upsert_journal_guideline
from parsers.normalize import normalize_guidelines
# from parsers.fetch import parse_html_or_pdf  # TODO: implement

def sha256(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode("utf-8")).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--journals", help="Comma-separated list")
    args = ap.parse_args()

    if args.sources.endswith(".json"):
        src = json.loads(Path(args.sources).read_text())
    else:
        # Use pyyaml for proper YAML parsing
        with open(args.sources, 'r') as f:
            src = yaml.safe_load(f)

    updated, unchanged, missing = [], [], []
    
    # Filter journals if --journals specified
    if args.journals:
        scope = set(map(str.strip, args.journals.split(",")))
    else:
        scope = None
    
    for j in src["journals"]:
        if scope and j["journal"] not in scope:
            continue
        
        # For now, use placeholder text since we don't have the HTML fetcher implemented
        raw = f"Sample guideline text for {j['journal']} journal"  # TODO: replace with parse_html_or_pdf(j["source_url"])
        
        if not raw:
            missing.append(j["journal"])
            continue
        
        norm = normalize_guidelines(raw)
        norm["journal"] = j["journal"]
        norm["publisher"] = j.get("publisher")
        norm["source_url"] = j["source_url"]
        norm["retrieved_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        norm["source_hash"] = sha256(raw)
        
        if args.dry_run:
            # Print normalized block without writing
            print(json.dumps({"journal": j["journal"], "normalized": norm}, indent=2))
        else:
            changed = upsert_journal_guideline(norm)
            (updated if changed else unchanged).append(j["journal"])

    if not args.dry_run:
        print(json.dumps({"updated": updated, "unchanged": unchanged, "missing": missing}, indent=2))

if __name__ == "__main__":
    main()