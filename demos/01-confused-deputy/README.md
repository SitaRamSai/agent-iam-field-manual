# Demo 01 — The Confused Deputy

A minimal Python agent that demonstrates the confused-deputy problem in
the LLM-agent context. Framework-less, single file, ≤200 LOC.

## What it does

1. Reads a user's email inbox (simulated or real).
2. The agent follows an attacker-supplied instruction embedded in an
   email body.
3. The agent exfiltrates data the user never authorized it to share,
   using the agent's own ambient credentials.

Output: a terminal session screenshot-ready for the Chapter 1 thread.

## Why framework-less

The point of this demo is the principle, not a framework. LangChain or
CrewAI would obscure the IAM failure inside framework abstractions. A
plain Python agent makes the confused deputy visible in ~150 lines.

## Run

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...   # or ANTHROPIC_API_KEY
python demo.py
```

Mock mode (no API key, no cost):
```bash
python demo.py --mock
```

## Status

- [ ] `demo.py` (real LLM path)
- [ ] `demo.py` mock path
- [ ] `requirements.txt`
- [ ] Sample inbox fixtures (`fixtures/inbox.json`)
- [ ] Terminal-session screenshot for the chapter
- [ ] Mitigation patch (a `demo_fixed.py` showing what scoped capabilities look like)

Target: working end-to-end by end of week 2. Mitigation patch by week 3.
