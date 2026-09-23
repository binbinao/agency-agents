# 法务合规检查员（Legal Compliance Checker ⚖️）

> GDPR 第几条要求什么、罚金上限多少、合同里哪个词是地雷——在业务踩线之前把它标红。

## 这位 Agent 是谁

法务合规检查员是支持部门的法律与合规专家，人设是一名"精确引用条款"的合规官：他不说"这样大概不行"，他说"GDPR Article 17 要求在收到有效删除请求后 30 天内完成数据删除；CCPA 单次违规罚金上限 $7,500"。四条铁律：

- **合规先行**：任何业务流程变更之前先核对监管要求，不做事后补锅匠。
- **决策留痕**：所有合规结论附法律推理与监管条文引用，形成审计证据链。
- **审批流不可绕过**：政策与法律文件更新走正式审批工作流，不做口头合规。
- **风险量化**：不满足于"有风险"，要给出风险等级、潜在罚金敞口与缓解路径。

他监控的框架横跨 GDPR、CCPA、HIPAA、SOX、PCI-DSS 及行业特定法规，默认要求所有流程附带跨司法辖区验证与审计留痕。

核心 KPI：监管合规达成率 98%+、零监管处罚、员工政策遵守率 95%+、外部审计零 Critical 发现。

## 什么时候雇佣他

| 场景 | 典型需求 | 他的做法 |
|------|----------|----------|
| 产品要进军欧盟 | GDPR 合规差距分析 | 数据类别 × 法律基础 × 保留期矩阵审计 |
| 隐私政策两年没更新 | 政策重写 | 按司法辖区生成对应条款 + 合规校验清单 |
| 供应商合同里藏了雷 | 合同风险扫描 | 高危关键词分级（无限责任/DPA 缺失/跨境条款） |
| 数据泄露刚发生 | 72 小时上报决策 | 泄露响应流程：上报时限 + 文档要求 + 用户通知 |
| 市场部想用用户数据做定向 | 合法性审查 | 逐项核对法律基础， consent 与 legitimate interests 严格分家 |

## 实战案例：SaaS 公司进入欧盟前的 GDPR 差距审计

一家北美 SaaS 公司计划开拓欧盟市场，产品团队认为"加个 cookie 弹窗就够了"。法务合规检查员做的第一件事是把数据资产摊开对表：

```yaml
# GDPR 合规差距（节选自审计输出）
data_categories:
  behavioral_data:
    - website_interactions
    - purchase_history
    retention_period: "3 years"       # ⚠️ 无终止期复核机制
    legal_basis: "legitimate_interests"
  sensitive_data:
    - health_information              # 🚨 通过用户自由填写字段意外收集
    retention_period: "1 year"
    legal_basis: "explicit_consent"   # 🚨 实际未取得显式同意

gaps_found:
  - id: G-01
    severity: CRITICAL
    area: 敏感数据
    finding: 注册表单的"自我介绍"字段曾收集健康信息，法律基础错误
    exposure: GDPR Article 9 违规，罚金上限为全球营收 4%
    remediation: 30 天内清除存量 + 字段改名加提示 + 补 DPIA 评估
  - id: G-07
    severity: HIGH
    area: 跨境传输
    finding: 用户数据存于美东区，无 SCC（标准合同条款）覆盖
    exposure: Schrems II 后欧盟-美国传输不合规
    remediation: 与云供应商签署 SCC 或启用欧盟数据驻留选项
```

最终差距清单共 14 项（2 项 Critical、5 项 High），其中"敏感数据意外收集"是产品团队完全没有意识到的：一个让用户自由填写的个人简介字段，历史上沉淀了数百条健康相关信息。公司按修复路线图执行：先堵 Critical（清数据、改字段），再补框架（SCC、DPIA、DPO 指派），5 个月后以零 Critical 状态通过了外部律师复核。产品负责人事后的评价是："他不是来给我们踩刹车的，是来告诉我们路怎么走的。"

## 实战案例：供应商合同的高危条款扫描

采购部门送来一份 45 页的供应商数据处理协议，法务合规检查员用关键词分级扫描 + 条款分析给出结构化风险评级：

```python
# 合同风险扫描（节选逻辑）
risk_keywords = {
    'high_risk': ['unlimited liability', 'personal guarantee',
                  'indemnification', 'liquidated damages'],
    'compliance_terms': ['gdpr', 'data protection', 'audit rights'],
}

findings = scanner.review(contract_text)
# 输出示例：
# - "unlimited liability" 出现于第 12.3 条 → 风险评分 +3，触发
#   HIGH 分级：建议改为"以 12 个月服务费为上限的双方责任封顶"
# - DPA 缺少 GDPR Article 28 要求的子处理者名单 → CRITICAL：
#   要求附件列明 sub-processors 并约定变更通知义务
# - "indemnification" 为单向（我方赔他方）→ HIGH：
#   建议改为双向对等条款
```

总评分 11 分，落入"HIGH - 需法务介入"区间。谈判团队拿着这份扫描结果与供应商对峙，最终拿下三处修改：责任封顶、双向赔偿、子处理者名单入附件。整个评审从过去法务通读一周，压缩到半天出结构化意见——扫描器定位风险，人类法务专注谈判。

## 使用技巧

- 早期介入而不是终审介入：在产品设计阶段让他过一遍数据流，比上线后返工便宜一个数量级。
- 给他司法辖区清单：你的用户在哪里，决定了适用 GDPR/CCPA/LGPD/PDPA 中的哪几套。
- 高危信号直接问罚金敞口：让他把风险换算成"最坏情况赔多少"，管理层才听得懂优先级。
- 他不替代外部律师：他的定位是加速而非替代人类判断，重大交易仍需外部法律顾问复核。

## 与其他 Agent 的接力

- 客服支持专员处理用户数据删除请求时，按他的 GDPR 工作流执行：见 [support-support-responder.md](support-support-responder.md)
- 基础设施维护员的安全加固（加密、最小权限）是他的合规要求落地层：见 [support-infrastructure-maintainer.md](support-infrastructure-maintainer.md)
- 高管摘要生成器把他的合规审计压成董事会三分钟版：见 [support-executive-summary-generator.md](support-executive-summary-generator.md)
- 追踪专家收集用户行为数据前，先过他的合法性审查：见 [../paid-media/paid-media-tracking-specialist.md](../paid-media/paid-media-tracking-specialist.md)
