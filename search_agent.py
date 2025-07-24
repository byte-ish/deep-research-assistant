"""
Search Agent

This module defines the SearchAgent, which takes a search term and produces a concise
summary of the web results. This agent focuses on extracting the most important points 
from search results, ignoring unnecessary details or commentary.

Workflow:
1. Receives a search term as input.
2. Uses the WebSearchTool to perform a web search.
3. Generates a concise 2–3 paragraph summary (under 300 words) of the results.
4. Returns the summary for further synthesis by the WriterAgent.

This agent is part of the research pipeline and provides raw, distilled information.
"""

from agents import Agent, WebSearchTool, ModelSettings

# Instructions for the AI agent
INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must be 2–3 paragraphs and less than 300 "
    "words. Capture only the main points. Write succinctly—no need for complete sentences or perfect grammar. "
    "This will be consumed by someone synthesizing a report, so it is vital you capture the essence and ignore any fluff. "
    "Do not include any commentary beyond the summary itself."
)

# SearchAgent: Performs web searches and summarizes the results
search_agent = Agent(
    name="SearchAgent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],  # Uses a web search tool with low context size
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),  # Ensures the web search tool is always used
)
