
---

### 文件二：`CONTRIBUTING.md` (项目根目录下)

```markdown
# 🤝 贡献指南 (Contributing Guide)

感谢你感兴趣并愿意为这个图书管理系统贡献代码！为了让协作更顺畅，请遵循以下规范：

## 一、报告 Bug 或提出建议
- 如果你发现了 Bug，或者有好的新功能想法，请先去 GitHub 的 **Issues** 页面搜索一下，看看是否已经有人提过。
- 如果没有重复，请**新建一个 Issue**，尽量清晰地描述你的问题（包括复现步骤、截图、错误日志等）。

## 二、贡献代码流程 (Pull Request)

### 1. 分支管理策略
本项目采用标准的 **GitHub Flow** 模式：
- **`main` 分支**：主分支，始终保证代码是稳定可运行的。
- **开发分支**：新建功能分支或修复分支，命名规范为 `feature/功能描述` 或 `fix/修复内容`。

### 2. 操作步骤 (从 Fork 到 PR)
1. **Fork** 本项目到你自己的 GitHub 账号下。
2. **Clone** 你的 Fork 到本地：`git clone https://github.com/你的用户名/library-system.git`
3. 创建新分支：`git checkout -b feature/你的功能名称`
4. 在新分支上完成你的代码修改，并进行充分的自测。
5. **保持同步**：如果原仓库 `main` 分支在此期间有更新，请先同步合并到你的分支，避免冲突。

### 3. 代码风格规范
- **后端 (Python)**：
  - 遵循 **PEP8** 规范。
  - 变量和方法命名使用 `snake_case` (例如 `book_name`)。
  - 修改 `models.py` 后，**必须同步更新** `schema.sql` 中的建表语句。
- **前端 (Vue)**：
  - 组件文件名使用大驼峰 `PascalCase` (如 `BookList.vue`)。
  - 开发完成后，请先运行 `npm run lint` 检查 ESLint 规范。

### 4. Git 提交信息规范
提交代码时，请使用清晰的 Commit Message：

**格式：** `<类型>: <简短描述>`

- `feat`: 增加新功能 (Feature)
- `fix`: 修复 Bug
- `docs`: 修改文档 (Documentation)
- `style`: 代码格式化（不改变功能逻辑）
- `refactor`: 代码重构 (既不是新增功能，也不是修 Bug)
- `test`: 增加或修改测试用例

**例子：**
- `feat: 新增按分类筛选图书功能`
- `fix: 修复还书接口库存数量未正确增加的问题`
- `docs: 更新 README 中的数据库配置说明`

### 5. 提交 Pull Request (PR)
1. 将你的分支推送到 GitHub：`git push origin feature/你的功能名称`
2. 在你的 GitHub 仓库页面，点击 **"Compare & pull request"**。
3. **目标分支**请务必选择本项目的 `main` 分支。
4. 在 PR 描述中详细说明你的改动（建议附上测试截图或 Postman 返回结果图）。
5. 提交 PR 后，等待维护者进行 Code Review 和合并。

## ⚠️ 注意事项
- **不要**直接向 `main` 分支 push 代码。
- 如果你在开发中新增了依赖包（比如 `pip install xxx` 或 `npm install xxx`），**请务必更新** `requirements.txt` 或 `frontend/package.json` 文件。
