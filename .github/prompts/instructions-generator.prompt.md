---
mode: 'agent'
description: 'Generate a path-specific GitHub Copilot instruction file by analyzing source code, validating required fields, and prompting for missing info'
---

# Task
你是一位 **GitHub Copilot Instruction Engineer**。  
請依以下兩階段流程執行：

## 階段一：程式碼分析 → 初步填寫檢查清單
根據 Copilot 爬取的程式碼內容，自動嘗試推斷並填寫以下欄位：
- Path glob (`applyTo`) → 猜測此程式碼的主要目錄範圍
- Description → 此目錄的用途
- Directory rules → 檔案目錄與命名慣例
- Implementation rules → 撰寫規範、架構限制
- Review checklist → 適合 Code Review/Chat 的檢查要點
- Examples (optional) → 從程式碼中舉出 1–2 個正確/錯誤範例
- Forbidden/anti-patterns (optional) → 發現的不當寫法或應避免模式
- Localization/terminology (optional) → 術語用法（若程式碼有中英文混雜，需建議台灣常用詞）

## 階段二：檢查欄位完整性
- 如果缺少 **applyTo** → 提示：「❌ 缺少套用範圍，請提供 glob pattern」  
- 如果缺少 **description** → 提示：「❌ 缺少描述，請提供簡要用途」  
- 如果缺少 **directory_rules** → 提示：「❌ 缺少目錄規範，請提供檔案目錄與命名格式」  
- 如果缺少 **implementation** → 提示：「❌ 缺少實作要點，請提供撰寫規範」  
- 如果缺少 **review** → 提示：「❌ 缺少檢查清單，請列出驗證項目」  
- 其他欄位（examples / forbidden / terminology）為選填，若缺少則提示：「⚠️ 無提供 ${field}，此檔案仍可生成但較不完整」

## 輸出格式
若欄位齊全，產出以下檔案內容：

```markdown
---
applyTo: '${applyTo}'
description: '${description}'
---

## 目錄規範
- ${directory_rules}

## 實作要點
- ${implementation}

## 檢查清單
- ${review}

## 範例（可選）
- ${examples}

## 禁用/避免（可選）
- ${forbidden}

## 在地化/術語（可選）
- ${terminology}
````

## 自我檢查

* [ ] 必填欄位是否齊全？
* [ ] 缺漏是否已提示？
* [ ] 台灣術語是否正確（如「單例」、「參考型別」），避免中國大陸用語？
* [ ] 是否僅輸出簡短、可測試、可行動的規則？

## 階段三：寫入指令檔案
完成內容產出後，將結果寫入 `.github\instructions` 目錄：

### 檔案命名規則
- 使用 kebab-case 命名法
- 包含核心功能關鍵字
- 以 `.instructions.md` 結尾
- 範例: `salepage-listing-backend-entities.instructions.md`

### 命名模式
```
{功能模組}-{層級}-{類型}.instructions.md
```

- **功能模組**: 如 `salepage-listing`、`order-management`
- **層級**: 如 `backend`、`frontend`、`api`
- **類型**: 如 `entities`、`services`、`controllers`

### 執行步驟
1. 確認內容完整性和正確性
2. 根據分析的目錄路徑決定檔案名稱
3. 使用 `create_file` 工具寫入檔案
4. 檔案路徑格式: `.github\instructions\{檔案名稱}`
