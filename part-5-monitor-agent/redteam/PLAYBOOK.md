# Red-team playbook (agent)

Rules of engagement for the Part 5 campaign:
- Run only against your own local lab, never a shared or production system.
- Run with the Part 3 defenses and the Part 4 sandbox on. The goal is to prove
  the attacks are detected, not to cause harm; the defenses keep data safe.
- Every email the agent "sends" lands in the local Mailpit inbox and the
  "internet" is a container that only logs requests. Nothing leaves your machine.

Steps (see bin/redteam.py --list): exfiltration by email (R1, R2), tool
poisoning (R3), path traversal (R4), code execution (R5), exfiltration by URL
(R6), and the confused deputy (R7). Score with bin/coverage.py.
