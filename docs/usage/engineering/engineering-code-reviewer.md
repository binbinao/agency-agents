# Code Reviewer（代码评审员）使用指南

> 👁️ **一句话定位**：像导师而非守门人那样评审代码——每条评论都在教你点什么，只看正确性/安全/可维护性/性能，不纠缠风格。

## 这位 Agent 是谁

Code Reviewer 是代码评审与质量保障专家。他评审过"数千个 PR"，信条是"最好的评审是教学，不只是批评"。他不管 tab 还是空格，只管五件事：正确性、安全性、可维护性、性能、测试覆盖。

他最大的特色是分级评论体系：

- 🔴 **Blocker（必须修）**：安全漏洞（注入/XSS/越权）、数据丢失风险、竞态死锁、破坏 API 契约、关键路径缺错误处理
- 🟡 **Suggestion（应该修）**：缺输入校验、命名混乱、重要行为缺测试、N+1 查询、该抽取的重复代码
- 💭 **Nit（锦上添花）**：无 linter 兜底时的风格、命名微调、文档空缺、备选思路

## 什么时候雇佣他

| 场景 | 你能得到的产出 |
|------|--------------|
| PR 合并前的质量把关 | 一份带 🔴🟡💭 分级的完整评审意见 |
| 担心代码有安全漏洞 | 定位到行号的具体漏洞说明（如"第 42 行 SQL 注入"）+ 修复建议 |
| 团队评审文化建设 | 可直接复用的评审评论格式与 checklist |
| 老代码看不懂不敢动 | 以"6 个月后还有人能看懂吗"为标准的可维护性评估 |

## 实战案例：一次教科书级的 SQL 注入评审

背景：一位工程师提交了用户查询接口的 PR，代码能跑、测试全绿。

你给他的输入：

```
请评审这段代码（用户查询接口 PR）：

app.get('/api/users/:name', async (req, res) => {
  const result = await db.query(
    `SELECT * FROM users WHERE name = '${req.params.name}'`
  );
  res.json(result);
});
```

他会给你的产出（还原他的标准评论格式）：

```
🔴 Security: SQL Injection Risk
Line 2: 用户输入被直接拼接进查询语句。

Why: 攻击者可以把 name 参数传成 `'; DROP TABLE users; --`，
     拿到全表数据甚至破坏数据库。

Suggestion:
- 改用参数化查询：
  db.query('SELECT * FROM users WHERE name = $1', [req.params.name])
```

随后他还会补几条 🟡：缺少 404 处理、没有认证中间件、响应缺少统一错误格式。最后以鼓励收尾并给出下一步——这是他"一次评审给全反馈、不挤牙膏"的规则体现。

**价值**：测试全绿不代表安全无洞。他的分级评论让作者第一眼就知道"哪条必须改、哪条可以辩、哪条纯属偏好"，把评审从对抗变成教学。

## 使用技巧

- 一次把完整的 diff/PR 给他，他明确反对"分好几轮挤牙膏式评论"。
- 意图不明的代码他倾向先提问而不是直接判错，你也可以主动附上背景说明，减少来回。
- 他会点名表扬好代码——如果你的 PR 里有精巧设计，期待被他 call out。
- 他的 checklist 可以直接搬进你们团队的 PR 模板，作为团队评审标准的起点。

## 与其他 Agent 的接力

- Frontend Developer 和 Backend Architect 的产出，合并前都应过他一遍。
- 他发现的安全问题超出常规修复范围时，升级给 **Security Engineer**（`engineering-security-engineer.md`）。
- 评审通过后由 **Git Workflow Master**（`engineering-git-workflow-master.md`）把控合并与分支纪律。
- 跨部门视角的完整故事，见[跨部门工程故事：一个功能从想法到上线](../story-cross-team-feature.md)。
