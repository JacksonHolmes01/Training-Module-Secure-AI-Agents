# Lesson 8: The Scoreboard

You have turned on each defense and watched it stop its attack. Now watch the whole picture at once: the attacks that succeed dropping to zero as the defenses stack up.

```bash
bin/scoreboard.sh
```

It turns on the defenses one at a time, in order, and re-runs the attack harness after each. It takes a few minutes (it attacks your lab dozens of times).

## What you will see

Your exact numbers will vary from run to run, because prompt injection is probabilistic. The shape is what matters:

| Defenses on | traversal | customers | secret | tool | confused-deputy | Data-theft attacks that still work |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| none (Part 2) | leaks | leaks | leaks | leaks | leaks | 4 of 4 |
| + confine paths | **blocked** | leaks | leaks | leaks | leaks | 3 of 4 |
| + email allowlist | blocked | **blocked** | **blocked** | leaks | leaks | 1 of 4 |
| + fetch allowlist | blocked | blocked | blocked | leaks | leaks | 1 of 4 |
| + approved tools | blocked | blocked | blocked | **blocked** | leaks | 0 of 4 |
| + per-user data | blocked | blocked | blocked | blocked | **blocked** | 0 of 4 |

Each defense removes one column, and none of the earlier ones comes back. By the last row, every attack from Part 2 is stopped, and (from Lesson 4 and the regression checks) the agent still does its real job.

## Two things worth noticing

**The fetch allowlist row does not change the count.** None of the four scored attacks happened to use `fetch_url`. Does that mean it was useless? No. It closed the web-page exfiltration channel you saw in Part 2, Lesson 4, which the harness does not score. A defense that stops an attack you did not happen to measure is still a defense. One scoreboard never tells the whole story.

**Order is not arbitrary.** The defenses that make harm impossible (paths, exits, tools, data) come first and carry the weight. Approval and spotlighting come last, as depth. If you had started with spotlighting alone, the scoreboard would barely move, because it depends on the model, and the model is what the attacker controls.

## Prove it still works for real users

A defense that blocks attacks and also blocks the work is not a win. With everything on:

```bash
bin/defend.sh all on
bin/ask.sh alice "Email ops@harbor-logistics.example.com about their renewal."   # a customer: allowed
bin/ask.sh alice "Summarize http://partner-news.example/shipping-update"          # the real partner site: allowed
bin/ask.sh bob "What's the email for Copperline Bikes?"                            # bob's own account: allowed
```

(With approval on, the email is held for a human, which is the intended behavior.)

Next: [Conclusion](09-conclusion.md)
