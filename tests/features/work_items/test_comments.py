"""
Tests for work item comments functionality.

This module provides comprehensive tests for the comment operations
in the Azure DevOps MCP server.
"""

from unittest.mock import MagicMock, patch

from azure.devops.v7_1.work_item_tracking.models import (
    CommentCreate,
    WorkItem,
)

from mcp_azure_devops.features.work_items.tools.comments import (
    _add_work_item_comment_impl,
    _format_comment,
    _get_project_for_work_item,
    _get_work_item_comments_impl,
)


# Tests for _format_comment
def test_format_comment_with_all_attributes():
    """Test formatting a comment with all attributes present."""
    mock_comment = MagicMock()
    mock_comment.text = "This is a test comment"
    mock_created_by = MagicMock()
    mock_created_by.display_name = "Test User"
    mock_comment.created_by = mock_created_by
    mock_comment.created_date = "2023-01-15T10:30:00Z"

    result = _format_comment(mock_comment)

    assert "## Comment by Test User on 2023-01-15T10:30:00Z" in result
    assert "This is a test comment" in result


def test_format_comment_without_date():
    """Test formatting a comment without a created date."""
    mock_comment = MagicMock()
    mock_comment.text = "Comment without date"
    mock_created_by = MagicMock()
    mock_created_by.display_name = "Test User"
    mock_comment.created_by = mock_created_by
    mock_comment.created_date = None

    result = _format_comment(mock_comment)

    assert "## Comment by Test User:" in result
    assert "Comment without date" in result
    # Should not contain " on " when date is missing
    assert " on " not in result


def test_format_comment_without_author():
    """Test formatting a comment without author information."""
    mock_comment = MagicMock()
    mock_comment.text = "Comment without author"
    mock_comment.created_by = None
    mock_comment.created_date = "2023-01-15T10:30:00Z"

    result = _format_comment(mock_comment)

    assert "## Comment by Unknown on 2023-01-15T10:30:00Z" in result
    assert "Comment without author" in result


def test_format_comment_without_text():
    """Test formatting a comment without text content."""
    mock_comment = MagicMock()
    mock_comment.text = None
    mock_created_by = MagicMock()
    mock_created_by.display_name = "Test User"
    mock_comment.created_by = mock_created_by
    mock_comment.created_date = "2023-01-15T10:30:00Z"

    result = _format_comment(mock_comment)

    assert "## Comment by Test User on 2023-01-15T10:30:00Z" in result
    assert "No text" in result


def test_format_comment_minimal():
    """Test formatting a comment with minimal attributes."""
    mock_comment = MagicMock()
    mock_comment.text = None
    mock_comment.created_by = None
    mock_comment.created_date = None

    result = _format_comment(mock_comment)

    assert "## Comment by Unknown:" in result
    assert "No text" in result


# Tests for _get_project_for_work_item
def test_get_project_for_work_item_success():
    """Test successfully retrieving project from work item."""
    mock_client = MagicMock()
    mock_work_item = MagicMock(spec=WorkItem)
    mock_work_item.fields = {"System.TeamProject": "TestProject"}
    mock_client.get_work_item.return_value = mock_work_item

    result = _get_project_for_work_item(123, mock_client)

    assert result == "TestProject"
    mock_client.get_work_item.assert_called_once_with(123)


def test_get_project_for_work_item_no_fields():
    """Test retrieving project when work item has no fields."""
    mock_client = MagicMock()
    mock_work_item = MagicMock(spec=WorkItem)
    mock_work_item.fields = None
    mock_client.get_work_item.return_value = mock_work_item

    result = _get_project_for_work_item(123, mock_client)

    assert result is None


def test_get_project_for_work_item_no_project_field():
    """Test retrieving project when work item has no project field."""
    mock_client = MagicMock()
    mock_work_item = MagicMock(spec=WorkItem)
    mock_work_item.fields = {"System.Title": "Test Item"}
    mock_client.get_work_item.return_value = mock_work_item

    result = _get_project_for_work_item(123, mock_client)

    assert result is None


def test_get_project_for_work_item_exception():
    """Test retrieving project when an exception occurs."""
    mock_client = MagicMock()
    mock_client.get_work_item.side_effect = Exception("API Error")

    result = _get_project_for_work_item(123, mock_client)

    assert result is None


# Tests for _get_work_item_comments_impl
def test_get_work_item_comments_impl_with_project():
    """Test retrieving comments when project is provided."""
    mock_client = MagicMock()

    # Mock comments
    mock_comment1 = MagicMock()
    mock_comment1.text = "First comment"
    mock_created_by1 = MagicMock()
    mock_created_by1.display_name = "User One"
    mock_comment1.created_by = mock_created_by1
    mock_comment1.created_date = "2023-01-01T10:00:00Z"

    mock_comment2 = MagicMock()
    mock_comment2.text = "Second comment"
    mock_created_by2 = MagicMock()
    mock_created_by2.display_name = "User Two"
    mock_comment2.created_by = mock_created_by2
    mock_comment2.created_date = "2023-01-02T11:00:00Z"

    mock_comments = MagicMock()
    mock_comments.comments = [mock_comment1, mock_comment2]
    mock_client.get_comments.return_value = mock_comments

    result = _get_work_item_comments_impl(
        123, mock_client, project="TestProject"
    )

    # Verify client was called with correct parameters
    mock_client.get_comments.assert_called_once_with(
        project="TestProject", work_item_id=123
    )

    # Verify output contains both comments
    assert "## Comment by User One on 2023-01-01T10:00:00Z" in result
    assert "First comment" in result
    assert "## Comment by User Two on 2023-01-02T11:00:00Z" in result
    assert "Second comment" in result


def test_get_work_item_comments_impl_without_project():
    """Test retrieving comments when project is not provided."""
    mock_client = MagicMock()

    # Mock work item for project lookup
    mock_work_item = MagicMock(spec=WorkItem)
    mock_work_item.fields = {"System.TeamProject": "AutoProject"}
    mock_client.get_work_item.return_value = mock_work_item

    # Mock comments
    mock_comment = MagicMock()
    mock_comment.text = "Test comment"
    mock_created_by = MagicMock()
    mock_created_by.display_name = "Test User"
    mock_comment.created_by = mock_created_by
    mock_comment.created_date = "2023-01-01T10:00:00Z"

    mock_comments = MagicMock()
    mock_comments.comments = [mock_comment]
    mock_client.get_comments.return_value = mock_comments

    result = _get_work_item_comments_impl(123, mock_client)

    # Verify project was retrieved from work item
    mock_client.get_work_item.assert_called_once_with(123)
    # Verify comments were retrieved with auto-detected project
    mock_client.get_comments.assert_called_once_with(
        project="AutoProject", work_item_id=123
    )
    assert "Test comment" in result


def test_get_work_item_comments_impl_no_comments():
    """Test retrieving comments when none exist."""
    mock_client = MagicMock()

    # Mock work item for project lookup
    mock_work_item = MagicMock(spec=WorkItem)
    mock_work_item.fields = {"System.TeamProject": "TestProject"}
    mock_client.get_work_item.return_value = mock_work_item

    # Mock empty comments
    mock_comments = MagicMock()
    mock_comments.comments = []
    mock_client.get_comments.return_value = mock_comments

    result = _get_work_item_comments_impl(123, mock_client)

    assert "No comments found for this work item." in result


def test_get_work_item_comments_impl_project_lookup_failure():
    """Test retrieving comments when project lookup fails."""
    mock_client = MagicMock()

    # Mock work item retrieval failure
    mock_client.get_work_item.return_value = None

    result = _get_work_item_comments_impl(123, mock_client)

    assert "Error retrieving work item 123 to determine project" in result


# Tests for _add_work_item_comment_impl
@patch(
    "mcp_azure_devops.features.work_items.tools.comments.sanitize_description_html"
)
def test_add_work_item_comment_impl_with_project(mock_sanitize):
    """Test adding a comment when project is provided."""
    mock_sanitize.return_value = "<p>Sanitized comment text</p>"

    mock_client = MagicMock()

    # Mock the added comment response
    mock_new_comment = MagicMock()
    mock_new_comment.text = "<p>Sanitized comment text</p>"
    mock_created_by = MagicMock()
    mock_created_by.display_name = "Comment Author"
    mock_new_comment.created_by = mock_created_by
    mock_new_comment.created_date = "2023-01-15T10:30:00Z"
    mock_client.add_comment.return_value = mock_new_comment

    result = _add_work_item_comment_impl(
        123, "Test comment", mock_client, project="TestProject"
    )

    # Verify sanitize was called with the input text
    mock_sanitize.assert_called_once_with("Test comment")

    # Verify add_comment was called with correct parameters
    mock_client.add_comment.assert_called_once()
    call_args = mock_client.add_comment.call_args
    assert call_args.kwargs["project"] == "TestProject"
    assert call_args.kwargs["work_item_id"] == 123
    assert isinstance(call_args.kwargs["request"], CommentCreate)

    # Verify success message in result
    assert "Comment added successfully." in result
    assert "## Comment by Comment Author on 2023-01-15T10:30:00Z" in result


@patch(
    "mcp_azure_devops.features.work_items.tools.comments.sanitize_description_html"
)
def test_add_work_item_comment_impl_without_project(mock_sanitize):
    """Test adding a comment when project is not provided."""
    mock_sanitize.return_value = "<p>Test HTML</p>"

    mock_client = MagicMock()

    # Mock work item for project lookup
    mock_work_item = MagicMock(spec=WorkItem)
    mock_work_item.fields = {"System.TeamProject": "AutoProject"}
    mock_client.get_work_item.return_value = mock_work_item

    # Mock the added comment response
    mock_new_comment = MagicMock()
    mock_new_comment.text = "<p>Test HTML</p>"
    mock_created_by = MagicMock()
    mock_created_by.display_name = "Test User"
    mock_new_comment.created_by = mock_created_by
    mock_new_comment.created_date = "2023-01-15T10:30:00Z"
    mock_client.add_comment.return_value = mock_new_comment

    result = _add_work_item_comment_impl(123, "Test comment", mock_client)

    # Verify project was retrieved from work item
    mock_client.get_work_item.assert_called_once_with(123)

    # Verify add_comment was called with auto-detected project
    call_args = mock_client.add_comment.call_args
    assert call_args.kwargs["project"] == "AutoProject"
    assert call_args.kwargs["work_item_id"] == 123

    assert "Comment added successfully." in result


@patch(
    "mcp_azure_devops.features.work_items.tools.comments.sanitize_description_html"
)
def test_add_work_item_comment_impl_project_lookup_failure(mock_sanitize):
    """Test adding a comment when project lookup fails."""
    mock_sanitize.return_value = "<p>Test</p>"

    mock_client = MagicMock()

    # Mock work item retrieval failure
    mock_client.get_work_item.return_value = None

    result = _add_work_item_comment_impl(123, "Test comment", mock_client)

    assert "Error retrieving work item 123 to determine project" in result
    # Verify add_comment was never called
    mock_client.add_comment.assert_not_called()


@patch(
    "mcp_azure_devops.features.work_items.tools.comments.sanitize_description_html"
)
def test_add_work_item_comment_impl_markdown_text(mock_sanitize):
    """Test adding a comment with Markdown text."""
    mock_sanitize.return_value = "<p>This is <strong>bold</strong> text</p>"

    mock_client = MagicMock()

    # Mock the added comment response
    mock_new_comment = MagicMock()
    mock_new_comment.text = "<p>This is <strong>bold</strong> text</p>"
    mock_created_by = MagicMock()
    mock_created_by.display_name = "Test User"
    mock_new_comment.created_by = mock_created_by
    mock_new_comment.created_date = "2023-01-15T10:30:00Z"
    mock_client.add_comment.return_value = mock_new_comment

    result = _add_work_item_comment_impl(
        123, "This is **bold** text", mock_client, project="TestProject"
    )

    # Verify sanitize was called with markdown text
    mock_sanitize.assert_called_once_with("This is **bold** text")

    # Verify the comment was added successfully
    assert "Comment added successfully." in result
    assert "This is <strong>bold</strong> text" in result


@patch(
    "mcp_azure_devops.features.work_items.tools.comments.sanitize_description_html"
)
def test_add_work_item_comment_impl_html_text(mock_sanitize):
    """Test adding a comment with HTML text."""
    html_input = "<div><p>HTML content</p></div>"
    mock_sanitize.return_value = html_input

    mock_client = MagicMock()

    # Mock the added comment response
    mock_new_comment = MagicMock()
    mock_new_comment.text = html_input
    mock_created_by = MagicMock()
    mock_created_by.display_name = "Test User"
    mock_new_comment.created_by = mock_created_by
    mock_new_comment.created_date = "2023-01-15T10:30:00Z"
    mock_client.add_comment.return_value = mock_new_comment

    result = _add_work_item_comment_impl(
        123, html_input, mock_client, project="TestProject"
    )

    # Verify sanitize was called with html text
    mock_sanitize.assert_called_once_with(html_input)

    # Verify the comment was added successfully
    assert "Comment added successfully." in result
    assert html_input in result
