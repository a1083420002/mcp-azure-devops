---
mode: 'agent'
---

# Prompt: Azure DevOps Work Item → Unit Test Generation (Task type = code)

> **Use case**: You are assisting with an Azure DevOps (VSTS) **Task**.
> ⚠️ **Scope restriction**: This prompt only applies when the **Work Item type is `Task` and Task type = `code`**.
> Your responsibility is to **generate and validate unit tests** based on the information handed off in the work item Discussion.
> **Frameworks**: C#, **xUnit**, **NSubstitute**, **FluentAssertions**.
> **Important**: Do not modify production code. Do not generate commits. Focus only on test code.

---

## Step 1: Retrieve Work Item Discussion Content

### Input: Work Item ID **or** Service/Method Specification
- **Option A - Work Item ID**: Fetch the **Discussion** entries for the specified `{VSTS_WORK_ITEM_ID}` using Azure DevOps integration/MCP tool
- Look specifically for comments titled: `[UTP-HANDOFF] Unit Test Inputs — {YYYY-MM-DD}` (if using Work Item ID)
- **Ignore** any content under `Task檢核結果`
- **Option B - Service/Method**: Accept user-specified Service or Method name to define test scope directly
- Verify information completeness

### Decision Point:
- **If handoff information exists**: Proceed to **Step 2.1**
- **If no handoff information or using Service/Method specification**: Proceed to **Step 2.2**

**If you have any questions, ask the user before proceeding.**

---

## Step 2: Parse and Confirm Unit Test Inputs

### 2.1: 提取測試相關的結構化資訊 (Extract Structured Test Information)
Extract and confirm the following fields from the `[UTP-HANDOFF]` section:
- **受影響檔案路徑** (Affected File Paths)
- **測試目標與簽章** (SUTs & Signatures) 
- **需模擬的協作物件** (Collaborators to Mock)
- **業務規則與觸發條件** (Business Rules & Triggers)
- **可觀察的結果** (Observable Outcomes)
- **負向測試/非目標** (Negative/Non-Goals)
- **邊界/錯誤案例** (Edge/Error Cases)
- **測試資料矩陣** (Test Data Matrix)
- **測試專案資訊** (Test Project Info)
- **程式碼約束條件** (Coding Constraints)

### 2.2: List Related Test Scenarios (from user specification)
Based on user-specified Service or Method:
- Analyze the target component's responsibilities
- Identify key business logic and edge cases
- Define mock dependencies and expected outcomes
- Establish test data variations

### Information Confirmation
- Include: affected files, test targets, mock objects, business rules, etc.
- Verify information completeness and request user confirmation
- If any field is unclear or missing, list targeted clarification questions

**If you have any questions, ask the user before proceeding.**

---

## Step 3: Plan Test Suite Architecture
- Map each **SUT** to 1 test class (e.g., `PaymentMiddlewareServiceTests`)
- List test methods to cover **rules**, **triggers**, **edge/error cases**, and **data variants**
- Define mock strategies (**NSubstitute**) and expected **assertions** (**FluentAssertions**)
- Exclude anything in **Negative/Non-Goals**
- Present the plan as a checklist and get user acknowledgment

**If you have any questions, ask the user before proceeding.**

---

## Step 4: Generate C# Test Code
Produce compile-ready xUnit code:
- **One file per SUT** test class
- Use **AAA pattern** (Arrange-Act-Assert); keep arrange blocks explicit
- Create **helpers/builders** as needed for data setup
- Respect **Coding Constraints** and project **namespaces**
- Output as **.cs snippets** only (no execution, no commits)

**Framework Requirements:**
- Using statements for xUnit, NSubstitute, FluentAssertions
- Correct namespace alignment
- `public class {SUT}Tests`
- `[Fact]` / `[Theory]` with `[InlineData]` where applicable
- Constructor-injected substitutes; avoid static/global state
- Expressive FluentAssertions with clear failure messages

**If you have any questions, ask the user before proceeding.**

---

## Step 5: Review With User and Adjust
- Show the generated test files
- Ask whether to add more **variants**/**error cases**, adjust **mock behaviors**, or tweak **naming/structure**
- Apply requested updates
- Confirm final test code quality

**If you have any questions, ask the user before proceeding.**

---

## Step 6: VS Code Test Task Execution

### 6.1: Create New VS Code Task Configuration ⚠️ **MANDATORY - DO NOT SKIP**
- Open `.vscode/tasks.json`
- Create a new task using the existing pattern structure:
  ```json
  {
    "label": "Test {YourTestClassName} Only",
    "type": "shell", 
    "command": "{same xunit.console.exe path}",
    "args": [
      "{test dll path}",
      "-class", 
      "{Namespace.TestClassName}",
      "-parallel", 
      "none",
      "-html", 
      "{TestResult-YourTestClassName}.html"
    ],
    "dependsOn": "{appropriate build task}",
    "problemMatcher": []
  }
  ```
- Replace all placeholders with actual values
- Save the modified tasks.json

### 6.2: Build Test Project
- Execute the build task that your new task depends on
- Ensure compilation succeeds before proceeding
- Fix any compilation errors in test code if needed

### 6.3: Execute VS Code Task
- Open VS Code Command Palette (`Ctrl+Shift+P`)
- Run: `Tasks: Run Task`
- Select: `"Test {YourTestClassName} Only"`
- Monitor terminal output for task initiation
- **⚠️ IMPORTANT**: Before proceeding to Step 6.4, **re-check terminal execution status**:
  - Verify the task has completed (look for completion messages)
  - Confirm no processes are still running
  - Check for any error messages or warnings
  - Ensure the HTML report file has been generated
- Note the HTML report path from output
- **Do not proceed to Step 6.4 until terminal execution is fully complete**

### 6.4: Analyze Test Results Report
- Open the generated HTML report: `{TestResult-YourTestClassName}.html`
- Extract from the report:
  - Total tests count
  - Passed/Failed/Skipped counts
  - For each failed test: method name, failure reason, stack trace, expected vs actual values

### 6.5: Propose Fixes and Confirm with User
Present structured fix proposals:
```
Test Execution Summary:
- Total: X tests
- Passed: Y tests  
- Failed: Z tests

Failed Tests Analysis:
1. Test: {TestMethodName}
   Error: {Error message}
   Root Cause: {Analysis}
   Proposed Fix: {Specific code change}

Ready to apply these fixes? Please confirm (Y/N):
```
**Wait for user confirmation before proceeding.**

### 6.6: Apply Fixes and Re-execute Task ⚠️ **MUST USE VS CODE TASK**
- Upon user confirmation, apply all approved fixes to test code
- Save all modified files
- **Re-run the VS Code task**: `"Test {YourTestClassName} Only"` (**NOT** manual commands)
- Check the new HTML report
- **If tests still fail**: Return to 6.4 for another analysis cycle (maximum 3 cycles)
- **If all tests pass**: Confirm "All tests passed successfully"
- **After 3rd attempt**: Escalate remaining issues to user

**If you have any questions, ask the user before proceeding.**

---

## Execution Discipline
- Execute **one step at a time**. Only when a step is complete, continue to the next
- Every step: **If you have any questions, ask the user before proceeding**
- Keep explanations concise; prioritize correctness and completeness of artifacts
- **Step 6.1 is mandatory** - never skip VS Code task creation
- **Step 6.6 must use VS Code task configuration** - not manual test execution

