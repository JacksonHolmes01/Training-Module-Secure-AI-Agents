# Lesson 6: What Hardening Cannot Fix

After hardening, the attacker inside the agent container still could do two things:

```
  read the database password?            YES
  reach the attacker site on the net?    YES
```

Hardening did not fix them because they are not about privilege inside the container. They are about what the container is **given**.

## The secret

The agent needs the database password to do its job, so the password is mounted into its container. Any code running **as the agent** can read it, root or not. Hardening cannot hide a secret from the process it was given to.

The answers are the ones you have already seen:
- For the **code tool**, the sandbox (Lesson 4) runs snippets in a container that was never given the secret. That is why the sandboxed snippet found `secrets I can see: []`.
- For the agent itself, you shrink the blast radius: give it the narrowest credential possible (Part 3's per-user database access is exactly this), and rotate secrets so a stolen one expires.

The lesson: do not mount a secret into a container that does not need it. The sandbox needs the CPU, not the database password, so it does not have it.

## The network

The agent could still reach `evil.example`, so a compromised agent could still send data out. The fix is **egress control**: let the agent reach only the hosts it actually needs.

See the gap, then close it:

```bash
bin/egress.sh test
```

```
  evil.example: REACHABLE
  partner-news.example: REACHABLE
```

```bash
bin/egress.sh on
```

```
Disconnected agent-api from ..._outside.
  evil.example: gaierror
```

Cut off from the outside network, the agent can no longer reach the attacker's site at all, at the network layer, no matter what its code tries. Restore it with `bin/egress.sh off`.

This blunt cut also blocks the legitimate partner site, because the lab puts both on one network. In production you keep the agent connected but route its outbound through an **allowlist proxy**, so only approved hosts answer and everything else is refused, the network-layer twin of Part 3's fetch allowlist.

The cleanest example of egress control is already in your lab: the **sandbox** has `network_mode: none`. The component that does not need the network was simply never given it. Give each part of the agent only the reach it needs.

Next: [Containment Review](07-review.md)
