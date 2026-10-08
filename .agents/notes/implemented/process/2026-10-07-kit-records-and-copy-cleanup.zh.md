# Decision: 记录套件自己的改动，并在拷贝时删掉套件的记录

[English](2026-10-07-kit-records-and-copy-cleanup.md) | 中文

Status：已实现（implemented）
Date: 2026-10-07
Class: process

## 问题

套件告诉每个采用者为一次非平凡改动写一份决策记录，而它自己的 `.agents/notes/implemented/` 已经攒下了四份分层记录。但安装说明把 `.agents/notes/` 原样拷贝，于是那些记录像采用者自己的历史一样，被带进了每个采用者的仓库。两个目标看起来互斥：记录套件的决策并发布噪音，或者把理由留在套件之外，让 `record-decision` / `decision-implemented` / `criteria-traced` 什么都管不到。此前的一次集成步骤选了后者，这就是集成/发布层曾经在没有记录的情况下发布的原因。

## 决策

套件把自己的非平凡改动记在 `.agents/notes/` 下，和它要求采用者做的一模一样。套件自己的记录是那些**具名**文件（`.agents/notes/*/<yyyy-mm-dd>-<slug>.md`）；每个目录里的 `TEMPLATE.md` 是会随之发布的骨架。`README.md` 的安装一节新增一个清理步骤：把套件拷进去之后，删掉那些具名记录，保留模板。

```sh
find .agents/notes -mindepth 3 -type f \( -name '*.md' -o -name '*.zh.md' -o -name '*.i18n.yaml' \) ! -name 'TEMPLATE.*' -delete
```

这次清理是安全的，因为每个 `.agents/notes/` 目录都保留着自己的 `TEMPLATE.md`，所以 `decision-*` 与 `criteria-traced` 仍然能匹配到一个文件，也就不会空洞地变红。`2026-10-07-integration-release-layer.md` 是在这条政策下写下的第一份记录；早先那四份分层记录都在它之前。

## 曾考虑的替代方案

**把套件的理由留在套件之外（此前的做法）。** 它落选了：一份套件并不 owns 的记录，不会被它的 `.agents/notes/` 索引，不会被 `decision-implemented` 或 `criteria-traced` 检查，也不会被下一个改动这份决策所管文件的人读到。只有在拷贝是唯一会搬动记录的事情时，它才站得住；一旦拷贝步骤会删掉它们，这个取舍就消失了。

**把套件自己的记录移出拷贝集合，例如移到 `notes-kit/`。** 它落选了：它把一条约定劈成"所有人都在用的模板"和"私藏书架"，于是套件自己的记录不再检验采用者所依赖的那些检查，安装集合还多出一条排除规则。把它们留在 `.agents/notes/` 里、只加一个显式的删除步骤，保住的是一条约定和一种形状。

**发布每一份记录，并写明采用者可以删掉它们。** 它落选了：一份没人读的记录不是中性的 —— 旧正文会作为事实回来。一份讲述套件自己历史的记录，除非被删掉，否则会被读成采用者的历史，所以删除是必需步骤，不是建议。

**加一个 `Scope: kit` 头字段，让记录自己表明身份。** 它落选了：模板是会发布的，把这个字段加进模板，就等于让每个采用者的记录都声明自己是套件内部的。`TEMPLATE.md` 与具名文件这条分界已经分开了这两个集合，而且只看路径就能判定。

## 后果

- 套件现在像任何采用者一样记录自己的决策，`criteria-traced` 也管得住它的标准。安装会把它们删掉，所以一份被拷贝的套件依然只从模板开始。
- `find .agents/notes -mindepth 3 -type f \( -name '*.md' -o -name '*.zh.md' -o -name '*.i18n.yaml' \) ! -name 'TEMPLATE.*' -delete` 成为安装的一部分。跳过它，就会把套件的历史留在一个下游仓库里，在那里它会被读成那个仓库的决策。
- 这条规则是一句话：**具名记录属于套件；`TEMPLATE.md` 是会发布的骨架。** 一条必须跟着套件走的事实，属于一份会发布出去的文档（`dev/README.md`、`documentation.md`、`evolution.md`），而不是 `.agents/notes/`。
- 没有闸门能检查这次删除：没有任何东西知道一份下游拷贝删掉了什么。`README.md` 写明这个步骤，责任在拷贝者身上。

## 验证

- [A1] `decision-proposed`, `decision-implemented`, and `decision-rejected` each still match a `TEMPLATE.md` after the named records are deleted, so the cleanup cannot create an empty corpus.
- [A2] `criteria-traced` accepts `.agents/notes/implemented/TEMPLATE.md` and `.agents/notes/proposed/TEMPLATE.md` with the named records absent, because each template's bullets already name declared checks.
- [A3] `publish-manifest` classifies every `.agents/notes/**` file as `internal` through the `.agents/notes/*` pattern, so adding and removing records needs no manifest change.
- [A4] `agent-inputs` lists `README.md`, so the install instructions are reviewed as a model-visible input; the delete step itself is a human action no check can verify.
