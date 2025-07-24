"""
Research Manager

This module defines the `ResearchManager` class, which orchestrates the entire deep research workflow:
1. Plan searches using the PlannerAgent.
2. Execute web searches in parallel using the SearchAgent.
3. Compile results into a comprehensive Markdown report using the WriterAgent.
4. Send the final report as an email using the EmailAgent.
5. Stream progress updates at every stage for UI feedback.

It uses the `Runner` utility to invoke agents and OpenAI's `trace` utilities for observability.
"""

import asyncio
from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent


class ResearchManager:
    """
    Orchestrates the deep research process.
    This class coordinates multiple AI agents to handle planning, searching, report writing, and emailing.
    """

    async def run(self, query: str):
        """
        Execute the deep research pipeline for a given query.

        Steps:
        1. Generate a unique trace ID for observability.
        2. Plan a set of web searches based on the query.
        3. Perform those searches in parallel and collect summaries.
        4. Write a long-form, detailed Markdown report.
        5. Send the report via email.
        6. Yield progress updates and the final Markdown report.

        Args:
            query (str): The research query provided by the user.

        Yields:
            str: Progress updates and the final Markdown report.
        """
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            # Provide trace link for debugging/monitoring
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"

            print("Starting research...")

            # Step 1: Plan searches
            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."

            # Step 2: Perform searches
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."

            # Step 3: Write report
            report = await self.write_report(query, search_results)
            yield "Report written, sending email..."

            # Step 4: Send email
            await self.send_email(report)
            yield "Email sent, research complete"

            # Step 5: Return final report
            yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """
        Plan the searches required to answer the query using the PlannerAgent.

        Args:
            query (str): The user’s research query.

        Returns:
            WebSearchPlan: A structured list of search items (reason + query).
        """
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """
        Perform web searches in parallel using the SearchAgent.

        Args:
            search_plan (WebSearchPlan): Planned search terms.

        Returns:
            list[str]: A list of summarized search results.
        """
        print("Searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []

        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")

        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """
        Perform a single web search for a search item using the SearchAgent.

        Args:
            item (WebSearchItem): The search query and its justification.

        Returns:
            str | None: The summarized search result, or None if the search fails.
        """
        input_data = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input_data,
            )
            return str(result.final_output)
        except Exception as e:
            print(f"Search failed for term '{item.query}': {e}")
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """
        Generate a detailed Markdown report using the WriterAgent.

        Args:
            query (str): The original research query.
            search_results (list[str]): Summarized web search results.

        Returns:
            ReportData: The final report object containing:
                        - Short summary
                        - Detailed Markdown report
                        - Suggested follow-up questions
        """
        print("Thinking about report...")
        input_data = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input_data,
        )
        print("Finished writing report")
        return result.final_output_as(ReportData)

    async def send_email(self, report: ReportData) -> None:
        """
        Send the final report as an email using the EmailAgent.

        Args:
            report (ReportData): The compiled research report.
        """
        print("Writing email...")
        await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Email sent")
