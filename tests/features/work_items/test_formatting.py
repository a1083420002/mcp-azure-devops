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
    """Test formatting of field values."""

    def test_format_none_value(self):
        """Test formatting None value."""
        result = _format_field_value(None)
        assert result == "None"

    def test_format_string_value(self):
        """Test formatting simple string value."""
        result = _format_field_value("Test String")
        assert result == "Test String"

    def test_format_integer_value(self):
        """Test formatting integer value."""
        result = _format_field_value(42)
        assert result == "42"

    def test_format_float_value(self):
        """Test formatting float value."""
        result = _format_field_value(3.14)
        assert result == "3.14"

    def test_format_dict_with_display_name(self):
        """
        Test formatting dictionary with displayName (person reference).
        """
        field_value = {
            "displayName": "John Doe",
            "uniqueName": "john.doe@example.com",
        }
        result = _format_field_value(field_value)
        assert result == "John Doe (john.doe@example.com)"

    def test_format_dict_with_display_name_no_unique_name(self):
        """Test formatting dictionary with displayName but no uniqueName."""
        field_value = {"displayName": "John Doe"}
        result = _format_field_value(field_value)
        assert result == "John Doe ()"

    def test_format_dict_without_display_name(self):
        """Test formatting dictionary without displayName."""
        field_value = {"key1": "value1", "key2": "value2"}
        result = _format_field_value(field_value)
        assert "key1: value1" in result
        assert "key2: value2" in result
        assert ", " in result

    def test_format_object_with_display_name_and_unique_name(self):
        """
        Test formatting object with display_name and unique_name.
        """
        mock_obj = MagicMock()
        mock_obj.display_name = "Jane Smith"
        mock_obj.unique_name = "jane.smith@example.com"
        result = _format_field_value(mock_obj)
        assert result == "Jane Smith (jane.smith@example.com)"

    def test_format_object_with_display_name_only(self):
        """Test formatting object with display_name attribute only."""
        mock_obj = MagicMock()
        mock_obj.display_name = "Project Team"
        # Remove unique_name attribute
        delattr(mock_obj, "unique_name")
        result = _format_field_value(mock_obj)
        assert result == "Project Team"

    def test_format_boolean_value(self):
        """Test formatting boolean value."""
        result_true = _format_field_value(True)
        assert result_true == "True"

        result_false = _format_field_value(False)
        assert result_false == "False"

    def test_format_list_value(self):
        """Test formatting list value."""
        result = _format_field_value([1, 2, 3])
        assert result == "[1, 2, 3]"


class TestFormatBoardInfo:
    """Test formatting of board-related information."""

    def test_format_with_board_column(self):
        """Test formatting with board column information."""
        fields = {"System.BoardColumn": "In Progress"}
        result = _format_board_info(fields)
        assert len(result) == 1
        assert result[0] == "Board Column: In Progress"

    def test_format_with_board_column_and_done_state(self):
        """Test formatting with board column and done state."""
        fields = {
            "System.BoardColumn": "In Progress",
            "System.BoardColumnDone": True,
        }
        result = _format_board_info(fields)
        assert len(result) == 2
        assert result[0] == "Board Column: In Progress"
        assert result[1] == "Column State: Done"

    def test_format_with_board_column_not_done(self):
        """Test formatting with board column not done."""
        fields = {
            "System.BoardColumn": "In Progress",
            "System.BoardColumnDone": False,
        }
        result = _format_board_info(fields)
        assert len(result) == 2
        assert result[0] == "Board Column: In Progress"
        assert result[1] == "Column State: Not Done"

    def test_format_with_no_board_column(self):
        """Test formatting with no board column information."""
        fields = {"System.Title": "Test Work Item"}
        result = _format_board_info(fields)
        assert len(result) == 0
        assert result == []

    def test_format_with_empty_fields(self):
        """Test formatting with empty fields dictionary."""
        fields = {}
        result = _format_board_info(fields)
        assert len(result) == 0
        assert result == []


class TestFormatBuildInfo:
    """Test formatting of build-related information."""

    def test_format_with_found_in_build(self):
        """Test formatting with found in build information."""
        fields = {"Microsoft.VSTS.Build.FoundIn": "Build 1.0.123"}
        result = _format_build_info(fields)
        assert len(result) == 1
        assert result[0] == "Found In: Build 1.0.123"

    def test_format_with_integration_build(self):
        """Test formatting with integration build information."""
        fields = {"Microsoft.VSTS.Build.IntegrationBuild": "CI Build #456"}
        result = _format_build_info(fields)
        assert len(result) == 1
        assert result[0] == "Integration Build: CI Build #456"

    def test_format_with_both_build_fields(self):
        """Test formatting with both build fields."""
        fields = {
            "Microsoft.VSTS.Build.FoundIn": "Build 1.0.123",
            "Microsoft.VSTS.Build.IntegrationBuild": "CI Build #456",
        }
        result = _format_build_info(fields)
        assert len(result) == 2
        assert result[0] == "Found In: Build 1.0.123"
        assert result[1] == "Integration Build: CI Build #456"

    def test_format_with_no_build_info(self):
        """Test formatting with no build information."""
        fields = {"System.Title": "Test Work Item"}
        result = _format_build_info(fields)
        assert len(result) == 0
        assert result == []

    def test_format_with_empty_fields(self):
        """Test formatting with empty fields dictionary."""
        fields = {}
        result = _format_build_info(fields)
        assert len(result) == 0
        assert result == []


class TestFormatWorkItem:
    """Test formatting of complete work items."""

    def test_format_minimal_work_item(self):
        """Test formatting work item with minimal fields."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 123
        mock_work_item.fields = {}

        result = format_work_item(mock_work_item)
        assert "# Work Item 123" in result

    def test_format_work_item_with_title(self):
        """Test formatting work item with title."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 123
        mock_work_item.fields = {"System.Title": "Test Bug"}

        result = format_work_item(mock_work_item)
        assert "# Work Item 123: Test Bug" in result

    def test_format_work_item_detailed_mode(self):
        """Test formatting work item in detailed mode."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 123
        mock_work_item.fields = {
            "System.Title": "Test Bug",
            "System.WorkItemType": "Bug",
            "System.State": "Active",
            "System.AssignedTo": {
                "displayName": "John Doe",
                "uniqueName": "john@example.com",
            },
        }
        mock_work_item.relations = None

        result = format_work_item(mock_work_item, detailed=True)

        assert "# Work Item 123: Test Bug" in result
        assert "- **System.AssignedTo**: John Doe (john@example.com)" in result
        assert "- **System.State**: Active" in result
        assert "- **System.Title**: Test Bug" in result
        assert "- **System.WorkItemType**: Bug" in result

    def test_format_work_item_basic_mode(self):
        """Test formatting work item in basic mode."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 456
        mock_work_item.fields = {
            "System.Title": "User Story",
            "System.WorkItemType": "User Story",
            "System.State": "New",
            "System.AssignedTo": {
                "displayName": "Jane Smith",
                "uniqueName": "jane@example.com",
            },
            "System.CreatedDate": "2023-01-01",
            "System.ChangedDate": "2023-01-02",
            "System.Description": "This is a detailed description",
        }
        mock_work_item.relations = None

        result = format_work_item(mock_work_item, detailed=False)

        # Should include basic fields
        assert "# Work Item 456: User Story" in result
        assert "- **System.WorkItemType**: User Story" in result
        assert "- **System.State**: New" in result
        assert (
            "- **System.AssignedTo**: Jane Smith (jane@example.com)" in result
        )
        assert "- **System.CreatedDate**: 2023-01-01" in result
        assert "- **System.ChangedDate**: 2023-01-02" in result

        # Should NOT include detailed fields in basic mode
        assert "System.Description" not in result

    def test_format_work_item_with_relations(self):
        """Test formatting work item with relations."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 789
        mock_work_item.fields = {"System.Title": "Task with Relations"}

        # Create mock relations
        mock_relation1 = MagicMock()
        mock_relation1.rel = "Parent"
        mock_relation1.url = "https://example.com/workitem/123"
        mock_relation1.attributes = {"name": "Parent Work Item"}

        mock_relation2 = MagicMock()
        mock_relation2.rel = "Child"
        mock_relation2.url = "https://example.com/workitem/456"
        mock_relation2.attributes = None

        mock_work_item.relations = [mock_relation1, mock_relation2]

        result = format_work_item(mock_work_item, detailed=True)

        assert "## Related Items" in result
        assert "- Parent URL: https://example.com/workitem/123" in result
        assert "- Child URL: https://example.com/workitem/456" in result
        assert ":: Attributes: {'name': 'Parent Work Item'}" in result

    def test_format_work_item_relations_not_in_basic_mode(self):
        """Test that relations are not shown in basic mode."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 999
        mock_work_item.fields = {"System.Title": "Task"}

        mock_relation = MagicMock()
        mock_relation.rel = "Parent"
        mock_relation.url = "https://example.com/workitem/123"
        mock_work_item.relations = [mock_relation]

        result = format_work_item(mock_work_item, detailed=False)

        # Relations should not appear in basic mode
        assert "## Related Items" not in result
        assert "Parent URL" not in result

    def test_format_work_item_with_none_fields(self):
        """Test formatting work item with None fields."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 111
        mock_work_item.fields = None
        mock_work_item.relations = None

        result = format_work_item(mock_work_item)
        assert "# Work Item 111" in result

    def test_format_work_item_alphabetical_order(self):
        """Test that fields are sorted alphabetically in detailed mode."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 222
        mock_work_item.fields = {
            "System.Title": "Test",
            "System.State": "Active",
            "System.AssignedTo": "User",
            "Custom.ZField": "Last",
            "Custom.AField": "First",
        }
        mock_work_item.relations = None

        result = format_work_item(mock_work_item, detailed=True)
        lines = result.split("\n")

        # Find field lines (they start with "- **")
        field_lines = [line for line in lines if line.startswith("- **")]

        # Extract field names
        field_names = []
        for line in field_lines:
            # Extract field name between "- **" and "**:"
            field_name = line.split("**")[1]
            field_names.append(field_name)

        # Check that field names are in alphabetical order
        assert field_names == sorted(field_names)

    def test_format_work_item_partial_basic_fields(self):
        """Test basic mode with only some of the important fields present."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 333
        mock_work_item.fields = {
            "System.Title": "Partial Fields",
            "System.WorkItemType": "Bug",
            # Missing State, AssignedTo, CreatedDate, ChangedDate
        }
        mock_work_item.relations = None

        result = format_work_item(mock_work_item, detailed=False)

        # Should include present fields
        assert "- **System.WorkItemType**: Bug" in result

        # Should not error on missing fields
        assert "System.State" not in result
        assert "System.AssignedTo" not in result

    def test_format_work_item_complex_field_types(self):
        """Test formatting with various complex field types."""
        mock_work_item = MagicMock(spec=WorkItem)
        mock_work_item.id = 444
        mock_work_item.fields = {
            "System.Title": "Complex Fields",
            "System.Tags": "tag1; tag2; tag3",
            "System.CreatedDate": "2023-01-01T10:00:00Z",
            "Microsoft.VSTS.Common.Priority": 1,
            "Microsoft.VSTS.Scheduling.StoryPoints": 5.0,
        }
        mock_work_item.relations = None

        result = format_work_item(mock_work_item, detailed=True)

        assert "- **System.Tags**: tag1; tag2; tag3" in result
        assert "- **System.CreatedDate**: 2023-01-01T10:00:00Z" in result
        assert "- **Microsoft.VSTS.Common.Priority**: 1" in result
        assert "- **Microsoft.VSTS.Scheduling.StoryPoints**: 5.0" in result
