# Lesson 8: Conclusion

You made the agent's behavior visible, and proved you can see an attack:

- **A security log** of every tool call and decision, recording what happened and why, and deliberately never the content, so the log does not become a second copy of the data you are protecting
- **Detection rules** for the signatures of the Part 2 attacks: outside email, outside tools, path traversal, blocked fetches, code execution, bursts
- **A red-team campaign** that attacks your own agent on purpose and **scores** which attempts your log caught, 6 of 7, then 7 of 7 once you accepted the trade-off of one noisier rule
- **The honest limits**: detection trails new attacks, cannot see what never happened, and watches only the agent's own actions

And the idea that separates this part from the three before it: **prevention and detection are different jobs.** Parts 3 and 4 stop the attack. Part 5 tells you it was tried. The blocked attack you never heard about is the one that teaches an attacker exactly where your walls are.

## The series

You have taken an AI agent all the way around:

| Part | You |
|---|---|
| 1 Build | gave a model real tools and watched it act |
| 2 Attack | made it email data out, hand data to a malicious tool, read secret files, and overreach |
| 3 Defend | confined the tools, controlled the exits, scoped data to the user, each measured |
| 4 Contain | sandboxed the code tool, gave every container least privilege, controlled egress |
| 5 Monitor | logged every action, wrote detection rules, and red-teamed the result |

An agent is a model that acts, and every capability you give it is a capability an attacker will try to borrow. Securing one is not a prompt you write once. It is defense in depth: least privilege in the code, containment in the infrastructure, and monitoring over all of it, each layer assuming the others will sometimes fail.

Thank you for working through the series. Go build agents that are secure from the first tool you hand them.

---

License: CC BY-SA 4.0. Jackson Holmes
