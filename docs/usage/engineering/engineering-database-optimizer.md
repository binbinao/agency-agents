# Database Optimizer（数据库优化师）使用指南

> 🗄️ **一句话定位**：用查询计划、索引策略和 schema 设计让数据库不再凌晨三点叫醒你——EXPLAIN ANALYZE 先行、外键必有索引、生产环境永不锁表。

## 这位 Agent 是谁

Database Optimizer 是数据库性能专家，主域 PostgreSQL，兼通 MySQL、Supabase、PlanetScale。他的思维方式是"query plan 优先"：任何优化动作前先跑 EXPLAIN ANALYZE，用执行计划的证据说话（Seq Scan 是坏味道、Index Scan 是好味道）。

他的八条规则节选：

- 每个查询部署前跑 EXPLAIN ANALYZE
- 每个外键配索引（join 性能的地基）
- 禁止 SELECT *（只取需要的列）
- 永远用连接池（绝不每请求开新连接）
- 迁移必须可回滚（写 DOWN migration）
- 生产建索引用 CONCURRENTLY（不锁表）

## 什么时候雇佣他

| 场景 | 你能得到的产出 |
|------|--------------|
| 某查询突然变慢 | EXPLAIN ANALYZE 诊断 + 索引/改写方案（前后对比数据） |
| 列表页越用越卡 | N+1 查询检测与修复（JOIN/批量聚合改写） |
| 新表设计 | 带约束、外键索引、部分索引的 schema |
| 生产环境要加列/索引 | 零锁表迁移方案（CONCURRENTLY + 可回滚） |
| Serverless 数据库连接爆掉 | 连接池方案（PgBouncer / Supabase transaction pooler） |

## 实战案例 1：Feed 页的 N+1 手术

背景：社交产品用户主页 feed 接口 p95 从 300ms 涨到 2.4 秒，DBA 查看慢查询日志发现同一接口反复执行相似查询。

你给他的输入：

```
用户主页接口：先查用户的 10 条帖子，再逐帖查评论和点赞数。
数据量增长后 p95 从 300ms → 2.4s。
```

他会给你的产出（要点还原）：

1. 定性 N+1（他的经典判定）：

```typescript
// ❌ 现状：10 条帖子 = 1 + 10 + 10 = 21 次查询
const posts = await db.query("SELECT * FROM posts WHERE user_id = $1", [id]);
for (const post of posts) {
  post.comments = await db.query("SELECT * FROM comments WHERE post_id = $1", [post.id]);
}
```

2. 单查询聚合改写：

```sql
EXPLAIN ANALYZE
SELECT p.id, p.title,
       json_agg(json_build_object('id', c.id, 'content', c.content)) AS comments
FROM posts p
LEFT JOIN comments c ON c.post_id = p.id
WHERE p.user_id = 123
GROUP BY p.id;
```

3. 配套索引（不是撒网，是对着查询设计）：

```sql
-- 外键索引（join 地基）
CREATE INDEX CONCURRENTLY idx_comments_post_id ON comments(post_id);
-- 部分索引：只索引用户真正会看到的已发布帖（索引更小、命中率更高）
CREATE INDEX idx_posts_user_published ON posts(user_id, created_at DESC)
WHERE status = 'published';
```

4. 前后对比交付（他的风格：before/after 计划截图 + 数字）：21 次查询 → 1 次；p95 2.4s → 180ms。

**价值**：同样的数据量，查询次数降 95%——优化不是堆硬件，是消除结构性浪费。

## 实战案例 2：生产库的零锁表迁移

背景：运营要求给千万行的订单表加"浏览计数"列，团队上一次直接 ALTER 导致锁表 40 秒、支付超时告警。

雇佣他时可以这样提示：

```
orders 表 1200 万行，要加 view_count 列。
上次类似操作锁表引发事故。请给安全迁移方案。
```

他会做的事：

1. 区分操作风险（他熟 PostgreSQL 11+ 行为）：带常量默认值的加列不重写表（仅元数据变更）——安全；建索引才是锁表大户。
2. 迁移拆分与顺序：

```sql
-- 加列：PG 11+ 带默认值不重写，秒级完成
ALTER TABLE orders ADD COLUMN view_count INTEGER NOT NULL DEFAULT 0;

-- 建索引：CONCURRENTLY，不阻塞读写
CREATE INDEX CONCURRENTLY idx_orders_view_count ON orders(view_count DESC);
```

3. 可回滚保证（规则 5）：DOWN migration 同步写好（DROP COLUMN / DROP INDEX），灰度窗口内可秒级撤退。
4. 事后沉淀：把"生产 DDL 检查单"（是否锁表/是否可回滚/是否低峰执行）固化为团队流程。

**价值**：同样的变更，这次 3 秒完成、读写零感知——安全迁移不是玄学，是对数据库行为规则的工程化应用。

## 使用技巧

- 慢查询把 SQL + EXPLAIN ANALYZE 输出一起给他（有真实行数与实际耗时），诊断质量远高于只给 SQL。
- 数据量级（行数、增长率）与查询频率说清楚，索引策略据此设计。
- Supabase/PlanetScale 场景明说，连接池与分发键策略是平台特定的。
- 别追求"所有查询都快"：他信奉对实际瓶颈做手术，反对过早优化。

## 与其他 Agent 的接力

- 表结构设计的最初版本常来自 **Backend Architect**（`engineering-backend-architect.md`），他负责性能层的深化。
- 分析型管道与湖仓归 **Data Engineer**（`engineering-data-engineer.md`），他主攻事务型数据库。
- 迁移的 CI/CD 与执行环境配合 **DevOps Automator**（`engineering-devops-automator.md`）。
- 跨部门视角，见[跨部门工程故事：一个功能从想法到上线](../story-cross-team-feature.md)。
