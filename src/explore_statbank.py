import json
import requests

BASE = "https://api.statbank.dk/v1"

def tableinfo(table: str) -> dict:
    r = requests.post(f"{BASE}/tableinfo",
                      json={"table": table, "lang": "en", "format": "JSON"},
                      timeout=30)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    for table in ["DNRENTD", "MPK100"]:
        info = tableinfo(table)
        print("=" * 70)
        print(table, "-", info["description"])
        for var in info["variables"]:
            print(f"\n  Variabel: {var['id']} ({var['text']})")
            for v in var["values"][:15]:
                print(f"     {v['id']:<12} {v['text']}")
            if len(var["values"]) > 15:
                print(f"     ... og {len(var['values']) - 15} flere")