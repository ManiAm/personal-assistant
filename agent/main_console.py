
import asyncio
import logging

from langchain_core.messages import AIMessage, HumanMessage
from agent_setup import build_agent

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log = logging.getLogger(__name__)

# Suppress HTTP logs
logging.getLogger("httpx").setLevel(logging.WARNING)


def print_banner(title):

    border = "=" * 80
    log.info("\n%s\n[User Question] %s\n%s\n", border, title, border)


def get_last_AI_message(message_list):

    for msg in reversed(message_list):

        if not isinstance(msg, AIMessage):
            continue

        content = msg.content.strip()
        if not content:
            continue

        return content

    return None


def prune_messages(message_list):

    for msg in message_list[:]:

        if isinstance(msg, HumanMessage) or (isinstance(msg, AIMessage) and msg.content):
            continue

        message_list.remove(msg)

    return message_list


async def run_console_mode():

    agent = await build_agent()

    state = {"messages": []}

    user_questions = [
        # "What is the time in Walnut Creek, CA?",
        # "What is the time zone in Walnut Creek, CA?",
        # "what's the timezone in Berlin?",

        # "What is the current weather in Walnut Creek, CA ?",
        # "What will the weather be like in Tokyo for the next 7 days?",

        # "Get the current quote for Cisco Systems.",
        # "Get company news for Cisco Systems from 2025-01-01 to 2025-04-01",
        # "What is ticker symbol for microsoft?",
        # "What are the top stock exchanges?",
        # "Is US stock market open now?",
        # "What are holidays for US stock market?",
        # "What's the current market cap of NVIDIA?",
        # "Compare NVIDIA stock price with Apple.",

        # "Who owns SpaceX?",
        # "What is Taylor Swift's net worth in 2025?",

        "Can you find a song titled 'Shape of You' by Ed Sheeran?",
        "I'm looking for a song called 'Rolling in the Deep' by Adele. Can you find it?",
        "Please find details about the artist 'Ariana Grande'.",

        "Can you list all the emails I received today?",

        "Can you list my upcoming events for this week?"
    ]

    for user_question in user_questions:

        print_banner(user_question)

        state["messages"].append(HumanMessage(content=user_question))

        response = await agent.ainvoke(state, config={"recursion_limit": 10})

        messages = response["messages"]

        final_answer = get_last_AI_message(messages)
        log.info("[Final Answer] %s", final_answer)

        # For debugging
        # for m in messages:
        #     print(f"[{m.__class__.__name__}] {m.content}")
        #     if hasattr(m, 'tool_calls'):
        #         print(f"Tool Calls: {m.tool_calls}")
        #     if hasattr(m, 'additional_kwargs'):
        #         print(f"Additional: {m.additional_kwargs}")

        state["messages"] = prune_messages(messages)


if __name__ == "__main__":

    asyncio.run(run_console_mode())
