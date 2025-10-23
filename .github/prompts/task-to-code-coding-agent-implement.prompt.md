---
agent: 'agent'
---

# Prompt: GitHub Copilot Coding Agent → Code Generation (Task type = code)

---

## Overview

This prompt is designed to work with **GitHub Copilot Coding Agent**, which:
- Executes in the **GitHub cloud**
- Automatically creates a **new branch**
- Generates code based on Task Analysis Summary
- Automatically **commits** the generated code
- Creates a **Pull Request** for review

⚠️ **Important**: Run `task-to-code-task-analysis` prompt first to prepare the Task Analysis Summary.

---

## Step 1 — Retrieve Task Analysis Summary

* Fetch the work item **Discussion** for `{VSTS_WORK_ITEM_ID}` from Azure DevOps using MCP Tool (e.g., `get_work_item`).
* Look for the most recent comment titled: **`[TASK-ANALYSIS] Task Analysis Summary — {YYYY-MM-DD}`**
* When reading **Discussion**, **ignore any content under `Task檢核結果`**.
* If Task Analysis Summary is NOT found:
  - ❌ **STOP**: Display error message:
    ```
    ❌ Task Analysis Summary not found!
    
    Please run the 'task-to-code-task-analysis' prompt first to generate the Task Analysis Summary.
    
    Required comment title: [TASK-ANALYSIS] Task Analysis Summary — {YYYY-MM-DD}
    ```
  - Do not proceed further.
* **If you have any questions, ask the user to confirm before proceeding.**

---

## Step 2 — Prepare Coding Agent Input

* Format the Task Analysis Summary into a structured prompt for GitHub Copilot Coding Agent.
* Ensure the prompt includes:
  - Complete Task Analysis Summary (all sections)
  - Coding constraints from repository instructions (.github/instructions/code_generation.instructions.md)
  - Project structure context


### Coding Agent Prompt Template

```markdown
# Code Generation Request

## Task Context
**Azure DevOps Task ID**: {VSTS_WORK_ITEM_ID}
**Task Title**: {Task Title from Work Item}

## Task Analysis Summary
{Complete Task Analysis Summary content from Discussion}

## Coding Constraints & Guidelines

### Project Environment
- **Language**: Python 
- **Architecture**: Clean Architecture (separate layers: Presentation, Business, Data)

### Code Quality Requirements
1. **Comments**: Use `#` for inline code explanations
2. **Boolean Checks**: MUST use `is False` or `== False` instead of `not`
3. **File Structure**: One class per file
4. **Async Methods**: All I/O operations must be async (use `async def` and `await`)
5. **Dependency Injection**: Use constructor injection; avoid direct instantiation inside classes
6. **Error Handling**: Log complete exceptions; use targeted except blocks
7. **String Handling**: Use f-strings for dynamic strings
8. **Type Hints**: Always include type hints for function parameters and return values
9. **Docstrings**: Use triple-quoted docstrings for functions and classes

### Testing
- ⚠️ **Do NOT generate or include any unit tests in this code generation**
- Unit tests will be generated separately using `task-to-code-unit-tests-generation` prompt

### Expected Output
- Generate all files specified in "Affected File Paths"
- Follow the exact structure defined in Task Analysis Summary
- Include necessary import statements
- Add docstrings (using triple quotes `"""`) for public functions and classes
- Add inline comments (`#`) for complex logic blocks

## Additional Instructions
- Create new files with complete implementation
- Modify existing files only where specified
- Preserve existing code structure where not explicitly changed
- Follow naming conventions: snake_case for functions/variables, PascalCase for classes
- Follow PEP 8 code style guide


```

* Display the formatted prompt to the user for review.
* **If you have any questions, ask the user to confirm before proceeding.**

---

## Step 3 — Trigger GitHub Copilot Coding Agent via MCP

* ⚠️ **Note**: This step uses MCP Tool `github-pull-request_copilot-coding-agent` to invoke the Coding Agent in GitHub cloud.

* Confirm with user before triggering:
  ```markdown
  ## 🚀 Ready to Trigger GitHub Copilot Coding Agent
  
  ### What will happen:
  1. MCP Tool will invoke GitHub Copilot Coding Agent via `github-pull-request_copilot-coding-agent`
  2. Coding Agent will execute in GitHub cloud
  3. A new branch will be automatically created
  4. Code will be generated based on Task Analysis Summary
  5. Generated code will be automatically committed
  6. A Pull Request will be created for review
  
  ### Estimated Cost:
  - Cloud execution time: ~2-5 minutes
  - Tokens used: ~{estimated based on summary size}
  
  ### After code generation:
  1. Review the generated code in the Pull Request
  2. Run local tests if needed
  3. Execute `task-to-code-unit-tests-generation` for unit tests
  4. Execute `task-to-code-code-review` for AI code review
  
  Proceed with GitHub Copilot Coding Agent? (Y/N)
  ```

* If user confirms:
  - Call the MCP Tool `github-pull-request_copilot-coding-agent` with the following parameters:
    - `title`: "{VSTS_WORK_ITEM_ID} - {Task Title from Work Item}"
    - `body`: Formatted Coding Agent Prompt (from Step 2)
  - Monitor the agent's progress
  
* Display progress updates:
  ```markdown
  ⏳ GitHub Copilot Coding Agent is working...
  - MCP Tool invocation: ✅
  - Branch creation: ✅
  - Code generation: 🔄 In progress...
  - Commit: ⏳ Pending...
  - Pull Request: ⏳ Pending...
  ```

* **If you have any questions, ask the user to confirm before proceeding.**

---

## Step 4 — Monitor Code Generation Results

* Once Coding Agent completes, retrieve the results:
  - Branch name
  - Commit SHA
  - Pull Request URL
  - List of files created/modified
  - Any errors or warnings from Coding Agent

* Display results to user:
  ```markdown
  ## ✅ Code Generation Complete
  
  **Task ID**: {VSTS_WORK_ITEM_ID}
  **Branch**: {branch_name}
  **Commit**: {commit_sha}
  **Pull Request**: {pr_url}
  
  ### Files Generated:
  - ✅ {file1_path}
  - ✅ {file2_path}
  - ✅ {file3_path}
  
  ### Files Modified:
  - ✅ {file4_path}
  - ✅ {file5_path}
  
  ### Next Steps:
  1. Review the generated code in the Pull Request
  2. Check out the branch locally if needed: `git fetch && git checkout {branch_name}`
  3. Run `task-to-code-unit-tests-generation` to generate unit tests
  4. Run `task-to-code-code-review` for AI code review
  
  Note: The code has been automatically committed. Manual commit is not needed.
  ```

* **If you have any questions, ask the user to confirm before proceeding.**

---

## Step 5 — Add Work Item Discussion for Unit-Test Handoff

* First, **ask the user if they can provide comments specifically for the staged files**.

  * **If yes**: record all unit-test–related information in the Discussion based on the staged files.
  * **If no**: record the information based on the current prompt content instead.
* Use `add_work_item_comment` to post a new **Discussion** comment (not under `Task檢核結果`) that captures all information needed by a future **Unit Test Prompt** to generate tests.
* Title the comment like: **`[UTP-HANDOFF] Unit Test Inputs — {YYYY-MM-DD}`**.
* Include the following **generic fields**:

  * **Affected File Paths (final)**
  * **SUTs & Signatures** (class/module, method/function names, signatures, visibility)
  * **Collaborators to Mock** (interfaces/classes, key methods, expected calls)
  * **Business Rules & Triggers** (conditions, flags, feature variants)
  * **Observable Outcomes** (return values, state changes, interactions, logs)
  * **Negative/Non-Goals**
  * **Edge/Error Cases**
  * **Test Data Matrix** (variants and conditions)
  * **Test Project Info** (project path, framework, NuGet packages)
  * **Coding Constraints** (nullable, analyzers, conventions)
* After posting, **confirm with the user** that the handoff is complete and accurate before the Unit Test Prompt consumes it.
* ⚠️ **Do not generate or execute any unit tests in this step.**
* When later **reading Discussion**, tools/prompts must continue to **ignore any content under `Task檢核結果`**.

**Generic template to paste in Discussion:**

```
[UTP-HANDOFF] Unit Test Inputs — {YYYY-MM-DD}

Affected File Paths:
- {relative/path/to/file1}
- {relative/path/to/file2}

SUTs & Signatures:
- {module}.{class_or_function}( {param_type1} param1, ... ) -> {return_type}
- Visibility: {public/internal/private}

Collaborators to Mock:
- {IMockInterface}.method({args}) — expected calls: {once/twice/never}

Business Rules & Triggers:
- Apply when: {conditions/flags}
- Variants: {modes/account types/feature flags}

Observable Outcomes:
- Returns: {expected}
- State: {flags/DTO fields}
- Interactions: {which collaborator with which args}
- Logs: {message IDs/patterns}

Negative/Non-Goals:
- Do not {behavior} when {condition}

Edge/Error Cases:
- {missing id/None/boundary} → {exception/fallback}

Test Data Matrix:
- ({variant1}, {conditionA}=True)
- ({variant2}, {conditionA}=False)

Test Project Info:
- Path: {TEST_PROJECT_PATH}
- Python Version/Packages: Python 3.8+; pytest; unittest.mock; pytest-asyncio

Coding Constraints:
- Type Hints: required; PEP 8: strict; Async: {enabled/disabled}
```

---

### Execution Rules

* **Execute one step at a time. Do not start the next step until the previous step is fully confirmed by the user.**
* ⚠️ **This prompt does NOT generate code directly. It delegates to GitHub Copilot Coding Agent.**
* ⚠️ **Please do not generate or execute any unit tests in this prompt.**
* The Coding Agent handles code generation and automatic commit.
* Always confirm with user before triggering expensive cloud operations.

---

