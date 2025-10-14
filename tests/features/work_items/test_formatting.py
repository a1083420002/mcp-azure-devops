"""Tests for work item formatting utilities."""

from unittest.mock import MagicMock

from azure.devops.v7_1.work_item_tracking.models import WorkItem

from mcp_azure_devops.features.work_items.formatting import (
    _format_board_info,
    _format_build_info,
    _format_field_value,
    format_work_item,
)


class TestFormatFieldValue:
    """Test _format_field_value function."""

    def test_format_none_value(self):
        """Test formatting None value."""
        result = _format_field_value(None)
        assert result == "None"

    def test_format_string_value(self):
        """Test formatting string value."""
        result = _format_field_value("Test String")
        assert result == "Test String"

    def test_format_number_value(self):
        """Test formatting number value."""
        result = _format_field_value(42)
        assert result == "42"

        result = _format_field_value(3.14)
        assert result == "3.14"

    def test_format_boolean_value(self):
        """Test formatting boolean value."""
        result = _format_field_value(True)
        assert result == "True"

        result = _format_field_value(False)
        assert result == "False"

    def test_format_dict_with_display_name(self):
        """Test formatting dictionary with displayName and uniqueName."""
        field_value = {
            "displayName": "John Doe",
            "uniqueName": "john.doe@example.com",
        }
        result = _format_field_value(field_value)
        assert result == "John Doe (john.doe@example.com)"

    def test_format_dict_with_display_name_no_unique_name(self):
        """Test formatting dictionary with displayName but no uniqueName."""
        field_value = {"displayName": "Jane Doe"}
        result = _format_field_value(field_value)
        assert result == "Jane Doe ()"

    def test_format_dict_without_display_name(self):
        """Test formatting dictionary without displayName."""
        field_value = {"key1": "value1", "key2": "value2", "key3": "value3"}
        result = _format_field_value(field_value)
        assert "key1: value1" in result
        assert "key2: value2" in result
        assert "key3: value3" in result

    def test_format_object_with_display_name_and_unique_name(self):
        """Test formatting object with display_name and unique_name."""
        mock_obj = MagicMock()
        mock_obj.display_name = "Test User"
        mock_obj.unique_name = "test.user@example.com"

        result = _format_field_value(mock_obj)
        assert result == "Test User (test.user@example.com)"

    def test_format_object_with_display_name_only(self):
        """Test formatting object with only display_name attribute."""
        mock_obj = MagicMock()
        mock_obj.display_name = "Test User"
        # Remove unique_name attribute
        del mock_obj.unique_name

        result = _format_field_value(mock_obj)
        assert result == "Test User"

    def test_format_generic_object(self):
        """Test formatting generic object without special attributes."""

        class GenericObject:
            def __str__(self):
                return "Generic Object String"

        obj = GenericObject()
        result = _format_field_value(obj)
        assert result == "Generic Object String"

    def test_format_list_value(self):
        """Test formatting list value."""
        result = _format_field_value([1, 2, 3])
        assert result == "[1, 2, 3]"


class TestFormatBoardInfo:
    """Test _format_board_info function."""

    def test_format_board_info_empty_fields(self):
        """Test formatting board info with empty fields."""
        result = _format_board_info({})
        assert result == []

    def test_format_board_info_with_board_column_only(self):
        """Test formatting board info with only board column."""
        fields = {"System.BoardColumn": "In Progress"}
        result = _format_board_info(fields)
        assert len(result) == 1
        assert result[0] == "Board Column: In Progress"

    def test_format_board_info_with_board_column_done(self):
        """Test formatting board info with board column and done state."""
        fields = {
            "System.BoardColumn": "Testing",
            "System.BoardColumnDone": True,
        }
        result = _format_board_info(fields)
        assert len(result) == 2
        assert result[0] == "Board Column: Testing"
        assert result[1] == "Column State: Done"

    def test_format_board_info_with_board_column_not_done(self):
        """Test formatting board info with board column and not done state."""
        fields = {
            "System.BoardColumn": "Development",
            "System.BoardColumnDone": False,
        }
        result = _format_board_info(fields)
        assert len(result) == 2
        assert result[0] == "Board Column: Development"
        assert result[1] == "Column State: Not Done"

    def test_format_board_info_without_board_column(self):
        """Test formatting board info without board column."""
        # Done state should not appear without board column
        fields = {"System.BoardColumnDone": True}
        result = _format_board_info(fields)
        assert result == []


class TestFormatBuildInfo:
    """Test _format_build_info function."""

    def test_format_build_info_empty_fields(self):
        """Test formatting build info with empty fields."""
        result = _format_build_info({})
        assert result == []

    def test_format_build_info_with_found_in(self):
        """Test formatting build info with FoundIn field."""
        fields = {"Microsoft.VSTS.Build.FoundIn": "Build 1.0.0"}
        result = _format_build_info(fields)
        assert len(result) == 1
        assert result[0] == "Found In: Build 1.0.0"

    def test_format_build_info_with_integration_build(self):
        """Test formatting build info with IntegrationBuild field."""
        fields = {"Microsoft.VSTS.Build.IntegrationBuild": "CI-Build-123"}
        result = _format_build_info(fields)
        assert len(result) == 1
        assert result[0] == "Integration Build: CI-Build-123"

    def test_format_build_info_with_both_fields(self):
        """Test formatting build info with both build fields."""
        fields = {
            "Microsoft.VSTS.Build.FoundIn": "Build 1.0.0",
            "Microsoft.VSTS.Build.IntegrationBuild": "CI-Build-123",
        }
        result = _format_build_info(fields)
        assert len(result) == 2
        assert result[0] == "Found In: Build 1.0.0"
        assert result[1] == "Integration Build: CI-Build-123"


class TestFormatWorkItem:
    """Test format_work_item function."""

    def test_format_work_item_basic_no_title(self):
        """Test formatting work item without title."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 123
        mock_work_item.fields = {}
        mock_work_item.relations = None

        result = format_work_item(mock_work_item, detailed=False)
        assert "# Work Item 123" in result

    def test_format_work_item_basic_with_title(self):
        """Test formatting work item with title."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 456
        mock_work_item.fields = {"System.Title": "Test Bug Title"}
        mock_work_item.relations = None

        result = format_work_item(mock_work_item, detailed=False)
        assert "# Work Item 456: Test Bug Title" in result

    def test_format_work_item_basic_mode(self):
        """Test formatting work item in basic mode."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 789
        mock_work_item.fields = {
            "System.Title": "Task Title",
            "System.WorkItemType": "Task",
            "System.State": "Active",
            "System.AssignedTo": {
                "displayName": "Test User",
                "uniqueName": "test@example.com",
            },
            "System.CreatedDate": "2024-01-01",
            "System.ChangedDate": "2024-01-15",
            "System.Description": "Some description",
            "Custom.Field": "Should not appear in basic mode",
        }
        mock_work_item.relations = None

        result = format_work_item(mock_work_item, detailed=False)

        # Should contain important fields
        assert "# Work Item 789: Task Title" in result
        assert "- **System.WorkItemType**: Task" in result
        assert "- **System.State**: Active" in result
        expected_assigned = (
            "- **System.AssignedTo**: Test User (test@example.com)"
        )
        assert expected_assigned in result
        assert "- **System.CreatedDate**: 2024-01-01" in result
        assert "- **System.ChangedDate**: 2024-01-15" in result

        # Should not contain non-important fields
        assert "Custom.Field" not in result
        assert "System.Description" not in result

    def test_format_work_item_detailed_mode(self):
        """Test formatting work item in detailed mode."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 999
        mock_work_item.fields = {
            "System.Title": "Detailed Task",
            "System.WorkItemType": "Task",
            "System.State": "New",
            "System.Description": "Detailed description",
            "Custom.Field": "Custom value",
            "System.Tags": "tag1; tag2",
        }
        mock_work_item.relations = None

        result = format_work_item(mock_work_item, detailed=True)

        # Should contain all fields in alphabetical order
        assert "# Work Item 999: Detailed Task" in result
        assert "- **Custom.Field**: Custom value" in result
        assert "- **System.Description**: Detailed description" in result
        assert "- **System.State**: New" in result
        assert "- **System.Tags**: tag1; tag2" in result
        assert "- **System.Title**: Detailed Task" in result
        assert "- **System.WorkItemType**: Task" in result

        # Check alphabetical ordering
        # Custom.Field should appear before System.* fields
        custom_index = result.index("Custom.Field")
        system_index = result.index("System.Description")
        assert custom_index < system_index

    def test_format_work_item_with_relations_detailed(self):
        """Test formatting work item with relations in detailed mode."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 111
        mock_work_item.fields = {"System.Title": "Work Item with Relations"}

        # Mock relations
        mock_relation1 = MagicMock()
        mock_relation1.rel = "Related"
        mock_relation1.url = (
            "https://dev.azure.com/org/project/_workitems/edit/222"
        )
        mock_relation1.attributes = {"name": "Related Work"}

        mock_relation2 = MagicMock()
        mock_relation2.rel = "Parent"
        mock_relation2.url = (
            "https://dev.azure.com/org/project/_workitems/edit/333"
        )
        mock_relation2.attributes = None

        mock_work_item.relations = [mock_relation1, mock_relation2]

        result = format_work_item(mock_work_item, detailed=True)

        # Should contain relations section
        assert "## Related Items" in result
        expected_related = (
            "- Related URL: "
            "https://dev.azure.com/org/project/_workitems/edit/222"
        )
        assert expected_related in result
        assert ":: Attributes: {'name': 'Related Work'}" in result
        expected_parent = (
            "- Parent URL: "
            "https://dev.azure.com/org/project/_workitems/edit/333"
        )
        assert expected_parent in result

    def test_format_work_item_with_relations_basic(self):
        """Test formatting work item with relations in basic mode."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 222
        mock_work_item.fields = {
            "System.Title": "Work Item Basic",
            "System.WorkItemType": "Bug",
            "System.State": "Active",
        }

        # Mock relations
        mock_relation = MagicMock()
        mock_relation.rel = "Related"
        mock_relation.url = (
            "https://dev.azure.com/org/project/_workitems/edit/333"
        )
        mock_work_item.relations = [mock_relation]

        result = format_work_item(mock_work_item, detailed=False)

        # Should not contain relations section in basic mode
        assert "## Related Items" not in result
        assert "Related URL" not in result

    def test_format_work_item_with_none_fields(self):
        """Test formatting work item with None fields."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 333
        mock_work_item.fields = None
        mock_work_item.relations = None

        result = format_work_item(mock_work_item, detailed=True)

        # Should handle None fields gracefully
        assert "# Work Item 333" in result

    def test_format_work_item_with_empty_relations(self):
        """Test formatting work item with empty relations list."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 444
        mock_work_item.fields = {"System.Title": "No Relations"}
        mock_work_item.relations = []

        result = format_work_item(mock_work_item, detailed=True)

        # Should not show relations section if empty
        assert "## Related Items" not in result

    def test_format_work_item_no_relations_attribute(self):
        """Test formatting work item without relations attribute."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 555
        mock_work_item.fields = {"System.Title": "No Relations Attribute"}
        # Remove relations attribute completely
        delattr(mock_work_item, "relations")

        result = format_work_item(mock_work_item, detailed=True)

        # Should handle missing relations attribute gracefully
        assert "# Work Item 555: No Relations Attribute" in result
        assert "## Related Items" not in result
