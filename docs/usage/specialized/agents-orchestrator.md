# Agents 编排器（Agents Orchestrator 🎛️）

> 从规格到上线的全自动开发管道指挥家：PM → 架构 → 逐任务 Dev-QA 循环 → 集成验收，质量门不放水。

## 这位 Agent 是谁

Agents 编排器是特殊专家部门的自主管道管理者，人设是一名"系统化、质量执念、流程驱动"的总指挥。他用一条初始命令驱动完整开发工作流：`project-manager-senior`（规格转任务）→ `ArchitectUX`（技术架构与 UX 基座）→ 开发与 QA 的逐任务循环 → `testing-reality-checker` 最终集成验证。他调度的专家名录覆盖设计、工程、营销、产品、支持、测试六大类数十个 Agent。

铁律围绕"质量门"：

- **绝不抄近路**：每个实现任务必须通过 QA 验证才能推进；推进决策只基于真实 Agent 产出与证据。
- **重试上限**：每任务最多 3 次重试，超限升级人工并标记阻塞，不无限空转。
- **清晰交接**：每个被调度的 Agent 收到完整上下文与具体指令，包含应引用的文件与交付物路径。
- **状态与留痕**：维护当前任务/阶段/完成度的管道状态，决策与推进过程全部记录。

他的决策逻辑是严格的门控：QA 通过 → 下一任务；QA 失败 → 带反馈回到开发（重试计数 +1）；3 次失败 → 标记阻塞继续管道其余部分，最终集成兜底；证据不明确时一律判 FAIL——安全默认。

## 什么时候雇佣他

| 场景 | 典型需求 | 他的做法 |
|------|----------|----------|
| 一份项目规格想全自动跑到交付 | 端到端管道 | 单命令启动四阶段流水线 |
| 多 Agent 各干各的成品拼不起来 | 统一编排 | 顺序阶段 + 逐任务验收 + 上下文传递 |
| 质量口头承诺、交付即翻车 | 质量门禁 | 每任务 PASS 才前进，QA 要截图证据 |
| 想知道管道现在卡在哪 | 状态报告 | 阶段/任务/QA 状态/重试计数/阻塞项模板化输出 |
| 最终上线前不放心 | 集成验收 | reality-checker 默认 NEEDS WORK，压倒性证据才放行 |

## 实战案例：八个任务的管道全程

某团队用一条命令启动编排器执行规格文件 `[project]-setup.md`。管道的实际运行记录（还原节选）：

```text
Phase 1 — project-manager-senior 读取规格生成任务清单：
  "quote EXACT requirements from spec, don't add luxury
   features that aren't there."
  → 产出 8 个任务，全部回引规格原文

Phase 2 — ArchitectUX 产出架构与 UX 基座：
  css/ 设计系统 + project-docs/*-architecture.md

Phase 3 — Dev-QA 循环（核心阶段）：
  Task 1: Frontend Developer 实现 → EvidenceQA 验收 PASS（1 次过）
  Task 2: Backend Architect 实现 → EvidenceQA FAIL
          （反馈：错误处理缺失，截图证据 2 张）
          → 回到开发修复 → 二次 QA PASS（重试 1/3）
  Task 3: EvidenceQA FAIL × 3（持续无法通过）
          → 标记 BLOCKED，附三次失败报告，管道继续 Task 4-8
  Task 4-8: 全部 PASS，其中 5 个首次通过

Phase 4 — testing-reality-checker 最终集成：
  跨任务交叉验证 + 全量自动化截图
  → 识别出 Task 3 阻塞功能缺口，整体判定 NEEDS WORK
  → 输出剩余工作清单，人工介入后二次运行通过
```

两个值得注意的细节。其一，PM Agent 的调度指令里那句"引用规格原文，不要加规格里没有的奢侈功能"是防需求膨胀的疫苗——多 Agent 系统最常见的交付漂移就是每个 Agent 都"顺手多做一些"。其二，Task 3 被阻塞时管道没有整体停下，而是标记阻塞、继续其余任务，把阻塞影响限制在单任务粒度，最终由集成阶段统一暴露缺口。这份"阻塞不等于死等"的设计让管道总时长可控。

## 实战案例：状态报告让干系人闭嘴

同一项目进行到 Phase 3 中段时，产品负责人来问"到底做得怎么样了"。编排器输出的状态报告（模板还原节选）：

```markdown
# WorkflowOrchestrator Status Report

## 🚀 Pipeline Progress
Current Phase: DevQALoop | Total Tasks: 8 | Completed: 5
Current Task: 6 - 支付流程表单（QA IN_PROGRESS）

## 🔄 Dev-QA Loop Status
Current Task Attempts: 1/3
Last QA Feedback: "校验错误提示未覆盖空输入场景，需补充"
Next Action: spawn dev 修复后重新验收

## 📈 Quality Metrics
Tasks Passed First Attempt: 4/5
Average Retries Per Task: 0.4
Screenshot Evidence Generated: 17
Status: ON_TRACK | Estimated Completion: 3.5h
```

产品负责人看完只回了一个字："好。"这份报告的设计逻辑是把"进度焦虑"翻译成可验证的数字：首次通过率 4/5、平均重试 0.4、截图证据 17 张——每一项都有对应的产出物可查，而非"快了快了"式的口头安抚。

## 使用技巧

- 规格写清楚再启动：管道质量上限由规格文件决定，"quote EXACT requirements"的前提是 requirements 本身明确。
- 用他的启动命令原样发起：单命令跑全流程是他设计的交互契约。
- 看 QA 反馈质量而非只看 PASS/FAIL：反馈越具体（截图、复现步骤），重试轮次越少。
- 阻塞任务别恐慌：标记阻塞后管道继续，集成阶段会兜底，人工介入时机看阻塞报告。

## 与其他 Agent 的接力

- 他调度的执行层：project-manager-senior、ArchitectUX、各开发 Agent、EvidenceQA、testing-reality-checker（按工程/设计/测试部门名册索引）
- MCP 构建师为管道中的 Agent 提供工具扩展：见 [specialized-mcp-builder.md](specialized-mcp-builder.md)
- 身份图操作员处理多 Agent 共享实体时的身份统一：见 [identity-graph-operator.md](identity-graph-operator.md)
- 自动化治理架构师与他是"该不该自动做"与"怎么自动做好"的分工：见 [automation-governance-architect.md](automation-governance-architect.md)
