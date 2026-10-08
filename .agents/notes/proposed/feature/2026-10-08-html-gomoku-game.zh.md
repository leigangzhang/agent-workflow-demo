# Proposal: 同屏双人的五子棋网页

[English](2026-10-08-html-gomoku-game.md) | 中文

Status: proposed
Date: 2026-10-08
Class: feature

## 问题

两个人坐在同一台机器前，想下一盘五子棋。今天最短的路径是一条网页搜索结果加一个塞满广告的页面，或者一个安装步骤比一盘棋还长的程序；本仓库里没有任何东西能下。

这件事的代价不止一盘棋。本仓库存在的意义，是在一个还没有代码的项目上跑完这套生命周期，而最小档那份决策在收束时承诺过：它的第一个 feature 会在这里被提案、决策、验证与评审。提案之后的每一个站点——契约、验证、评审——至今只在文档上演练过，从没面对过一个程序，面对过浏览器展示给人的行为。在一个真实模块落地之前，「这些检查（check）是有效的」只是一句关于 Markdown 的话。

## 提案

这个 feature 是一个页面加一个模块，二者都不带依赖，再加一条证明该模块的测试通道。

- `src/gomoku/rules.js` —— 规则引擎。一个经典脚本，对外只发布一个全局名 `Gomoku`，并用一行带守卫的语句把同一个对象交给 Node（`if (typeof module !== "undefined") module.exports = Gomoku;`）。它不碰 DOM，也不定义第二个全局名。它的全部接口就是 `Gomoku.SIZE`（15）、`Gomoku.start(size)`、`Gomoku.place(game, row, col)` 与 `Gomoku.winner(game)`。一局棋是一个普通对象——`{ size, board, turn, winner, moves }`——而 `place` 返回一个新对象：`{ ok: true, game }` 或 `{ ok: false, reason }`，其中 `reason` 取 `out-of-range`、`occupied`、`finished` 之一。胜负判定只读刚落下的这一子穿过的那四条线。
- `src/gomoku/index.html` —— 页面。一个经典的 `<script src="rules.js">`、一张 15×15 的真实 `<button>` 交叉点网格、一行状态、一个重开按钮。所有用户可见文案都来自同一个 `STRINGS` 映射。点击交叉点就在该点落子；点击已被占用的点不改变任何东西；分出胜负或和棋之后，棋盘在重开之前不再接受落子。
- `src/gomoku/rules.test.js` —— 黄金回放，由 Node 自带的运行器执行。Node 本来就装在本仓库的开发机器上，而页面在浏览器里本来也需要一个 JavaScript 运行时，所以这条通道的成本是声明它，而不是安装它。不会新增 `package.json`，也没有依赖要装。
- `tools/workflow.json` —— `source` 改动面（surface）的证据（evidence）条目今天还是占位串 `<the narrowest owning test for the changed module>`。这次改动把它换成真实命令 `node --test src/gomoku/rules.test.js`，并把同一条命令加进 `tests` 改动面，于是这条 JavaScript 通道被声明在 `change-scope.py` 与 `run-evidence.py` 本来就会读的地方。
- `README.md`、`README.zh.md`、`README.i18n.yaml` —— 在 `## Where to go` 下加一条指向页面的条目，并重新记录这一对。

规则采用常见的一套：15×15，黑先，横、竖、斜任一方向连成五子或更多即胜；长连（六子及以上）也算胜；棋盘下满而无五连则为和棋。交叉点用按钮而不是 canvas 像素，因此页面可以用键盘操作，测试也按元素寻址而不是按坐标。

一个待定问题，v1 已按此定，且改起来很便宜：页面文案只有中文，因为提出需求的人写中文。收在一个映射里，日后要加英文侧只是改一行。

## 曾考虑的替代方案

**把规则内联进一个自包含的 `index.html`。** 否决：这样一来胜负规则只能经由浏览器触达，单元层就得配一个浏览器驱动和一个安装步骤。拆出一个经典脚本，规则就能被一个普通 JavaScript 运行时直接测。

**用 ES 模块，靠 `python3 -m http.server` 提供服务。** 否决：浏览器拒绝在 `file://` 下导入 `type="module"`，因为页面的源是 `null`。模块图会让人在开局之前先起一个服务、敲一条终端命令，而双击文件是从「我拿到了页面」到「我在下棋」最短的一条路。

**只保留 Playwright 或无头 Chrome 一条通道。** 按同样的理由再高一层否决：它会引入本仓库刻意从未有过的安装步骤，而且要拿浏览器去验证一个普通运行时就能跑的纯函数。

**用 Python 重写胜负规则再测它。** 否决：同一条规则的两份实现就是两个事实，迟早漂移。黄金回放必须打在实际交付的 JavaScript 上。

**用 canvas 绘制、按像素做命中测试。** 否决：它用可寻址的元素换来了页面与每条测试里的坐标算术，还丢掉了键盘可达性。

**加一个电脑对手，或用带禁手的连珠规则。** v1 否决：需求方要的是同屏双人；禁手规则会改动胜负判定，还需要它自己的验收标准。等第二位玩家提出时再重审。电脑对手那一半已另有提案：[为五子棋页面加一个电脑对手](2026-10-08-gomoku-computer-opponent.zh.md)；禁手那一半不变。

## 验收标准

- [A1] `tests` —— `node --test src/gomoku/rules.test.js` 覆盖横、竖、两条斜线四个方向的胜利、长连、一个必须判不赢的断开四子、落在已占交叉点、越界落子、终局后落子、下满成和，以及 `place` 不修改入参；删掉任一方向的判定，这条通道就判红。
- [A2] `source` —— 从 `file://` 直接打开 `src/gomoku/index.html`，不起服务、不发网络请求，就能看到 15×15 的棋盘；一段脚本化的真实交叉点点击序列最终显示胜利信息；点击已被占用的交叉点后棋盘不变；重开后棋盘为空。
- [A3] `i18n` —— `python3 tools/pair-docs.py --check` 报出这份记录（record）的三个兄弟文件齐全且同步，并在页面链接补进两侧之后，继续让 `README.md`、`README.zh.md` 与一致性记录（consistency record）`README.i18n.yaml` 保持同档。
- [A4] `workflow` —— `tools/workflow.json` 把 `node --test src/gomoku/rules.test.js` 声明为 `tests` 与 `source` 改动面上的可运行证据，于是 `python3 tools/run-evidence.py --check` 能解析它，实跑记下的是 PASS 或 FAIL，而不是一条人工条目。

## 风险

- 本仓库的套件只用标准库 Python，Node 由此成为第二种运行时。套件那条规矩管的是要安装的依赖，而页面在浏览器里本来就需要 JavaScript 运行时，但边界确实移动了：Node 缺席的环境里，`run-evidence.py` 报的是 UNKNOWN，那是工具问题，读者不能把它读成通过。若「贡献者没装 Node」成为真实情况就重审这条；退路是把浏览器里的观察标成未验证，那更弱，必须照实写明。
- 把共享的 `source` 证据占位串换成一条具体命令，只在本仓库只有一个源码模块时成立。第二个模块一出现，这条命令就是假绿；到那时它必须长成按模块分派的映射，或者把改动面拆开。
- 自由规则下「五子或更多即胜」，遇到长连时连珠玩家会判它错。等有人要求禁手时重审，那要写一份新记录，而不是改这一份。
- 页面落在 `src/gomoku/`，此前没有任何改动面的模式点名过这个位置；`source` 今天匹配 `src/*`，所以不需要新增声明。页面一旦搬家，证据要跟着走，否则这条通道会静默地不再运行。

## 交付阶段

1. 规则引擎与它的通道 —— `src/gomoku/rules.js`、`src/gomoku/rules.test.js` 与 `tools/workflow.json` 里的证据条目；这一段能在完全没有页面的情况下落地并测通。
2. 页面与入口 —— `src/gomoku/index.html`、两侧 README 里的一条链接，以及收掉 [A2] 的那次浏览器观察。
