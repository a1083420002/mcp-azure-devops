"""
Tests for work item utility functions.

This module tests the utility functions in utils.py, particularly
the sanitize_description_html function with markdown support.
"""


from mcp_azure_devops.features.work_items.tools.utils import (
    _convert_markdown_to_html,
    sanitize_description_html,
)


class TestConvertMarkdownToHtml:
    """Test cases for _convert_markdown_to_html function."""

    def test_headers(self):
        """Test markdown header conversion."""
        # Single header
        assert _convert_markdown_to_html("# Header 1") == "<h1>Header 1</h1>"
        assert _convert_markdown_to_html("## Header 2") == "<h2>Header 2</h2>"
        assert _convert_markdown_to_html("### Header 3") == "<h3>Header 3</h3>"

        # Multiple headers
        text = "# Title\n## Subtitle\n### Section"
        expected = "<h1>Title</h1>\n<h2>Subtitle</h2>\n<h3>Section</h3>"
        assert _convert_markdown_to_html(text) == expected

    def test_bold_text(self):
        """Test bold text conversion."""
        # Double asterisk
        assert (
            _convert_markdown_to_html("**bold text**")
            == "<strong>bold text</strong>"
        )

        # Double underscore
        assert (
            _convert_markdown_to_html("__bold text__")
            == "<strong>bold text</strong>"
        )

        # Mixed in sentence
        text = "This is **bold** and this is __also bold__."
        expected = "This is <strong>bold</strong> and this is <strong>also bold</strong>."
        assert _convert_markdown_to_html(text) == expected

    def test_italic_text(self):
        """Test italic text conversion."""
        # Single asterisk
        assert (
            _convert_markdown_to_html("*italic text*")
            == "<em>italic text</em>"
        )

        # Single underscore
        assert (
            _convert_markdown_to_html("_italic text_")
            == "<em>italic text</em>"
        )

        # Mixed in sentence
        text = "This is *italic* and this is _also italic_."
        expected = "This is <em>italic</em> and this is <em>also italic</em>."
        assert _convert_markdown_to_html(text) == expected

    def test_mixed_bold_italic(self):
        """Test mixed bold and italic formatting."""
        text = "This is **bold** and *italic* and __bold__ and _italic_."
        expected = "This is <strong>bold</strong> and <em>italic</em> and <strong>bold</strong> and <em>italic</em>."
        assert _convert_markdown_to_html(text) == expected

    def test_code_blocks(self):
        """Test code block conversion."""
        # Code blocks with triple backticks
        text = "```\ncode here\nmore code\n```"
        expected = "<pre><code>\ncode here\nmore code\n</code></pre>"
        assert _convert_markdown_to_html(text) == expected

        # Inline code with single backticks
        text = "This is `inline code` in text."
        expected = "This is <code>inline code</code> in text."
        assert _convert_markdown_to_html(text) == expected

    def test_links(self):
        """Test link conversion."""
        text = "[Google](https://google.com)"
        expected = '<a href="https://google.com">Google</a>'
        assert _convert_markdown_to_html(text) == expected

        # Multiple links
        text = "Visit [Google](https://google.com) or [GitHub](https://github.com)."
        expected = 'Visit <a href="https://google.com">Google</a> or <a href="https://github.com">GitHub</a>.'
        assert _convert_markdown_to_html(text) == expected

    def test_unordered_lists(self):
        """Test unordered list conversion."""
        # Dash lists
        text = "- Item 1\n- Item 2\n- Item 3"
        expected = (
            "<ul>\n<li>Item 1</li>\n<li>Item 2</li>\n<li>Item 3</li>\n</ul>"
        )
        assert _convert_markdown_to_html(text) == expected

        # Asterisk lists
        text = "* Item 1\n* Item 2"
        expected = "<ul>\n<li>Item 1</li>\n<li>Item 2</li>\n</ul>"
        assert _convert_markdown_to_html(text) == expected

    def test_ordered_lists(self):
        """Test ordered list conversion."""
        text = "1. First item\n2. Second item\n3. Third item"
        expected = "<ol>\n<li>First item</li>\n<li>Second item</li>\n<li>Third item</li>\n</ol>"
        assert _convert_markdown_to_html(text) == expected

    def test_complex_markdown(self):
        """Test complex markdown with multiple elements."""
        text = """# Project Title

This is a **bold** statement with *italic* text.

## Features

- Feature 1 with `code`
- Feature 2 with [link](https://example.com)

```
code block here
```

Visit our [website](https://example.com) for more info."""

        result = _convert_markdown_to_html(text)

        # Check that key elements are converted
        assert "<h1>Project Title</h1>" in result
        assert "<strong>bold</strong>" in result
        assert "<em>italic</em>" in result
        assert "<h2>Features</h2>" in result
        assert "<ul>" in result and "</ul>" in result
        assert "<li>Feature 1 with <code>code</code></li>" in result
        assert (
            '<li>Feature 2 with <a href="https://example.com">link</a></li>'
            in result
        )
        assert "<pre><code>" in result and "</code></pre>" in result
        assert '<a href="https://example.com">website</a>' in result


class TestSanitizeDescriptionHtml:
    """Test cases for sanitize_description_html function."""

    def test_none_input(self):
        """Test with None input."""
        assert sanitize_description_html(None) is None
        assert sanitize_description_html("") == ""

    def test_existing_html_passthrough(self):
        """Test that existing HTML passes through unchanged."""
        html_inputs = [
            "<div>Already HTML</div>",
            "<p>Paragraph content</p>",
            "<h1>Header</h1>",
            "<ul><li>List item</li></ul>",
            "<strong>Bold</strong>",
            "<em>Italic</em>",
            "<code>Code</code>",
        ]

        for html_input in html_inputs:
            assert sanitize_description_html(html_input) == html_input

    def test_plain_text_conversion(self):
        """Test plain text conversion to HTML."""
        plain_text = "This is plain text\nwith a line break."
        expected = "<div>This is plain text<br>with a line break.</div>"
        assert sanitize_description_html(plain_text) == expected

    def test_markdown_detection_and_conversion(self):
        """Test markdown detection and conversion."""
        # Headers should trigger markdown processing
        text = "# Header\nSome content"
        result = sanitize_description_html(text)
        assert "<h1>Header</h1>" in result
        assert result.startswith("<div>")
        assert result.endswith("</div>")

        # Bold text should trigger markdown processing
        text = "This is **bold** text"
        result = sanitize_description_html(text)
        assert "<strong>bold</strong>" in result

        # Links should trigger markdown processing
        text = "Visit [Google](https://google.com)"
        result = sanitize_description_html(text)
        assert '<a href="https://google.com">Google</a>' in result

        # Lists should trigger markdown processing
        text = "- Item 1\n- Item 2"
        result = sanitize_description_html(text)
        assert "<ul>" in result and "<li>" in result

    def test_markdown_elements_coverage(self):
        """Test all supported markdown elements."""
        markdown_text = """# Header 1
## Header 2
### Header 3

This is **bold** and *italic* text.

Here's some `inline code` and a [link](https://example.com).

```
code block
```

- Unordered item 1
- Unordered item 2

1. Ordered item 1
2. Ordered item 2"""

        result = sanitize_description_html(markdown_text)

        # Verify all elements are converted
        assert "<h1>Header 1</h1>" in result
        assert "<h2>Header 2</h2>" in result
        assert "<h3>Header 3</h3>" in result
        assert "<strong>bold</strong>" in result
        assert "<em>italic</em>" in result
        assert "<code>inline code</code>" in result
        assert '<a href="https://example.com">link</a>' in result
        assert "<pre><code>" in result
        assert "<ul>" in result
        assert "<ol>" in result
        assert result.startswith("<div>") and result.endswith("</div>")

    def test_edge_cases(self):
        """Test edge cases for markdown processing."""
        # Empty string after strip
        assert sanitize_description_html("   ") == "<div>   </div>"

        # Text that looks like markdown but isn't well-formed
        text = "This is *proper italic* text"
        result = sanitize_description_html(text)
        assert (
            "<em>proper italic</em>" in result
        )  # Should detect and convert well-formed italic

        # Mixed HTML and markdown (should detect as HTML and pass through)
        text = "<p>This is **not** markdown</p>"
        result = sanitize_description_html(text)
        assert result == text  # Should pass through as HTML

    def test_real_world_scenarios(self):
        """Test real-world usage scenarios."""
        # User story acceptance criteria
        acceptance_criteria = """## Acceptance Criteria

- [ ] User can **login** with email
- [ ] System shows *welcome* message  
- [ ] All `API endpoints` work correctly
- [ ] Documentation is available at [docs](https://example.com)

### Technical Notes

```python
def login(email, password):
    return authenticate(email, password)
```"""

        result = sanitize_description_html(acceptance_criteria)
        assert "<h2>Acceptance Criteria</h2>" in result
        assert "<strong>login</strong>" in result
        assert "<em>welcome</em>" in result
        assert "<code>API endpoints</code>" in result
        assert '<a href="https://example.com">docs</a>' in result
        assert "<pre><code>" in result  # Code block is created

        # Bug description
        bug_description = """# Bug Report

**Steps to reproduce:**
1. Open the application
2. Click on *Settings*  
3. Try to save configuration

**Expected:** Settings should be saved
**Actual:** Application crashes

**Error message:**
```
NullReferenceException at line 42
```

See also: [Similar Issue](https://github.com/example/issue/123)"""

        result = sanitize_description_html(bug_description)
        assert "<h1>Bug Report</h1>" in result
        assert "<strong>Steps to reproduce:</strong>" in result
        assert "<em>Settings</em>" in result
        assert "<ol>" in result  # Numbered list
        assert "<pre><code>" in result  # Code block is created
        assert (
            '<a href="https://github.com/example/issue/123">Similar Issue</a>'
            in result
        )
