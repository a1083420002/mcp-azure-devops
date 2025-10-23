# 這是一個 .NET Framework 4.8 的專案，請協助我完成以下任務

# 任務內容如下，請依序完成
1. 使用 MCP Tool 中 azure_devops_work_item 或是 get_work_item_details 取得 User Story 需求內容 (Description 區塊)
2. 依照取得的需求內容，檢查現有的程式碼及 git 異動，比對出還沒完成實作的內容，規劃並整理出預計執行的方法
3. 針對規劃出的做法，再次對照 User Story 的需求內容，確認有符合需求
4. **** 將需要新增/修改的檔案表列提供給使用者確認 ****
    - 絕對不可跳過這一步驟！
5. 依照確認後的方法，完成實作程式碼
    - 有新增注入或使用到 Service、Repository 或 Model/Entity，記得新增 using 的 namespace!
6. 檢查目前的異動與確定好的規劃作法相符。若不相符，再繼續調整
7. 最後務必針對 Service 的方法補上單元測試
    - 單元測試的檔案名稱必須與 Service 的檔案名稱相同，並且放在 `WebStore\Frontend\BLV2.Tests\` 目錄下
    - 單元測試的命名規則為 {xxx}ServiceTests.cs，並且必須使用 NSubstitute 作為 mocking 套件
   
# 實作需求任務時必須遵守以下準則：
0. 必須參考 #file:../copilot-instructions.md 的內容了解相關規範
1. {xxx}Service.cs 檔案內的相關方法皆為商務邏輯，必須要有單元測試保護，單元測試並使用 NSubstitute 作為 mocking 套件
2. 一個 .cs 檔案只包含一個 class
3. 當使用或呼叫的方法不存在時，嘗試新增實作該方法
    - 例如：當你在 {xxx}Service.cs 裡面使用了 {xxx}Repository.cs 的方法，但 {xxx}Repository.cs 裡面沒有實作該方法，請你幫我新增該方法的實作
4. 沒有呼叫或使用到的方法，不要做任何修改或刪除
5. assign value 的時候必須確認 entity/object 存在該欄位
6. 這個專案不要使用 async 等非同步做法
7. 新增檔案後，請將該檔案加入所屬路徑對應專案的 .csproj 的 ItemGroup 區塊
    - 如果新增的是 {xxx}Service.cs 檔案，則須將路徑對應新增至 `NineYi.WebStore.Frontend.BLV2.csproj`
    - 如果新增的是 {xxx}Repository.cs 檔案，則須將路徑對應新增至最接近的 DA csproj
    - 如果新增的是 Model/Entity 檔案，則須將路徑對應新增至 `NineYi.WebStore.BE.csproj` 專案
8. 有使用新的 Service、Repository 或 Model/Entity，記得新增 using 的 namespace
9. terminal 相關指令不支援 "&&"，因此如果多個指令動作，請分行執行
10. 請不要修改與此無關的其他程式碼。請保持原有邏輯不變，只針對需要修改的地方進行調整。
11. 依賴注入優先透過建構子注入
12. 新建立的檔案請依照以下結構放置位置
    - API 的 entry point 放置於 NineYi.WebStore.WebAPI project，路徑在 `WebStore\WebAPI\`
    - 業務邏輯歸屬於 Business Layer 層，例如 {xxx}Service.cs，屬於 NineYi.WebStore.Frontend.BLV2 project，路徑在 `WebStore\Frontend\BLV2\`
    - 資料存取屬於 Data Access Layer，例如 {xxx}Repository.cs，依照對應的 DB 屬於對應的 project，路徑在 `WebStore\DA\`
    - 傳遞與 mapping 資料的實體，例如 request entity, response entity 或是 value object 等，放在 `WebStore\Frontend\BE\`
    - 不在上述列舉路徑的，請務必詢問使用者放置位置


!!!! 請依步驟一步一步開始執行 !!!!