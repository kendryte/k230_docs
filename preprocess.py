# 移除封面、免责声明等内容

import glob

if __name__ == '__main__':
    docs = glob.glob("**/*.md", recursive=True)
    # docs = glob.glob("zh/03_other/K230_SDK_版本说明.md")
    for d in docs:
        with open(d, 'rb') as f:
            text = f.read()
        # 删除封面
        pos1 = text.find(b'![cover]')
        if pos1 < 0:
            print(f"{d} does not match ![cover]")
        else:
            pos2 = text.find(b'[TOC]')
            if pos2 < 0:
                pos2 = text.find(b'[toc]')
                if pos2 < 0:
                    pos3 = text.find(b'page-break-after')
                    if pos3 >= 0:
                        pos2 = text.find(b'page-break-after', pos3 + 16)
                        if pos2 >= 0:
                            pos2 += 31
                        else:
                            pos2 = pos3 + 31
                else:
                    pos2 += 5
            else:
                pos2 += 5
            if pos1 < 0 or pos2 < 0:
                print(f"{d} does not match ![cover]")
            else:
                text = text[:pos1] + text[pos2:]
        # 删除前言
        pos1 = text.find('## 前言'.encode('utf-8'))
        pos2 = text.find(b'\n## ', pos1 + 10)
        if pos2 < 0:
            pos2 = text.find(b'\r## ', pos1 + 10)
        if pos1 < 0 or pos2 < 0:
            print(f"{d} does not match 前言")
        else:
            text = text[:pos1] + text[pos2:]
        with open(d, 'wb') as f:
            f.write(text)
