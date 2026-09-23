# 跨部门工程故事：一个功能从想法到上线

> 这是 Agency 智能体名册的一次"全链路演习"：用一个虚拟项目串起 6 位 agent，展示他们如何像一支真实团队那样接力交付。每位 agent 的文档链接在文末。

## 项目背景

虚构一家公司「星舟科技」，产品是面向中小商家的 SaaS 订阅系统。客服侧信号显示：商家每周都在问"我能不能给老客户发一张限时折扣券"。高管拍板要做「优惠券」功能，6 周后上线配合双十一大促。

这个需求横跨产品、设计、工程三个部门——正好让 6 位 agent 各就各位。

## 第一幕：Product Manager 把想法变成证据（第 1 周）

**出场：🧭 Product Manager（Alex）**

需求到达 Alex 桌上时只有一句话："商家想要优惠券"。他的第一反应不是写 PRD，而是连续追问三层"为什么"：

- 为什么商家要这个？——访谈 8 家商家后，真实诉求是"唤回 30 天未下单的老客户"，折扣只是他们想象的解法。
- 为什么是现在？——客服数据显示该主题工单 120 张/月，占总量 15%，且双十一前 6 周是最后的开发窗口。
- 为什么是我们做？——竞品已有基础券能力， churn 访谈里 3 家商家因此转向竞品。

他把发现写进机会评估，用 RICE 打分（Reach 高、Impact 2、Confidence 80%、Effort M），结论是 Build。同时他明确写了"不做什么"：v1 不做满减券、不做分享裂变券、不做券模板市场——每一条都附理由，防止范围蠕变。

**交接物**：一份 PRD，含问题陈述、成功指标（老客 30 天回访率 42% → 55%）、用户故事与验收标准、发布计划（内测 → 封测 50 家 → GA 灰度 20% → 100%）、回滚标准。

## 第二幕：Software Architect 定方向（第 1 周末）

**出场：🏛️ Software Architect**

Alex 的 PRD 到工程侧后，第一个问题不是"怎么写代码"，而是"券该放在系统的哪里"。Software Architect 组织了一场事件风暴：

- 领域事件浮出水面：`优惠券已创建`、`券已发放`、`券已核销`、`券已过期`。
- 边界判定：优惠券是独立的限界上下文，不塞进现有的订单域——它有独立的生命周期和不变量（如"一张券只能核销一次"）。
- 选型权衡：他没有直接说"上微服务"，而是给出对比——星舟是 20 人团队、单体运行良好，结论是**模块化单体 + 独立优惠券模块**，通过领域事件与订单模块解耦。理由：可逆性优先，未来真需要独立扩展再拆。

他把决策写进 ADR-007：Context（20 人团队、6 周窗口）、Decision（模块化单体）、Consequences（放弃独立扩展性，换取交付速度与运维简单）。

**交接物**：ADR + 限界上下文图 + 模块接口契约草案。

## 第三幕：Backend Architect 落地数据与 API（第 2-3 周）

**出场：🏗️ Backend Architect**

拿着 ADR，Backend Architect 开始工程化。他的产出带着鲜明的"安全与监控默认包含"风格：

- 表设计：`coupons`（名称、类型、折扣规则、有效期、预算上限）与 `coupon_redemptions`（券实例、状态机：已发放/已使用/已过期），核销用幂等键防止并发双花——这正是 Code Reviewer 后面会盯的点。
- 唯一性约束兜住业务不变量：`UNIQUE(coupon_id, order_id)` 让"一券一单"在数据库层就不可违反。
- API 设计：发券、核销、查询三个 REST 端点，带版本化、限流、统一错误格式；核销接口用数据库行锁 + 状态检查保证并发安全。
- 缓存策略：热门券的只读配置走 Redis，核销路径保持强一致不缓存。

**交接物**：DDL + API 契约 + 并发安全说明。API 契约随即同步给前端。

## 第四幕：UI Designer 与 Frontend Developer 双线并进（第 2-4 周）

**出场：🎨 UI Designer → 🖥️ Frontend Developer**

UI Designer 没有直接画"优惠券页面"，而是先补设计系统欠账：商家后台此前各页面视觉碎片化，他先落了一版设计 token（色板、字阶、8px 间距系统、暗色主题变量），再基于 token 出券创建与发放界面——按钮、表单、状态徽章全部走 token。

关键设计决策都带无障碍标注：券状态用"图标+文字"而非纯颜色区分（色盲友好），对比度按 4.5:1 卡线，触控目标 44px 起步。

Frontend Developer 拿到设计系统与 API 契约后并行开工：组件按 token 一一映射实现，`coupons` 列表页用虚拟化应对商家上千张券的长列表，核销结果用骨架屏处理加载态。他的自检清单里 Core Web Vitals 与 ARIA 标注和功能代码同步交付。

**交接物**：设计 token + 高保真界面 + 前端实现（含性能与无障碍验收自检）。

## 第五幕：Code Reviewer 把关（第 4-5 周）

**出场：👁️ Code Reviewer**

前后端代码提 PR。Code Reviewer 的一次性完整评审里，最有代表性的一条：

🔴 他发现前端核销倒计时用了商家本地时间做过期判断——商家改设备时间就能用过期券。修复方案：过期判定以服务端时间为准，前端只做展示。这条评论同时给了 Why（攻击场景）和修法，作者看完就懂了为什么。

🟡 他点名表扬了后端的幂等键设计，同时建议给"券预算耗尽"路径补集成测试；💭 顺带提了两个命名可以更贴业务域。评审以"该 PR 整体质量高，修掉 1 个 blocker 即可合并"收尾。

**交接物**：分级评审意见，blocker 修复后合并。

## 第六幕：DevOps Automator 护送上线的最后一公里（第 5-6 周）

**出场：⚙️ DevOps Automator**

代码进了 main，接力棒交给 DevOps Automator。他为这次 GA 设计了金丝雀发布：

- 流水线四段门禁：安全扫描 → 测试 → 构建 → 部署，任何一段红灯都不放行。
- 灰度策略：先 20% 商家启用 feature flag，观察 48 小时。
- 自动刹车：Prometheus 告警规则盯住核销接口错误率与 p95 延迟，超阈值自动回滚 flag——对应 Alex PRD 里写好的回滚标准。
- 发布当天：Alex 按 PRD 的 GTM 计划通知客服团队（提前培训过 FAQ）、发布站内公告、48 小时内发出上线总结。

上线两周后核对指标：老客 30 天回访率 51%（目标 55%，方向正确），券相关工单没有新增，核销接口 p95 稳定在 180ms。

## 这个故事展示了什么

- **接力而非重复**：每位 agent 只在自己最专业的区段出手，交接物（PRD → ADR → API 契约 → 设计系统 → 评审意见 → 流水线）都是下一位的输入。
- **规则驱动的个性**：Alex 的"说清楚不做什么"、Architect 的"可逆性优先"、Reviewer 的 🔴🟡💭 分级、DevOps 的"自动回滚标配"——这些不是脚本，是各自人设里的 Critical Rules 在真实流程中的体现。
- **质量内建**：安全、无障碍、监控不是最后一环补的，而是从 Backend Architect 的约束设计到 DevOps 的告警规则层层嵌入。

## 出场角色文档

| Agent | 使用文档 |
|-------|---------|
| 🧭 Product Manager | [product-manager.md](../product/product-manager.md) |
| 🏛️ Software Architect | [engineering-software-architect.md](engineering/engineering-software-architect.md) |
| 🏗️ Backend Architect | [engineering-backend-architect.md](engineering/engineering-backend-architect.md) |
| 🎨 UI Designer | [design-ui-designer.md](../design/design-ui-designer.md) |
| 🖥️ Frontend Developer | [engineering-frontend-developer.md](engineering/engineering-frontend-developer.md) |
| 👁️ Code Reviewer | [engineering-code-reviewer.md](engineering/engineering-code-reviewer.md) |
| ⚙️ DevOps Automator | [engineering-devops-automator.md](engineering/engineering-devops-automator.md) |
