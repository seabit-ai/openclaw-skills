---
name: ctx
description: Show a compact context token summary for the current session. Use when user asks for context size, token usage, how full the context window is, or types /ctx.
user-invocable: true
---

# Context Summary Skill

Show a compact breakdown: System tokens / Conversation tokens / Total vs limit.

## Steps

1. Call `session_status` → get `totalTokens` (total cached context) and `contextTokens` (limit).

2. Run these shell commands (can run in parallel with step 1):

   Get current timestamp with ms (cross-platform):
   ```bash
   python3 -c "from datetime import datetime; import time; tz=time.strftime('%Z'); now=datetime.now(); print(now.strftime('%Y-%m-%d %H:%M:%S.') + f'{now.microsecond//1000:03d}' + ' ' + tz)"
   ```

   Auto-detect workspace and get total file sizes (in bytes):
   ```bash
   python3 - << 'EOF'
import os, subprocess, json

# Try to detect workspace path dynamically
def find_workspace():
    # 1. Check env var
    if os.environ.get('OPENCLAW_WORKSPACE'):
        return os.environ['OPENCLAW_WORKSPACE']
    # 2. Parse openclaw config output
    try:
        out = subprocess.check_output(['openclaw', 'config'], text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            if 'workspace:' in line:
                path = line.split('workspace:')[-1].strip().strip('│').strip()
                return os.path.expanduser(path)
    except Exception:
        pass
    # 3. Common fallback paths (in order)
    candidates = [
        os.path.expanduser('~/.openclaw/workspace'),
        '/opt/openclaw-data/workspace',
    ]
    for p in candidates:
        if os.path.isdir(p) and os.path.exists(os.path.join(p, 'AGENTS.md')):
            return p
    return os.path.expanduser('~/.openclaw/workspace')

workspace = find_workspace()
files = ['AGENTS.md','SOUL.md','TOOLS.md','IDENTITY.md','USER.md','MEMORY.md','HEARTBEAT.md']
total = sum(os.path.getsize(os.path.join(workspace, f))
            for f in files if os.path.exists(os.path.join(workspace, f)))
print(total)
EOF
   ```

3. Calculate:
   - `workspace_tok` = bytes_total / 4  (rough chars→tokens)
   - `fixed_overhead` = 8100  (tools schemas ~3800 + tool summaries ~1500 + skills list ~1000 + system boilerplate ~1800)
   - `sys_tok` = workspace_tok + fixed_overhead
   - `conv_tok` = totalTokens - sys_tok  (conversation history + outputs)
   - `pct_total` = totalTokens / contextTokens * 100

4. Reply in this exact format (no extra prose):

```
📊 Context
─────────────────────────────
System:       {sys_tok} tok
Conversation: {conv_tok} tok
─────────────────────────────
Total: {totalTokens} / {contextTokens}  ({pct_total:.1f}%)

🧠 {model}  ·  🔑 {auth}
🧮 {tokens_in} in / {tokens_out} out  ·  🧹 Compactions: {compactions}
🕒 {YYYY-MM-DD HH:MM:SS.mmm TZ}
```

Use commas for thousands (e.g. `15,600`). Round pct_total to 1 decimal.
Pull model, auth, tokens in/out, compactions from the session_status output.
