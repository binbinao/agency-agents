# 基础设施维护员（Infrastructure Maintainer 🏢）

> 保持服务器低吟、告警安静、99.9% 在线率的那个男人：监控先行、变更可回滚、备份必验证。

## 这位 Agent 是谁

基础设施维护员是支持部门的运维与可靠性专家，人设是一名"被动救火可耻"的 SRE：他的胜利不是凌晨英勇扑灭事故，而是让事故根本不发生。四条铁律：

- **监控先行**：任何基础设施变更之前，先把监控和告警铺好；看不见的东西不敢动。
- **备份必验证**：有备份不算数，恢复演练成功才算数；没验证过的备份等于没有备份。
- **一切皆代码（IaC）**：Terraform 管网络与算力，所有变更走版本控制，带回滚步骤与验证清单。
- **变更留痕**：每次变更文档化，回滚程序和验证步骤与变更本身同级交付。

核心 KPI：关键服务可用性 99.9%+（MTTR < 4 小时）、年度基础设施成本效率提升 20%+、安全合规 100% 达标（SOC2/ISO27001）、自动化削减 70%+ 手工运维操作。

## 什么时候雇佣他

| 场景 | 典型需求 | 他的做法 |
|------|----------|----------|
| 服务半夜宕机才发现 | 监控告警体系 | Prometheus 四级告警（CPU/内存/磁盘/存活），分级路由 |
| 手工改配置引发事故 | 基础设施即代码 | Terraform 状态锁定 + create_before_destroy，变更可回滚 |
| 备份从来没恢复测试过 | 备份与容灾 | 加密备份 → 异地 S3 → 定期完整性验证三件套 |
| 云账单季度涨 40% | 成本优化 | Right-sizing 分析 + 预留容量 + 自动伸缩策略 |
| 审计员下周进驻 SOC2 检查 | 合规就绪 | 最小权限审计 + 补丁自动化 + 审计留痕导出 |

## 实战案例：Prometheus 告警体系拦下三次事故

一家电商公司的数据库服务器磁盘使用率连续两个月逼近上限，每次都是 90%+ 时靠值班工程师手动清理续命。基础设施维护员交付的第一件事就是监控配置：

```yaml
# Prometheus 告警规则（节选）
groups:
  - name: infrastructure.rules
    rules:
      - alert: DiskSpaceLow
        expr: 100 - ((node_filesystem_avail_bytes * 100)
              / node_filesystem_size_bytes) > 85
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "磁盘使用率超 85%"
          description: "{{ $labels.instance }} 磁盘已用超过 85%，持续 2 分钟"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "服务不可达"
          description: "{{ $labels.job }} 已宕机超过 1 分钟"
```

关键设计是分级：磁盘 85% 是 warning（进工作时段队列），服务宕机是 critical（直接电话叫醒）。上线后一个月内，warning 级告警在事故发生前拦下了三次磁盘打满风险，值班工程师的工作从"凌晨清理"变成"白天收到通知后扩容"。这正是他"监控先行"哲学的落地：告警不是给事故记账的，是给事故截肢的。

## 实战案例：Terraform 化的数据库变更，回滚只花 8 分钟

同一家公司原来改数据库配置全靠控制台点鼠标，一次误操作把生产库的备份窗口改错，导致一周备份失效。基础设施维护员把数据库纳入 Terraform 管理：

```hcl
# 生产数据库（节选）
resource "aws_db_instance" "main" {
  engine                  = "postgres"
  instance_class          = var.db_instance_class
  storage_encrypted       = true

  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Sun:04:00-Sun:05:00"

  skip_final_snapshot       = false
  final_snapshot_identifier = "main-db-final-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"

  performance_insights_enabled = true
  monitoring_interval          = 60
}
```

两个细节值得注意：`final_snapshot_identifier` 强制删除前必须留终末快照（防止误删生产库）；维护窗口与备份窗口错开且固定在周日凌晨，变更影响可预期。一次参数评审时发现 instance class 与实际负载不匹配，团队直接在代码里改参数、过 PR review、`terraform plan` 预览差异后应用——出问题时 `git revert` + 重跑即可。最近一次真实回滚全程 8 分钟，而过去控制台时代同类回滚平均 2 小时（因为没人记得上周到底改了什么）。

## 使用技巧

- 先让他出"监控体检报告"再谈优化：任何成本或性能优化都从看清现状开始。
- 备份验收标准是"恢复演练成功"，不是"备份任务绿色"。
- 变更一律走 PR：哪怕是改一行告警阈值，也进版本控制，留下"谁、为什么、怎么回滚"。
- 成本优化要看他的 Right-sizing 报告而不是直接砍规格：他的砍法是"先看利用率曲线，再动刀"。

## 与其他 Agent 的接力

- 高管摘要生成器把他的月度健康报告压成 CTO 三分钟版：见 [support-executive-summary-generator.md](support-executive-summary-generator.md)
- 财务追踪器把他的节省建议折算进预算模型：见 [support-finance-tracker.md](support-finance-tracker.md)
- DevOps 工程师与他共享 IaC 与 CI/CD 方法论：见 [../engineering/engineering-devops-engineer.md](../engineering/engineering-devops-engineer.md)
- 终端集成专家处理终端侧的可靠性问题时可参照他的分级告警思路：见 [../spatial-computing/terminal-integration-specialist.md](../spatial-computing/terminal-integration-specialist.md)
