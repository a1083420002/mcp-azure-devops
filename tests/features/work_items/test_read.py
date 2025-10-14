"""
Unit tests for the work item read tools.
"""

from unittest.mock import MagicMock

from azure.devops.v7_1.work_item_tracking.models import WorkItem

from mcp_azure_devops.features.work_items.tools.read import _get_work_item_impl

# Tests for _get_work_item_impl with single work item


def test_get_work_item_impl_single_basic():
    """Test retrieving basic info for a single work item."""
    mock_client = MagicMock()

    # Mock work item
    mock_work_item = MagicMock(spec=WorkItem)
    mock_work_item.id = 123
    mock_work_item.fields = {
        "System.WorkItemType": "Bug",
        "System.Title": "Test Bug",
        "System.State": "Active",
        "System.TeamProject": "Test Project",
    }
    mock_client.get_work_item.return_value = mock_work_item

    result = _get_work_item_impl(123, mock_client, detailed=False)

    # Verify client was called correctly
    mock_client.get_work_item.assert_called_once_with(123, expand="all")

    # Check that the result contains expected basic info
    # Title is in the header for basic view
    assert "# Work Item 123: Test Bug" in result
    assert "- **System.WorkItemType**: Bug" in result
    assert "- **System.State**: Active" in result
    # TeamProject is not in the important fields for basic view
    assert "System.TeamProject" not in result


def test_get_work_item_impl_single_detailed():
    """Test retrieving detailed info for a single work item."""
    mock_client = MagicMock()

    # Mock work item with more fields for detailed view
    mock_work_item = MagicMock(spec=WorkItem)
    mock_work_item.id = 456
    mock_work_item.fields = {
        "System.WorkItemType": "Task",
        "System.Title": "Test Task",
        "System.State": "Closed",
        "System.TeamProject": "Test Project",
        "System.Description": "This is a detailed description",
        "System.AssignedTo": {
            "displayName": "Test User",
            "uniqueName": "test@example.com",
        },
        "System.CreatedBy": {"displayName": "Creator User"},
        "System.CreatedDate": "2023-01-01",
        "System.IterationPath": "Project\\Sprint 1",
        "System.AreaPath": "Project\\Area",
        "System.Tags": "tag1; tag2",
    }
    mock_client.get_work_item.return_value = mock_work_item

    result = _get_work_item_impl(456, mock_client, detailed=True)

    # Verify client was called correctly
    mock_client.get_work_item.assert_called_once_with(456, expand="all")

    # Check that the result contains both basic and detailed info
    assert "# Work Item 456" in result
    assert "- **System.WorkItemType**: Task" in result
    assert "- **System.Title**: Test Task" in result
    assert "- **System.State**: Closed" in result
    assert "- **System.Description**: This is a detailed description" in result
    assert "- **System.AssignedTo**: Test User (test@example.com)" in result
    assert "- **System.CreatedBy**: Creator User" in result
    assert "- **System.IterationPath**: Project\\Sprint 1" in result
    assert "- **System.AreaPath**: Project\\Area" in result
    assert "- **System.Tags**: tag1; tag2" in result


def test_get_work_item_impl_single_error():
    """Test error handling when retrieving a single work item."""
    mock_client = MagicMock()
    mock_client.get_work_item.side_effect = Exception("Test error")

    result = _get_work_item_impl(123, mock_client)

    assert "Error retrieving work item 123: Test error" in result


# Tests for _get_work_item_impl with multiple work items


def test_get_work_item_impl_multiple_basic():
    """Test retrieving basic info for multiple work items."""
    mock_client = MagicMock()

    # Mock work items
    mock_work_item1 = MagicMock(spec=WorkItem)
    mock_work_item1.id = 123
    mock_work_item1.fields = {
        "System.WorkItemType": "Bug",
        "System.Title": "Test Bug",
        "System.State": "Active",
    }

    mock_work_item2 = MagicMock(spec=WorkItem)
    mock_work_item2.id = 456
    mock_work_item2.fields = {
        "System.WorkItemType": "Task",
        "System.Title": "Test Task",
        "System.State": "Closed",
    }

    mock_client.get_work_items.return_value = [
        mock_work_item1,
        mock_work_item2,
    ]

    result = _get_work_item_impl([123, 456], mock_client, detailed=False)

    # Verify client was called correctly
    mock_client.get_work_items.assert_called_once_with(
        ids=[123, 456], error_policy="omit", expand="all"
    )

    # Check that the result contains both work items
    # Title is in the header for basic view
    assert "# Work Item 123: Test Bug" in result
    assert "- **System.WorkItemType**: Bug" in result
    assert "- **System.State**: Active" in result

    assert "# Work Item 456: Test Task" in result
    assert "- **System.WorkItemType**: Task" in result
    assert "- **System.State**: Closed" in result


def test_get_work_item_impl_multiple_detailed():
    """Test retrieving detailed info for multiple work items."""
    mock_client = MagicMock()

    # Mock work items with detailed fields
    mock_work_item1 = MagicMock(spec=WorkItem)
    mock_work_item1.id = 123
    mock_work_item1.fields = {
        "System.WorkItemType": "Bug",
        "System.Title": "Test Bug",
        "System.State": "Active",
        "System.Description": "Bug description",
        "System.AssignedTo": {
            "displayName": "User One",
            "uniqueName": "user1@example.com",
        },
    }

    mock_work_item2 = MagicMock(spec=WorkItem)
    mock_work_item2.id = 456
    mock_work_item2.fields = {
        "System.WorkItemType": "Task",
        "System.Title": "Test Task",
        "System.State": "Closed",
        "System.Description": "Task description",
        "System.AssignedTo": {
            "displayName": "User Two",
            "uniqueName": "user2@example.com",
        },
    }

    mock_client.get_work_items.return_value = [
        mock_work_item1,
        mock_work_item2,
    ]

    result = _get_work_item_impl([123, 456], mock_client, detailed=True)

    # Verify client was called correctly
    mock_client.get_work_items.assert_called_once_with(
        ids=[123, 456], error_policy="omit", expand="all"
    )

    # Check that the result contains detailed info for both work items
    assert "# Work Item 123" in result
    assert "- **System.Description**: Bug description" in result
    assert "- **System.AssignedTo**: User One (user1@example.com)" in result

    assert "# Work Item 456" in result
    assert "- **System.Description**: Task description" in result
    assert "- **System.AssignedTo**: User Two (user2@example.com)" in result


def test_get_work_item_impl_multiple_empty_results():
    """Test handling of empty results when retrieving multiple work items."""
    mock_client = MagicMock()
    mock_client.get_work_items.return_value = []

    result = _get_work_item_impl([123, 456], mock_client)

    assert result == "No work items found."


def test_get_work_item_impl_multiple_with_none_values():
    """Test handling of None values in multiple work items (failed
    retrievals)."""
    mock_client = MagicMock()

    # Mock one valid work item and one None (failed retrieval)
    mock_work_item = MagicMock(spec=WorkItem)
    mock_work_item.id = 123
    mock_work_item.fields = {
        "System.WorkItemType": "Bug",
        "System.Title": "Test Bug",
        "System.State": "Active",
    }

    mock_client.get_work_items.return_value = [
        mock_work_item,
        None,  # Failed retrieval
    ]

    result = _get_work_item_impl([123, 456], mock_client)

    # Should only include the valid work item
    assert "# Work Item 123" in result
    assert "- **System.WorkItemType**: Bug" in result
    # Should not have any error messages about the None value
    assert "456" not in result


def test_get_work_item_impl_multiple_all_none_values():
    """Test handling when all work items return None (all failed
    retrievals)."""
    mock_client = MagicMock()
    mock_client.get_work_items.return_value = [None, None]

    result = _get_work_item_impl([123, 456], mock_client)

    assert result == "No valid work items found with the provided IDs."


def test_get_work_item_impl_multiple_error():
    """Test error handling when retrieving multiple work items."""
    mock_client = MagicMock()
    mock_client.get_work_items.side_effect = Exception("Test error")

    result = _get_work_item_impl([123, 456], mock_client)

    assert "Error retrieving work items [123, 456]: Test error" in result


def test_get_work_item_impl_multiple_string_ids():
    """Test that string IDs in list are converted to integers."""
    mock_client = MagicMock()

    mock_work_item = MagicMock(spec=WorkItem)
    mock_work_item.id = 123
    mock_work_item.fields = {
        "System.WorkItemType": "Bug",
        "System.Title": "Test Bug",
        "System.State": "Active",
    }

    mock_client.get_work_items.return_value = [mock_work_item]

    # Pass string IDs that should be converted to integers
    # Type ignore needed because signature expects int but implementation
    # handles conversion
    result = _get_work_item_impl(["123", "456"], mock_client)  # type: ignore

    # Verify that IDs were converted to integers
    mock_client.get_work_items.assert_called_once_with(
        ids=[123, 456], error_policy="omit", expand="all"
    )

    assert "# Work Item 123" in result
