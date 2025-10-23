---
mode: 'agent'
---

# Prompt: Comprehensive Code Validation with Dual Review System

> **Use case**: Validate staged code changes against Task Description using checklist and Dify review
> **Execution**: Run after code generation completion
> **Critical**: Execute each step sequentially. Complete each step before proceeding to the next.

---

## Step 1 — Load materials, perform checklist validation and present report

* Capture staged changes directly without temporary files:
  - Use `get_changed_files` tool with `["staged"]` parameter to get all staged files (focus only on .cs files)
  - Use `read_file` tool to read the complete content of each staged .cs file
  - Skip all non-`.cs` files (e.g., .json, .config, .csproj, etc.)
  - Compare with unstaged version using git commands if needed for diff analysis
* Load validation materials:
  - Retrieve Task Description from Azure DevOps or user
  - Load checklist from `.github\checklists\code-implementation-checklist.md`
* Apply checklist validation to the staged code changes
* **CRITICAL**: For each checklist section in `code-implementation-checklist.md`:
  - **Line-by-line verification**: Compare implementation against Task Description requirements
  - **Exact match validation**: Ensure code implements ONLY what's specified, nothing extra
  - **Scope creep detection**: Flag any implementations beyond stated requirements
  - Mark as: [✅] PASS, [⚠️] PARTIAL, [❌] FAIL, or [N/A] Not Applicable
  - Document evidence with specific diff line references
  - **For Goals & Key Implementation**: List each requirement and verify one-by-one
* Present focused validation report directly to user:
  ```markdown
  ## Code Implementation Validation Report
  
  Date: [Current Date]
  Files Reviewed: [Count]
  
  ### Part 1: Checklist Findings

  #### Critical Issues from Checklist:
  1. [Issue description] - File:Line
  2. [Issue description] - File:Line
  
  #### Scope Creep Issues (Extra Implementations):
  1. [Extra implementation description] - File:Line - Not required in Task Description
  2. [Extra implementation description] - File:Line - Not required in Task Description
  ```
* Display full compliance analysis in console for user reference

## Step 2 — Execute Dify code review

* Execute Dify review script:
  ```powershell
  powershell -ExecutionPolicy Bypass -File ".github\ps\dify_code_review_request.ps1"
  ```
* Wait for Dify API response completion
* Read response from console output
* Parse and prepare Dify findings for presentation

## Step 3 — Consolidate findings and display final review results

* Merge findings from checklist validation and Dify review
* Remove duplicate issues between sources
* Group similar issues together by type and severity
* Categorize by priority: Priority 1 (Blockers), Priority 2 (Critical), Priority 3 (Minor)
* Present comprehensive consolidated review results to user:
  ```markdown
  ### Part 2: Dify Code Review Results
  [Parse and format Dify findings]
  
  *Note: Dify reviewer primarily focuses on syntax and coding standards but may not identify business logic issues found in checklist validation*
  
  ### Part 3: Consolidated Recommendations
  
  #### Priority 1 - Blockers (Must Fix):
  Source: [Checklist/Dify]
  - Issue: [Description]
  - Location: [File:Line]
  - Suggested Fix: [Code example]
  
  #### Priority 2 - Critical (Should Fix):
  [Items that should be fixed before testing]
  
  #### Priority 3 - Minor (Nice to Have):
  [Improvements that can be deferred]
  ```
* **DO NOT modify code directly without explicit user approval**

## Step 4 — Display issues and provide code fix options

* Display all identified issues organized by priority with numbered options for selection:
  ```markdown
  ### 發現的程式碼問題清單 (依優先級排序)
  
  #### Priority 1 - Blockers (Must Fix):
  
  1. [Issue Title]
     - **Source**: [Checklist/Dify]
     - **Location**: [File:Line]
     - **Description**: [Detailed issue description]
     - **Suggested Fix**: [Brief fix description]
  
  2. [Issue Title]
     - **Source**: [Checklist/Dify]
     - **Location**: [File:Line]
     - **Description**: [Detailed issue description]
     - **Suggested Fix**: [Brief fix description]
  
  #### Priority 2 - Critical (Should Fix):
  
  3. [Issue Title]
     - **Source**: [Checklist/Dify]
     - **Location**: [File:Line]
     - **Description**: [Detailed issue description]
     - **Suggested Fix**: [Brief fix description]
  
  4. [Issue Title]
     - **Source**: [Checklist/Dify]
     - **Location**: [File:Line]
     - **Description**: [Detailed issue description]
     - **Suggested Fix**: [Brief fix description]
  
  #### Priority 3 - Minor (Nice to Have):
  
  5. [Issue Title]
     - **Source**: [Checklist/Dify]
     - **Location**: [File:Line]
     - **Description**: [Detailed issue description]
     - **Suggested Fix**: [Brief fix description]
  
  [... continue numbering sequentially for all issues]
  ```

* Ask user to select which issues to fix: 
  ```
  請選擇要修復的問題項目：
  
  選項：
  - 輸入特定編號 (例如：1,3,5 或 1-5 或 1,3-7,9)
  - 輸入 'all' 修復全部問題
  - 輸入 'none' 不修復任何問題
  
  您的選擇：
  ```

* Based on user selection:
  - Parse the user's input to determine which issues to fix
  - For selected issues, automatically apply the code fixes using appropriate file editing tools
  - Display progress for each fix being applied:
    ```markdown
    正在修復問題 [編號]: [Issue Title]
    - 修改檔案: [File Path]
    - 套用修復: [Fix Description]
    ✅ 修復完成
    ```
  - After all selected fixes are applied, display summary:
    ```markdown
    ### 修復摘要
    - 總計修復問題數: [Count]
    - 修改檔案數: [Count] 
    - Priority 1 修復數: [Count]
    - Priority 2 修復數: [Count]
    - Priority 3 修復數: [Count]
    
    建議接下來執行程式碼檢核以確認修復結果。
    ```

---

### Configuration
* **Checklist Path**: `.github\checklists\code-implementation-checklist.md`
* **Dify Script**: `.github\ps\dify_code_review_request.ps1`

### Prerequisites
1. Git repository with staged changes
2. PowerShell execution policy allows script execution
3. Dify API endpoint accessible

### Execution Rules
* Execute each step sequentially - complete one before proceeding
* Never modify code without explicit user approval
* Preserve UTF-8 encoding for all file operations
* Display reports directly to user
