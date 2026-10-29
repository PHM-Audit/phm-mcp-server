#!/usr/bin/env python3
"""PHM MCP server -- deterministic physics plausibility tools for MCP clients.

Exposes the phm-lite-check offline subset as Model Context Protocol tools:
  - physics_text_check(text)        scan text for implausible numeric claims
  - physics_quantity_check(v, unit) one quantity against physical law
  - robotics_data_check(record)     robotics/embodied-AI dataset record

Zero-external-service: all checks run locally, deterministic, offline subset
of the PHM engine (proprietary methods excluded).
Requires: mcp (pip install mcp) and phm-lite-check (pip install from GitHub).
Run: python server.py   (stdio transport, Claude Desktop standard)
"""
import json

from mcp.server.fastmcp import FastMCP

from phm_lite_check import check_text, check_quantity
from phm_lite_check.robotics import check_robotics_record

mcp = FastMCP("phm-physics-check")


@mcp.tool()
def physics_text_check(text: str) -> str:
    """Check LLM-generated text for physically implausible numeric claims
    (deterministic offline checker).

    Args:
        text: any text containing quantities with units, probabilities,
              kinematic claims, e.g. "the missile flies at 450 km/h,
              confidence 1.8"

    Returns:
        JSON: verdict PASS/WARN/FAIL + structured violations
    """
    return json.dumps(check_text(text))


@mcp.tool()
def physics_quantity_check(value: float, unit: str) -> str:
    """Check one numeric value against physical law (deterministic offline checker).

    Args:
        value: the numeric value, e.g. 299792459
        unit:  unit string, e.g. "m/s", "km/h", "degC"

    Returns:
        JSON: verdict PASS/WARN/FAIL + violations
    """
    vs = check_quantity(value, unit)
    worst = "PASS"
    if any(v.severity == "FAIL" for v in vs):
        worst = "FAIL"
    elif any(v.severity == "WARN" for v in vs):
        worst = "WARN"
    return json.dumps({"verdict": worst,
                       "violations": [v.to_dict() for v in vs],
                       "engine": "PHM-Lite", "deterministic": True})


@mcp.tool()
def robotics_data_check(record_json: str) -> str:
    """Check a robotics / embodied-AI dataset record for physical plausibility
    (deterministic offline checker).

    Args:
        record_json: JSON object with optional keys 'quaternion'/'quaternions'
                     (list of [w,x,y,z]), 'timestamps' (numeric list),
                     'units' (dict), plus numeric arrays to NaN/Inf-scan

    Returns:
        JSON: verdict PASS/WARN/FAIL + violations + summary
    """
    try:
        payload = json.loads(record_json)
    except json.JSONDecodeError as e:
        return json.dumps({"verdict": "FAIL",
                           "violations": [{"rule": "input_format", "severity": "FAIL",
                                           "detail": f"invalid JSON: {e}"}]})
    return json.dumps(check_robotics_record(payload))


if __name__ == "__main__":
    mcp.run()
