"""Writing things with LLMs."""

import logging
import warnings
from pathlib import Path

import litellm
from smolagents import AgentLogger, LiteLLMModel, LogLevel, ToolCallingAgent

from .tools import (
    ask_user,
    broadcast,
    load_document,
    measure_document_length,
    open_word_document,
    save_as_word,
)

logger = logging.getLogger("write_a_thing")


def write(prompt: str, file_paths: list[Path], model: str, temperature: float) -> None:
    """Write a thing using LLMs and store it as a Word document.

    Args:
        prompt:
            The prompt to write about.
        file_paths:
            A list of file paths to documents that provide context for the writing.
        model:
            The LiteLLM model ID to use for the agent.
        temperature:
            The temperature to use for the model. Use 0.0 for greedy decoding.
    """
    # Suppress logging
    litellm.suppress_debug_info = True
    warnings.filterwarnings("ignore", category=UserWarning)
    for logging_name in logging.root.manager.loggerDict:
        if logging_name != "write_a_thing":
            logging.getLogger(logging_name).setLevel(logging.CRITICAL)

    logger.info("🥱 Waking up the agent...")
    writer = ToolCallingAgent(
        tools=[
            ask_user,
            broadcast,
            measure_document_length,
            load_document,
            save_as_word,
            open_word_document,
        ],
        model=LiteLLMModel(model_id=model, temperature=temperature),
        logger=AgentLogger(level=LogLevel.ERROR),
        max_steps=100,
    )
    file_paths_str = "\n".join(file_path.as_posix() for file_path in file_paths)
    writer.run(
        task=f"""
            You have to write a document based on the following instructions:

            <instructions>
            {prompt}
            </instructions>

            You should open and use the following documents as context:

            <documents>
            {file_paths_str}
            </documents>


            ### Writing Process

            You should have answers of the following questions before you start writing:

            - "How long should the document be?"
            - "What tone should the document have (e.g., formal, informal, technical)?"
            - If you need to clarify how the given files need to be used, you can ask
              the user.
            - Any other questions that you think are necessary to write the document, if
              the user has not provided answers to them already.

            These questions are subject to the following rules:

            - Only ask these questions if the user has not provided answers to them
              already.
            - Only ask a single question at a time.
            - When you are ready to start writing, you should broadcast the message
              "✍️ Writing your thing..." to the user.
            - During the writing process, feel free to broadcast humorous messages
              to the user indicating that you are dawdling, getting distracted,
              thinking about other things, etc. This is to make the writing process
              more engaging and fun for the user. Remember that all broadcasts must
              be brief and start with an emoji.


            ### Document Requirements

            - You should write the document in Markdown format.
            - The document should be well-structured, with headings, paragraphs, etc.
            - Use double newlines instead of single newlines.
            - Use "- " for bullet points and "1." for numbered lists.
            - Always include double newlines before the first item in a bulleted or
              numbered list.
            - Do not mention the file names or file paths in the document.
            - Do not mention the tone or length of the document in the document itself.


            ### Revision Process

            When you have finished writing the document, follow the following steps:

            1. Check yourself if the document satisfies all the requirements. If not,
               then broadcast that you are revising, fix the document and repeat this
               step. During the revision process, you can again broadcast humorous
               messages as before. Remember that broadcasts must be brief and start with
               an emoji.
            2. Save the document as a Word file with a suitable file name in snake case
               in the current directory.
            3. Ask the user if they want to open the generated document, and open it if
               they agree.
            4. Ask the user if they have any feedback on the document. If they do,
               broadcast that you are revising, fix the document based on their
               feedback, and go back to step 1. During this process, you can again
               broadcast humorous messages as before. Remember that broadcasts must be
               brief and start with an emoji.
            5. If they do not have any feedback, then stop the process and broadcast
               "✅ Your thing is ready!" to the user.
        """
    )
