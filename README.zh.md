# agent-workflow-demo

[English](README.md) | 中文

一套"拷贝式"工作流套件：十一站生命周期、可执行闸门、中英成对文档。本仓库按**最小档**运行它，因此发布、演化、退役、否决记录与事故复盘都是"声明的缺席"，而不是已安装。

## 去哪找什么

- 每一站产出什么、由哪条闸门判定：[dev/README.md](dev/README.zh.md)
- 文档怎么写、怎么预算、怎么发布：[docs/README.md](docs/README.zh.md)
- agent 加载的常驻规则，以及唯一的命令清单：[AGENTS.md](AGENTS.md)

## 跑闸门

```sh
python3 tools/check-invariants.py --self-test   # the checks can fail
python3 tools/check-invariants.py               # the conventions hold
python3 tools/pair-docs.py --check              # every pair is in step
python3 tools/gen-docs.py --check               # the generated page is current
python3 tools/run-evidence.py --check           # every declared command resolves
python3 -m unittest discover -s tests           # the kit's own contract tests
```
