"""The tools used by the agents."""

import logging
import re
from pathlib import Path

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
    return input(f"❓ {question}\n👉 ")


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
def save_as_word(markdown_content: str, output_path: str) -> bool:
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

    output_path_obj = Path(output_path)
    while output_path_obj.exists():
        version_number_match = re.search(r"(?<=v)[1-9]$", output_path_obj.stem)
        if version_number_match is not None:
            version_number = int(version_number_match.group(0))
            output_path_obj = output_path_obj.with_name(
                output_path_obj.stem.replace(
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
    logger.info(f"✅ All done! Document saved at {output_path_obj.as_posix()}.")
    return True
