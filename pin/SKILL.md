---
name: pin
description: "把当前排查/讨论自动总结成一条可审计的笔记，并写入 memory/YYYY-MM-DD.md；必要时创建独立 investigation notes 并在 daily note 里引用。"
---

# /pin — 自动落盘（daily note + 可选独立调查笔记）

## 何时用
- 在一次排查/事故/设计讨论**收敛到关键结论**时，调用 `/pin` 把“发生了什么 / 证据 / 根因 / 修复 / 后续”写入 `memory/YYYY-MM-DD.md`。
- 如果排查很复杂、跨度很长：同时创建一个独立的 investigation notes 文件，并在 daily note 里加引用。

## 输入
- `/pin`（无参数）：由 agent **自动总结当前上下文**并落盘。
- `/pin <你提供的要点>`：把你提供的要点整理后落盘（仍保持模板化、可审计）。
- 约定：如你在输入里明确提到“创建独立笔记/单独文件/开一份 investigation notes”，则创建独立文件。

## 输出要求（写入内容模板）
写入 daily note 时，使用如下结构（尽量短，但可审计）：

- 标题：`## Pin: <一句话标题>`
- 时间：本地时间，精确到毫秒
- 小节（按需省略为空的项）：
  - **背景/目标**
  - **现象**
  - **关键证据**（命令 + 关键日志片段，1-3 条即可）
  - **根因**（明确、可验证；不确定就写“假设”）
  - **修复/验证**（做了什么 + 如何确认好了）
  - **后续/TODO**
- 若创建独立 investigation notes：
  - 在 daily note 里追加 `详见: <path>`
  - 独立文件里可更长，允许持续更新（非 append-only）。

## 文件落盘规则（必须执行）
- Daily note：`<workspace>/memory/YYYY-MM-DD.md`
  - 若不存在则创建
  - 允许同一天多次 `/pin`（多条 Pin 追加在文件末尾）

- 独立调查笔记（可选）：`<workspace>/research/YYYY-MM-DD/investigation-<slug>.md`
  - 用于复杂排查的长文档，允许反复改写、补充证据

## 实现（用 exec 运行脚本，避免手工写错路径）
1) 先确保脚本存在：`scripts/pin.py`
2) 用 `exec` 在 **gateway host** 运行（本机）:

```bash
python3 <this_skill_dir>/scripts/pin.py \
  --input "<用户输入或空>" \
  --create-investigation "auto" \
  --workspace "auto"
```

- `--workspace auto`：脚本按以下顺序定位 workspace：
  1) `OPENCLAW_WORKSPACE`
  2) 解析 `openclaw config` 输出（若可用）
  3) 回退：`~/.openclaw/workspace`、`/opt/openclaw-data/workspace`

## 注意
- 这是**可审计**的落盘：写完后要在聊天里回显：
  - 写入的文件路径
  - 新增的标题行（或前 3 行）
- 不要把 `SOUL.md/IDENTITY.md` 这类实例私有文件内容写进去。
