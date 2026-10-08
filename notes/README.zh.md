# 决策记录

[English](README.md) | 中文

这里住着一类设计文档。**决策记录**留下一个塑造本套件的决定或提案 —— *为什么*、它比下去了什么、代价是什么：模板与闸门承载不了的那些部分。本文件规定记录住在哪、何时需要写一份，以及文件内的格式。

## 布局与命名

每份记录有两根轴，都写在它的**路径**里 —— `notes/` 下的 `{lifecycle}/{class}/yyyy-mm-dd-topic-title.md`：

- **生命周期**（顶层目录）是记录的状态，状态改变时记录在目录之间移动：
  - **`proposed/`** —— 已设计但未实现，或只完成了一部分；闸门 `decision-proposed`。
  - **`implemented/`** —— 决定已交付，并且**与真正交付的东西保持一致**：之后路径、名字或默认值移动时，记录在同一次改动里跟着改 —— 只改事实，绝不改决定；闸门 `decision-implemented`、`no-proposal-era-headings`。
  - **`rejected/`** —— 考虑过并否决；只在它的理由还能阻止一个诱人的错误时留着，否则连三件套一起删掉；闸门 `decision-rejected`。
- **类目**（嵌套目录）是决定的*种类*，取自下一节的封闭集合；闸门 `note-class`。

文件名里的日期是这件事**第一次被提出**的日期。记录之间的交叉引用一律用相对 Markdown 链接，绝不用裸文字或编号：链接能挺过搬动，而且 `pair-docs.py --check` 会解析它的 fragment。

模板住在上一层，即 `notes/<lifecycle>/TEMPLATE.md` —— 骨架由生命周期决定，不由类目决定 —— 每个模板还负责让对应检查不至于匹配不到文件，因为空语料判无效，而不是判通过。

这棵生命周期树就是清单：浏览它的类目目录，或者从 [docs/README.md](../docs/README.zh.md) 的索引进来。不要为这棵树再加一个集中索引页：第二份清单就是第二个事实，而已经存在的索引本来就路由到这里。

## 分类

每份记录属于一个写在路径里的类目，封闭集合声明在 [workflow.json](../tools/workflow.json) 的 `note-class` 检查中。闸门会拒掉集合之外的目录、未知的生命周期、缺失的 `Class:` 行，以及与所在目录不一致的 `Class:` 行。新增一个类目，就是在同一次改动里既改那个列表、又改这张表。

| 类目 | 覆盖什么 |
|---|---|
| `feature` | 面向用户或模型的新能力。 |
| `bug-fix` | 修掉一个缺陷，或补上一条事故记录暴露出来的缺口。 |
| `simplification` | 删掉行为或表面积，而不新增能力。 |
| `architecture` | 关于本套件**交付物本身**的结构性决定 —— 各部分怎么关联、词汇是什么。 |
| `process` | 交付物**周围**的工具、政策或流程：闸门、记录、发布、文档规则。 |
| `testing` | 测试基础设施与策略。 |

**架构 vs 流程**这条界线：架构讲的是交付物本身；流程讲的是它周围的机器、以及治理这台机器的规则。`refactor` 是有意缺席的 —— 它唯一的判别标准"可观测行为变了吗？"已经属于 `simplification`。

## 归档与删除

只描述机械改动或局部调整的已实现记录，连同它的英文、中文与 sidecar 文件一起删掉，并修好每一条入链。一个小的缺陷修复、一个新能力，或一个实质性的决定，不会因为实现小就够格被删。

当已交付的决定已经完整、它的理由不太可能再指导未来的工作、而这份记录仍然对某段历史负责时，把它封进 `notes/archived/{class}/yyyy-mm-dd-topic-title.md`。只要它的被否方案、归属边界、某条负向保证或重新引入的条件还在指导人，就让它留在活跃树里。**永远不要封存一份提案**：过时的提案应当被否决。被否决的记录只在它还能阻止一个似是而非的错误时才留着。

归档会移动完整的三件套、保留 `Status: implemented`，并在两种语言的文件里插入同一行 `Archived: <yyyy-mm-dd>`。闸门 `archive-seal` 把每份被封存文件的文本与它的摘要、归档日期、以及 [manifest.json](archived/manifest.json) 里写下的理由绑在一起，所以未登记的掉落、丢失的文件、被改动的字节、与登记不一致的日期都会变红。一旦封存，记录即冻结：永不编辑、重排、翻译、修补或移动。"删除 / 合并 / 封存"这个判断属于 [evolution.md](../docs/evolution.md) 里的选择器，不属于词数、年龄或配额。

被完全取代的已实现记录，可以在把它并进当前拥有该决定的记录之后删掉 —— 前提是承接方保留了每一条独特的理由、被否方案、后果与已点名的缺口，且所有入链都修好。部分取代不算：让两份记录互相交叉引用，并保留仍然为真的事实。

## 何时需要写一份

在工作发生的那次改动里写下或更新记录，而且只写那些代码、测试与常驻文档解释不了的、持久的决策理由（[规则](../AGENTS.md)）。实质性的未来工作从 `proposed/` 起步；已经做出的决定从 `implemented/` 起步。更新**已经拥有该决定**的那份记录，就算满足了这条规则，所以不要造第二份。

机械改动与局部调整豁免。记录绝不被改写成**另一个**决定：写一份新的并交叉引用，除非旧的那份够格按上面的规则被合并。把 `implemented/` 记录改成与交付物一致，是要求而不是禁止。

## 文件格式

每份活跃记录都遵循同一种文件内格式，由 `decision-proposed`、`decision-implemented`、`no-proposal-era-headings`、`criteria-traced` 与 `note-class` 执行。字面的骨架就是那些模板 —— 格式只有一份，不是两份。

### 头部块

每份记录开头都是下面这几行，顺序如此：

| 行 | 取值 |
|---|---|
| `# Proposal: <title>` 或 `# Decision: <title>` | 生命周期自己的前缀：提案保持 `Proposal`，移动过的记录带 `Decision` |
| `Status: <status>` | `proposed`、`implemented`，或 `rejected — <一行理由>`；必须与所在目录一致 |
| `Date: <yyyy-mm-dd>` | 第一次被提出的日期，与文件名里的日期相同 |
| `Class: <class>` | 路径里的类目，逐字相同；`note-class` 会拿它与目录交叉核对 |

状态里不写日期，也不写除否决理由以外的任何括号内容 —— 日期由文件名承载，其余一切由记录本身承载。

### 正文骨架

每份记录的正文都以 `## Problem` 开头 —— 动机，要写成离开方案也能独立成立。反复出现的小节只用下面这些名字，别的都不用；真正专有的小节（某道闸门的契约、某种表格形状）夹在必需小节之间。

- `proposed/`：`## Problem` · `## Proposal` · `## Alternatives considered` · `## Acceptance criteria` · `## Risks`。
- `implemented/`：`## Problem` · `## Decision` · `## Alternatives considered` · `## Consequences` · `## Testing`。
- `rejected/`：冻结的提案；判定写在 `Status:` 行上。

`## Proposal` 可以用将来时 —— 工作还没落地时，计划与开放问题都属于它。`## Decision` 用现在时陈述已交付的现实。`## Testing` 让每条验收编号活下来，而 `## Consequences` 记下这次取舍付出了什么、又换来了什么。

### 曾考虑的替代方案——必需

每份记录都带 `## Alternatives considered`，且不得为空：每个真正的替代方案都要写明它为什么输了，一个加粗起头的段落一条。没写下被它比下去什么的决定，会招来重新争论 —— 整个这一层存在的意义就是防这个。这条要求在两种语言下都有闸门，所以翻译过的记录不可能悄悄把它丢掉。

### 在生命周期之间移动

在目录之间移动记录，意味着在同一次改动里更新 `Status:` 行、并重新满足目标目录的骨架。具体来说，`proposed/` → `implemented/` 把 `## Proposal` 改写成现在时的 `## Decision`，把 `## Acceptance criteria` 与 `## Risks` 折叠进 `## Consequences`（或者对"如今钉住行为"的那部分写成现在时的 `## Testing`），并保留每一条验收编号 —— 编号正是告诉读者哪条检查证明哪条标准的东西。`proposed/` → `rejected/` 只把理由加到状态行上并冻结正文。闸门 `no-proposal-era-headings` 会拒掉仍带着 `## Proposal`、`## Plan`、`## Migration plan` 或 `## Acceptance criteria` 的已移动记录。

### 中文对侧文件

`.zh.md` 对侧逐节镜像它的英文同侧，并在这对文件旁放一份 `.i18n.yaml` 一致性记录（[i18n.md](../docs/i18n.md)）。机器检查的头部记号 —— `# Proposal: `、`# Decision: `，以及 `Status:`、`Date:`、`Class:` 三行 —— 逐字保持英文；只有标题与正文被翻译。

## 去哪看

- 怎么写：骨架在 [notes/proposed/TEMPLATE.md](proposed/TEMPLATE.md) 与 [notes/implemented/TEMPLATE.md](implemented/TEMPLATE.md)。
- 一次改动该写哪份记录：[evolution.md](../docs/evolution.md) 里的选择器（指向英文原文 —— 宿主管辖的配对要求两侧链接逐字一致，页顶可切到中文）。
- 每一节必须写什么：[documentation.md](../docs/documentation.md) 里的文档 kind（同上，英文原文）。
- 这个仓库做过的全部记录：本树，按文件名从新到旧。
