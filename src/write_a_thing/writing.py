"""Writing things with LLMs."""

from pathlib import Path

from smolagents import AgentLogger, LiteLLMModel, LogLevel, ToolCallingAgent

from .tools import (
    ask_user,
    count_characters,
    count_lines,
    count_pages,
    count_words,
    load_document,
    open_word_document,
    save_as_word,
)


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
    writer = ToolCallingAgent(
        tools=[
            count_characters,
            count_words,
            count_lines,
            count_pages,
            ask_user,
            load_document,
            save_as_word,
            open_word_document,
        ],
        model=LiteLLMModel(model_id=model, temperature=temperature),
        logger=AgentLogger(level=LogLevel.ERROR),
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


            ### Questions to Ask the User

            You should have answers of the following questions before you start writing:

            - How long should the document be?
            - What tone should the document have (e.g., formal, informal, technical)?

            Only ask these questions if the user has not provided answers to them yet.
            Also, if it is not clear to you how the files should be used, you should
            ask the user for clarification. Always try to deduce the answers to all
            questions yourself, but if you cannot, ask the user.


            ### Requirements

            - You should write the document in Markdown format.
            - The document should be well-structured, with headings, paragraphs, etc.
            - Use double newlines instead of single newlines.
            - Use "- " for bullet points and "1." for numbered lists.
            - Always include double newlines before a bulleted or numbered list.
            - Do not mention the file names or file paths in the document.
            - Do not mention the tone or length of the document in the document itself.


            ### Revision Process

            When you have finished writing the document, follow the following steps:

            1. Check yourself if the document satisfies all the requirements. If not,
               then fix the document and repeat this step.
            2. Save the document as a Word file with a suitable file name in snake case
               in the current directory.
            3. Ask the user if they want to open the generated document, and open it if
               they agree.
            4. Ask the user if they have any feedback on the document. If they do,
               fix the document based on their feedback, and go back to step 1.
            5. If they do not have any feedback, then stop the process and do not ask
               any more questions.
        """
    )
