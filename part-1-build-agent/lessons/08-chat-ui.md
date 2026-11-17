# Lesson 8: The Chat UI

Open **http://localhost:7860**.

- **You are:** choose `alice` or `bob`. The UI sends that person's API key to NGINX from the server side; the key never reaches your browser
- Type a request. Under each answer, **What the agent did** lists every tool call with its arguments

Try a few of the requests from Lesson 4, then try the same request as alice and as bob. With the same request, the agent behaves the same way for both people. That is the problem Lesson 5 described.

Keep the inbox open in another tab (**http://localhost:8025**) while you chat. When the agent sends an email, it appears there within a second.

Next: [What Could Go Wrong](09-what-could-go-wrong.md)
