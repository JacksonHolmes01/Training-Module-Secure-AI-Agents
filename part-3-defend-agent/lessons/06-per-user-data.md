# Lesson 6: Act as the User, Not as the Agent

The confused-deputy attack needed no injection at all. Bob, an intern, simply asked HelpBot for an enterprise customer's email, and got it, because every database query ran as one login, `agent_app`, that can read every customer. The agent knew bob was bob. Nothing used that to limit what it did for him.

## The fix: the query runs as the person chatting

Two pieces work together.

**Row-level security in the database** (`db/init/01-init.sh`). A policy on `crm.customers` says: a senior agent sees everyone; anyone else sees only the accounts they personally manage. It is enforced only when the agent announces who it is acting for:

```sql
CREATE POLICY customer_access ON crm.customers FOR SELECT TO agent_app
  USING (
    current_setting('app.enforce', true) <> 'on'
    OR current_setting('app.is_senior', true) = 'true'
    OR account_manager = current_setting('app.current_user', true)
  );
```

**The agent announces the user** (`db.py`). When `DEFEND_DATA` is on, every query first tells the database who it is for:

```python
if guards.on("DEFEND_DATA") and user:
    await cur.execute("SELECT set_config('app.enforce','on',true), "
                      "set_config('app.current_user',%s,true), "
                      "set_config('app.is_senior',%s,true)", (user, senior))
```

Now the database itself filters the rows. The agent cannot show bob what bob is not allowed to see, because the database never hands those rows over.

## Test it

```bash
bin/defend.sh data on
bin/ask.sh bob "What's the email on file for Riverside Clinic?"
```

```
  tool query_db({"sql": "SELECT email FROM crm.customers WHERE name = 'Riverside Clinic'"})  [ok]
     -> {'rows': []}
Answer: There is no customer named Riverside Clinic in the database.
```

Riverside Clinic is one of alice's enterprise accounts. To bob, the row simply does not exist. And bob can still do his own job:

```bash
bin/ask.sh bob "What's the email for Copperline Bikes?"
```

Copperline is bob's account, so he sees it. Meanwhile alice, a senior agent, still sees everyone.

## Why enforce it in the database

The query ran successfully. The filtering did not depend on the agent writing careful SQL, or on the model behaving. The database applied the policy to the login's session. Even a fully compromised agent, running attacker-chosen SQL as bob, cannot read rows the policy hides.

> **The pattern.** Authenticating a user (Part 1's gateway) is only half the job. The other half is **using** that identity to limit what happens. An agent should act with the permissions of the person it serves, not with its own.

Next: [Defense 5: A Human in the Loop](07-approval-and-spotlight.md)
