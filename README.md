<a href="https://github.com/alexandrainst/write_a_thing">
<img
    src="https://filedn.com/lRBwPhPxgV74tO0rDoe8SpH/alexandra/alexandra-logo.jpeg"
	width="239"
	height="175"
	align="right"
/>
</a>

# Write A Thing

Use LLMs to help you write your things.

______________________________________________________________________
[![Code Coverage](https://img.shields.io/badge/Coverage-0%25-red.svg)](https://github.com/alexandrainst/write_a_thing/tree/main/tests)
[![Documentation](https://img.shields.io/badge/docs-passing-green)](https://alexandrainst.github.io/write_a_thing)
[![License](https://img.shields.io/github/license/alexandrainst/write_a_thing)](https://github.com/alexandrainst/write_a_thing/blob/main/LICENSE)
[![LastCommit](https://img.shields.io/github/last-commit/alexandrainst/write_a_thing)](https://github.com/alexandrainst/write_a_thing/commits/main)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://github.com/alexandrainst/write_a_thing/blob/main/CODE_OF_CONDUCT.md)

Developer:

- Dan Saattrup Nielsen (dan.nielsen@alexandra.dk)


## Quickstart

The easiest way to use the package is as a
[uv](https://docs.astral.sh/uv/getting-started/installation/) tool.

First, you should ensure that you have a `.env` file in your current working directory
with the following content:

```env
GEMINI_API_KEY=<your-google-api-key>
```

You can then start writing documents using the following command:

```bash
uvx write-a-thing <your-prompt> [-f <file-to-use-in-document>] [-f <another-file-to-use-in-document>]
```

This both installs the package and runs the command. You can also replace
`GEMINI_API_KEY` with, e.g., `OPENAI_API_KEY`, but then you will need to change the LLM
model used with the `--model` option when running the command.

You can see all available arguments by running the following command:

```bash
uvx write-a-thing --help
```
