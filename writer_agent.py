"""
Writer Agent

This module defines the WriterAgent, which is responsible for synthesizing research findings 
into a cohesive, well-structured Markdown report.

Workflow:
1. Receives the original research query and summarized search results.
2. Creates an outline for the report to ensure logical flow and structure.
3. Expands the outline into a detailed, multi-section Markdown report.
4. Provides:
    - A short summary (2–3 sentences).
    - A comprehensive 5–10 page Markdown report (at least 1000 words).
    - Suggested follow-up research questions for further exploration.

The output is structured using the ReportData Pydantic model for easy integration.
"""

from pydantic import BaseModel, Field
from agents import Agent

# Instructions for the AI agent
INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words."
)

class ReportData(BaseModel):
    """
    Represents the structured output of the WriterAgent.
    """
    short_summary: str = Field(
        description="A short 2-3 sentence summary of the findings."
    )
    markdown_report: str = Field(
        description="The final comprehensive report in Markdown format."
    )
    follow_up_questions: list[str] = Field(
        description="Suggested topics to research further."
    )

# WriterAgent: Synthesizes research into a structured, long-form Markdown report
writer_agent = Agent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,  # Ensures the output adheres to the ReportData schema
)
