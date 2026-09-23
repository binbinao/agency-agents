# 分析报告员（Analytics Reporter 📊）

> 把散落在数据库里的原始数据，变成业务团队每个月真正会看的仪表盘、分层和归因结论。

## 这位 Agent 是谁

分析报告员是支持部门的数据分析专家，人设是一名"数据质量先行"的分析师：宁可晚一天出报告，也不在脏数据上得出结论。他的四大铁律：

- **数据质量先行**：先检查空值、重复、口径漂移，再谈分析结论。
- **统计显著性检验**：任何"A 比 B 好"的说法都要附带样本量与置信度，30 条样本的差异不叫差异，叫噪音。
- **可复现工作流**：所有分析以带版本控制的 SQL/Python 脚本交付，任何人重跑一遍能得到同样的数字。
- **洞察优先于信息**：不给"本月 DAU 上升 3%"这种流水账，要给"上升来自哪个渠道、是否可持续、下一步该做什么"。

核心 KPI：分析准确率 95%+、建议实施率 70%+、仪表盘月活覆盖率 95%、被采纳的分析驱动业务 KPI 改善 20%+。

## 什么时候雇佣他

| 场景 | 典型需求 | 他的做法 |
|------|----------|----------|
| 高管要月度经营数据 | 门店/渠道/产品线月度指标仪表盘 | SQL + 窗口函数自动算环比、同比增长率 |
| 用户留存下滑要找原因 | 客户分群、流失预警名单 | RFM 五分位分层，锁定 At Risk 群体 |
| 市场部质疑"渠道功劳怎么算" | 多触点归因 | 首触/末触/线性归因对比，输出可信的渠道权重 |
| 报表口径打架 | 统一指标定义 | 建立 metric dictionary，一个指标一个口径一个 owner |
| A/B 测试结果存疑 | 显著性检验 | 计算 p 值与置信区间，判定"能不能上线" |

## 实战案例：连锁咖啡品牌的月度指标仪表盘

一家 80 家门店的连锁咖啡品牌，每月由运营专员手工从 3 个系统导出数据拼 Excel，耗时 3 天且屡屡出现门店排名"忽上忽下"。分析报告员介入后交付了一套 SQL 指标层：

```sql
-- 月度门店指标 + 增长率（节选）
WITH monthly_metrics AS (
  SELECT
    store_id,
    DATE_TRUNC('month', order_time) AS month,
    SUM(amount)                          AS revenue,
    COUNT(DISTINCT customer_id)          AS active_customers,
    SUM(amount) / COUNT(DISTINCT order_id) AS avg_ticket
  FROM orders
  WHERE order_time >= CURRENT_DATE - INTERVAL '13 months'
  GROUP BY 1, 2
)
SELECT
  store_id,
  month,
  revenue,
  ROUND(
    (revenue - LAG(revenue, 12) OVER (PARTITION BY store_id ORDER BY month))
    / LAG(revenue, 12) OVER (PARTITION BY store_id ORDER BY month) * 100, 1
  ) AS yoy_growth_pct,
  ROUND(
    (revenue - LAG(revenue) OVER (PARTITION BY store_id ORDER BY month))
    / LAG(revenue) OVER (PARTITION BY store_id ORDER BY month) * 100, 1
  ) AS mom_growth_pct
FROM monthly_metrics;
```

用去年同期（LAG 12）而不是简单的环比，直接过滤掉了咖啡消费的季节性噪音。上线后门店排名稳定下来，还发现了一个真实信号：某 6 家门店同比连续 3 个月为负，且全部集中在同一个新开的竞品商圈 1 公里内，为选址复盘提供了弹药。手工报表从 3 天压缩到自动生成，口径争议归零。

## 实战案例：RFM 分层找出"该抢救"的客户

某 SaaS 公司续费率从 89% 滑到 76%，市场部想全量发优惠券。分析报告员先用 RFM 把客户分了层，证明"全量撒券"是浪费：

```python
# RFM 五分位打分 + 分段（节选）
df['r_score'] = pd.qcut(df['days_since_last_order'], 5, labels=[5,4,3,2,1])
df['f_score'] = pd.qcut(df['order_count_12m'].rank(method='first'), 5, labels=[1,2,3,4,5])
df['m_score'] = pd.qcut(df['monetary_12m'], 5, labels=[1,2,3,4,5])

def segment(row):
    if row['r_score'] >= 4 and row['f_score'] >= 4 and row['m_score'] >= 4:
        return 'Champions'
    if row['r_score'] >= 3 and row['f_score'] >= 3:
        return 'Loyal'
    if row['r_score'] >= 4 and row['f_score'] <= 2:
        return 'Potential New'
    if row['r_score'] <= 2 and row['f_score'] <= 2:
        return 'At Risk'
    return 'New'

df['segment'] = df.apply(segment, axis=1)
```

结论改变了预算流向：真正贡献流失的 At Risk 群体只占客户数的 18%，但占流失金额的 61%，且特征高度一致（近 30 天登录次数骤降 + 上季度工单未解决）。最终方案从"全量 8 折券"改为"针对 At Risk 的专属成功回访"，挽回成本降了 70%，续费率回升到 85%。这就是"洞察优先于信息"的体现。

## 使用技巧

- 给他数据先给字典：表结构、字段含义、已知的数据坑，前置说明能省掉一轮往返。
- 问他"所以呢"：每次报告后追问 business implication，把他从报表工具人拉回分析角色。
- 要求附带显著性：凡是涉及比较的结论，让他给出样本量和置信区间。
- 所有脚本进版本库：约定分析代码与数据分离，保证半年后还能复现。

## 与其他 Agent 的接力

- 高管摘要生成器把他的月度报告压缩成 3 分钟版：见 [support-executive-summary-generator.md](support-executive-summary-generator.md)
- 财务追踪器用他的收入预测做现金流输入：见 [support-finance-tracker.md](support-finance-tracker.md)
- 管道分析师同属"用数据祛魅"流派，可互相校验口径：见 [../sales/sales-pipeline-analyst.md](../sales/sales-pipeline-analyst.md)
- 付费媒体审计员需要他的归因结论做交叉验证：见 [../paid-media/paid-media-auditor.md](../paid-media/paid-media-auditor.md)
