# Review: 同屏双人五子棋页面，以及它暴露的两道闸门（2026-10-08）

[English](2026-10-08-core-html-gomoku.md) | 中文

## 状态

这份评审找出的两处缺陷都已在 `dsh-router-preset` 的 `559558a` 修掉，评审自己那些判红的观察也在那份版本上重跑过：报告了假通过的两条现在报出项目声明，报了 `invalid output` 的那条现在返回合法的成功。关于本仓库简报的那条判断是对的，简报已更正。一条作为局限接受而不修；最后一条（证据记录的命名）已由一个更晚的会话在 kit 侧收掉，见该条下面的「状态」。

修与本节由一个更晚的会话写下。下面的评审保持原样，包括它对当时那份版本成立的观察；后面某次观察改变了某条判断的含义时，话写在**该条下面的「状态」里**，而不是去改那条判断本身。

## 主张

`src/gomoku/rules.js`、`src/gomoku/rules.test.js` 与 `src/gomoku/index.html` 交付一个从 `file://` 就能打开、能下到分出胜负的同屏双人五子棋页面；而这次交付撞上的两处闸门缺陷，都在它们各自所在的地方修掉了：`tools/pair-docs.py` 修在本仓库，交付闸门修在共享的 `dsh-router-preset`。

## 证据

本会话写了 `src/gomoku/*`，所以这是一次同源评审（same-source review），给不出站 7 要的那种独立性。它能做的是把这次修复所带的观察逐条重跑、并读它们的输出，下面每条就是这个。闸门那几条是在 dsh web profile 重启之后重跑的。

**交付闸门（`~/dsh-playgroud/tools/dsh-router-preset`，重启后生效）。**

- `node --test tests/delivery-gate.test.mjs` → `# tests 19`、`# pass 19`、`# fail 0`；`node scripts/patch-bootstrap.mjs --check` → `patch-bootstrap.mjs: --check: all patches applied`；在 `/Users/ray/dsh-playgroud/.router-preset-probe` 下跑 `node .agent-presets/router-standard/router-bootstrap-v34.selftest.mjs` → `SELFTEST PASS`。
- `dev_visual_check(…, workspace=/Users/ray/Workspace/agent-workflow-demo)` 对两张不同截图 → `Error: tool "dev_visual_check" returned invalid output: "value.proof" is not a declared property (additionalProperties: false)`，而 `.dsh/visual-proof.json` 照样被写出来。
- `.dsh/visual-proof.json` 现在写着 `"provider": "deepseek-official"`、`"model": "deepseek-flash"`、`"match": true`，两张 `760x880` 的指纹不同。它不再指向简报那次探针留下的 fixture provider。
- `delivery_check(file=…/src/gomoku/index.html, url=file:///…/src/gomoku/index.html, evidence=<page 已复核 + 两张截图已复核>)` **不传** `workspace` → `[PASS] page-verify: 2 screenshot(s), 760x880/760x880, fingerprints distinct; visual read not required by tools/workflow.json (delivery.page.visual is not true)`，而把同一个文件读回来打印的是 `delivery.page.visual = True`。
- 同一次调用、把 `.dsh/visual-proof.json` 删掉 → 仍然 `[PASS]`，理由还是同一句 `not true`，说明项目层根本没被查过。
- 同一次调用、传 `workspace=/Users/ray/Workspace/agent-workflow-demo` 且 proof 在 → `[PASS] page-verify: … read by deepseek-official/deepseek-flash: 第一张截图：顶部标题「五子棋」，其下状态文字「黑方落子」…`。
- 同一次调用、传 `workspace` 且把 proof 删掉 → `[FAIL] page-verify: … tools/workflow.json requires a visual read (delivery.page.visual) but no proof is at .dsh/visual-proof.json — run dev_visual_check on these screenshots`。
- 把一张截图覆盖成另一张后跑 `dev_visual_check(…)` → `visual-check: FAIL ❌ … 1 fingerprint(s) repeat: two claimed states are the same picture`。

**闸门在修复后的版本（`559558a`）上重跑，工作目录不是本项目。**

- `node --test tests/delivery-gate.test.mjs` → `# tests 23`、`# pass 23`、`# fail 0`；`node scripts/patch-bootstrap.mjs --check` → `patch-bootstrap.mjs: --check: all patches applied`；`node scripts/gen.mjs --check` → `gen.mjs: cordis.patch.yml is up to date`。
- `delivery_check(file=…/src/gomoku/index.html, url=file:///…, evidence=<page reviewed + 两张截图 reviewed>)`，**不传** `workspace`，在 `cwd=/private/tmp` 下、proof 在位 → `[PASS] page-verify: 2 screenshot(s), 760x880/760x880, fingerprints distinct; read by deepseek-official/deepseek-flash: Screenshot 1: title 「五子棋」, status line 「黑方落子」, a 15×15 grid board with no stones…` —— 调用方什么都不用点名，项目层就被走到、proof 就被审到。
- 同一次调用，先把 `.dsh/visual-proof.json` 改名移走 → `[FAIL] page-verify: … tools/workflow.json requires a visual read (delivery.page.visual) but no proof is at .dsh/visual-proof.json — run dev_visual_check on these screenshots`。之后 proof 已还原，`.dsh/` 没留下多余文件。
- `dev_visual_check` 的成功返回现在能通过工具自己声明的 schema：通道里的 `a successful dev_visual_check return validates against the schema the tool declares` 放行声明过的形状，并对一个多带一个未声明属性的返回值判红。
- 那条通道里有四处变异被看过变红再还原：祖先向上走、workspace 兜底链、声明里的 `proof` 属性、proof 一致性。

**`pair-docs` 的修复（本仓库）。**

- `python3 tools/pair-docs.py --write .agents/notes/implemented/feature/2026-10-08-core-html-gomoku.md` → `pair-docs: wrote .agents/notes/implemented/feature/2026-10-08-core-html-gomoku.i18n.yaml`，退出码 0。同一条命令在修复前会被判 `not an in-scope pair`。
- `python3 -m unittest tests.test_pairing.ANamedPathKeepsItsOwnPrefix -v` → `Ran 5 tests in 0.059s`、`OK`。
- 本会话跑的反向对照：把 `select_anchors` 变异回 `item.lstrip("./")`，同一条通道报 `FAILED (errors=2)`，具名写入退出 1 并打印 `pair-docs: agents/notes/implemented/feature/2026-10-08-core-html-gomoku.md is not an in-scope pair (see pairing in tools/workflow.json)`；把文件恢复后回到 `OK`。

**交付的页面与引擎。**

- `node --test src/gomoku/rules.test.js` → `# tests 13`、`# pass 13`、`# fail 0`。
- `node -e '<在第 14 行、第 14 列、第 0 行与两条角部斜线上各下一串五子>'` → 五处全部 `"winner":"black"`、各处 `moves: 9`，说明连子扫描能处理棋盘边界。
- 把 `isPoint` 的列边界变异成 `col <= size` 后跑 `node --test src/gomoku/rules.test.js` → `# pass 12`、`# fail 1`：越界那条判红，说明边界是被钉住的，而不是假设的。
- `git status --porcelain` 与 `git diff --stat` → 17 个已跟踪路径改动，`125 insertions(+), 178 deletions(-)`，另有未跟踪的 `src/`、两张 `dev/evidence/*.png` 与新记录三元组。
- `python3 tools/change-scope.py --base origin/main --strict` → `Every changed path matches a declared surface.`
- `python3 tools/check-invariants.py --self-test` → `self-test PASSED`；`python3 tools/check-invariants.py` → 退出码 0；`python3 tools/pair-docs.py --check` → `24 pair(s) in scope, all complete and in step`；`python3 tools/gen-docs.py --check` → `up to date (88 lines)`；`python3 -m unittest discover -s tests` → `Ran 76 tests`、`OK (skipped=2)`。
- 简报点名的那次删除：`git ls-files dev/evidence/` 里没有 `2026-10-08-i18n-decisions-prose-and-more-5.md`，`git status --porcelain` 里也没有它的删除项，而历史里唯一提交过的 `-5` 是 `dev/evidence/2026-10-08-main-5.md`，它在 `0533bde` 里被改名为 `…-i18n-decisions-prose-and-more-4.md`，那个路径现在仍被跟踪。
- 收尾：冒烟用的 loopback 服务已停；对它的端口再 `curl` 已经失败，没有留下监听进程。

## 发现

- **阻塞项** —— 调用 `delivery_check` 时不传 `workspace`，项目自己声明的视觉策略会被静默跳过。位置：`router-bootstrap-v34.mjs:457-475`，`readDeliveryPolicy` 读的是 `<root>/tools/workflow.json`，而 root 由 `workspaceOf`（`:430-443`）给出，它会退回会话头里的 `cwd`。影响：对一个文件里写着 `delivery.page.visual: true` 的项目，闸门打印出相反的话，只在通用层判 `page-verify`，从不审计 proof——于是页面可以在完全没有视觉核对的情况下交付，而它给出的理由是一句假话。证据：上面两次不传 `workspace` 的 `[PASS]`（其中一次 proof 已被删掉），对上从文件里读回的 `delivery.page.visual = True`；传了 `workspace` 之后，同一次调用就进入项目层——没有 proof 它判红，有 proof 它通过。
  **状态 —— 已修**，`559558a`。解析顺序现在是：显式 `workspace` → 会话头 `cwd` → 由交付物自身向上走到项目根；`workspaceOf` 的最后一跳落在那个根上，相对截图路径因此也能解析。proof 的写与读共用同一个锚点。按「不传 `workspace`、cwd 指向别处」重跑：项目层被走到（见「证据」）。评审对症状的诊断是对的，比成因窄了一层：读取器只试交付物的直接父目录，所以永远走不到仓库根，而它点名的 `cwd` 兜底是二阶隐患而不是机制本身。
- **建议** —— `dev_visual_check` 在项目声明了视觉要求时**无法成功返回**。位置：`router-bootstrap-v34.mjs:1243-1245` 声明的输出 schema 是 `{ ok, lines }` 且 `additionalProperties: false`，而 `:681` 的成功返回是 `{ ok: true, proof, lines }`。影响：每一次成功调用到了 agent 这边都是 `Error: … invalid output`，把它读成「检查失败」的 agent 要么一遍遍重跑，要么报一个假阴性，而工具自己的 PASS 行从未被渲染出来。证据：连续两次成功调用都报同一个错，而 proof 文件的内容照旧往前推进。
  **状态 —— 已修**，`559558a`。`proof` 现在声明在两处注册的输出 schema 里，通道会拿工具声明的 schema 校验成功返回。评审对影响的读法完全准确：一个成功却让宿主报 schema 错的道具，会让 agent 白重跑一次，还把它自己的 PASS 行藏起来。
- **建议** —— 视觉审计信的是指纹与 `match` 标志，从不是「谁产的」。位置：`verifyDeclaredVisual`（`:535-560`）与它审计的 proof 文件。影响：政策要的是一次独立的模型阅读，而闸门分不出真读和替身；又因为 proof 落在被 git 忽略的目录里，本仓库没有任何检查看得见它。证据：proof 自己的 `provider`/`model` 字段——本会话看着它从 `fixture` 变成 `deepseek-official`，而闸门的结论与这两者都无关。
  **状态 —— 作为局限接受，不修。** 要验「谁产的」需要一个本闸门没有的签发方身份，加上去等于把交付检查变成身份系统。这条局限现在写在闸门自己的文档里（`dsh-router-preset/delivery-gate.NOTES.md`），proof 的 `provider`/`model` 字段保持可读，留给审它的人。
- **建议** —— 简报那条删除前提不是本工作树的事实。位置：`dev/evidence/`。影响：被要求处理「删掉 `…-more-5.md`」的评审者会去找一条 git 里并不存在的、已跟踪路径的删除，甚至可能记下一次并不存在的改动。证据：`git ls-files dev/evidence/` 里没有该路径，`git status --porcelain` 里没有它的 ` D`，而历史里唯一提交过的 `-5` 已被 `0533bde` 改名改走。
  **状态 —— 确认成立，改的是简报**，不是这条判断。那条前提来自会话日志里的一行 `rm -f …`，当时没有回 git 里核；评审那三项检查是对的。修复新增的 `AGENTS.md` 规矩约束的仍是已提交路径，而这个文件从来不是。
- **建议** —— 证据记录既带 `-N` 后继编号，又按「它覆盖了哪些改动面」改名，于是编号不再构成一条序列。位置：`tools/run-evidence.py` 的 `unique_record_path` 对上那条命名规矩。影响：已提交的 `main-5.md` 变成了 `…-more-4.md`，而同一时期还存在一个无关的、未跟踪的 `…-more-5.md`；那个后缀后来又被一次新运行占走——读者正是这样把一条后继读成已跟踪文件的删除。证据：`0533bde` 里的改名、本会话早些时候写下的未跟踪 `-6`，以及刚刚被复用的 `-5`。
  **状态 —— 已在 kit 侧修掉**（`agent-workflow-kit`），落在本发现所要求的那份记录 `2026-10-08-gates-a-run-names-its-record.md` 里：名字带上这次运行覆盖的改动面与它自己的 UTC 时刻，「第一个空位 `-<n>`」只在同一秒内的两次运行上存活，于是删除再也不能把一个名字交给另一份主张。`tools/run-evidence.py` 与 `tests/test_evidence.py` 已逐字节同步到这里；把旧规矩恢复回去，两条新用例都判红。

在那些必须跑起来才看得见的类别里，交付的引擎与页面没有发现缺陷：四条边与两条角部斜线都能取胜，列边界会让变异判红，和棋与纯性用例通过，冒烟用的服务也已拆除。项目层一旦被走到，视觉链路能认出交付页面在两个状态下的样子。

## 归宿

- **变成了一条规则** —— `AGENTS.md` 的 `## Closing the gate`，这次修复以七条落了地：为过闸门而必须传的开关就是闸门缺陷、过不了的检查不是用来满足的、两次证据形态失败就该收手、收尾时闸门还红就必须说出来、检查红不了的验收标准就是愿望、已提交路径的删除也是一次改动、共享闸门拥有机制而项目拥有策略。推理与被否的路线写在[承载它们的记录](../../.agents/notes/implemented/process/2026-10-08-gates-a-check-must-be-able-to-pass.zh.md)里。
- **在上游变成了一条检查（check）** —— 通用层与三态决策由 `dsh-router-preset` 的 `tests/delivery-gate.test.mjs` 钉住，本次评审重跑过它。它不是本仓库 `tools/workflow.json` 里的检查，因为闸门住在共享包里，而它项目层的那一半读的是本文件里的 `delivery.page.visual`。
- **在这里变成了一条检查** —— `tools/pair-docs.py` 的 `select_anchors` 与 `tests/test_pairing.py` 的 `ANamedPathKeepsItsOwnPrefix`；本次评审亲眼看着它们在修复前的变异下判红、恢复后通过。
- **已在上游变成一条检查** —— workspace 的退回路径，`559558a` 落地（`the policy is found from the deliverable path…` 等三条）。`the policy reader takes the project declaration, and nothing else` 这条已经存在；它缺一个负例：会话头指向别的目录时，不得读成「项目没有要求」；同时读取器应当沿交付物自身路径向上找，而不是只试它的直接父目录。
- **已在上游变成一条检查** —— `dev_visual_check` 的输出 schema，`559558a` 落地：把 `proof` 声明进成功形状，或干脆不返回它，并补一条「成功调用必须通过校验」的测试。
- **刻意什么都不做** —— 那次删除本身与编号冲突。`-5` 那份记录从未被提交，因此不主张任何改动面，也没有入站链接需要修；新规矩约束的是已提交路径，而给 `dev/evidence/` 加一份清单，对没人读的运行输出来说，维护成本高过它抓住的东西。
- **刻意什么都不做** —— 给 `src/gomoku/rules.test.js` 补一条边线取胜用例。边界已经被越界那条用例钉住（`col <= size` 变异会让它判红），两条扫描方向也被现有四个轴覆盖，所以新用例无法为任何现有通道漏掉的回归变红。

## 刻意承担的风险

- 页面的视觉那一半现在有了真闸门，而且自 `559558a` 起不需要调用方点名就能走到，默认调用会审 proof。剩下的是 proof 落在仓库之外，本仓库没有任何检查看得见它（见下一条风险）。
- 视觉 proof 落在被 git 忽略的目录里，所以这个承诺只能在会话内审计，对任何读仓库的检查都不可见。
- `source` 只承载一条具体命令（`node --test src/gomoku/rules.test.js`）；第二个源码模块一出现它就是假绿，已实现那份记录的 `## Consequences` 里已经写明。
- 本次评审对 `src/gomoku/*` 是同源的。上面那些观察都是人工重跑的，但渲染判断仍然只有一双眼睛；缺的另一半，是第二位读者去看那两张截图。
- 页面文案只有中文，规则是自由规则：长连（六子）也算胜，连珠玩家会判它错。
- `delivery_check` 过去在不点名 `workspace` 时会空洞地通过；`559558a` 之后那条路径会走到项目层，没有 proof 就判红，证据一节的重跑展示了这一点。旧行为留在本记录里，作为它当初的发现，而不是对当前版本的描述。
