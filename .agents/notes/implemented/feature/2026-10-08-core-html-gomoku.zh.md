# Decision: 同屏双人的五子棋网页

[English](2026-10-08-core-html-gomoku.md) | 中文

Status: implemented
Date: 2026-10-08
Class: feature

## 问题

两个人坐在同一台机器前，想下一盘五子棋。最短的路径是一条网页搜索结果加一个塞满广告的页面，或者一个安装步骤比一盘棋还长的程序。

这件事的代价不止一盘棋。本仓库存在的意义，是在一个还没有代码的项目上跑完这套生命周期，而最小档那份决策在收束时承诺过：它的第一个 feature 会在这里被提案、决策、验证与评审。提案之后的每一个站点——契约、验证、评审——都只在文档上演练过，从没面对过一个程序，面对过浏览器展示给人的行为。在一个真实模块落地之前，「这些检查（check）是有效的」只是一句关于 Markdown 的话。

## 决策

这盘棋以一个页面加一个模块交付，二者都不带依赖，外加一条证明该模块的测试通道。

- `src/gomoku/rules.js` —— 规则引擎。一个经典脚本，在浏览器里设 `window.Gomoku`，在 Node 里给 `module.exports`，不碰 DOM。它的接口是 `Gomoku.SIZE`（15）、`Gomoku.start(size)`、`Gomoku.place(game, row, col)` 与 `Gomoku.winner(game)`。一局棋是 `{ size, board, turn, winner, moves }`：`board` 按行主序放着 `size * size` 个格子，每格是 `null`、`"black"` 或 `"white"`；`turn` 是轮到谁走，棋局结束后则是最后走的那一方；`winner` 是 `null`、`"black"`、`"white"` 或 `"draw"`；`moves` 按落子顺序列出棋子。`place` 返回新的一局，绝不改动传给它的那一局，并用 `{ ok: false, reason }` 拒绝一步棋，`reason` 取 `out-of-range`、`occupied` 或 `finished`。它只看刚落这一子穿过的那四条轴线来定胜负，所以一步棋的代价是那几条线的长度，而不是整张棋盘。黑先；连成五子或更多即胜，六子及以上的长连也算；棋盘下满而无五连为和棋。
- `src/gomoku/index.html` —— 页面。一个经典的 `<script src="rules.js">`、`role="grid"` 下 15 行各 15 个 `<button>` 交叉点、一行状态、一个重开按钮。所有用户可见文案都来自同一个 `STRINGS` 映射，只有中文。每次点击都交给 `Gomoku.place`，被拒绝就什么也不画，因此页面自己不持有任何规则：合法性、轮次与胜负全部来自引擎，而双人对局的轮次从不会自己往前走。
- `src/gomoku/rules.test.js` —— 黄金回放，由 Node 自带的运行器执行：`node --test src/gomoku/rules.test.js`。没有 `package.json`，也没有依赖要装。
- `tools/workflow.json` —— `tests` 与 `source` 两个改动面（surface）都把 `node --test src/gomoku/rules.test.js` 声明为可运行证据（evidence）。`source` 改动面上原先那个占位串已经没有了。
- `README.md`、`README.zh.md`、`README.i18n.yaml` —— 两侧 `## Where to go` 下各有一条指向页面的条目，并重新记录了这一对。

页面从 `file://` 就能打开：拿到文件与开始下棋之间，没有服务、没有网络请求、也没有构建步骤。

## 曾考虑的替代方案

**把规则内联进一个自包含的 `index.html`。** 否决：这样一来胜负规则只能经由浏览器触达，单元层就得配一个浏览器驱动和一个安装步骤。拆出一个经典脚本，规则就能被一个普通 JavaScript 运行时直接测，而现在的测试通道正是这么做的。

**用 ES 模块，靠 `python3 -m http.server` 提供服务。** 否决：浏览器拒绝在 `file://` 下导入 `type="module"`，因为页面的源是 `null`。模块图会让人在开局之前先起一个服务、敲一条终端命令，而双击文件是从「我拿到了页面」到「我在下棋」最短的一条路。

**把 Playwright 或无头 Chrome 作为本仓库的测试通道。** 否决：它会引入本仓库刻意从未有过的安装步骤，而且要拿浏览器去验证一个普通运行时就能跑的纯函数。后果是写明的、不是藏起来的：页面自身的行为靠人工观察，`## 验证` 把它标成 `unpinned`。

**用 Python 重写胜负规则再测它。** 否决：同一条规则的两份实现就是两个事实，迟早漂移。黄金回放打的就是实际交付的 JavaScript。

**用 canvas 绘制、按像素做命中测试。** 否决：它用可寻址的元素换来了页面与每条测试里的坐标算术，还丢掉了键盘可达性。交付的按钮可以用键盘操作，而测试寻址的就是一次点击。

**加一个电脑对手，或用带禁手的连珠规则。** 本记录否决：需求方要的是同屏双人；禁手规则会改动胜负判定，还需要它自己的验收标准。对手那一半现在由[给五子棋页面加一个电脑对手](../../proposed/feature/2026-10-08-core-computer-opponent.zh.md)提案；禁手那一半不变。

## 后果

本仓库有了一个可玩的产物，也有了第一条「程序行为会变红」的通道。引擎不必经浏览器就能测，页面不持有任何规则，拿到目录的人就拿到了这盘棋。

- Node 在此成为第二种运行时，而本仓库的套件只用标准库 Python。页面在浏览器里本来就需要 JavaScript 运行时，但边界确实移动了：Node 缺席的环境里，`run-evidence.py` 报的是 UNKNOWN，那是工具问题，读者不能把它读成通过。退路是把浏览器里的观察标成未验证，那更弱。
- `source` 改动面只承载一条具体命令，这只在本仓库只有一个源码模块时成立。第二个模块一出现，这条命令就是假绿；到那时它必须长成按模块分派的映射，或者把改动面拆开。
- 自由规则下「五子或更多即胜」，遇到长连时连珠玩家会判它错。推翻它要写一份新记录，而不是改这一份。
- 页面文案只有中文，因为提出需求的人写中文。收在一个映射里，日后要加英文侧只是改一行。
- 这份记录里与 DOM 有关的一半，没有任何命令钉住：`source` 通道跑的是引擎，不是页面。浏览器拿引擎做什么，靠人工观察，而 `run-evidence.py` 从不把人工条目算作已验证。
- 页面落在 `src/gomoku/`，此前没有任何改动面的模式点名过这个位置；`source` 匹配 `src/*`，所以不需要新增声明。页面一旦搬家，证据要跟着走，否则这条通道会静默地不再运行。

重审时机：当第二个模块让 `source` 通道变成假绿时，当不能假定贡献者机器上有 Node 时，当有人要求禁手规则或要求第二套语言文案时，或者当[对手那份记录](../../proposed/feature/2026-10-08-core-computer-opponent.zh.md)的第 2 阶段把页面行为变成仓库必须运行、而不是观察的东西时。

## 验证

- [A1] `tests` —— `node --test src/gomoku/rules.test.js` 回放四个方向的胜利、长连、一个必须判不赢的断开四子、落在已有子的交叉点、越界的点、终局后的落子、下满成和，以及 `place` 的纯性。每个方向各自一条用例，所以从引擎里删掉任一方向，恰好那一条判红，实跑记 PASS。
- [A2] `source` —— 页面自身的行为是 `unpinned`：这个改动面上的通道跑的是 `node --test src/gomoku/rules.test.js`，它够不到 DOM，而本仓库不跑浏览器驱动。代替命令的那次观察，是在 `file://` 下的真实页面上人工做的：15 行共 225 个交叉点、黑方五次点击落到可见的胜利信息、点击已占交叉点后棋盘不变、终局后再点被拒、重开清空棋盘、聚焦一个交叉点后按 Enter 可以落子、页面不发任何网络请求。它是一条人工条目，`run-evidence.py` 永不把它报成通过。那次观察的两张截图就存在证据记录旁边：`dev/evidence/2026-10-08-core-html-gomoku-headless.png` 与 `dev/evidence/2026-10-08-core-html-gomoku-win.png`。
- [A3] `i18n` —— `python3 tools/pair-docs.py --check` 报出这份记录（record）的三个兄弟文件齐全且同步，并让 `README.md`、`README.zh.md` 与 `README.i18n.yaml` 随两侧都有的那条游戏链接保持同档。
- [A4] `workflow` —— `tools/workflow.json` 把 `node --test src/gomoku/rules.test.js` 声明在 `tests` 与 `source` 改动面上，因此 `python3 tools/change-scope.py --base origin/main` 对 `src/gomoku/` 的改动会同时点名这两个改动面，而 `python3 tools/run-evidence.py --base origin/main` 会真的跑这条通道并记 PASS，而不是一条人工条目。
