# Lesson 7: Containment Review

Put the layers together and see the whole picture. With the code sandbox and hardening both on:

```bash
bin/defend.sh sandbox on
bin/harden.sh on
```

**The code tool** runs where there is nothing to steal:

```bash
python3 -c "print('sandbox has no network and no secrets, proven in Lesson 4')"
```

**The containers** resist a foothold:

```bash
python3 bin/audit.py        # agent-api and sandbox at 9/9
bin/attacker_demo.sh        # no root, no code changes, no dropped tools, no installs
```

**The attacks from Part 2 still fail**, now with containment under the Part 3 defenses. Turn the Part 3 defenses on and run the harness:

```bash
bin/defend.sh all on
python3 attacks/run_attacks.py
```

```
0 of 4 data-theft attacks succeeded at least once.
```

## How the layers relate

Think of it as depth, each layer catching what the one before it might miss:

| If this fails... | ...this still holds |
|---|---|
| A prompt-injection guard (Part 3) | The egress allowlist: data still cannot leave |
| The egress guard | Least privilege: the attacker in the container can do little |
| Least privilege | The sandbox: code execution never had secrets or network |
| Everything in the app | The database's own per-user rules still filter the rows |

No single control is trusted to be perfect. That is the point of defense in depth: you assume each layer will sometimes fail, and you make sure the next one is there.

## A single scorecard never tells the whole story

The audit says 76%, not 100%, because the database and model containers are not fully hardened here. The attacker demo still shows two YES lines. Neither means the agent is unsafe; it means those risks are handled by **other** controls (the sandbox, egress, per-user data) that the audit does not score. Read every number for what it measures, and know what it leaves out.

Next: [Conclusion](08-conclusion.md)
