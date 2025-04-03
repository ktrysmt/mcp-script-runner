import subprocess
import json
import os
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("mcp-script-runner")

cmd_dir = os.getenv("COMMAND_DIRECTORY", "commands/")


async def exec_command(command: str) -> str:
    """execute shell command
        スクリプトファイルをコマンドとして実行する
        各ファイルの一行目にはシェバンが記載されているため直接ファイル実行が可能である
        Args:
            command: "script_file_name"
    """

    # permissionがない場合は付与する
    if not os.access(cmd_dir + command, os.X_OK):
        try:
            os.chmod(cmd_dir + command, 0o755)
        except OSError as e:
            return json.dumps({"error": f"Failed to set execute permission: {e}"})

    result = subprocess.run(
        f"{cmd_dir}{command}",
        shell=True,
        capture_output=True,
        text=True
    )
    return json.dumps(
        {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        },
        ensure_ascii=False
    )


async def list_commands() -> str:
    """list all command names"""
    commands = []
    if not os.path.isdir(cmd_dir):
        return json.dumps({"error": f"Command directory '{cmd_dir}' not found."})
    try:
        for file in os.listdir(cmd_dir):
            if os.path.isfile(os.path.join(cmd_dir, file)):
                commands.append(file)
    except Exception as e:
        return json.dumps({"error": f"Error listing commands: {e}"})
    return json.dumps(commands, ensure_ascii=False)


def main():
    mcp.tool()(exec_command)
    mcp.tool()(list_commands)
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
