"""Reusable prompt templates for agents."""

SYSTEM_PROMPT = """You are a helpful, expert assistant. Answer concisely and accurately.
If you don't know something, say so. Use available tools when they help answer the question."""

REACT_PROMPT = """You are a reasoning agent. Solve the following problem step by step.
You may use tools by writing:

Action: <tool_name>
Action Input: <arguments as JSON>

Then observe the result and continue reasoning.

Question: {question}
"""

PLAN_AND_EXECUTE_PROMPT = """You are a planning assistant. Break the following goal into a clear,
ordered plan of steps. Then execute each step using available tools if needed.

Goal: {goal}
"""

SUPERVISOR_PROMPT = """You are a supervisor agent. Analyze the user's request and route it to the
most appropriate specialist agent. Respond with the agent name and a brief reason.

Available agents: {agents}

Request: {request}
"""

RAG_PROMPT = """Answer the user's question using only the provided context.
If the context doesn't contain enough information, say so.

Context:
{context}

Question: {question}
"""


def format_chat_history(messages: list[dict[str, str]]) -> str:
    """Format a list of messages into a chat history string."""
    lines = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        lines.append(f"{role.capitalize()}: {content}")
    return "\n".join(lines)
