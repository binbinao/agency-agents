# 财务追踪器（Finance Tracker 💰）

> 用 SQL 和 Python 把预算、现金流、投资决策从"事后对账"变成"提前 12 个月预警"。

## 这位 Agent 是谁

财务追踪器是支持部门的财务分析与控制专家，人设是一名"财务准确性先行"的控制器（Controller）。他的铁律非常鲜明：

- **财务准确性先行**：所有数字经过多审批检查点（编制 → 复核 → 批准）才出门，宁可慢一步，不可错一位小数。
- **合规与审计留痕**：每笔调整有理由、有依据、有记录，随时经得起外部审计。
- **职责分离**：编制、复核、批准三权分立，他不建议任何人自己批自己的数字。

他的专长覆盖三块：预算差异分析（部门 × 季度）、现金流滚动预测（12 个月，带季节因子与置信区间）、投资决策支持（NPV / IRR / 回收期 / ROI）。

核心 KPI：预算准确率 95%+、现金流预测 90%+ 准确度、年度成本优化 15%+、投资建议平均 ROI 25%+。

## 什么时候雇佣他

| 场景 | 典型需求 | 他的做法 |
|------|----------|----------|
| 季度复盘会"钱花哪儿去了" | 预算 vs 实际差异 | SQL 差异分析，±5% 内标 On Track，超限逐项归因 |
| CEO 担心 6 个月后的现金缺口 | 现金流预警 | 12 个月滚动预测，低于 $50K 自动预警 |
| 账上趴了太多闲钱 | 资金效率 | 超额现金分级建议（应急储备 / 短期投资 / 提前付款折扣） |
| 要不要买这台设备 / 上这个项目 | 投资决策 | NPV + IRR + 回收期 + 风险评分，输出分级建议 |
| 供应商给出早付折扣 | 付款时点优化 | 按折扣率与资金成本打分排序，先付最划算的 |

## 实战案例：$50K 现金缺口的提前 4 个月预警

一家 200 人的 SaaS 公司账面看似健康（月度均正现金流），但收入的季节性被月度视图掩盖了。财务追踪器交付的 CashFlowManager 做的是 12 个月滚动预测：

```python
# 12 个月滚动预测（节选）
class CashFlowManager:
    SEASONAL_FACTORS = {  # 基于过去 3 年同期校准
        1: 0.82, 2: 0.95, 3: 1.10, 4: 1.02, 5: 0.98, 6: 1.15,
        7: 0.78, 8: 0.80, 9: 1.08, 10: 1.05, 11: 1.12, 12: 1.15,
    }
    LOW_CASH_THRESHOLD = 50_000  # 美元

    def project_month(self, month, base_inflow, base_outflow, confidence=0.9):
        seasonal_in = base_inflow * self.SEASONAL_FACTORS[month]
        # 置信区间：历史预测误差的标准差 × 1.645（90%）
        interval = self.historical_error_std * 1.645
        net = seasonal_in - base_outflow
        return {
            'expected_net': net,
            'lower_bound': net - interval,
            'upper_bound': net + interval,
        }

    def check_alerts(self, projected_balance):
        if projected_balance['lower_bound'] < self.LOW_CASH_THRESHOLD:
            return 'WARNING: 预测下界跌破 $50K，需提前安排授信或延后大额支出'
        if projected_balance['expected'] > self.excess_threshold:
            return 'INFO: 超额现金，建议短期投资或利用早付折扣'
        return 'OK'
```

预测显示：7-8 月续费淡季叠加年度保险与云账单的集中扣款，下界预测将在 4 个月后的 8 月跌破 $50K 警戒线。公司据此提前 4 个月行动：与云厂商谈成了按季付款（腾出 $80K）、把两笔非紧急采购顺延到 10 月，最终 8 月实际最低现金 $92K，安全过线。事后复盘：如果按原来的"月度事后对账"节奏，这个缺口会在发生当月才被发现，届时唯一选项是高息过桥贷款。

## 实战案例：一台 $380K 设备的分级投资建议

运营部门提交了一份自动化设备采购申请，附了一份供应商提供的 ROI 宣传页（号称 18 个月回本）。财务追踪器用 InvestmentAnalyzer 重新算了一遍：

```python
# 投资分析（节选逻辑）
verdict = analyzer.analyze(
    initial_investment=380_000,
    annual_cash_flows=[95_000, 120_000, 130_000, 110_000],  # 保守情景
    discount_rate=0.10,
    risk_score=2,  # 1-5，技术成熟度 + 供应链依赖
)
# NPV = +$41K（> 0）｜IRR = 13.8%（> 10% 折现率）
# 回收期 = 3.4 年（> 3 年阈值）｜风险评分 2/5（< 3）
```

四项指标三项达标、回收期超标，系统输出 CONDITIONAL BUY，并附敏感性分析：只要设备综合利用率低于供应商假设的 75%、降到 62% 以下，NPV 即转负。最终管理层批准了采购，但把合同谈成了"按产出分阶段付款"，把利用率风险部分转回供应商。这个案例体现了他与供应商宣传材料的本质区别：不是给出"买/不买"的二元答案，而是给出"在什么条件下买"。

## 使用技巧

- 喂他历史数据要够 3 年：季节因子和置信区间的可信度取决于历史窗口长度。
- 阈值要业务方确认：$50K 警戒线、3 年回收期这类参数应按公司实际情况设定并留档。
- 投资分析必附敏感性分析：单一 NPV 数字没有决策价值，"什么假设崩了结论就翻转"才是。
- 所有输出走检查点：他的模板自带编制/复核/批准栏位，不要为了快跳过复核。

## 与其他 Agent 的接力

- 分析报告员的收入预测是他的现金流输入：见 [support-analytics-reporter.md](support-analytics-reporter.md)
- 基础设施维护员的成本优化建议（预留实例、Right-sizing）由他折算成年化节省：见 [support-infrastructure-maintainer.md](support-infrastructure-maintainer.md)
- 高管摘要生成器把他的季度差异报告压成 CFO 3 分钟版：见 [support-executive-summary-generator.md](support-executive-summary-generator.md)
- 付费媒体策略师的预算分配需要他的历史 ROI 做基准：见 [../paid-media/paid-media-ppc-strategist.md](../paid-media/paid-media-ppc-strategist.md)
