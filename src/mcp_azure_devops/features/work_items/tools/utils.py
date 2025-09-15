"""
Utility functions for Azure DevOps work item tools.

This module provides shared utility functions used across work item tools.
"""

import re
from typing import Optional


def _convert_markdown_to_html(text: str) -> str:
    """
    Convert basic markdown formatting to HTML.

    Supports common markdown elements:
    - Headers (# ## ###)
    - Bold (**text** or __text__)
    - Italic (*text* or _text_)
    - Code blocks (```code``` or `inline`)
    - Links ([text](url))
    - Unordered lists (- item)
    - Ordered lists (1. item)
    - Line breaks and paragraphs

    Args:
        text: Markdown text to convert

    Returns:
        HTML formatted text
    """
    lines = text.split("\n")
    result_lines = []
    in_ul = False
    in_ol = False
    in_code_block = False
    code_block_content = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Handle code blocks
        if line.strip().startswith("```"):
            if not in_code_block:
                # Start code block
                in_code_block = True
                code_block_content = []
                i += 1
                continue
            else:
                # End code block
                in_code_block = False
                result_lines.append("<pre><code>")
                result_lines.extend(code_block_content)
                result_lines.append("</code></pre>")
                i += 1
                continue

        # If we're in a code block, just collect the content
        if in_code_block:
            code_block_content.append(line)
            i += 1
            continue

        # Process the line for other markdown elements
        processed_line = line

        # Headers (must be at start of line)
        if line.strip().startswith("### "):
            processed_line = f"<h3>{line.strip()[4:]}</h3>"
        elif line.strip().startswith("## "):
            processed_line = f"<h2>{line.strip()[3:]}</h2>"
        elif line.strip().startswith("# "):
            processed_line = f"<h1>{line.strip()[2:]}</h1>"
        else:
            # Apply inline formatting to non-header lines
            # Inline code first (to protect from other formatting)
            processed_line = re.sub(
                r"`([^`]+)`", r"<code>\1</code>", processed_line
            )

            # Bold
            processed_line = re.sub(
                r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", processed_line
            )
            processed_line = re.sub(
                r"__([^_]+)__", r"<strong>\1</strong>", processed_line
            )

            # Italic (be careful not to conflict with bold)
            processed_line = re.sub(
                r"(?<!\*)\*([^*\s][^*]*[^*\s]|\w)\*(?!\*)",
                r"<em>\1</em>",
                processed_line,
            )
            processed_line = re.sub(
                r"(?<!_)_([^_\s][^_]*[^_\s]|\w)_(?!_)",
                r"<em>\1</em>",
                processed_line,
            )

            # Links
            processed_line = re.sub(
                r"\[([^\]]+)\]\(([^)]+)\)",
                r'<a href="\2">\1</a>',
                processed_line,
            )

        # Handle lists
        stripped = line.strip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            # Close ordered list if we were in one
            if in_ol:
                result_lines.append("</ol>")
                in_ol = False
            # Open unordered list if not already in one
            if not in_ul:
                result_lines.append("<ul>")
                in_ul = True
            # Process the list item content for inline formatting
            item_content = stripped[2:]
            item_content = re.sub(
                r"`([^`]+)`", r"<code>\1</code>", item_content
            )
            item_content = re.sub(
                r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", item_content
            )
            item_content = re.sub(
                r"__([^_]+)__", r"<strong>\1</strong>", item_content
            )
            item_content = re.sub(
                r"(?<!\*)\*([^*\s][^*]*[^*\s]|\w)\*(?!\*)",
                r"<em>\1</em>",
                item_content,
            )
            item_content = re.sub(
                r"(?<!_)_([^_\s][^_]*[^_\s]|\w)_(?!_)",
                r"<em>\1</em>",
                item_content,
            )
            item_content = re.sub(
                r"\[([^\]]+)\]\(([^)]+)\)",
                r'<a href="\2">\1</a>',
                item_content,
            )
            result_lines.append(f"<li>{item_content}</li>")
        elif re.match(r"^\d+\. ", stripped):
            # Close unordered list if we were in one
            if in_ul:
                result_lines.append("</ul>")
                in_ul = False
            # Open ordered list if not already in one
            if not in_ol:
                result_lines.append("<ol>")
                in_ol = True
            # Extract and process item content
            item_content = re.sub(r"^\d+\. ", "", stripped)
            item_content = re.sub(
                r"`([^`]+)`", r"<code>\1</code>", item_content
            )
            item_content = re.sub(
                r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", item_content
            )
            item_content = re.sub(
                r"__([^_]+)__", r"<strong>\1</strong>", item_content
            )
            item_content = re.sub(
                r"(?<!\*)\*([^*\s][^*]*[^*\s]|\w)\*(?!\*)",
                r"<em>\1</em>",
                item_content,
            )
            item_content = re.sub(
                r"(?<!_)_([^_\s][^_]*[^_\s]|\w)_(?!_)",
                r"<em>\1</em>",
                item_content,
            )
            item_content = re.sub(
                r"\[([^\]]+)\]\(([^)]+)\)",
                r'<a href="\2">\1</a>',
                item_content,
            )
            result_lines.append(f"<li>{item_content}</li>")
        else:
            # Regular line - close any open lists
            if in_ul:
                result_lines.append("</ul>")
                in_ul = False
            if in_ol:
                result_lines.append("</ol>")
                in_ol = False
            result_lines.append(processed_line)

        i += 1

    # Close any remaining open lists or code blocks
    if in_ul:
        result_lines.append("</ul>")
    if in_ol:
        result_lines.append("</ol>")
    if in_code_block:
        # Unclosed code block - treat as regular content
        result_lines.append("<pre><code>")
        result_lines.extend(code_block_content)
        result_lines.append("</code></pre>")

    # Join and handle line breaks
    html = "\n".join(result_lines)

    # Don't add any additional line break processing since we want to preserve
    # the structure we've built
    return html


def sanitize_description_html(description: Optional[str]) -> Optional[str]:
    """
    Convert description text to HTML format, supporting both plain text and markdown.

    This function can process:
    - Plain text (converts line breaks to <br> tags)
    - Markdown format (converts to HTML)
    - HTML format (passes through unchanged)

    Supported markdown elements:
    - Headers: # ## ###
    - Bold: **text** or __text__
    - Italic: *text* or _text_
    - Code: `inline` or ```blocks```
    - Links: [text](url)
    - Lists: - item or 1. item

    Args:
        description: Original description text in plain text, markdown, or HTML format

    Returns:
        Processed HTML text with preserved formatting
    """
    if not description:
        return description

    desc_stripped = description.strip()

    # If it already looks like HTML, return as-is
    if (
        desc_stripped.startswith("<")
        and ">" in desc_stripped
        and (
            "<html" in desc_stripped.lower()
            or "<p>" in desc_stripped.lower()
            or "<div" in desc_stripped.lower()
            or "<h1>" in desc_stripped.lower()
            or "<h2>" in desc_stripped.lower()
            or "<h3>" in desc_stripped.lower()
            or "<ul>" in desc_stripped.lower()
            or "<ol>" in desc_stripped.lower()
            or "<li>" in desc_stripped.lower()
            or "<strong>" in desc_stripped.lower()
            or "<em>" in desc_stripped.lower()
            or "<code>" in desc_stripped.lower()
        )
    ):
        return description

    # Check if it contains markdown elements
    has_markdown = (
        # Headers
        re.search(r"^#{1,3} ", desc_stripped, re.MULTILINE)
        or
        # Bold/italic
        re.search(
            r"\*\*[^*]+\*\*|__[^_]+__|(?<!\*)\*[^*]+\*(?!\*)|(?<!_)_[^_]+_(?!_)",
            desc_stripped,
        )
        or
        # Code blocks or inline code
        re.search(r"```[^`]*```|`[^`]+`", desc_stripped)
        or
        # Links
        re.search(r"\[[^\]]+\]\([^)]+\)", desc_stripped)
        or
        # Lists
        re.search(r"^[-*] |^\d+\. ", desc_stripped, re.MULTILINE)
    )

    if has_markdown:
        # Convert markdown to HTML
        description_html = _convert_markdown_to_html(description)
    else:
        # Plain text - just convert line breaks
        description_html = description.replace("\n", "<br>")

    return f"<div>{description_html}</div>"
