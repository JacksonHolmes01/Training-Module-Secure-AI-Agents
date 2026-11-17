# Lesson 8: Conclusion

Part 3 defended the agent in its code. Part 4 assumed that code could fail, and limited what a failure costs:

- **Sandboxed the code tool.** `run_python` runs in a container with no network, no secrets, a read-only filesystem, and hard limits. The most dangerous capability an agent can have now has the least power. The same malicious snippet that read every secret and reached the attacker in Lesson 3 found nothing in Lesson 4
- **Gave every container least privilege.** Non-root, read-only, no capabilities, no privilege escalation, capped, pinned. An audit measured it (38% to 76%), and an attacker-inside demo showed a container foothold shrink from total to almost nothing
- **Controlled egress.** Cut off from untrusted networks, a compromised agent cannot send data out, no matter what its code attempts. The sandbox, with no network at all, is the ideal in miniature

And you saw the honest limits: hardening cannot hide a secret from the process it is given to, or block a network the container is on. Those are fixed by giving each part only what it needs, which is the single idea under every lesson in this part and the last: **least privilege.**

## Where the series stands

You have built an agent, attacked it, defended it, and contained it. One thing is still missing. Every block, every sandbox refusal, every audit failure in this part happened quietly. Nobody was watching.

**Part 5: Monitor the Agent.** Turn every tool call and every blocked action into a structured log. Write detection rules that fire on the signatures of these attacks. Run a red-team campaign against the finished system and score what your logs actually caught, so a real attack raises an alarm instead of passing in silence.

---

License: CC BY-SA 4.0. Jackson Holmes
