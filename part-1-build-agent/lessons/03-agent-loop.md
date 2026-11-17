# Lesson 3: The Agent Loop

Ask HelpBot something:

```bash
bin/ask.sh alice "What does our policy say about refunds over 1000 dollars?"
```

```
User: alice   (2 model calls, 4.2s)
  tool search_docs({"query": "refunds over 1000 dollars"})  [ok]
     -> [Refund Policy] Refunds are available within 30 days of purchase. Refunds over $1,000 need approval from a team lead...
Answer: Our policy states that refunds over $1,000 need approval from a team lead. They are available within 30 days of purchase.
```

Two model calls for one question. Here is why.

---

## The loop

Open `agent-api/app/agent.py` and find `run_agent`. Stripped down, it is:

```python
for step in range(1, MAX_STEPS + 1):
    raw = await ollama_chat(messages)        # 1. ask the model
    text, calls = parse_reply(raw)           # 2. did it ask for tools?
    if not calls:
        return text                          #    no: that is the answer
    for call in calls:                       # 3. yes: run each tool
        result = await FUNCTIONS[call["name"]](call["arguments"], user)
    messages.append(results)                 # 4. show the model the results, loop again
```

In the example above:
1. **Model call 1.** The model reads the question and decides it needs the knowledge base. It asks for `search_docs`
2. The agent runs `search_docs` and adds the documents it found to the conversation
3. **Model call 2.** The model reads the documents and writes the answer. No more tools, so the loop ends

`AGENT_MAX_STEPS` (6 in `.env`) caps how many times the loop can go round, so a confused model cannot loop forever.

---

## Tool calling is just text

How does a model "ask for a tool"? Look at what it actually writes. This sends one request straight to the model and prints its raw reply:

```bash
docker exec agent-api python -c "
import asyncio
from app import agent
m = [{'role': 'system', 'content': agent.SYSTEM_PROMPT.format(user='alice') + agent.TOOL_INSTRUCTIONS},
     {'role': 'user', 'content': 'Summarize http://intranet.local/holidays.html'}]
print(asyncio.run(agent.ollama_chat(m)))"
```

```
<tool_call>
{"name": "fetch_url", "arguments": {"url": "http://intranet.local/holidays.html"}}
</tool_call>
```

That is all a tool call is: text in a format the model was trained to write. `parse_reply()` finds the `<tool_call>` blocks with a regular expression and reads the JSON inside. The model never runs anything itself. **Your code** decides to run what the model asked for.

Keep that in mind for the rest of the series. Every defense in Part 3 lives in that gap, between "the model asked" and "the code ran it".

> **Why not let Ollama parse tool calls?** Ollama can do it, and you will see that in many tutorials. Building this lab, its built-in parser silently dropped some perfectly valid calls, and the agent did nothing with no error. Parsing them here is about 20 lines, and you can see every step.

## How the model learns which tools exist

`TOOL_INSTRUCTIONS` lists every tool's **schema** in the system prompt: its name, a description, and its arguments. The model never sees the code behind a tool, only these descriptions. It chooses tools by reading them, which means a tool's description is an instruction to the model. Part 2 abuses exactly that.

## The trace

Every tool call is recorded in a **trace**: which tool, which arguments, whether it worked, and the start of what it returned. `bin/ask.sh` prints it, the chat UI shows it, and the API returns it in every `/chat` response. **What an agent did matters more than what it said**, and an agent can easily claim to have done something it did not, or do something it never mentions.

Next: [The Tools](04-tools.md)
