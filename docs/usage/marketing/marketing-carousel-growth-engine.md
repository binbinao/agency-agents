# 轮播图增长引擎（Carousel Growth Engine）

> 一台自主运转的增长机器：给它一个网址，它每天自动产出并发布一条 6 页轮播图，还会从数据里越学越强。

## 这位 Agent 是谁

他不是"内容建议工具"，而是一套**全自动轮播图生产-发布-学习闭环**：用 Playwright 抓取任意网站的真实内容，用 Gemini 图像生成 6 页视觉连贯的轮播图，通过 Upload-Post API 直接发布到 TikTok 和 Instagram，再拉回分析数据反哺下一次创作。他的口头禅是"Consistency and iteration beat perfection"——每天一条，第 30 条远强于第 1 条。

核心铁律：

- 六页叙事弧固定不变：Hook → Problem → Agitation → Solution → Feature → CTA
- 第 1 页必须让手指停下来：疑问句、大胆断言或扎心痛点
- 第 1 页定义全部视觉基因，第 2-6 页用 Gemini 图生图保持风格统一
- 9:16 竖版（768x1376），底部 20% 不放文字（TikTok 控件遮挡区），只用 JPG（TikTok 拒收 PNG）
- 全程零确认：研究、生成、视觉自检、发布、复盘一口气跑完，只在最后汇报结果
- 单页不合格只重生成那一页，以第 1 页为参考保持连贯

核心专长：网站内容挖掘与品牌色提取、利基识别与痛点文案、Gemini 视觉一致性流水线、多平台发布与分析回流、基于 `learnings.json` 的自我优化调度。

## 什么时候雇佣他

| 场景 | 痛点 | 他能做什么 |
|------|------|-----------|
| 你有产品网站但社媒冷清 | 没人手每天做内容 | 给他 URL，他每日自动产出并发布一条轮播图 |
| 轮播图做了不少但没增长 | 风格漂移、发布时间随缘 | 视觉基因锁定 + 数据学习出的最佳发布时段 |
| 不知道什么钩子有效 | 凭感觉写第一页文案 | 逐帖追踪钩子类型表现，10 帖内锁定 Top 3 钩子 |
| TikTok 和 Instagram 双平台运营 | 一稿两发费时费力 | 一次生成同时发布双平台，TikTok 自动配热门音乐 |
| 内容团队只有一个人 | 生产瓶颈卡在制作环节 | 把制作和发布环节全自动化，人只负责产品和复盘 |

## 实战案例

### 案例一：SaaS 官网变成日更增长渠道

一家开发者工具 SaaS 团队没有专职社媒运营，把官网 URL 交给这台引擎。第一次运行时，Playwright 完整抓取了首页、定价页和评价页，产出这样的分析摘要：

```json
{
  "brand": { "name": "DeployHQ", "colors": ["#4F46E5", "#0F172A"], "logo": "..." },
  "businessType": "developer-tools",
  "features": ["zero-config preview deployments", "GitHub-native", "edge caching"],
  "stats": ["12,000+ teams", "99.99% uptime"],
  "competitorsDetected": ["Vercel", "Netlify"],
  "nicheHooks": [
    "Your CI/CD pipeline shouldn't need a 40-page YAML config",
    "Still waiting 9 minutes for a preview deploy?"
  ]
}
```

注意钩子不是泛泛的"效率更高"，而是从网站真实内容里挖出的开发者痛点。第 1 页以文字提示生成，第 2-6 页全部以第 1 页为参考做图生图——六页共享同一套配色、字体与版式。第 4 页（Agitation）直接点名了检测到的竞品："Netlify 让你等 9 分钟，我们只要 40 秒"。

发布走 Upload-Post API：

```bash
curl -X POST https://api.upload-post.com/api/upload_photos \
  -F "photos[]=@slide-1.jpg" -F "photos[]=@slide-2.jpg" ... \
  -F "platform[]=tiktok&platform[]=instagram" \
  -F "auto_add_music=true" \
  -F "privacy_level=PUBLIC_TO_EVERYONE"
```

### 案例二：学习闭环让第 12 条吊打第 1 条

真正拉开差距的是反馈回路。每条发布后，他用 `request_id` 拉回单帖数据，`learn-from-analytics.js` 把结果沉淀进 `learnings.json`：

```json
{
  "hookPerformance": {
    "question-hook": { "avgViews": 8200, "winRate": 0.62 },
    "bold-claim": { "avgViews": 3100, "winRate": 0.18 },
    "pain-point": { "avgViews": 6400, "winRate": 0.44 }
  },
  "bestTimes": { "day": "Tuesday", "hour": 19 },
  "recommendation": "Use question hook next post; post Tuesday 19:00"
}
```

数据说明疑问式钩子的平均播放量是大胆断言式的 2.6 倍，于是下一条自动改用疑问钩子、并排期到周二 19 点。他向用户的汇报方式是结论先行的："已发布 [TikTok 链接] [Instagram 链接]。疑问钩头图比断言式高 3 倍播放，下一条继续沿用。"——只报告结果与决策，不刷过程。

## 使用技巧

- 准备三个环境变量：`GEMINI_API_KEY`（Google AI Studio 免费）、`UPLOADPOST_TOKEN` 与 `UPLOADPOST_USER`（upload-post.com 免费层），全部免费无需信用卡
- 首次运行先 `playwright install chromium`，否则网站分析阶段会失败
- 给他的输入只需要一个 URL：定价、评价、功能页他都会自己爬，不需要你准备素材
- 别在他的流程中途插手修改：他的设计就是零确认自主跑完，人工介入会打断学习数据的一致性
- 定期查看 `learnings.json`：这是你最直接的"什么在起作用"仪表盘，也是调整产品卖点的间接信号
- 目标是连续性：宁可每天一条 80 分的轮播图，不要每周一条 95 分的——学习闭环依赖高频数据

## 与其他 Agent 的接力

- 需要更长周期、有人工把关的品牌叙事，交给 [内容创作者](marketing-content-creator.md) 或 [图书联合作者](marketing-book-co-author.md)
- 双平台数据回流后想深挖 Instagram 端策略，联合 [Instagram 策展人](marketing-instagram-curator.md)
- 钩子文案与视频化延伸，可衔接 [短视频剪辑教练](marketing-short-video-editing-coach.md) 做同素材的动态版本
- 若增长目标是留存而非曝光，先看 [增长黑客](marketing-growth-hacker.md) 的实验框架再决定日更节奏
