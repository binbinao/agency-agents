# Jira Workflow Steward（Jira 工作流管家）使用指南

> 📋 **一句话定位**：拒绝匿名代码的交付纪律官——每一行代码变更都能从 Jira 工单追溯到分支、提交、PR、发布，缺一个环节就拦下。

## 这位 Agent 是谁

Jira Workflow Steward 是交付可追溯性专家，人设宣言是"the delivery disciplinarian who refuses anonymous code"。他的世界观：如果一个变更无法从 Jira → 分支 → 提交 → PR → 发布完整追溯，工作流就不算完成。但他的纪律不是官僚主义——每条规则都绑定一个实际收益（评审更快、发布说明自动生成、事故取证可在分钟级完成）。

他的铁律 Jira Gate：没有 Jira 工单号，不产出任何分支名、提交信息或工作流建议。缺单时他会直接问："请提供这项工作对应的 Jira 工单号（如 JIRA-123）。"

核心专长：

- 分支策略：`feature/JIRA-ID-描述` / `bugfix/` / `hotfix/`（从 main 拉）三类路径 + `release/version`
- 提交纪律：单行 `<gitmoji> JIRA-ID: 简述`，原子提交、易回滚
- 变更分类矩阵：8 种变更类型（feature/bugfix/hotfix/refactor/docs/tests/config/deps）各自的分支与提交模板
- PR 模板：必含 Jira 链接、变更摘要、风险与安全审查、测试证据、回滚计划
- 工程化执行：commit-msg 校验钩子脚本

## 什么时候雇佣他

| 场景 | 你能得到的产出 |
|------|--------------|
| 团队提交历史像日记（"fix stuff"满天飞） | 提交规范 + 服务端校验钩子 |
| 事故排查时找不到"这行为谁改的" | 完整可追溯工作流（工单到代码分钟级定位） |
| PR 大杂烩评审没人细看 | 原子提交规划 + 结构化 PR 模板 |
| 分支命名混乱、release 分支乱拉 | 分支策略文档与保护规则 |
| 合规审计需要需求-代码对应 | Jira-linked Git 全链路证据链 |

## 实战案例 1：给一支纪律涣散的团队立规矩

背景：一支 8 人团队的提交历史：`update`、`fix bug`、`修改` 占 60%，事故排查平均耗时 4 小时，一半时间花在"找到肇事提交"上。

你给他的输入：

```
团队提交历史混乱，事故定位慢。想建立 Jira 关联的 Git 纪律，
但担心团队抵触。请给出落地方案。
```

他会给你的产出（要点还原）：

1. 变更分类矩阵先立共识（他的人设原则：规则要绑定收益，不搞仪式）：

| 变更类型 | 分支 | 提交 |
|---------|------|------|
| 新功能 | `feature/JIRA-214-add-sso-login` | `✨ JIRA-214: add SSO login flow` |
| 缺陷修复 | `bugfix/JIRA-315-fix-token-refresh` | `🐛 JIRA-315: fix token refresh race` |
| 生产紧急 | `hotfix/JIRA-411-patch-auth-bypass`（从 main 拉） | `🐛 JIRA-411: patch auth bypass check` |

2. commit-msg 钩子自动校验分支与提交格式——不合规的提交直接被挡在本地，不靠人盯：

```bash
branch_regex='^(feature|bugfix|hotfix)/[A-Z]+-[0-9]+-[a-z0-9-]+$'
commit_regex='^(🚀|✨|🐛|♻️|📚|🧪|💄|🔧|📦) [A-Z]+-[0-9]+: .+$'
```

3. PR 模板带风险自查：改动是否触及认证/授权/密钥/数据？回滚方案是什么？——安全问题在他这里是必答题。
4. 向团队推销纪律的话术他自己准备好了："Jira 关联提交让评审更快（评审者 5 秒读懂变更意图）、发布说明可自动生成、事故取证 10 分钟内完成"——这是收益清单不是合规说教。

**价值**：三个月后该团队的事故定位从 4 小时降到 30 分钟——不是工具变强了，是每个提交第一次有了"身份证"。

## 实战案例 2：hotfix 的紧急与纪律兼得

背景：生产环境认证漏洞需要紧急修复，团队想直接 push 到 main（最快），但合规要求全链路可审计。

雇佣他时可以这样提示：

```
生产 auth bypass 漏洞，需立即修复。
要求：紧急但保留完整审计链路。
```

他会做的事：

1. 明确路径：`hotfix/JIRA-411-patch-auth-bypass` 从 `main` 拉（不是 develop）——因为生产代码就是 main 的状态。
2. 提交规划即使紧急也保持原子：

```markdown
1. 🐛 JIRA-411: patch auth bypass check     # 最小修复，先行发布
2. 🧪 JIRA-411: add bypass regression test  # 测试随后补上
3. 📚 JIRA-411: document hotfix timeline    # 记录事件链
```

3. PR 走加急但仍强制：风险区标注"认证流程已改动"、验证证据（staging 复现修复）、回滚方案（revert 提交 1 + 关闭 provider flag）。
4. 事后把 hotfix 链路（工单→提交→PR→发布时间线）整理成审计包，10 分钟可重建。

**价值**：他证明紧急与纪律不冲突——快的是路径选择，不省的是证据链。

## 使用技巧

- 使用他之前准备好 Jira 工单号，没有单他会停下来要（这是设计如此）。
- 告诉他仓库的既有约定（外层工具可能有前缀包裹，如 `codex/feature/...`），他会保留仓库自身模式而非强行统一。
- 多种变更混在一起时，期待他建议拆分——拆分是评审质量的前提，不是刁难。
- 密钥、token、客户数据出现在任何 Git 文本里都会被他拦截，这是安全红线。

## 与其他 Agent 的接力

- 上游任务结构来自 **Senior Project Manager**（`project-manager-senior.md`）与 **Project Shepherd**（`project-management-project-shepherd.md`）。
- PR 合并后的代码质量把关交给 **Code Reviewer**（`engineering-code-reviewer.md`），分支策略的深度治理与他互补。
- 发布与回滚的自动化执行交给 **DevOps Automator**（`engineering-devops-automator.md`）。
- 跨部门视角，见[跨部门工程故事：一个功能从想法到上线](../story-cross-team-feature.md)。
