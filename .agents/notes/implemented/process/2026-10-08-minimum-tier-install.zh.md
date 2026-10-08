# Decision: 按最小档安装这套工作流套件

[English](2026-10-08-minimum-tier-install.md) | 中文

Status: implemented
Date: 2026-10-08
Class: process

## Problem

本仓库是一个演示项目：它存在的意义，是在一个还没有代码的项目上跑这套套件的生命周期，并作为第一个 feature 被提案、决策、验证、评审的地方。它需要一套人与 agent 从第一次提交起就能照着做的纪律。

把所有站点都装上，意味着在任何一站还没有主体的时候，就先把发布、演化、退役、否决记录与事故复盘的家和闸门背在身上。套件自己的规矩是：匹配不到文件的检查就是空壳，所以被开关称为已安装、家却是空的阶段，按设计就是红的。树要么判红，要么被逼着放一些毫无意义的占位文件。

## Decision

`tools/tiers.json` 里写着 `default: minimum`，并对本仓库不运行的七个站点显式写 `none`：implementation、integration、release、evolution、retirement、rejection、incident。这些站点的家——`dev/release`、`dev/upgrade-guide`、`dev/postmortem`、`notes/archived`、`notes/rejected`——在树里不存在，因此开关与树双向一致。

已安装九个阶段：intent、proposal、decision、contract、capabilities、verification、review、documentation、tests。`dev/contracts` 与 `dev/capabilities` 保留，因为检查引擎自己的定义、提供者与消费者就住在那里，而最小档正是这个引擎运行的地方。

套件自己的决策记录在安装时已删除；`notes/` 只留下每个生命周期的 `TEMPLATE.md`、它的 `README.md` 与它的 `AGENTS.md`。`README.md`、`README.zh.md`、`README.i18n.yaml` 是本仓库自己的，因为套件的拷贝清单刻意不含根 README。

`AGENTS.md` 同样是本仓库自己的：它的"先读"入口指向套件自己的两张地图，它写明目前没有安装步骤，原先指到被删的家的两条规则也改成不依赖链接而独立成立。

## Alternatives considered

**装交付档（delivery）。** 否决：它会加上发布与演化，而本仓库什么都没发布过，也没有已被消费、需要演化的面。分档是对"这个项目在做什么"的陈述；在还没有发布记录可写的时候先加上它，就是占位。

**装长期档（long-lived）。** 理由同上、更进一步否决：契约、集成、退役、否决记录与事故复盘，每一个都需要一个本仓库并不具备的主体。

**照搬套件但不裁剪，也不声明任何档位。** 否决：被声明为已安装、家却是空的阶段，按设计就判红；而把目录留着却没有任何东西可查，正是套件拒绝的那种空壳闸门。

**把套件的决策记录一起拷过来。** 否决：套件的决定是套件自己的历史，本仓库的读者会把它们当成这个仓库的决定。

## Consequences

本仓库起步时就只有"还没有代码的项目确实能产出其产物"的那些站点：提案、决策、契约、测试、评审，以及承载它们的文档。日后升档，就是改一次 `tools/tiers.json`，外加"创建该站第一件产物"的那次改动；这里做出的决定没有一条需要推翻。

代价是 `dev/README.md` 里的生命周期地图与 `docs/evolution.md` 里的政策，描述着本仓库并不运行的站点。这是刻意的——读者需要知道这把梯子上有什么——而读目录树的闸门现在都读开关，所以指向缺席站点的家的链接是静默的，而不是判红。

重审时机：当本仓库有了对外发布的面（那就是交付档），或者经历了多轮演化、且贡献者不止一人（那就是长期档）。

## Testing

- [A1] `tier-manifest` 在开关与树任一方向不一致时判红，因此被声明 `none` 却家中有文件的站点、或已安装却家为空的站点，都会红。
- [A2] `agent-input-links` 解析本仓库里 agent 加载文件的每一条相对链接，即 `AGENTS.md`、十二个技能，以及各记录模板。
- [A3] `i18n` —— `pair-docs --check` 保证 `README.md`、`README.zh.md`、`README.i18n.yaml` 三件齐全且同步。
- [A4] `tests` —— `unittest` 在本仓库里跑套件的契约测试；其阶段被开关声明为缺席的那两条测试报 skipped，而不是 error。
- [A5] `note-class` 把这份记录约束在它所在目录编码的类目上。
