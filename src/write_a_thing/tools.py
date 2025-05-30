"""The tools used by the agents."""

import logging
import re
import subprocess
from pathlib import Path

import pypandoc
from docling.document_converter import DocumentConverter
from docling.exceptions import ConversionError
from emoji import is_emoji
from smolagents import tool

from .utils import log_once

logger = logging.getLogger("write_a_thing")


@tool
def ask_user(question: str) -> str:
    """Ask the user a question and return their response.

    Args:
        question:
            The question to ask the user.

    Returns:
        The user's response to the question.
    """
    return input(f"❓ {question}\n👉 ")


@tool
def broadcast(message: str) -> str:
    """Broadcast a message to the user.

    All broadcasts must be brief and start with an emoji.

    Args:
        message:
            A message to broadcast, starting with an emoji.

    Returns:
        A confirmation message stating whether the writing process has been initiated.
    """
    if not message or not is_emoji(string=message[0]):
        return (
            "Broadcast failed as your message did not start with an emoji. Please "
            "try again."
        )

    log_once(message=message)
    return "Successfully broadcasted the message."


@tool
def measure_document_length(text: str) -> dict[str, float | int]:
    """Measure the length of the given text.

    This returns the number of characters, words, lines, and pages in the text.

    Args:
        text:
            The text to measure.

    Returns:
        A mapping with the following keys:
            - "characters": The number of characters in the text.
            - "words": The number of words in the text.
            - "lines": The number of lines in the text.
            - "pages": The estimated number of pages in the text.
    """
    logger.info("🧮 Measuring text length...")
    return dict(
        characters=len(text),
        words=len(text.split()),
        lines=len(text.splitlines()),
        pages=round(len(text) / 1800, ndigits=2),
    )


@tool
def load_document(file_path: str) -> str:
    """Load a document from the given file path.

    The `file_path` should point to an existing document file.

    Args:
        file_path:
            The path to the document file.

    Returns:
        The Markdown parsed content of the document.
    """
    logger.info(f"📄 Loading document from {file_path}...")
    try:
        converter = DocumentConverter()
        docling_doc = converter.convert(source=file_path).document
        document = docling_doc.export_to_markdown()
    except ConversionError:
        with open(file_path, "r", encoding="utf-8") as file:
            document = file.read()
    return document


@tool
def save_as_word(markdown_content: str, output_path: str) -> bool:
    """Save the given Markdown content as a Word document.

    Args:
        markdown_content:
            The Markdown content to save as a Word document.
        output_path:
            The path where the Word document will be saved.

    Returns:
        The path to the saved Word document.
    """
    logger.info(f"💾 Saving document as Word at {output_path}...")

    output_path_obj = Path(output_path)
    while output_path_obj.exists():
        version_number_match = re.search(r"(?<=v)[1-9]$", output_path_obj.stem)
        if version_number_match is not None:
            version_number = int(version_number_match.group(0))
            output_path_obj = output_path_obj.with_name(
                output_path_obj.name.replace(
                    f"v{version_number}", f"v{version_number + 1}"
                )
            )
        else:
            output_path_obj = output_path_obj.with_name(
                f"{output_path_obj.stem}-v1{output_path_obj.suffix}"
            )

    pypandoc.convert_text(
        source=markdown_content,
        to="docx",
        format="markdown",
        outputfile=output_path_obj.as_posix(),
    )
    return True


@tool
def open_word_document(file_path: str) -> None:
    """Open a Word document.

    Args:
        file_path:
            The path to the Word document file.
    """
    logger.info(f"📄 Opening Word document from {file_path}...")
    operating_system = subprocess.run(
        ["uname", "-s"], capture_output=True, text=True
    ).stdout.strip()
    match operating_system:
        case "Linux":
            subprocess.run(["xdg-open", file_path], check=True)
        case "Darwin":
            subprocess.run(["open", file_path], check=True)
        case "Windows":
            subprocess.run(["start", file_path], shell=True, check=True)
