import os
import re


def remove_numbers_from_headings(file_path):
    """删除MD文件标题中的所有数字编号（包括所有变体）"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.readlines()

    modified = False
    for i, line in enumerate(content):
        # 匹配所有变体：数字+点/纯数字/多级编号，有无空格均可
        # 示例：
        # ### 1.2.标题 → ### 标题
        # ## 3 标题 → ## 标题
        # # 2标题 → # 标题
        match = re.match(r"^(#{1,6})\s*(?:\d+[.\s]*)+(.*)", line)
        if match:
            new_line = f"{match.group(1)} {match.group(2).lstrip()}\n"
            content[i] = new_line
            modified = True

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(content)
        print(f"已处理: {file_path}")


def process_directory(directory):
    """递归处理目录下的所有MD文件"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                remove_numbers_from_headings(file_path)


if __name__ == "__main__":
    zh_directory = "en"
    if os.path.exists(zh_directory):
        process_directory(zh_directory)
        print("处理完成！")
    else:
        print(f"错误：目录 '{zh_directory}' 不存在")
