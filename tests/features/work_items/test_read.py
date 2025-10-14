"""
Unit tests for work item read operations.

This module contains comprehensive tests for the read.py module,
including tests for retrieving single and multiple work items.
"""

from unittest.mock import MagicMock

from azure.devops.v7_1.work_item_tracking.models import WorkItem

from mcp_azure_devops.features.work_items.tools.read import (
    _get_work_item_impl,
)


class TestGetWorkItemImpl:
    """Test suite for _get_work_item_impl function."""

    def test_get_single_work_item_detailed(self):
        """Test retrieving a single work item with detailed information."""
        mock_client = MagicMock()

        # Mock work item with detailed fields
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 123
        mock_work_item.fields = {
            "System.WorkItemType": "Bug",
            "System.Title": "Test Bug",
            "System.State": "Active",
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

        result = _get_work_item_impl(123, mock_client, detailed=True)

        # Verify the result contains detailed information
        assert "# Work Item 123" in result
        assert "- **System.WorkItemType**: Bug" in result
        assert "- **System.Title**: Test Bug" in result
        assert "- **System.State**: Active" in result
        assert (
            "- **System.Description**: This is a detailed description"
            in result
        )
        assert (
            "- **System.AssignedTo**: Test User (test@example.com)" in result
        )
        assert "- **System.CreatedBy**: Creator User" in result
        assert "- **System.IterationPath**: Project\\Sprint 1" in result
        assert "- **System.AreaPath**: Project\\Area" in result
        assert "- **System.Tags**: tag1; tag2" in result

        # Verify client was called correctly
        mock_client.get_work_item.assert_called_once_with(123, expand="all")

    def test_get_single_work_item_basic(self):
        """Test retrieving a single work item with basic information."""
        mock_client = MagicMock()

        # Mock work item with basic fields
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 456
        mock_work_item.fields = {
            "System.WorkItemType": "Task",
            "System.Title": "Test Task",
            "System.State": "In Progress",
            "System.AssignedTo": {
                "displayName": "Task Owner",
                "uniqueName": "owner@example.com",
            },
            "System.CreatedDate": "2023-02-01",
            "System.ChangedDate": "2023-02-15",
            "System.Description": "This should not appear in basic mode",
        }
        mock_client.get_work_item.return_value = mock_work_item

        result = _get_work_item_impl(456, mock_client, detailed=False)

        # Verify basic fields are present
        assert "# Work Item 456" in result
        assert "- **System.WorkItemType**: Task" in result
        assert "- **System.State**: In Progress" in result
        assert (
            "- **System.AssignedTo**: Task Owner (owner@example.com)" in result
        )
        assert "- **System.CreatedDate**: 2023-02-01" in result
        assert "- **System.ChangedDate**: 2023-02-15" in result

        # Verify detailed field is NOT present in basic mode
        assert "This should not appear in basic mode" not in result

    def test_get_multiple_work_items(self):
        """Test retrieving multiple work items at once."""
        mock_client = MagicMock()

        # Mock multiple work items
        mock_work_item1 = MagicMock(spec=WorkItem)
        mock_work_item1.id = 101
        mock_work_item1.fields = {
            "System.WorkItemType": "Bug",
            "System.Title": "First Bug",
            "System.State": "Active",
        }

        mock_work_item2 = MagicMock(spec=WorkItem)
        mock_work_item2.id = 102
        mock_work_item2.fields = {
            "System.WorkItemType": "Task",
            "System.Title": "First Task",
            "System.State": "Closed",
        }

        mock_work_item3 = MagicMock(spec=WorkItem)
        mock_work_item3.id = 103
        mock_work_item3.fields = {
            "System.WorkItemType": "User Story",
            "System.Title": "First Story",
            "System.State": "New",
        }

        mock_client.get_work_items.return_value = [
            mock_work_item1,
            mock_work_item2,
            mock_work_item3,
        ]

        result = _get_work_item_impl([101, 102, 103], mock_client)

        # Verify all work items are in the result
        assert "# Work Item 101" in result
        assert "First Bug" in result
        assert "# Work Item 102" in result
        assert "First Task" in result
        assert "# Work Item 103" in result
        assert "First Story" in result

        # Verify results are separated by double newlines
        assert "\n\n" in result

        # Verify client was called correctly
        mock_client.get_work_items.assert_called_once_with(
            ids=[101, 102, 103], error_policy="omit", expand="all"
        )

    def test_get_multiple_work_items_with_none_values(self):
        """Test handling of None work items in list (error_policy omit)."""
        mock_client = MagicMock()

        # Mock work items with one None (simulating omitted failed retrieval)
        mock_work_item1 = MagicMock(spec=WorkItem)
        mock_work_item1.id = 201
        mock_work_item1.fields = {
            "System.WorkItemType": "Bug",
            "System.Title": "Valid Bug",
            "System.State": "Active",
        }

        mock_work_item2 = MagicMock(spec=WorkItem)
        mock_work_item2.id = 203
        mock_work_item2.fields = {
            "System.WorkItemType": "Task",
            "System.Title": "Valid Task",
            "System.State": "Closed",
        }

        # Return list with None (202 failed to retrieve)
        mock_client.get_work_items.return_value = [
            mock_work_item1,
            None,
            mock_work_item2,
        ]

        result = _get_work_item_impl([201, 202, 203], mock_client)

        # Verify only valid work items are in the result
        assert "# Work Item 201" in result
        assert "Valid Bug" in result
        assert "# Work Item 203" in result
        assert "Valid Task" in result

        # Verify no errors appear for the None item
        assert "None" not in result
        assert "Error" not in result

    def test_get_work_items_empty_list(self):
        """Test handling of empty work item list."""
        mock_client = MagicMock()
        mock_client.get_work_items.return_value = []

        result = _get_work_item_impl([999], mock_client)

        assert result == "No work items found."

    def test_get_work_items_all_none(self):
        """Test when all work items in list are None."""
        mock_client = MagicMock()
        mock_client.get_work_items.return_value = [None, None, None]

        result = _get_work_item_impl([301, 302, 303], mock_client)

        assert result == "No valid work items found with the provided IDs."

    def test_get_single_work_item_with_relations(self):
        """Test retrieving a work item with related items."""
        mock_client = MagicMock()

        # Mock work item with relations
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 401
        mock_work_item.fields = {
            "System.WorkItemType": "User Story",
            "System.Title": "Story with Relations",
            "System.State": "Active",
        }

        # Mock relations
        mock_relation1 = MagicMock()
        mock_relation1.rel = "System.LinkTypes.Hierarchy-Forward"
        mock_relation1.url = (
            "https://dev.azure.com/org/_apis/wit/workItems/402"
        )
        mock_relation1.attributes = {"name": "Child"}

        mock_relation2 = MagicMock()
        mock_relation2.rel = "System.LinkTypes.Related"
        mock_relation2.url = (
            "https://dev.azure.com/org/_apis/wit/workItems/403"
        )
        mock_relation2.attributes = {"name": "Related"}

        mock_work_item.relations = [mock_relation1, mock_relation2]

        mock_client.get_work_item.return_value = mock_work_item

        result = _get_work_item_impl(401, mock_client, detailed=True)

        # Verify relations are included
        assert "## Related Items" in result
        assert "System.LinkTypes.Hierarchy-Forward" in result
        assert "System.LinkTypes.Related" in result
        assert "https://dev.azure.com/org/_apis/wit/workItems/402" in result
        assert "https://dev.azure.com/org/_apis/wit/workItems/403" in result

    def test_get_single_work_item_without_relations_detailed(self):
        """Test retrieving detailed work item without relations."""
        mock_client = MagicMock()

        # Mock work item without relations
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 501
        mock_work_item.fields = {
            "System.WorkItemType": "Bug",
            "System.Title": "Bug without Relations",
            "System.State": "New",
        }
        mock_work_item.relations = None

        mock_client.get_work_item.return_value = mock_work_item

        result = _get_work_item_impl(501, mock_client, detailed=True)

        # Verify no relations section appears
        assert "## Related Items" not in result
        assert "# Work Item 501" in result

    def test_get_single_work_item_error(self):
        """Test error handling when retrieving single work item fails."""
        mock_client = MagicMock()
        mock_client.get_work_item.side_effect = Exception(
            "Work item not found"
        )

        result = _get_work_item_impl(999, mock_client)

        assert "Error retrieving work item 999: Work item not found" in result

    def test_get_multiple_work_items_error(self):
        """Test error handling when retrieving multiple work items fails."""
        mock_client = MagicMock()
        mock_client.get_work_items.side_effect = Exception(
            "Network connection failed"
        )

        result = _get_work_item_impl([101, 102], mock_client)

        assert "Error retrieving work items [101, 102]" in result
        assert "Network connection failed" in result

    def test_get_work_item_with_string_ids_in_list(self):
        """Test handling of string IDs in list (should be converted)."""
        mock_client = MagicMock()

        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 601
        mock_work_item.fields = {
            "System.WorkItemType": "Task",
            "System.Title": "String ID Test",
            "System.State": "Active",
        }

        mock_client.get_work_items.return_value = [mock_work_item]

        # Pass string IDs (should be converted to int)
        # type: ignore - intentionally testing runtime conversion
        result = _get_work_item_impl(["601"], mock_client)  # type: ignore[arg-type]

        # Verify it works
        assert "# Work Item 601" in result
        assert "String ID Test" in result

        # Verify the IDs were converted to integers
        call_args = mock_client.get_work_items.call_args
        assert call_args[1]["ids"] == [601]

    def test_get_work_item_title_in_header(self):
        """Test that work item title appears in the header."""
        mock_client = MagicMock()

        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 701
        mock_work_item.fields = {
            "System.Title": "Important Bug",
            "System.WorkItemType": "Bug",
            "System.State": "Active",
        }

        mock_client.get_work_item.return_value = mock_work_item

        result = _get_work_item_impl(701, mock_client)

        # Verify title is in the header
        assert "# Work Item 701: Important Bug" in result

    def test_get_work_item_without_title(self):
        """Test retrieving work item without a title field."""
        mock_client = MagicMock()

        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 801
        mock_work_item.fields = {
            "System.WorkItemType": "Task",
            "System.State": "New",
        }

        mock_client.get_work_item.return_value = mock_work_item

        result = _get_work_item_impl(801, mock_client)

        # Verify header exists without title
        assert "# Work Item 801\n" in result or result.startswith(
            "# Work Item 801\n"
        )

    def test_get_work_items_basic_mode_for_list(self):
        """Test basic mode with multiple work items."""
        mock_client = MagicMock()

        # Mock multiple work items
        mock_work_item1 = MagicMock(spec=WorkItem)
        mock_work_item1.id = 901
        mock_work_item1.fields = {
            "System.WorkItemType": "Bug",
            "System.Title": "Bug One",
            "System.State": "Active",
            "System.AssignedTo": {
                "displayName": "User One",
                "uniqueName": "user1@example.com",
            },
            "System.CreatedDate": "2023-03-01",
            "System.ChangedDate": "2023-03-10",
            "System.Description": "Should not appear",
        }

        mock_work_item2 = MagicMock(spec=WorkItem)
        mock_work_item2.id = 902
        mock_work_item2.fields = {
            "System.WorkItemType": "Task",
            "System.Title": "Task One",
            "System.State": "Closed",
            "System.AssignedTo": {
                "displayName": "User Two",
                "uniqueName": "user2@example.com",
            },
            "System.CreatedDate": "2023-03-05",
            "System.ChangedDate": "2023-03-15",
            "System.Tags": "Should not appear",
        }

        mock_client.get_work_items.return_value = [
            mock_work_item1,
            mock_work_item2,
        ]

        result = _get_work_item_impl([901, 902], mock_client, detailed=False)

        # Verify basic fields are present
        assert "# Work Item 901" in result
        assert "- **System.State**: Active" in result
        assert (
            "- **System.AssignedTo**: User One (user1@example.com)" in result
        )

        assert "# Work Item 902" in result
        assert "- **System.State**: Closed" in result
        assert (
            "- **System.AssignedTo**: User Two (user2@example.com)" in result
        )

        # Verify detailed fields are NOT present
        assert "Should not appear" not in result
        assert "System.Description" not in result
        assert "System.Tags" not in result
