FROM python:3.12-slim

# git is required by pip to install phm-lite-check from GitHub
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml server.py ./

# Installs mcp, numpy and phm-lite-check (pinned via pyproject dependency)
RUN pip install --no-cache-dir .

# stdio transport (MCP standard) — Glama/Smithery introspection compatible
ENTRYPOINT ["python", "server.py"]
