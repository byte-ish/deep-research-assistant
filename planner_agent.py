"""
Planner Agent

This module defines the PlannerAgent, which is responsible for analyzing a user's query 
and coming up with a set of web search terms to gather the most relevant information.

Workflow:
1. Takes a research query as input.
2. Generates a plan containing multiple search items, each with a search term and reasoning.
3. Returns the plan as a structured `WebSearchPlan` object.

It uses a GPT-based Agent to generate these search terms.
"""

from pydantic import BaseModel, Field
from agents import Agent

# Number of search terms to generate for each query
HOW_MANY_SEARCHES = 5

# Instructions provided to the AI agent
INSTRUCTIONS = (
    f"You are a helpful research assistant. Given a query, come up with a set of web searches "
    f"to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for."
)


class WebSearchItem(BaseModel):
    """
    Represents a single web search item with reasoning and the search query.
    """
    reason: str = Field(
        description="Your reasoning for why this search is important to the query."
    )
    query: str = Field(
        description="The search term to use for the web search."
    )


class WebSearchPlan(BaseModel):
    """
    Represents a structured plan for performing web searches.
    It contains a list of WebSearchItem objects.
    """
    searches: list[WebSearchItem] = Field(
        description="A list of web searches to perform to best answer the query."
    )


# PlannerAgent: Uses GPT to generate search terms for a given research query
planner_agent = Agent(
    name="PlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,  # Ensures the output matches the WebSearchPlan schema
)
