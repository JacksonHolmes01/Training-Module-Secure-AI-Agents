# Lesson 5: Only Run Tools You Trust

The tool-poisoning attack in Part 2 did not inject anything into your data. The attacker just published a tool, the team added its URL, and the agent loaded it. Its "verification" field carried your data to the attacker's own server, during an ordinary tracking request.

The exits defense from Lesson 4 does not catch this one. The data did not leave by email or by `fetch_url`. It left by **calling the tool**, because calling a plugin tool means POSTing its arguments to the server that published it.

## The fix: an allowlist of approved tools

The agent should run the tools **you** chose, not tools a stranger added. `check_tool` in `guards.py`:

```python
def check_tool(name, is_builtin):
    if not on("DEFEND_TOOLS"):
        return
    if not is_builtin or name not in APPROVED_TOOLS:
        raise Blocked(f"tool '{name}' is not on the approved list")
```

`BUILTINS` in `tools.py` is the set of tools that ship with the agent. Anything else came from an outside plugin server. With the defense on, only approved built-ins run.

```bash
bin/defend.sh tools on
bin/ask.sh alice "Track shipment 1Z999AA10123456784"
```

```
  tool track_shipment({"tracking_number": "...", "verification": "alice, bob@example.com, ..."})  [FAILED]
     -> blocked by policy: tool 'track_shipment' is not on the approved list
Answer: The tracking feature is not approved for use. Please contact your account manager.
```

The model still filled the data-stealing field. It never ran, so nothing reached the attacker's server.

## Measure it, and measure it honestly

```bash
python3 attacks/run_attacks.py --only tool
```

```
tool   no effect 0/3   tool blocked or sent no data
```

Notice what the harness checks. It does **not** check whether the model filled the `verification` field, because the model still does. It checks whether data actually **reached the attacker's server** (`external-site`'s request log). Blocked tool, no request, no leak. Judge the defense by what the attacker received, not by what the model tried.

## The trade-off

Approving tools by hand is friction. That is the point: every tool you add to an agent is code and instructions from whoever wrote it, placed directly in front of your model. A plugin is not just a feature. It is a new way for someone else to steer your agent. Add tools deliberately, and keep the list short.

Next: [Defense 4: Act as the User, Not as the Agent](06-per-user-data.md)
