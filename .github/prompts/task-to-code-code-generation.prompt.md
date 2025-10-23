---
agent: 'agent'
---

# Prompt: Azure DevOps Work Item → Code Generation (Task type = code)

> **Use case**: You are assisting with an Azure DevOps (VSTS) Task. Follow the steps below, interacting with the user whenever clarification is needed.
> **Note**: Execute strictly one step at a time. Do not proceed to the next step until the previous step is completed and confirmed.

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

## Step 2 — Implement according to the confirmed logic

* Reconfirm the final **implementation logic** and proceed to implement the code accordingly. Provide code snippets or patches, and include notes on configuration, migration steps (if any), and rollback strategy.
* ⚠️ **Important: Do NOT generate or execute any unit tests.**
* **If you have any questions, ask the user to confirm before proceeding.**

## Step 3 — Add Work Item Discussion for Unit-Test Handoff

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
- {TypeOrModule}.{Method}( {ParamType1} p1, ... ) : {ReturnType}
- Visibility: {public|internal|...}

Collaborators to Mock:
- {ICollaborator}.Method({Args}) — expected calls: {once/twice/never}

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
- {missing id/null/boundary} → {exception/fallback}

Test Data Matrix:
- ({variant1}, {conditionA}=true)
- ({variant2}, {conditionA}=false)

Test Project Info:
- Path: {TEST_PROJECT_PATH}
- TFMs/NuGets: net8.0; xunit/xunit.runner.visualstudio; FluentAssertions; NSubstitute

Coding Constraints:
- Nullable: {enable/disable}; Analyzers: {list}
```

## Step 4 — Generate Suggested Commit

* Generate a **suggested commit message** following the rules below:

  **Format:**

  ```
  VSTS{VSTS_WORK_ITEM_ID}- <type>[optional scope]: <description>
  ```

  **Rules:**

  1. Only include the title in the first line: `VSTS{VSTS_WORK_ITEM_ID}- <type>[optional scope]: <description>`
  2. If a description body is needed, separate it from the title with one blank line.
  3. The description body should provide detailed information.
  4. List sections in this order: Title, Modified files, Detailed description.
  5. Do not add punctuation at the end of the commit message.

  **Valid types:**

  * `fix`: bug fix (corresponds to PATCH in SemVer)
  * `feat`: new feature (corresponds to MINOR in SemVer)
  * `test`: add or update tests
  * `refactor`: code refactoring (not a new feature or bug fix)

  **Examples:**

  ```
  VSTS12345 - fix: resolve null pointer exception
  VSTS12346 - feat: add user authentication
  VSTS12347 - test: add tests for login
  VSTS12348 - refactor: simplify pipeline
  ```

* Confirm the generated commit message with the user before finalizing.

---

### Execution rule

* **Execute one step at a time. Do not start the next step until the previous step is fully confirmed by the user.**
* ⚠️ **Please do not generate or execute any unit tests.**

