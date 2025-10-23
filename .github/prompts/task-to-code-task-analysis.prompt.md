---
agent: 'agent'
---

# Prompt: Azure DevOps Work Item → Task Analysis (Task type = code)

> **Use case**: Analyze a Task and prepare a comprehensive implementation summary for GitHub Copilot Coding Agent.
> **Note**: Execute strictly one step at a time. Do not proceed to the next step until the previous step is completed and confirmed.
> ⚠️ **Critical**: This prompt does NOT generate any code. It only analyzes and summarizes.

---

## Overview

This prompt performs **Task Analysis** to prepare a structured summary that will be fed to GitHub Copilot Coding Agent for actual code generation. The analysis ensures all requirements are clear before expensive cloud-based code generation begins.

---

## Step 1 — Retrieve work item context

* Fetch the work item **Description** and **Discussion** (comments/history) for `{VSTS_WORK_ITEM_ID}` from Azure DevOps. If an MCP Tool is available, call it (e.g., `get_work_item`) to obtain the latest content. Otherwise, ask the user to paste the current Description and recent Discussion thread.
* When reading **Discussion**, **ignore any content under `Task檢核結果`**.
* **If you have any questions, ask the user to confirm before proceeding.**

---

## Step 2 — Gap check with the user

* Review the retrieved Description & Discussion and identify **missing or unclear content** (e.g., requirements, constraints, edge cases, environment details, acceptance criteria).
* Present a concise checklist of gaps and **ask the user whether these should be supplemented**. If supplementation is needed, discuss and capture the exact wording to add.
* **If you have any questions, ask the user to confirm before proceeding.**

---

## Step 3 — Key implementation logic (list & verify)

* List the **Key Implementation Logic** for this task as bullet points:
  - **Inputs**: What data/parameters does this implementation receive?
  - **Outputs**: What does it return or produce?
  - **Data Flow**: How does data move through the system?
  - **Error Handling**: What exceptions or edge cases must be handled?
  - **Logging/Telemetry**: What should be logged for debugging and monitoring?
  - **Performance Considerations**: Any specific performance requirements or constraints?
* Highlight any **uncertainties or assumptions** and confirm them with the user. If anything is incorrect, correct it and restate the final logic.
* **If you have any questions, ask the user to confirm before proceeding.**

---

## Step 4 — Dependencies analysis

* Propose any **packages/dependencies** that might be required:
  - For each dependency, recommend a **specific version** (prefer LTS/stable or organization standard)
  - Explain **why** this dependency is needed
  - Confirm with the user before adopting
* List any **internal dependencies**:
  - Services or repositories that need to be injected
  - Interfaces that must be implemented
  - Existing components that will be modified
* **If you have any questions, ask the user to confirm before proceeding.**

---

## Step 5 — Update Task Description (if needed)

* If the **Task scope or plan** changed based on Steps 2–4, use the **MCP Tool `update_work_item`** to update the Task **Description** following the exact format below. 
* Ask the user to review the drafted content before sending the update.

**Required sections:**
  * **Context & Scope**
  * **Goals & Non-Goals**
  * **Work Summary**
  * **Design Considerations & Trade-offs**
  * **Key Implementation Logic**
  * **Affected File Paths**
  * **Dependencies and Task Relationships**
  * **Cross-cutting Concerns**

* **If you have any questions, ask the user to confirm before proceeding.**

---

## Step 6 — Generate Task Analysis Summary

* Create a comprehensive **Task Analysis Summary** that will be posted to the work item's **Discussion** as a comment.
* This summary will be the **sole input** for GitHub Copilot Coding Agent to generate code.
* Use `add_work_item_comment` to post the summary with the title: **`[TASK-ANALYSIS] Task Analysis Summary — {YYYY-MM-DD}`**

### Task Analysis Summary Template

```markdown
[TASK-ANALYSIS] Task Analysis Summary — {YYYY-MM-DD}

## 📋 Implementation Overview
{Brief description of what needs to be implemented}

## 🎯 Key Implementation Logic

### Inputs
- {Input parameter 1}: {type} - {description}
- {Input parameter 2}: {type} - {description}

### Outputs
- {Return type}: {description}
- {Side effects}: {description}

### Data Flow
1. {Step 1 description}
2. {Step 2 description}
3. {Step 3 description}

### Error Handling
- **Scenario**: {error condition}
  - **Action**: {how to handle}
  - **Exception**: {exception type if applicable}

### Logging/Telemetry
- {Log point 1}: {what to log and why}
- {Log point 2}: {what to log and why}

### Performance Considerations
- {Consideration 1}
- {Consideration 2}

## 📦 Dependencies

### External Packages
- **Package**: {package name} v{version}
  - **Purpose**: {why needed}
  - **Usage**: {how it will be used}

### Internal Dependencies
- **Service/Repository**: {name}
  - **Interface**: {interface name}
  - **Methods**: {method signatures}
  - **Injection**: {how to inject}

## 📁 Affected File Paths

### Files to Create
- `{full/path/to/NewFile1.cs}` - {purpose}
- `{full/path/to/NewFile2.cs}` - {purpose}

### Files to Modify
- `{full/path/to/ExistingFile1.cs}`
  - **Changes**: {what changes are needed}
  - **Methods**: {methods to modify/add}
- `{full/path/to/ExistingFile2.cs}`
  - **Changes**: {what changes are needed}
  - **Methods**: {methods to modify/add}

## 🔧 Implementation Details

### Class Structure
```
{ClassName}
├── Constructor: {parameters}
├── Public Methods:
│   ├── {MethodName1}({params}): {return type}
│   └── {MethodName2}({params}): {return type}
└── Private Methods:
    └── {MethodName3}({params}): {return type}
```

### Key Algorithms/Logic
- **{Logic Point 1}**: {detailed explanation}
- **{Logic Point 2}**: {detailed explanation}

### Validation Rules
- {Rule 1}: {description}
- {Rule 2}: {description}

## ⚙️ Configuration & Settings
- **App Settings**: {any configuration keys needed}
- **Connection Strings**: {any connection strings}
- **Environment Variables**: {any env vars}

## 🔄 Migration/Rollback Strategy
- **Migration Steps**: {if applicable}
- **Rollback Plan**: {how to rollback if needed}
- **Data Impact**: {any data changes}

## ⚠️ Edge Cases & Constraints
- **Edge Case 1**: {description} → {how to handle}
- **Edge Case 2**: {description} → {how to handle}
- **Constraint 1**: {description}
- **Constraint 2**: {description}

## 🧪 Testing Considerations
- **Unit Test Focus**: {what should be tested}
- **Mock Objects**: {what needs to be mocked}
- **Test Data**: {what test data is needed}

## 📝 Additional Notes
{Any other important information for code generation}
```

* After posting, **confirm with the user** that the Task Analysis Summary is complete and accurate.
* **If you have any questions, ask the user to confirm before proceeding.**

---

## Execution Rules

* **Execute one step at a time. Do not start the next step until the previous step is fully confirmed by the user.**
* ⚠️ **This prompt does NOT generate any code. It only analyzes and prepares the Task Analysis Summary.**
* All analysis must be clear, specific, and actionable for the Coding Agent.
* If any requirement is ambiguous, ask the user for clarification before proceeding.

---

