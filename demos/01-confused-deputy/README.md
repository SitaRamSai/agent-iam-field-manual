# Demo 01 — The Confused Deputy

A framework-less Python PoC for the failure mode described in
[Chapter 1](../../chapters/01-confused-deputy/chapter.md). One vulnerable
agent, one mitigated agent, the same fixtures.

## What it shows

A support agent reads three emails. One of them is from an attacker who
embedded an instruction in the email body asking the agent to send a
customer record to an attacker-controlled address.

- [`demo.py`](demo.py) executes every tool call the model emits using
  the runtime's ambient authority. The record leaves the building.
  Stdout prints `EXFILTRATED`.
- [`demo_fixed.py`](demo_fixed.py) runs the same scenario behind an
  authorization boundary. The user issues a scoped delegation token
  naming the action and resource they actually approved. Every tool
  call is re-checked against the token. The attacker's instruction
  reaches the model. The model emits a tool call. The boundary refuses
  it. Stdout prints `REFUSED`. Every decision is in an audit log with
  user, actor, tool, resource, decision, and reason.

## Run

Default — mock model, zero dependencies, deterministic. This is what CI runs:

```bash
python3 demos/01-confused-deputy/demo.py
python3 demos/01-confused-deputy/demo_fixed.py
```

Optional — real provider (uses an API key from the environment if
present, falls back to mock if not):

```bash
export OPENAI_API_KEY=sk-...        # or
export ANTHROPIC_API_KEY=sk-ant-...
python3 demos/01-confused-deputy/demo.py --real
```

Optional — local model via Ollama on `localhost:11434`:

```bash
ollama run llama3.2 &
python3 demos/01-confused-deputy/demo.py --local --model llama3.2
```

No paid services required. No third-party Python packages required.
Pure standard library.

## Expected output

`demo.py` ends with a line that starts with `EXFILTRATED`. `demo_fixed.py`
ends with a line that starts with `REFUSED:`. CI greps for both.

## Why framework-less

The point of the demo is the structural failure, not a framework. Hiding
the tool boundary behind an agent library would obscure the IAM lesson.
Plain Python, single file, makes the confused deputy visible.
