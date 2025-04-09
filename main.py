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

    full_path = os.path.join(cmd_dir, command)

    # permissionがない場合は付与する
    if not os.access(full_path, os.X_OK):
        try:
            os.chmod(full_path, 0o755)
        except OSError as e:
            return json.dumps({"error": f"Failed to set execute permission: {e}"})

    result = subprocess.run(
        full_path,
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


def extract_description(script_path):
    """
    指定スクリプトの2行目コメントからdescriptionを抽出
    """
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) < 2:
                return ""
            return lines[1].strip()
    except Exception:
        pass
    return ""


def main():
    # commands配下のすべてのファイルをツール登録
    if os.path.isdir(cmd_dir):
        for filename in os.listdir(cmd_dir):
            script_path = os.path.join(cmd_dir, filename)
            if not os.path.isfile(script_path):
                continue

            description = extract_description(script_path)

            # 各shell script実行用ツールをdescription付きで登録
            def gen_tool(cmd_name):
                async def run_shell():
                    return await exec_command(cmd_name)
                return run_shell

            mcp.tool(description=description, name=filename)(
                gen_tool(filename))

    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
