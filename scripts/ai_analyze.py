import json, os, sys, urllib.request

def call_llm(prompt: str) -> dict:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return {"healthy": True, "reason": "no LLM key; defaulting to healthy", "rollback": False}
    body = json.dumps({
        "model": "gpt-4o-mini",
        "messages": [{"role":"user","content":prompt}],
        "temperature": 0
    }).encode()
    req = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        txt = json.load(r)["choices"][0]["message"]["content"]
    try: return json.loads(txt)
    except: return {"healthy": True, "reason": "parse error", "rollback": False}

if __name__ == "__main__":
    prompt = "Analyze these logs and return JSON: {\"healthy\":bool,\"reason\":str,\"rollback\":bool}\n" + sys.argv[1]
    print(json.dumps(call_llm(prompt), indent=2))
