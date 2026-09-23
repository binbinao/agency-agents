# Frontend Developer（前端开发）使用指南

> 🖥️ **一句话定位**：构建响应式、可访问、像素级还原设计的现代 Web 应用，性能优化与 WCAG 合规是默认要求。

## 这位 Agent 是谁

Frontend Developer 是现代 Web 技术专家，精通 React/Vue/Angular/Svelte、UI 实现与性能优化。他的两条铁律：性能优先开发（Core Web Vitals 从第一天抓起）和无障碍设计（WCAG 2.1 AA 起步，ARIA、键盘导航、读屏兼容全套）。

核心专长：

- 现代框架组件开发：TypeScript、虚拟化长列表、memo/useCallback 级别的渲染优化
- 像素级设计实现：设计稿到代码的高保真还原
- Core Web Vitals 优化：LCP < 2.5s、FID < 100ms、CLS < 0.1
- PWA 与离线能力、代码分割与懒加载
- 测试与质量：单测、集成测试、CI/CD 集成、零控制台报错

## 什么时候雇佣他

| 场景 | 你能得到的产出 |
|------|--------------|
| 设计稿要变成高质量代码 | 带响应式 + 无障碍标注的组件实现 |
| 长列表页面卡顿 | 虚拟化方案（如 @tanstack/react-virtual），渲染时间可降 80% |
| 首屏加载慢 | 代码分割 + 懒加载 + 图片格式优化方案，初始加载可降 60% |
| 组件库/设计系统建设 | 可复用组件架构，复用率目标 80%+ |
| 无障碍合规改造 | WCAG 2.1 AA 审查 + 修复方案 |

## 实战案例：5 万行数据的商品管理表格

背景：运营后台的商品列表要展示 5 万条数据，现有实现滚动卡顿、内存占用高。

你给他的输入：

```
React 商品管理表格，数据量 5 万行，列：商品名/类目/价格/状态/操作。
现状：一次性渲染全部 DOM，滚动掉帧。
要求：滚动流畅、支持行点击、Lighthouse 性能分 90+。
```

他会给你的产出（要点还原）：

1. 虚拟化渲染方案，只渲染可视区 + overscan 的行：

```tsx
const rowVirtualizer = useVirtualizer({
  count: data.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 50,
  overscan: 5,
});
```

2. `memo` 包裹组件、`useCallback` 固定行点击回调，避免全表重渲染。
3. 无障碍不是事后补丁：`role="table"` / `role="row"` / `aria-label` 直接写进首个版本。
4. 交付时附性能声明：Lighthouse 90+、无控制台报错、组件复用率目标。

**价值**：同样是"把表格做出来"，他交付的是一份带性能预算和无障碍验收标准的工程实现。

## 使用技巧

- 把设计稿（或 UI Designer 的设计系统产出）直接给他，他的"像素级还原"能力需要输入基准。
- 说清楚目标浏览器与设备范围，他会据此决定优雅降级策略。
- 性能问题给数字（加载几秒、帧率多少），他按 Core Web Vitals 口径给你整改方案。
- 他默认写 TypeScript 和测试，如果项目是 JS 或无测试基建，提前说明。

## 与其他 Agent 的接力

- 界面设计规范来自 **UI Designer**（`design-ui-designer.md`）的设计系统，token 对 token 直接映射。
- 后端接口契约来自 **Backend Architect**；联调问题找他定位是前端还是后端责任。
- 代码完成后交给 **Code Reviewer**（`engineering-code-reviewer.md`）评审再合并。
- 跨部门视角的完整故事，见[跨部门工程故事：一个功能从想法到上线](../story-cross-team-feature.md)。
