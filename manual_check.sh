#!/usr/bin/env bash
# manual_check.sh —— 跑本地预提交检查，与 CI 的 lint 阶段完全一致
#
# 用法（从仓库根目录）:
#   ./manual_check.sh                  # 跑全部两项检查
#   ./manual_check.sh lint             # 只跑 markdownlint
#   ./manual_check.sh link             # 只跑 lychee
#   ./manual_check.sh lint link        # 跑全部（等价于无参数）
#
# 行为说明:
#   - 即使某一项检查失败也会继续跑下一项，最后统一汇总（你一次看到所有问题）
#   - 退出码: 0 全部通过 / 1 有失败 / 2 docker 缺失 / 3 参数错误
#   - 这两个检查和 CI 的 lychee_link_check + markdown_lint job 跑的是同一组 docker 镜像

set -u  # 故意不开 -e，见上面的「行为说明」

# --- 颜色（终端不是 tty 时自动降级） --------------------------------------
if [ -t 1 ]; then
    C_RED='\033[0;31m'
    C_GREEN='\033[0;32m'
    C_YELLOW='\033[1;33m'
    C_NC='\033[0m'
else
    C_RED=''; C_GREEN=''; C_YELLOW=''; C_NC=''
fi

# --- 切到脚本所在目录（= 仓库根） ---------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# --- 解析参数（默认全跑） -----------------------------------------------
RUN_LINT=0
RUN_LINK=0
if [ $# -eq 0 ]; then
    RUN_LINT=1
    RUN_LINK=1
else
    for arg in "$@"; do
        case "$arg" in
            lint) RUN_LINT=1 ;;
            link) RUN_LINK=1 ;;
            -h|--help)
                sed -n '2,15p' "$0"
                exit 0
                ;;
            *)
                echo -e "${C_RED}未知参数: $arg${C_NC}" >&2
                echo "支持: lint | link | (无参数 = 全部)" >&2
                exit 3
                ;;
        esac
    done
fi

# --- docker 依赖检查 ----------------------------------------------------
if ! command -v docker >/dev/null 2>&1; then
    echo -e "${C_RED}ERROR: docker 不在 PATH 中，无法跑检查。${C_NC}" >&2
    exit 2
fi

# --- 镜像（与 .gitlab-ci.yml 完全保持一致） -----------------------------
MARKDOWN_IMAGE="ai.b-bug.org:5000/markdown:latest"
LYCHEE_IMAGE="ai.b-bug.org:5000/huangziyi/lychee:latest"
LYCHEE_UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# --- 各检查的退出码（用变量收集，最后统一判断） ------------------------
LINT_EXIT=0
LINK_EXIT=0

# --- 1. markdownlint ----------------------------------------------------
if [ "$RUN_LINT" -eq 1 ]; then
    echo
    echo -e "${C_YELLOW}==== [1/2] markdownlint ====${C_NC}"
    docker run --rm \
        -v "$(pwd)":/workspace \
        -w /workspace \
        "$MARKDOWN_IMAGE" \
        /bin/sh -c "find . -name '*.md' -print0 | xargs -0 markdownlint-cli2"
    LINT_EXIT=$?
    if [ "$LINT_EXIT" -eq 0 ]; then
        echo -e "${C_GREEN}✓ markdownlint: 通过${C_NC}"
    else
        echo -e "${C_RED}✗ markdownlint: 失败 (exit=$LINT_EXIT)${C_NC}"
    fi
fi

# --- 2. lychee ----------------------------------------------------------
if [ "$RUN_LINK" -eq 1 ]; then
    echo
    echo -e "${C_YELLOW}==== [2/2] lychee link check ====${C_NC}"
    docker run --rm \
        -v "$(pwd)":/workspace \
        -w /workspace \
        "$LYCHEE_IMAGE" \
        --user-agent "$LYCHEE_UA" \
        /workspace
    LINK_EXIT=$?
    if [ "$LINK_EXIT" -eq 0 ]; then
        echo -e "${C_GREEN}✓ lychee: 通过${C_NC}"
    else
        echo -e "${C_RED}✗ lychee: 失败 (exit=$LINK_EXIT)${C_NC}"
    fi
fi

# --- 汇总 ---------------------------------------------------------------
echo
echo "========================================"
if [ "$LINT_EXIT" -eq 0 ] && [ "$LINK_EXIT" -eq 0 ]; then
    echo -e "${C_GREEN}✓ 全部检查通过，可以提交。${C_NC}"
    exit 0
else
    echo -e "${C_RED}✗ 有检查未通过，请修复后再提交：${C_NC}"
    [ "$LINT_EXIT" -ne 0 ] && echo -e "  - markdownlint  失败 (exit=$LINT_EXIT)"
    [ "$LINK_EXIT" -ne 0 ] && echo -e "  - lychee        失败 (exit=$LINK_EXIT)"
    echo
    echo "提示:"
    echo "  - markdownlint 错误: 找对应文件:行号，修改 .markdownlint.jsonc 中放行的规则，或修文档"
    echo "  - lychee 错误:       修复指向不存在的本地文件 / 失效 URL；外链 4xx 等可在 .lycheeignore 加白名单"
    exit 1
fi
