"""Writing things with LLMs."""

from pathlib import Path

from smolagents import AgentLogger, LiteLLMModel, LogLevel, ToolCallingAgent

from .tools import ask_user, load_document, save_as_word


def write(prompt: str, file_paths: list[Path], model: str) -> str:
    """Write a thing using LLMs and store it as a Word document.

    Args:
        prompt:
            The prompt to write about.
        file_paths:
            A list of file paths to documents that provide context for the writing.
        model:
            The LiteLLM model ID to use for the agent.

    Returns:
        The final answer from the agent, which contains the path to the saved Word
        document.
    """
    writer = ToolCallingAgent(
        tools=[ask_user, load_document, save_as_word],
        model=LiteLLMModel(model_id=model),
        logger=AgentLogger(level=LogLevel.ERROR),
    )
    file_paths_str = "\n".join(file_path.as_posix() for file_path in file_paths)
    final_answer = writer.run(
        task=f"""
            You have to write a document based on the following instructions:

            <instructions>
            {prompt}
            </instructions>

            You should open and use the following documents as context:

            <documents>
            {file_paths_str}
            </documents>

            You should always have answers of the following questions before you start
            writing:

            <questions>
            1. How long should the document be?
            2. What tone should the document have (e.g., formal, informal, technical)?
            </questions>

            If the user has already provided answers to these questions, you should
            not ask them again. But if the user has not provided answers, you should ask
            the user these questions one by one and wait for their response.

            Also, if it is not clear to you how the files should be used, you should
            ask the user for clarification.

            When you are done writing the document, save the document as a Word file
            with a suitable file name in snake case in the current directory, and tell
            the user that the document has been saved.
        """
    )
    assert isinstance(final_answer, str), "The final answer should be a string."
    return final_answer.strip()
