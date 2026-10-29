# phm-mcp-server

**Deterministic physics plausibility tools for MCP clients** (Claude
Desktop, Cursor, Cline, and any Model Context Protocol host).

Three offline, deterministic checkers — zero network calls, zero model
calls, pure standard-library rules from the [phm-lite-check](https://github.com/PHM-Audit/phm-lite-check)
offline subset of the PHM engine:

| Tool | Checks |
|------|--------|
| `physics_text_check` | unit consistency, speed-of-light limit, probability ranges, kinematics in LLM text |
| `physics_quantity_check` | one value vs physical law |
| `robotics_data_check` | quaternion normalization, timestamp sanity, NaN/Inf, unit annotation in robotics records |

These checks are necessary, not sufficient: a PASS verdict does not imply
correctness. Not affiliated with or endorsed by Anthropic, OpenAI, or the
MCP project; adapters are community-provided.

## Claude Desktop setup

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "phm-physics-check": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {}
    }
  }
}
```

Prerequisites:

```bash
pip install mcp
pip install git+https://github.com/PHM-Audit/phm-lite-check
```

## Example tool call

```json
{"tool": "physics_text_check", "args": {"text": "confidence 1.8 of success."}}
→ {"verdict": "FAIL", "violations": [{"rule": "probability_out_of_range",
   "detail": "Probability 1.8 outside [0, 1]"}], "engine": "PHM-Lite"}
```

## Scope

Offline deterministic subset only (proprietary deep checks excluded).
Python >= 3.10, deps: `mcp` + `phm-lite-check` (both pip-installable).
