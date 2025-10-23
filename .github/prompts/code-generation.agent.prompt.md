---
mode : 'agent'
tools : ['azure_devops_work_item', 'get_work_item_details']
---
# 任務內容如下，請依序完成
1. 使用 MCP Tool 中 azure_devops_work_item 或是 get_work_item_details 取得 User Story 需求內容 (Description 區塊)
2. 依照取得的需求內容，規劃並整理出預計執行的方法
3. 針對規劃出的做法，再次對照 User Story 的需求內容，確認有符合需求
4. **** 將需要新增/修改的檔案表列提供給使用者確認 ****
    - 絕對不可跳過這一步驟！
5. 依照確認後的方法，完成實作程式碼
    - 有新增注入或使用到 Service、Repository 或 Model/Entity，記得新增 using 的 namespace!
6. 執行 MSBuild 確認能 build 成功    
7. 執行 dotnet test 確認單元測試成功
8. 執行以下指令將異動 staged
    - `git add -A`
9. 執行以下指令取得 git staged 內的異動，並寫入檔案
    - `git diff --staged > .\.tmp\diff_content.txt`
10. 確認上一步執行完成後，執行以下指令以將 git diff 的內容提供給 Dify 進行 code review
    - `powershell -ExecutionPolicy Bypass -File ".\ps\dify_code_review_request.ps1"`
11. 確認上一步執行完成後，讀取 `.\.tmp\response_debug.json` 內容中的 answer 呈現給使用者
12. 依照 Dify 的 code review 結果，將需要修改的部分進行修改
13. 確認修改完成後，執行以下指令將異動 staged
    - `git add -A`
14. 進行 git commit，commit message title 為 `VSTS[需求編號] - feat: [需求名稱]`
