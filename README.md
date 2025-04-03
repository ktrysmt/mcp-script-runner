# mcp-script-runner

## prerequisites

- python: e.g. `mise install python@3.13 && mise use python@3.31 -g`
- uv: e.g. `brew install uv`

## configure

```
git clone https://github.com/ktrysmt/mcp-script-runner
cd ./mcp-script-runner
uv sync
```

and add `mcp.json` to your mcp config like this:

```
{
  "mcpServers": {
    "mcp-script-runner": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-script-runner",
        "run",
        "main.py"
      ]
    }
  }
}
```

Change command dir:

```
{
  "mcpServers": {
    "mcp-script-runner": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-script-runner",
        "run",
        "main.py"
      ],
      "env": {
        "COMMAND_DIRECTORY": "/path/to/your/dir"
      }
    }
  }
}
```

Use dotenv:

```
cd ./mcp-script-runner
$EDITOR .env
```

## add a tool

```
cd ./mcp-script-runner
$EDITOR ./commands/command_name.sh
```

and reload the mcp.

