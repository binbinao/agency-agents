# Backend Architect（后端架构师）使用指南

> 🏗️ **一句话定位**：设计撑住一切的底层系统——数据库、API、云与扩展性，安全与监控是默认配置而非可选项。

## 这位 Agent 是谁

Backend Architect 是资深后端架构专家，专注可扩展系统设计、数据库架构、API 开发与云基础设施。他的所有设计默认包含安全措施与监控——不是你要求才有，是他的人设规则。

核心专长：

- 数据/Schema 工程：10 万级实体的高效数据结构、ETL 管道、亚 20ms 查询的持久层
- 微服务架构：横向独立扩展、事件驱动高吞吐、API 网关设计
- 可靠性保障：熔断、优雅降级、备份与容灾、自动扩缩容
- 性能与安全优化：缓存策略、认证授权、纵深防御、最小权限

## 什么时候雇佣他

| 场景 | 你能得到的产出 |
|------|--------------|
| 新系统需要整体架构设计 | 系统架构规格书（服务拆分 + 通信模式 + 数据模式 + 部署模式） |
| 数据库表结构设计 | 带索引、约束、软删除的完整 DDL + 查询优化说明 |
| API 需要规范化 | 带安全中间件、限流、错误处理的框架级示例代码 |
| 系统要扛大促流量 | 缓存 + 读写分离 + 队列削峰的完整方案 |
| 需要量化的质量目标 | p95 < 200ms、可用性 99.9%、查询 < 100ms 等成功指标 |

## 实战案例：电商数据库从设计到扛量

背景：新电商平台要设计用户与商品模块，预估商品量 50 万，要求首页商品查询 p95 < 200ms。

你给他的输入：

```
请为一个电商平台设计 users 和 products 表：
- 商品量约 50 万，需要按类目筛选、按价格排序、按名称搜索
- 用户表需要软删除，邮箱登录
- 首页商品查询 p95 < 200ms
```

他会给你的产出（要点还原）：

1. 完整 DDL：UUID 主键、`password_hash` 用 bcrypt、价格 `DECIMAL(10,2)` 加 CHECK 约束、库存非负约束、时间戳带时区。
2. 精确的索引策略——注意他的索引不是撒网式的，而是对着查询场景设计：

```sql
CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_products_category ON products(category_id) WHERE is_active = true;
CREATE INDEX idx_products_price ON products(price) WHERE is_active = true;
CREATE INDEX idx_products_name_search ON products USING gin(to_tsvector('english', name));
```

3. 部分索引（`WHERE deleted_at IS NULL` / `WHERE is_active = true`）避免索引膨胀，GIN 索引支撑名称全文搜索。
4. 提醒你补缓存层：高频商品读走 Redis，数据库只承担长尾查询。

**价值**：你拿到的不是"建表语句"，而是一份能直接进代码评审、带性能预算的数据库工程方案。

## 使用技巧

- 直接说出你的性能预算（QPS、p95 延迟、数据量级），他的设计会围绕数字收敛。
- 他默认输出带安全中间件（helmet、限流、参数化查询）的代码骨架，别嫌长，那是你免于安全审计返工的保险。
- 想要"方案对比"时明确说，否则他默认给"他认为最优的那一套"。
- 与 Software Architect 的分工：架构选型（单体还是微服务）找前者，选型后的服务/库表/缓存落地找他。

## 与其他 Agent 的接力

- API 契约确定后交给 **Frontend Developer**（`engineering-frontend-developer.md`）实现界面。
- 上线部署方案交给 **DevOps Automator**（`engineering-devops-automator.md`）做 CI/CD 与监控。
- 数据库性能调优的深度场景可再请 **Database Optimizer**（`engineering-database-optimizer.md`）。
- 跨部门视角的完整故事，见[跨部门工程故事：一个功能从想法到上线](../story-cross-team-feature.md)。
