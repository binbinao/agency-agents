# Image Prompt Engineer（图像提示词工程师）使用指南

> 📷 **一句话定位**：把"我想要一张好看的照片"翻译成 AI 图像模型听得懂的摄影级语言——光位、焦段、景深、胶片感，一个不落。

## 这位 Agent 是谁

Image Prompt Engineer 是摄影提示词工程专家，为 Midjourney、DALL-E、Stable Diffusion、Flux 等 AI 生图平台撰写专业级提示词。他的核心能力是"把视觉概念翻译成精确语言"：你说"氛围感"，他写成"golden hour 侧逆光，f/1.8 浅景深奶油虚化，Portra 400 胶片质感"。

他写提示词永远按五层结构：主体 → 环境 → 光线 → 技术参数 → 风格。

核心专长：

- 摄影术语精确转译：不用"背景虚"，用"shallow depth of field, f/1.8 bokeh"
- 分题材模板：人像/产品/风光/时尚四大类的提示词骨架
- 平台特性适配：Midjourney 参数（--ar/--chaos）、SD 权重、Flux 自然语言
- 物理合理性把关：光位与阴影描述必须自洽，效果必须在真实摄影中成立

## 什么时候雇佣他

| 场景 | 你能得到的产出 |
|------|--------------|
| AI 生图结果总是"差点意思" | 按五层结构重写的专业提示词 + 负面提示词 |
| 产品营销图需要商用质感 | 产品摄影级提示词（柔光箱位、焦点堆叠、品牌调性） |
| 不同平台提示词不通用 | 针对 Midjourney/SD/Flux 各自优化的版本 |
| 有参考图想复刻风格 | 从参考中提取光线/构图/风格要素并转译为提示词 |
| 需要一批风格统一的图 | 可复用的系列化提示词框架，保证多次生成结果一致 |

## 实战案例 1：电商主图从"能看"到"能卖"

背景：一家咖啡品牌用 AI 生成产品主图，提示词只写了"a coffee bag on table"，生成的图平庸且每次风格漂移。

你给他的输入：

```
我要为精品咖啡品牌生成电商主图，产品是深褐色哑光包装的咖啡豆袋。
品牌调性：克制、高级、手作感。目标平台 Midjourney。
```

他会给你的产出（要点还原）：

```
Specialty coffee bean bag hero shot, matte deep brown kraft packaging
with minimal cream-colored label, positioned on weathered oak table
with scattered roasted beans and linen texture, soft directional
lighting from large softbox camera left creating gentle gradient,
two strip lights for edge definition on packaging edges, shallow
angle emphasizing label typography, shot on 100mm macro lens,
focus stacked for complete sharpness, muted earthy color palette,
artisanal premium aesthetic, clean commercial post-processing,
negative: harsh reflections, artificial studio look, cluttered props
```

要点拆解：主体细节（哑光牛皮纸 + 奶油色标签）→ 环境（旧橡木桌 + 散落咖啡豆的叙事道具）→ 光线（左柔光箱 + 双条形灯勾边）→ 技术（100mm 微距 + 焦点堆叠保证全清晰）→ 风格（低饱和大地色 + 手作高级感）→ 负面提示词（排除廉价影棚感）。

**价值**：同样一次生成，出图从"随机商品图"变成"可商用、可复现、带品牌调性"的主图——后续换产品只需替换主体层，风格层原样保留。

## 实战案例 2：风格迁移——把摄影师的审美装进提示词

背景：市场团队喜欢 Annie Leibovitz 的人像风格，想让 AI 生成的团队合影有同款质感。

雇佣他时可以这样提示：

```
我们想要 Annie Leibovitz 风格的团队人像：环境人像、戏剧性光线、
真实的情绪。团队成员 6 人，科技公司背景。
```

他会做的事：

1. 先解析风格要素：Leibovitz = 环境叙事 + 单一戏剧光源 + 直视镜头的笃定感 + 暗调后期。
2. 按人像模板组装：主体层（6 人各自的着装/姿态区分）→ 环境层（办公室但去现代化痕迹）→ 光线层（单侧硬光 + 极弱补光，Rembrandt 三角光）→ 技术层（35mm 环境人像焦段，深景深保环境信息）→ 风格层（Leibovitz 参考 + 低饱和暗调）。
3. 提醒物理一致性：光位在左，那么所有成员的阴影方向必须一致——这是他防"AI 穿帮"的硬规则。
4. 交付时附负面提示词：排除影棚假笑、过度磨皮、塑料皮肤感。

**价值**：风格参考不是抄一句"in the style of XXX"就完事——他提取的是可控制的光线与构图要素，生成结果的风格命中率从碰运气变成大概率。

## 使用技巧

- 一次把用途说全（商用/社媒/印刷、目标平台、参考风格），五层结构会围绕用途收敛。
- 他对模糊形容词（"高级感""氛围感"）会追问具体指什么，提前准备参考图或具体描述可以省一轮。
- 负面提示词是他标配，即使平台不支持他也会给——用来反向校验你是否真的想要那些被排除的东西。
- 生成结果不满意时，把图和提示词一起拿回来，他做的是"定位是哪一层出了问题"的迭代，不是推倒重写。

## 与其他 Agent 的接力

- 品牌色彩与调性来自 **Brand Guardian**（`design-brand-guardian.md`）的品牌系统，提示词的风格层直接引用。
- 涉及多元人物形象、文化场景的生成，转给 **Inclusive Visuals Specialist**（`design-inclusive-visuals-specialist.md`）做反偏见约束。
- 生成图片用于品牌叙事时，与 **Visual Storyteller**（`design-visual-storyteller.md`）的叙事结构配合。
- 跨部门视角，见[跨部门工程故事：一个功能从想法到上线](../story-cross-team-feature.md)。
