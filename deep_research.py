"""
Deep Research Application Entry Point

This script provides a Gradio-based web interface for performing in-depth research
on any given topic. It orchestrates the research workflow using the `ResearchManager`
class, which plans searches, performs web lookups, compiles the results into a
detailed Markdown report, and streams progress updates to the user interface.

How it works:
1. Loads environment variables (for API keys, configuration).
2. Sets up a Gradio UI with a textbox (for queries) and a button (to start research).
3. Calls `ResearchManager.run()` asynchronously to execute the multi-agent research pipeline.
4. Streams live updates and the final report back to the UI.

Author: [Your Name]
"""

import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

# Load environment variables from .env files (API keys, config values, etc.)
# The `override=True` ensures that environment variables in the .env file
# take precedence over existing environment variables in the environment.
load_dotenv(override=True)


async def run(query: str):
    """
    Handle a user-submitted research query.

    This asynchronous generator streams progress updates and the final Markdown report
    back to the Gradio interface as chunks. The heavy lifting is done by ResearchManager,
    which coordinates multiple AI agents (Planner, Search, Writer, Email).
    
    Args:
        query (str): The research topic provided by the user.

    Yields:
        str: Progress updates and final research report (Markdown formatted).
    """
    async for chunk in ResearchManager().run(query):
        yield chunk


# Build the Gradio interface
with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    # Title of the application
    gr.Markdown("# Deep Research")

    # Text input for the user to specify a research topic
    query_textbox = gr.Textbox(
        label="What topic would you like to research?",
        placeholder="Enter a research topic (e.g., 'Impact of AI on Healthcare')"
    )

    # Button to trigger the research process
    run_button = gr.Button("Run", variant="primary")

    # Area to display progress updates and final report (Markdown formatted)
    report = gr.Markdown(label="Report")

    # Bind actions: Clicking the button or pressing Enter runs the `run()` function
    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

# Launch the Gradio app in the browser
ui.launch(inbrowser=True)
