import re
import os


def remove_number_prefix_from_links(file_path):
    """
    处理Markdown文件，移除链接锚点中的数字前缀
    示例：
    - [xxx](#211-xxx) → [xxx](#xxx)
    - [yyy](#1.1-yyy) → [yyy](#yyy)
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 正则表达式匹配带编号的链接
    pattern = re.compile(r"(\[[^\]]+\]\(#)(?:\d+\.)*\d+-([^\)]+\))", re.IGNORECASE)

    # 替换为无编号的链接
    new_content = pattern.sub(r"\1\2", content)

    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"已处理文件: {file_path}")
    else:
        print(f"无需处理: {file_path}")


def process_directory(directory):
    """递归处理目录下的所有Markdown文件"""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                remove_number_prefix_from_links(file_path)


if __name__ == "__main__":
    target_dir = "en"  # 修改为你的文档目录
    if os.path.exists(target_dir):
        process_directory(target_dir)
        print("处理完成！")
    else:
        print(f"错误：目录 '{target_dir}' 不存在")
