"""Mitigated variant: scoped delegation + complete mediation.

Same model, same inbox, same attacker email as demo.py. The difference
is the authorization boundary in front of the tools.

Mitigation shape:
  - Principal separation: user, agent runtime, and tool runner are
    three distinct principals.
  - Scoped delegation: before the agent acts, the runtime requests an
    intent-scoped delegation token from a (mock) authorization server.
    The token names the user, names the agent as the actor, and
    enumerates the actions and resources the user actually approved.
  - Complete mediation: every tool call is re-checked against the
    token before execution. Calls outside the token's scope are
    refused.
  - Audit chain: each decision is logged with user, actor, tool,
    resource, decision, reason, timestamp, and a request id.

Run:  python demo_fixed.py [--real | --local] [--model NAME]
"""

from __future__ import annotations

import argparse
import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from demo import (
    load_accounts, load_inbox, model_local, model_mock, model_real,
)

FIXTURES = Path(__file__).parent / "fixtures"


@dataclass
class IntentToken:
    """Scoped delegation token. Names user, actor, and approved scope.

    Analogous in shape to an RFC 8693 token with `act` (actor) claim
    and resource/audience targeting. This is a teaching mock; do not
    reuse it as a real-world token format.
    """
    user: str
    actor: str
    allowed: list[dict[str, str]]
    request_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])


AUDIT: list[dict[str, str]] = []


def audit(token: IntentToken, tool: str, args: dict[str, Any],
          decision: str, reason: str) -> None:
    AUDIT.append({
        "ts": str(int(time.time())),
        "request_id": token.request_id,
        "user": token.user,
        "actor": token.actor,
        "tool": tool,
        "resource": str(args),
        "decision": decision,
        "reason": reason,
    })


# --- Authorization server (mock) ----------------------------------------

def issue_token(user: str, agent: str,
                intent: list[dict[str, str]]) -> IntentToken:
    """The user (out of band) tells the auth server what they intended.

    The agent never gets to widen the scope on its own."""
    return IntentToken(user=user, actor=agent, allowed=list(intent))


def authorized(token: IntentToken, tool: str,
               args: dict[str, Any]) -> tuple[bool, str]:
    for rule in token.allowed:
        if rule.get("action") != tool:
            continue
        for key, value in rule.items():
            if key == "action":
                continue
            if str(args.get(key)) != str(value):
                break
        else:
            return True, f"matches rule {rule}"
    return False, "no matching rule in delegation token"


# --- Tools wrapped by the mediation boundary ----------------------------

def mediated_get_account(token: IntentToken, args: dict[str, Any]
                         ) -> dict[str, str]:
    ok, reason = authorized(token, "get_account", args)
    audit(token, "get_account", args,
          "allow" if ok else "deny", reason)
    if not ok:
        return {"error": "refused: " + reason}
    accounts = load_accounts()
    return accounts.get(args["account_id"],
                        {"error": "no such account"})


def mediated_send_email(token: IntentToken, args: dict[str, Any]
                        ) -> dict[str, str]:
    ok, reason = authorized(token, "send_email", args)
    audit(token, "send_email", args,
          "allow" if ok else "deny", reason)
    if not ok:
        return {"error": "refused: " + reason}
    return {"status": "sent", "to": args["to"]}


MEDIATED_TOOLS = {
    "get_account": mediated_get_account,
    "send_email": mediated_send_email,
}


# --- Runtime -----------------------------------------------------------

def run_agent(model_fn: Any) -> None:
    inbox = load_inbox()
    user_intent = [
        {"action": "get_account", "account_id": "a-1042"},
    ]
    token = issue_token(
        user="alice@acme.example",
        agent="support-agent/v1",
        intent=user_intent,
    )
    print(f"[auth] issued token {token.request_id} for {token.user}: "
          f"{token.allowed}")
    print(f"[agent] read {len(inbox)} messages from inbox")
    refused = 0
    for i, msg in enumerate(inbox, 1):
        subj = msg.get("subject", "")[:60]
        print(f"\n[agent] message {i}/{len(inbox)} "
              f"from {msg['from']} — {subj!r}")
        calls = model_fn([msg])
        print(f"[agent] model emitted {len(calls)} tool call(s) "
              f"for message {i}")
        for call in calls:
            name, args = call.get("name"), dict(call.get("args", {}))
            fn = MEDIATED_TOOLS.get(name)
            if not fn:
                audit(token, name, args, "deny", "unknown tool")
                print(f"[boundary] unknown tool: {name}")
                refused += 1
                continue
            result = fn(token, args)
            verdict = "allow" if "error" not in result else "deny"
            print(f"[boundary] {verdict} {name}({args}) -> {result}")
            if verdict == "deny":
                refused += 1
    print("\n--- audit log ---")
    for row in AUDIT:
        print(json.dumps(row))
    if refused and not any(
            r["decision"] == "allow" and r["tool"] == "send_email"
            for r in AUDIT):
        print(f"\nREFUSED: {refused} out-of-scope call(s) blocked by "
              "the authorization boundary.")
    else:
        print("\nNo out-of-scope calls blocked.")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--real", action="store_true")
    g.add_argument("--local", action="store_true")
    p.add_argument("--model", default=None)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.real:
        model_fn = lambda inbox: model_real(inbox, args.model)
    elif args.local:
        model_fn = lambda inbox: model_local(inbox, args.model or "llama3.2")
    else:
        model_fn = model_mock
    run_agent(model_fn)


if __name__ == "__main__":
    main()
