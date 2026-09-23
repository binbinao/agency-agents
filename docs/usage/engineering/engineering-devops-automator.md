# DevOps Automator（DevOps 自动化工程师）使用指南

> ⚙️ **一句话定位**：把基础设施全自动化——让团队发布更快、睡得更香，监控告警与自动回滚是标配。

## 这位 Agent 是谁

DevOps Automator 是基础设施自动化与 CI/CD 专家。他的人生信条是"自动化优先"：手动流程在他眼里都是待消灭对象。所有交付默认包含监控、告警与自动回滚能力。

核心专长：

- 基础设施即代码：Terraform / CloudFormation / CDK
- CI/CD 流水线：GitHub Actions / GitLab CI / Jenkins，安全扫描内嵌
- 零停机部署：蓝绿、金丝雀、滚动发布
- 可观测性：Prometheus + Grafana 监控、日志聚合、分布式追踪
- 成本优化：资源规格调优，目标年降 20%

## 什么时候雇佣他

| 场景 | 你能得到的产出 |
|------|--------------|
| 发布全靠手动 SSH | 完整 CI/CD 流水线（扫描→测试→构建→蓝绿部署→健康检查） |
| 流量高峰就崩 | 自动扩缩容 + 负载均衡 + 队列削峰的 Terraform 方案 |
| 出了事才知道 | Prometheus 告警规则（错误率、P95 延迟阈值告警） |
| 多环境管理混乱 | dev/staging/prod 的环境自动化与配置隔离 |
| 云账单月月涨 | 资源右移（right-sizing）与成本优化方案 |

## 实战案例：给电商主站配一条可回滚的生产流水线

背景：电商团队目前发布靠手动打包上传，一次发布 2 小时，出问题靠人肉回滚，上周大促前发布翻车停机 40 分钟。

你给他的输入：

```
技术栈：Node.js + Docker + Kubernetes。
现状：手动部署，无监控，发布即赌博。
目标：push 到 main 自动发布，零停机，出问题自动回滚。
```

他会给你的产出（要点还原）：

1. 四段式 GitHub Actions 流水线，段段有门禁：

```yaml
jobs:
  security-scan:   # 依赖漏洞扫描 + 静态安全分析，不过不准进
  test:            # 单测 + 集成测试
  build:           # 镜像构建推送，tag 用 commit SHA
  deploy:          # 蓝绿部署：切流量前先跑健康检查
```

2. 蓝绿部署细节：先部署 green 环境并 `kubectl rollout status` 等健康检查通过，再切流量——上周那种"发布翻车停机"在新流程里会止步于健康检查。
3. 告警规则同样关键，错误率和延迟超标自动触发：

```yaml
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
- alert: HighResponseTime
  expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
```

4. 附交付标准：MTTR < 30 分钟、一天多次发布、可用性 99.9%。

**价值**：把"发布即赌博"变成"带自动刹车的高速公路"——2 小时人肉发布变成 push 即走，事故从"用户先发现"变成"告警先响"。

## 使用技巧

- 告诉他你的云平台与团队规模，他的方案会按成本与复杂度收敛（小团队他不会硬塞 service mesh）。
- 提供现有发布流程的痛点描述（停机多久、回滚多久），他会优先攻击最痛的点。
- 他的产出是"配置即代码"，建议纳入 git 管理，享受与业务代码同等的评审待遇。
- 监控告警的接收渠道（Slack/邮件/PagerDuty）要提前告诉他。

## 与其他 Agent 的接力

- 应用代码经 **Code Reviewer** 评审后，由他负责流水线的自动发布环节。
- 基础设施容量规划与 **Backend Architect** 的架构设计对齐。
- 生产事故响应的深度场景，交给 **Incident Response Commander**（`engineering-incident-response-commander.md`）。
- 跨部门视角的完整故事，见[跨部门工程故事：一个功能从想法到上线](../story-cross-team-feature.md)。
