# Code Implementation Quality Checklist

> **Purpose**: Validate that generated code meets all Task Description requirements
> **Usage**: Apply after code generation from task-to-code-code-generation.prompt.md

## Checklist Items

### Section 1: 背景與範圍 (Context & Scope)
- [ ] **Code matches described context** - Implementation aligns with stated purpose
- [ ] **Scope boundaries respected** - Only implements what's in scope, nothing out of scope
- [ ] **Correct modules/systems modified** - Changes are in the specified components

### Section 2: 目標與非目標 (Goals & Non-Goals)
- [ ] **All goals implemented exactly** - Each listed goal has corresponding code, no more, no less
- [ ] **No additional implementations beyond goals** - Code implements ONLY what's specified in goals
- [ ] **Non-goals strictly avoided** - Code doesn't implement what's explicitly excluded
- [ ] **Scope creep prevented** - No extra features or enhancements beyond requirements
- [ ] **Measurable objectives met precisely** - Implementation satisfies success criteria exactly as specified

### Section 3: 工作摘要 (Work Summary)
- [ ] **Main deliverables created** - Core classes/methods as described exist
- [ ] **Implementation approach followed** - Code structure matches summary
- [ ] **All specified components present** - Nothing described is missing

### Section 4: 設計考量與權衡 (Design Considerations & Trade-offs)
- [ ] **Design patterns applied** - Specified patterns correctly implemented
- [ ] **Trade-offs correctly handled** - Design decisions reflected in code
- [ ] **Technical constraints respected** - Limitations properly addressed
- [ ] **Architecture guidelines followed** - Code aligns with design considerations

### Section 5: 關鍵實作重點 (Key Implementation Logic)
- [ ] **All key points implemented exactly** - Each bullet point has corresponding code, verified one-by-one
- [ ] **No extra implementations beyond key points** - Code contains ONLY specified logic, nothing additional
- [ ] **Logic correctly translated** - Business rules accurately coded without additions
- [ ] **Data structures match specification exactly** - Classes/interfaces as described, no extra properties/methods
- [ ] **Validation logic present as specified** - Input validation and error handling implemented per requirements only
- [ ] **Implementation boundaries respected** - Code stays within defined implementation scope

### Section 6: 單元測試計畫 (Unit Test Plan)
- [ ] **Test scenarios covered** - Unit tests exist for each planned scenario
- [ ] **Edge cases tested** - Boundary conditions have test coverage
- [ ] **Validation tests present** - Data validation logic is tested
- [ ] **Mock objects properly used** - Dependencies correctly mocked

### Section 7: 影響的檔案路徑 (Affected File Paths)
- [ ] **All specified files created/modified** - File list matches Task Description
- [ ] **File paths correct** - Files in exact specified locations
- [ ] **No unexpected files** - Only authorized files changed
- [ ] **File naming consistent** - Names match specification exactly

### Section 8: 跨領域考量 (Cross-cutting Concerns)
- [ ] **Security measures implemented** - Sensitive data protection, validation
- [ ] **Performance optimized** - Efficient algorithms, no unnecessary overhead
- [ ] **Maintainability ensured** - Clear code structure, proper documentation
- [ ] **Scalability considered** - Design supports future growth as specified

## Validation Rules
- Code must implement ALL required functionality **EXACTLY AS SPECIFIED**
- Code must NOT implement anything beyond requirements (no scope creep)
- No placeholder or TODO comments in critical logic
- All specified classes and methods must exist and be functional
- Unit tests must pass and provide adequate coverage
- **CRITICAL**: Each implementation item must be verified against Task Description line-by-line
- **CRITICAL**: Any extra implementations beyond requirements result in FAIL for that section