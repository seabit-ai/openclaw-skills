#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path


def now_local_iso_ms():
    # local time with milliseconds
    dt = datetime.now().astimezone()
    base = dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    tz = dt.strftime('%Z')
    return f"{base} {tz}".strip()


def resolve_workspace_auto():
    env_ws = os.environ.get('OPENCLAW_WORKSPACE')
    if env_ws:
        return Path(env_ws).expanduser()

    # Try: openclaw config (best effort)
    try:
        out = subprocess.check_output(['openclaw', 'config', 'get', 'workspace'], stderr=subprocess.DEVNULL, text=True).strip()
        if out:
            return Path(out).expanduser()
    except Exception:
        pass

    # Common fallbacks
    for p in ['~/.openclaw/workspace', '/opt/openclaw-data/workspace']:
        pp = Path(p).expanduser()
        if pp.exists():
            return pp

    # Last resort: current dir
    return Path.cwd()


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s or 'notes'


from typing import Optional


def ensure_file(path: Path, header: Optional[str] = None):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text((header or '') + ('\n' if header else ''), encoding='utf-8')


def append_daily_pin(daily_path: Path, title: str, body_md: str, when: str, ref_path: Optional[str]):
    ensure_file(daily_path, header=f"# {daily_path.stem}")

    lines = []
    lines.append("")
    lines.append(f"## Pin: {title}")
    lines.append("")
    lines.append(f"**时间**：{when}")
    lines.append("")
    lines.append(body_md.strip())
    if ref_path:
        lines.append("")
        lines.append(f"详见：`{ref_path}`")
    lines.append("")

    with daily_path.open('a', encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")


def write_investigation(path: Path, title: str, body_md: str, when: str):
    ensure_file(path)
    content = f"# {title}\n\n**创建时间**：{when}\n\n{body_md.strip()}\n"
    path.write_text(content, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default='')
    ap.add_argument('--workspace', default='auto')
    ap.add_argument('--create-investigation', default='auto', choices=['auto', 'yes', 'no'])
    ap.add_argument('--title', default='')
    args = ap.parse_args()

    ws = resolve_workspace_auto() if args.workspace == 'auto' else Path(args.workspace).expanduser()

    today = datetime.now().astimezone().strftime('%Y-%m-%d')
    daily = ws / 'memory' / f'{today}.md'

    user_text = (args.input or '').strip()
    # Allow callers to pass literal "\\n" sequences.
    user_text = user_text.replace('\\r\\n', '\n').replace('\\n', '\n')

    # Heuristics
    want_investigation = False
    if args.create_investigation == 'yes':
        want_investigation = True
    elif args.create_investigation == 'no':
        want_investigation = False
    else:
        # auto
        if any(k in user_text.lower() for k in ['investigation', '单独', '独立', '长文', '复杂', 'postmortem', '复盘']):
            want_investigation = True

    # Title
    title = args.title.strip()
    if not title:
        if user_text:
            title = user_text.splitlines()[0][:60]
        else:
            title = '自动总结（请在正文中补充/改写）'

    when = now_local_iso_ms()

    # Body: keep minimal; agent can pass fully formed markdown.
    if user_text:
        body = user_text
    else:
        body = (
            "- **背景/目标**：\n"
            "- **现象**：\n"
            "- **关键证据**：\n"
            "- **根因**：\n"
            "- **修复/验证**：\n"
            "- **后续/TODO**：\n"
        )

    ref = None
    if want_investigation:
        slug = slugify(title)
        inv = ws / 'research' / today / f'investigation-{slug}.md'
        write_investigation(inv, title=title, body_md=body, when=when)
        ref = str(inv)
        # For daily note, keep shorter and point to inv
        daily_body = (
            "- **摘要**：已创建独立调查笔记（可持续更新）。\n"
            "- **状态**：进行中/已收敛（按需改）\n"
        )
        append_daily_pin(daily, title=title, body_md=daily_body, when=when, ref_path=ref)
    else:
        append_daily_pin(daily, title=title, body_md=body, when=when, ref_path=None)

    print(f"OK\nDAILY_NOTE={daily}\nINVESTIGATION_NOTE={ref or ''}")


if __name__ == '__main__':
    main()
