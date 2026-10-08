# 扩展这套件

[English](extending.md) | 中文

本套件强制执行的一切，就是**一个文件里的数据 + 五个脚本**。本页是"改套件自己"的操作指南：某个目标对应哪一处改动，以及怎么知道改对了。[documentation.md](documentation.zh.md) owns 文档 kind，[i18n.md](i18n.zh.md) owns 配对规则，[tools/AGENTS.md](../tools/AGENTS.md) owns 工具规矩。

## 动手之前

- 唯一的配置是 [tools/workflow.json](../tools/workflow.json)：改动面、检查、证据命令与配对范围都在那里。
- **数据类扩展**——加一个改动面、一条记录检查、一个技能、一条预算——**不许动代码**。只有真正新增一条**判定规则**才动 [tools/check-invariants.py](../tools/check-invariants.py)，而且它必须带着自己的正负样本一起落地。
- 改套件本身就是改一个被设计过的系统，所以它走同样的站：提案、决策记录，以及真的跑过的证据。

## 数据类改动

1. **改一个改动面** —— 在 [tools/workflow.json](../tools/workflow.json) 的 `surfaces` 里加一条。`name` 唯一，每条 `dev/evidence` 必须是读者能粘贴就运行的命令而不是一句描述；可选的 `exclude` 用来摘掉 `patterns` 本来会认领的路径（glob 表达不了否定）。
2. **加一条记录检查** —— 先加 `checks` 条目，再建它要匹配的文件。匹配不到任何文件的检查判**无效**，所以模板要先落地。
3. **加一个技能** —— 建 `.agents/skills/<name>/SKILL.md`，写齐 `skill-record` 要求的四节，`description` 写**触发条件**而不是内容摘要。
4. **加一条预算** —— 给检查 `maxLines` 或 `maxWords`，至少一个。只有空白分隔的正文才适合按词计；中文常驻文档按行计，而没有词间分隔的文本用任何按词的单位都会严重低估。
5. **加一份契约镜像** —— 在源码里加 `begin`/`end` 标记、把块粘进文档、并登记进 [contracts/mirrors.json](../dev/contracts/mirrors.json)。三件事同一次改动落地，否则 `contract-mirror` 变红。
6. **加一个能力** —— 在源码里加行首 `# capability: <key>`、写登记条目；是 seam 就把 Definition / Provider / Consumer 的路径填全。发现自动，分类手写。
7. **加一条可追溯的验收标准** —— 在[提案记录](../.agents/notes/proposed/TEMPLATE.zh.md)的验收小节里写 `- [A<n>] \`<已声明的 check id 或 surface>\` <可观测结果>`。按决定本身、而不是它碰到的文件来选类目；编号要活到实现期骨架里。
8. **做一次发布决定** —— 在 [docs/publish.json](publish.json) 里归类。`public` 逐条点名文件，不接受通配。
9. **加一份生成页** —— 写生成器与它的 `--check` 模式，然后在 `generated-docs` 面上声明那条命令。生成页只读；生成器才是源。
10. **加一份文档** —— 给它 kind 与家；是政策家就再加一条 `required-sections` 检查；然后归类并配对（[i18n.md](i18n.zh.md)）。
11. **加一个记录家** —— 一个目录只要**自己有规矩**，就给它一个 `README.md` 当落地页、一个 `AGENTS.md` 装该子树专属规矩，或者两者都要；只装一份模板的目录两者都不需要。

## 新增一条判定规则

改一条检查怎么判定，是**四处齐改**，四处必须同时落地：

1. [tools/check-invariants.py](../tools/check-invariants.py) 里的 runner；
2. 在 `RUNNERS` 与 `SUPPORTED_KINDS` 里注册；
3. 一条 `--self-test` 用例：一个违规样本 + 一个合规样本，外加它每新增一条判定就配一个探针；
4. [contracts/kinds.md](../dev/contracts/kinds.zh.md) 里的镜像粘贴 —— `contract-mirror` 会拿它和被标记的源码区间逐字比对。

没有样本能让它变红的规则是噪音，不是守卫。

## 怎么知道改对了

跑 [AGENTS.md](../AGENTS.md#commands) 里那组命令：`--self-test` 证明每道守卫都能失败，真实扫描证明这些约定在这棵树上成立，每个生成器的 `--check` 证明它的页是当前投影，`pair-docs.py --check` 证明每一对都齐全同步。然后跑 `run-evidence.py`，让这次运行被**记录**下来而不是被断言，并在宣布改完之前读一遍那份记录。
