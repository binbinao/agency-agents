# Data Engineer（数据工程师）使用指南

> 🔧 **一句话定位**：构建把原始数据变成可信分析资产的管道——Medallion 三层湖仓、幂等管道、数据契约、血缘追踪，SLA 达成率 99.5% 是底线。

## 这位 Agent 是谁

Data Engineer 是数据管道与湖仓平台专家，人设钩子是"Builds the pipelines that turn raw data into trusted, analytics-ready assets"。他的性格是"可靠性痴迷"：凌晨三点排查静默数据损坏的经历塑造了他的工程观——管道必须幂等（重跑不产生重复）、schema 漂移必须告警（绝不静默污染）、每一行金层数据必须带质量分与血缘。

他的架构信条（Medallion）：

- Bronze（铜层）：原始、不可变、只追加，永不在原地转换
- Silver（银层）：清洗、去重、标准化，跨域可 join
- Gold（金层）：面向业务、聚合、SLA 背书，按查询模式优化
- 金层消费者禁止直读铜层/银层

## 什么时候雇佣他

| 场景 | 你能得到的产出 |
|------|--------------|
| 数据散落各系统，分析靠人肉导表 | 端到端 ETL/ELT 管道 + 湖仓分层架构 |
| 报表数据经常"对不上" | 数据契约 + 全链路质量校验（dbt tests + GX） |
| 全量刷新烧钱又慢 | CDC 增量管道（成本可降 90%+） |
| 需要实时/准实时数据 | Kafka + 流式处理管道（含迟到数据处理） |
| 数据血缘说不清（合规审计要求） | 血缘追踪 + 数据目录建设 |

## 实战案例 1：营销数据仓库的 Medallion 改造

背景：公司营销数据从 6 个平台（广告/CRM/电商/社媒）手动导 CSV 拼表，分析师每周花 20 小时对数，且每次活动复盘的数据都是"差不多对"。

你给他的输入：

```
6 个数据源要汇入统一分析层：
3 个有 API，2 个只能导文件，1 个有数据库直连。
分析需求： campaign 级 ROI 看板，T+1 更新可接受。
当前痛点：对数耗时大，口径各说各话。
```

他会给你的产出（要点还原）：

1. 先做源画像与契约（他的流程第一步）：各源的字段结构、更新频率、CDC 能力摸底；与消费方（分析师）定死 gold 层口径——"campaign ROI 的归因窗口是 7 天还是 30 天"这类争议在契约阶段终结。
2. Bronze 层：六源全部只追加落地，带三列审计元数据（`_ingested_at`、`_source_system`、`_source_file`）——出问题可完整重放。
3. Silver 层：窗口函数按主键去重（保留最新）、类型/币种/国家码标准化、null 显式处理（填充/标记/拒绝按字段规则，绝不隐式传播）。
4. Gold 层：campaign 日粒度 ROI 聚合，dbt 契约强制执行（enforced: true）——字段类型、非空、唯一约束在模型层锁定，schema 变更想"悄悄混进来"会直接构建失败：

```yaml
models:
  - name: silver_orders
    config:
      contract:
        enforced: true
    columns:
      - name: order_id
        tests: [not_null, unique]
      - name: revenue
        tests:
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 1000000
```

5. 可观测性：新鲜度 SLA（1 小时内必须有新数据）+ 行数异常告警，5 分钟内推送 PagerDuty。

**价值**：分析师每周 20 小时对数归零，ROI 口径唯一化——数据从"各说各话的素材"变成"有 SLA 的资产"。

## 实战案例 2：全量刷新的成本手术

背景：一个日级管道每晚全量重刷 2TB 大表，云成本每月 $3,600 且随数据增长线性上升。

雇佣他时可以这样提示：

```
夜间全量刷新 2TB，月成本 $3.6K 且逐月上涨。
要求：降到 10% 以内，数据质量不降。
```

他会做的事：

1. 量化对比先行（他的沟通风格：用数字说话）："全量 $12/次 vs 增量 $0.40/次——切换省 97%。"
2. CDC 方案：源库开启变更捕获，Bronze 只追加变更行；Silver 用 MERGE（Delta Lake upsert）按主键更新——幂等性保证重跑安全。
3. 历史分区保留：全量刷改为分区级 `replaceWhere`，只重写变更日期的分区。
4. 增量正确性验证：随机抽 3 天做增量 vs 全量的结果对账，证明等价后才切换。

**价值**：月成本 $3,600 → $310（-91%），且管道时长从 5 小时缩到 25 分钟——凌晨三点的告警也随之消失。

## 使用技巧

- 把数据源清单（系统/访问方式/数据量）和消费场景（看板/ML/合规）一次给全，分层架构据此设计。
- 口径争议（归因窗口、去重规则）在契约阶段拍板，他会强制各方签字。
- 成本敏感场景主动提出，增量化是他的第一刀。
- 静默失败是他的头号敌人：告警渠道（PagerDuty/Slack/Teams）提前配置。

## 与其他 Agent 的接力

- 破损数据的自动修复（管道不停机场景）交给 **AI Data Remediation Engineer**（`engineering-ai-data-remediation-engineer.md`）。
- 消费侧的模型训练交给 **AI Engineer**（`engineering-ai-engineer.md`）。
- 事务型数据库的 schema 与索引优化归 **Database Optimizer**（`engineering-database-optimizer.md`）。
- 管道部署与调度基建配合 **DevOps Automator**（`engineering-devops-automator.md`）。
- 跨部门视角，见[跨部门工程故事：一个功能从想法到上线](../story-cross-team-feature.md)。
