import os
import json

def convert_json_to_text(data, indent=0):
    """辞書やリストを自然文テキストに再帰的に変換"""
    lines = []
    indent_space = " " * indent

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{indent_space}{key}：")
                lines.append(convert_json_to_text(value, indent + 2))
            else:
                lines.append(f"{indent_space}{key}：{value}")
    elif isinstance(data, list):
        for i, item in enumerate(data, 1):
            lines.append(f"{indent_space}- {convert_json_to_text(item, indent + 2)}")
    else:
        lines.append(f"{indent_space}{data}")

    return "\n".join(lines)


def convert_all_json_in_dir(input_dir="."):
    """指定ディレクトリ内の .json ファイルをすべて .txt に変換"""
    files = [f for f in os.listdir(input_dir) if f.endswith(".json")]

    if not files:
        print("変換対象のJSONファイルが見つかりません。")
        return

    for filename in files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(input_dir, filename.replace(".json", ".txt"))

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            text_content = convert_json_to_text(json_data)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text_content)

            print(f"✅ {filename} → {os.path.basename(output_path)} に変換しました。")

        except Exception as e:
            print(f"⚠️ {filename} の変換中にエラーが発生しました: {e}")


if __name__ == "__main__":
    print("📘 カレントディレクトリ内のJSONを自然文テキストに変換します...")
    convert_all_json_in_dir(".")
