# 移除封面、免责声明等内容

import glob

if __name__ == '__main__':
    docs = glob.glob("**/*.md", recursive=True)
    # docs = glob.glob("zh/02_applications/business_poc/K230_场景实战_智能门锁.md")
    for d in docs:
        with open(d, 'rb') as f:
            text = f.read()
        pos1 = text.find(b'![cover]')
        if pos1 < 0:
            print(f"{d} does not match")
            continue
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
            print(f"{d} does not match")
            continue
        with open(d, 'wb') as f:
            f.write(text[:pos1])
            f.write(text[pos2:])
