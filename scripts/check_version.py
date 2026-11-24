#!/usr/bin/env python3

# check_version.py —— 官网版本号必须与 Selfupdate 的 latest.toml 一致
#
# 为什么需要它：4.6.0 发版时官网一直显示 4.5.2。原因是版本号的主体不在
# `index.html` 里，而在 `i18n.js` 的 8 个 `'version.block'`（8 种语言），
# `index.html` 只有两行静态兜底 —— 只改一处、甚至只改 index.html，看起来都「像
# 改过了」。人靠记不可靠，所以做成一道闸门。
#
# 检查两项：
#   1. `i18n.js` 里**每一条** `'version.block'` 都含有 latest.toml 的 version 与
#      release_date（缺一条就失败，等于某种语言的访客看到旧版本）；
#   2. `index.html` 里 `.version-block` 的两行静态兜底同样一致。
#
# 用法：
#   python3 scripts/check_version.py                       # 默认读 ../Selfupdate
#   python3 scripts/check_version.py --latest <latest.toml> # 指定文件
#
# 退出码：0 一致；1 不一致（逐条列出）。

import argparse
import pathlib
import re
import sys

RED = "\033[1;31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# 现在支持的语言数。新增语言时这个数要跟着改 —— 少一种语言没人会发现，
# 那正是 4.6.0 那次漏改的形态。
EXPECTED_VERSION_BLOCKS = 8


def fail(message):
    print(f"{RED}🌊 {message}{RESET}")
    return 1


def read_toml_version(path):
    text = path.read_text(encoding="utf-8")
    version = re.search(r'^version\s*=\s*"([^"]+)"', text, re.M)
    date = re.search(r'^release_date\s*=\s*"([^"]+)"', text, re.M)
    if not version or not date:
        raise SystemExit(f"{RED}🌊 Error: {path} 里没有 version / release_date{RESET}")
    return version.group(1), date.group(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--latest", default="../Selfupdate/macwavedata/latest.toml",
                        help="Selfupdate 的 macwavedata/latest.toml")
    parser.add_argument("--root", default=".", help="Pages 仓库根目录")
    args = parser.parse_args()

    latest = pathlib.Path(args.latest)
    if not latest.is_file():
        print(f"{YELLOW}🌊 提示：找不到 {latest}，用 --latest 指过去（CI 里是先 checkout 该仓库）{RESET}")
        return 1

    version, date = read_toml_version(latest)
    root = pathlib.Path(args.root)
    problems = []

    # 1. i18n.js：每一条 version.block
    i18n = root / "i18n.js"
    blocks = [(n, line) for n, line in enumerate(i18n.read_text(encoding="utf-8").splitlines(), 1)
              if "'version.block'" in line]
    if len(blocks) != EXPECTED_VERSION_BLOCKS:
        problems.append(f"i18n.js 里 version.block 有 {len(blocks)} 条，"
                        f"期望 {EXPECTED_VERSION_BLOCKS} 条（新增/删除语言时改脚本里的常量）")
    for line_no, line in blocks:
        if version not in line:
            problems.append(f"i18n.js:{line_no} 版本号不是 {version}")
        if date not in line:
            problems.append(f"i18n.js:{line_no} 日期不是 {date}")

    # 2. index.html：静态兜底那两行
    index = (root / "index.html").read_text(encoding="utf-8")
    static_lines = [line.strip() for line in index.splitlines() if 'class="v-line"' in line]
    if len(static_lines) != 2:
        problems.append(f'index.html 里 class="v-line" 有 {len(static_lines)} 行，期望 2 行（版本 + 日期）')
    joined = " ".join(static_lines)
    if version not in joined:
        problems.append(f"index.html 的静态兜底没有 {version}")
    if date not in joined:
        problems.append(f"index.html 的静态兜底没有 {date}")

    if problems:
        print(f"{RED}🌊 官网版本号与 {latest} 不一致（{version} / {date}）：{RESET}")
        for item in problems:
            print(f"{RED}🌊   - {item}{RESET}")
        print(f"{YELLOW}🌊 发版时容易漏的正是这里：i18n.js 每种语言一条，index.html 只是兜底。{RESET}")
        return 1

    print(f"{GREEN}🌊 官网版本号一致：{version} / {date}"
          f"（i18n.js {len(blocks)} 语言 + index.html 静态兜底）{RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
