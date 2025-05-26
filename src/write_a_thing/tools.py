"""The tools used by the agents."""

import logging
import os

import pypandoc
from docling.document_converter import DocumentConverter
from docling.exceptions import ConversionError
from smolagents import tool

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
    return input(f"Question for you: {question}\n> ")


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
        return docling_doc.export_to_markdown()
    except ConversionError:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()


@tool
def save_as_word(markdown_content: str, output_path: str) -> str:
    """Save the given Markdown content as a Word document.

    Args:
        markdown_content:
            The Markdown content to save as a Word document.
        output_path:
            The path where the Word document will be saved.

    Returns:
        The path to the saved Word document.

    Raises:
        FileExistsError: If the output file already exists.
        ValueError: If the content could not be parsed.
    """
    logger.info(f"💾 Saving document as Word at {output_path}...")
    if os.path.exists(output_path):
        raise FileExistsError(
            f"The file {output_path} already exists. Please choose a different name."
        )
    return pypandoc.convert_text(
        source=markdown_content, to="docx", format="markdown", outputfile=output_path
    )
