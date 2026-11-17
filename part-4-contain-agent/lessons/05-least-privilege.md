# Lesson 5: Least Privilege for Every Container

The sandbox protects the code tool. But the agent container itself runs the whole agent, and if an attacker ever got code running there (a vulnerable library, a bug in a tool), what could they do? Find out.

## The attacker inside the agent container

`bin/attacker_demo.sh` runs commands as the agent container's user, the way an attacker with a foothold would. With nothing hardened yet:

```bash
bin/harden.sh off     # make sure hardening is off
bin/attacker_demo.sh
```

```
  run as root?                           YES  uid 0 (root)
  read the database password?            YES  read it
  modify the agent's own code?           YES  patched main.py
  drop a tool in /tmp and run it?        YES  run
  install software (apt-get)?            YES  apt works
  reach the attacker site on the net?    YES  reached evil.example
```

Everything. Root, secrets, rewrite the agent's own code, install tools, phone home. A foothold in this container is total.

## Audit the containers

`bin/audit.py` scores every container against a hardening checklist (the same checks as the database-hardening series: non-root, no capabilities, no privilege escalation, read-only filesystem, limits, pinned images):

```bash
python3 bin/audit.py
```

```
agent-api       ...  3/9
agent-sandbox   ...  8/9
...
Total: 31 of 81 checks pass (38%)
```

Notice `agent-sandbox` already scores high: you built it hardened in Lesson 4. The rest start weak.

## Turn hardening on

```bash
bin/harden.sh on
```

This applies `hardening/harden.yml`: the agent and the Python helpers run as a non-root user with a read-only filesystem, every container drops its Linux capabilities and blocks privilege escalation, process counts are capped, and images are pinned by digest. Re-audit:

```bash
python3 bin/audit.py
```

```
agent-api       ...  9/9
agent-sandbox   ...  9/9
agent-external  ...  9/9
Total: 62 of 81 checks pass (76%)
```

(The database, model, and mail containers score lower: they are stateful third-party services, and hardening them is the subject of the database series. Here the agent is what we are containing.)

## The attacker, contained

```bash
bin/attacker_demo.sh
```

```
  run as root?                           no   uid 10001
  read the database password?            YES  read it
  modify the agent's own code?           no   Read-only file system
  drop a tool in /tmp and run it?        no   Permission denied
  install software (apt-get)?            no
  reach the attacker site on the net?    YES  reached evil.example
```

Most of the attacker's options are gone. A foothold is no longer total: they cannot become root, change the agent's code, drop and run tools, or install anything.

Two lines still say **YES**. Those are not oversights. They are the next lesson.

Next: [What Hardening Cannot Fix](06-egress.md)
