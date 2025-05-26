"""The Command-line Interface (CLI) for writing things with LLMs."""

import logging
from pathlib import Path

import click
import litellm
from dotenv import load_dotenv

from .writing import write

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("write_a_thing")


@click.command(name="write-a-thing")
@click.argument("prompt", type=str)
@click.option(
    "--file",
    "-f",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    multiple=True,
    help="Path to a file containing information related to what you want to write.",
)
@click.option(
    "--model",
    type=str,
    default="gemini/gemini-2.5-pro-preview-05-06",
    show_default=True,
    help="The model to use for the agents.",
)
def main(prompt: str, file: list[str], model: str) -> None:
    """Write a thing using a prompt and an optional file."""
    # Suppress logging
    litellm.suppress_debug_info = True
    logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)
    logging.getLogger("httpx").setLevel(logging.CRITICAL)
    logging.getLogger("docling.document_converter").setLevel(logging.CRITICAL)
    logging.getLogger("docling.pipeline.base_pipeline").setLevel(logging.CRITICAL)

    # Write the thing and store it as a Word document
    logger.info("✍️ Writing your thing...")
    response = write(prompt=prompt, file_paths=[Path(f) for f in file], model=model)
    logger.info(f"✅ {response}")


if __name__ == "__main__":
    main()
