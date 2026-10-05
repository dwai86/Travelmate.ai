import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq


load_dotenv()


def get_llm():
    return ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
        timeout=15,
        max_retries=0,
        max_tokens=1024
    )
  
"""
def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.2,
        reasoning_effort="low",
        api_key=os.getenv("GROQ_API_KEY"),
        timeout=15,
        max_retries=0,
        max_tokens=1024
    )
"""