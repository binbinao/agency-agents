# CMS Developer（CMS 开发工程师）使用指南

> 🧱 **一句话定位**：Drupal 与 WordPress 的实战专家——"CMS 不是约束，是与内容编辑团队签订的契约"，配置全部进代码，编辑 30 分钟内学会发布是验收标准。

## 这位 Agent 是谁

CMS Developer 是 Drupal/WordPress 主题与插件开发的资深专家，从本地 NGO 官网到百万级流量的企业 Drupal 平台都建过。他把 CMS 当一等工程环境对待：内容建模、代码化配置、主题系统、编辑体验，全套工程化方法——而不是拖拽式搭站工具。

他的七条铁律节选：

- 永不与 CMS 对着干：用 hooks/filters/插件体系，不篡改内核
- 配置属于代码：Drupal 配置走 YAML 导出，WordPress 行为配置进 `wp-config.php` 而非数据库
- 内容模型先行：写一行主题代码前，字段、内容类型、编辑工作流必须锁定
- 只用子主题/自定义主题：绝不直接改父主题或第三方主题
- 扩展必须审查：推荐任何插件/模块前查更新日期、装机量、安全通告
- 无障碍不可协商：WCAG 2.1 AA 起步

## 什么时候雇佣他

| 场景 | 你能得到的产出 |
|------|--------------|
| 企业站/内容站选型 Drupal 还是 WordPress | 匹配内容模型复杂度的选型决策 + 理由 |
| 定制主题开发 | 代码化主题（design token + 模板体系 + 资产管线） |
| 编辑团队抱怨 CMS 难用 | 编辑工作流改造（Gutenberg/ACF Blocks 或 Layout Builder） |
| 站点慢（LCP 超标） | 性能审计 + 缓存/资源加载优化方案 |
| 站点安全状况不明 | 插件/模块审查 + 安全加固清单 |

## 实战案例 1：企业站的内容模型驱动重建

背景：一家 B2B 公司的 WordPress 站：营销团队每次发案例研究都要"复制旧页面再改"，字段内容散落在正文段落里，无法统一展示样式。

你给他的输入：

```
WordPress 6.7 站点。案例研究（Case Study）目前是普通页面，
编辑手动拼装。需要结构化：字段（客户名/行业/成果数据/证言）
+ 统一卡片列表页 + 编辑能自助发布。
```

他会给你的产出（要点还原）：

1. 内容模型先行（铁律 3）：先锁定 Case Study 内容类型与字段结构，再动主题代码。
2. 一切进代码（铁律：代码优先于管理界面）：

```php
// 自定义文章类型用代码注册，不是后台 UI 手点
register_post_type('case_study', [
    'supports'    => ['title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'],
    'show_in_rest' => true,   // Gutenberg + REST 支持
    'rewrite'     => ['slug' => 'case-studies'],
]);
```

3. ACF 字段组走 JSON 同步（`acf-json/` 目录），环境间迁移可版本化。
4. 卡片列表用 Gutenberg 自定义 block（block.json + render.php），编辑插入即所见即所得。
5. 交付验收含编辑体验指标：非技术编辑 30 分钟内完成首次发布（他的 Success Metrics 明文）。

**价值**：案例研究发布从"找开发帮忙拼页面"变成编辑自助 20 分钟搞定；字段结构化后，全站案例卡片的样式改一处生效全局。

## 实战案例 2：插件泛滥站点的瘦身治理

背景：一个 WordPress 站装了 47 个插件，3 个两年未更新（有安全通告），页面 TTFB 1.8 秒。

雇佣他时可以这样提示：

```
47 个插件、3 个有未修复安全通告、TTFB 1.8s。
请做安全与性能治理。
```

他会做的事：

1. 插件逐一审查（铁律 5 的执行）：更新日期、活跃装机量、开放 issue、安全通告——47 个里判定 12 个冗余（功能重复或未使用）、3 个高危。
2. 功能替代方案：冗余插件先找 core/主题能否原生覆盖，再考虑自写轻量 snippet——"能不装就不装"是他的插件哲学。
3. 高危插件立即处理：有替代的换、无替代的下线该功能并记录技术债。
4. 性能治理：对象缓存（Redis）、图片懒加载、脚本 defer、安全头（CSP/HSTS）配置进代码而非散落插件。
5. 交付运维交接清单：更新维护计划、每季度安全巡检流程。

**价值**：插件 47 → 32、安全通告清零、TTFB 1.8s → 520ms——治理的复利是此后每次更新都不再是赌博。

## 使用技巧

- 给他内容模型需求时说清编辑团队构成（技术程度、发布频率），他的工作流设计围绕编辑体验。
- 明确 CMS 与版本（WordPress 6.x / Drupal 10/11 + 关键扩展），他的代码产出会版本对齐。
- 多语言、电商（WooCommerce）、headless（WP 后端 + Next.js 前端）需求提前声明，架构选择完全不同。
- 无障碍要求（AA 还是 AAA）与性能预算（Core Web Vitals 目标）提前定，他按指标工程化。

## 与其他 Agent 的接力

- 站点视觉与设计系统来自 **UI Designer**（`design-ui-designer.md`），他负责落进 CMS 主题层。
- Headless 架构的前端实现交给 **Frontend Developer**（`engineering-frontend-developer.md`）。
- 慢查询与大数据量（复杂 Views、重 WooCommerce 目录）升级给 **Database Optimizer**（`engineering-database-optimizer.md`）。
- 技术审计深度场景分别转 **SEO Specialist**（`marketing/`）、**Accessibility Auditor**（`testing/`）、**Security Engineer**（`engineering-security-engineer.md`）。
- 跨部门视角，见[跨部门工程故事：一个功能从想法到上线](../story-cross-team-feature.md)。
