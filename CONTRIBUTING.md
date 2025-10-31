# 贡献指南

感谢你对预制件模板项目的关注！本文档将指导你如何贡献代码。

## 开始之前

在开始贡献之前，请确保：

1. ✅ 阅读了 [README.md](README.md) 了解项目概况
2. ✅ 熟悉 Python 3.11+ 的基本语法
3. ✅ 了解 Git 的基本操作

## 开发环境设置

### 1. Fork 并克隆仓库

```bash
# Fork 此仓库到你的账号
# 然后克隆你的 fork
git clone https://github.com/YOUR-USERNAME/prefab-template.git
cd prefab-template
```

### 2. 安装 uv（如果尚未安装）

```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. 同步依赖

```bash
# uv 会自动创建虚拟环境并安装依赖
uv sync --dev
```

## 开发工作流

### 创建功能分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 编写代码

1. **修改 `src/main.py`**: 添加或修改函数
2. **更新 `prefab-manifest.json`**: 同步函数签名
3. **编写测试**: 在 `tests/test_main.py` 中添加测试用例
4. **更新文档**: 如有必要，更新 README.md

### 代码规范

#### Python 代码风格

遵循 PEP 8 规范：

```python
# ✅ 好的示例
def calculate_total(items: list, tax_rate: float = 0.1) -> dict:
    """
    计算订单总金额

    Args:
        items: 商品列表
        tax_rate: 税率（默认 10%）

    Returns:
        包含总金额的字典
    """
    subtotal = sum(item['price'] for item in items)
    tax = subtotal * tax_rate

    return {
        "success": True,
        "subtotal": subtotal,
        "tax": tax,
        "total": subtotal + tax
    }

# ❌ 不好的示例
def calc(i,t=0.1):  # 无类型提示，变量名不清晰
    s=sum([x['price'] for x in i])  # 无空格
    return {"total":s*(1+t)}  # 无文档字符串
```

#### 函数设计原则

1. **单一职责**: 一个函数只做一件事
2. **清晰命名**: 使用动词+名词的形式（如 `analyze_dataset`, `process_data`）
3. **类型提示**: 所有参数和返回值都应有类型提示
4. **文档字符串**: 使用 Google 风格的 Docstring
5. **返回结构化数据**: 优先返回字典，包含 `success` 字段

#### Manifest 规范

```json
{
  "name": "function_name",
  "description": "清晰简洁的功能描述（一句话）",
  "parameters": [
    {
      "name": "param_name",
      "type": "str|int|float|bool|list|dict",
      "description": "参数的详细说明",
      "required": true
    }
  ],
  "returns": {
    "type": "dict",
    "description": "返回值的结构说明，包括所有字段"
  }
}
```

### 运行测试

在提交代码前，**必须**确保所有测试通过：

```bash
# 运行单元测试
uv run pytest tests/ -v

# 代码风格检查
uv run flake8 src/ --max-line-length=120

# 验证 Manifest
uv run python scripts/validate_manifest.py
```

### 提交代码

#### Commit 消息规范

使用语义化的 commit 消息：

```bash
# 功能新增
git commit -m "feat: 添加用户认证功能"

# Bug 修复
git commit -m "fix: 修复计算错误的问题"

# 文档更新
git commit -m "docs: 更新 README 使用说明"

# 测试相关
git commit -m "test: 添加边界情况测试"

# 构建/CI
git commit -m "ci: 优化 GitHub Actions 流程"
```

**格式**: `<type>: <description>`

**Type 类型**:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `test`: 测试相关
- `refactor`: 代码重构
- `style`: 代码格式（不影响功能）
- `ci`: CI/CD 相关
- `chore`: 其他杂项

### 推送并创建 Pull Request

```bash
# 推送到你的 fork
git push origin feature/your-feature-name

# 在 GitHub 上创建 Pull Request
# 选择 base: main ← compare: your-branch
```

#### PR 描述模板

```markdown
## 变更说明

简要描述此 PR 的目的和改动内容。

## 变更类型

- [ ] 新功能 (feat)
- [ ] Bug 修复 (fix)
- [ ] 文档更新 (docs)
- [ ] 代码重构 (refactor)
- [ ] 测试改进 (test)
- [ ] CI/CD 优化 (ci)

## 测试检查清单

- [ ] 单元测试已通过 (`uv run pytest tests/ -v`)
- [ ] 代码风格检查通过 (`uv run flake8 src/`)
- [ ] Manifest 验证通过 (`uv run python scripts/validate_manifest.py`)
- [ ] 已添加新的测试用例（如适用）

## 相关 Issue

关联的 Issue: #issue_number（如有）

## 截图（如适用）

如果是 UI 相关变更，请提供截图。
```

## 代码审查

### 审查标准

提交的代码将根据以下标准进行审查：

1. ✅ **功能正确性**: 代码按预期工作
2. ✅ **测试覆盖**: 关键逻辑有测试覆盖
3. ✅ **代码质量**: 遵循代码规范，逻辑清晰
4. ✅ **文档完整**: 有适当的注释和文档
5. ✅ **向后兼容**: 不破坏现有功能（除非是 breaking change）

### 反馈处理

1. 认真阅读审查意见
2. 及时回复和讨论
3. 根据反馈修改代码
4. 再次请求审查

## 发布新版本

只有维护者可以发布新版本。发布流程：

1. 更新 `prefab-manifest.json` 中的版本号
2. 更新 README.md 中的版本相关信息（如有）
3. 创建 Git Tag: `git tag v1.x.x`
4. 推送 Tag: `git push origin v1.x.x`
5. GitHub Actions 自动构建和发布

## 报告问题

如果你发现 Bug 或有功能建议：

1. 先搜索 [Issues](https://github.com/your-org/prefab-template/issues) 确认是否已存在
2. 如果不存在，创建新 Issue
3. 使用清晰的标题和详细的描述
4. 如果是 Bug，提供复现步骤和环境信息

### Bug 报告模板

```markdown
## Bug 描述

清晰简洁地描述 Bug。

## 复现步骤

1. 执行 '...'
2. 调用 '...'
3. 看到错误 '...'

## 预期行为

描述你期望发生什么。

## 实际行为

描述实际发生了什么。

## 环境信息

- Python 版本: [e.g. 3.11.5]
- 操作系统: [e.g. Ubuntu 22.04]
- 预制件版本: [e.g. 1.0.0]

## 额外信息

其他相关的日志、截图等。
```

## 获得帮助

如果你需要帮助：

- 📖 查阅 [README.md](README.md) 和此文档
- 💬 在 [Discussions](https://github.com/your-org/prefab-template/discussions) 提问
- 🐛 如果是 Bug，创建 [Issue](https://github.com/your-org/prefab-template/issues)

## 行为准则

参与此项目即表示你同意遵守我们的行为准则：

- 尊重所有贡献者
- 接受建设性批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

## 致谢

感谢所有为此项目做出贡献的开发者！你的努力让预制件生态系统更加强大。

---

**Happy Coding! 🚀**
