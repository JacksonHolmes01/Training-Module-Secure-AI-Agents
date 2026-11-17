# Lesson 10: Conclusion

You built an AI agent and watched it work:

- **The agent loop:** the model asks for tools, your code runs them, and the results go back to the model until it answers
- **Tool calling is text:** the model writes a `<tool_call>` block, and your code decides whether to run it
- **Tools are capabilities:** search, files, web, database, tickets, and email, all chosen by the model
- **Identity:** NGINX turns each person's key into a name that nobody can forge, and the API only trusts names that come through the gateway
- **The database is a real boundary:** the model tried to delete tickets and the database refused
- **Traces:** every action is recorded, so you can see what the agent did, not just what it said

And you found the weak points: an agent that obeys whatever text it reads, can send anything anywhere, reads any path, and acts for everyone with the same rights.

## What comes next

**Part 2: Attack the Agent.** Plant instructions in a document and a web page, and watch HelpBot email customer data to an outside address, leak secrets through a web address, read files it should never see, and act for bob as if he were alice.

---

License: CC BY-SA 4.0. Jackson Holmes
