#!/usr/bin/env python3
"""rfcli.py

一个简单的命令行参数解析示例，使用 argparse 提供全局选项与子命令。

用法示例：
  python rfcli.py --help
  python rfcli.py run mytask --repeat 3 -v -c config.yaml --dry-run
  python rfcli.py config set timeout 30
"""

from __future__ import annotations

import argparse
import sys
from typing import List

__version__ = "0.1.0"


def build_parser() -> argparse.ArgumentParser:
	"""构建并返回顶层 ArgumentParser（可供测试）。"""
	parser = argparse.ArgumentParser(
		prog="rfcli",
		description="轻量的命令行工具示例（中文帮助）",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter,
	)

	# 全局选项
	parser.add_argument(
		"-v",
		"--verbose",
		action="count",
		default=0,
		help="增加输出详细程度（可叠加，例如 -vv）",
	)
	parser.add_argument(
		"-c",
		"--config",
		metavar="FILE",
		help="指定配置文件路径",
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="只打印将要执行的操作，但不真正执行",
	)

	subparsers = parser.add_subparsers(dest="cmd", required=True)

	# run 子命令
	run_p = subparsers.add_parser("run", help="运行某个任务")
	run_p.add_argument("task", help="要运行的任务名称或脚本路径")
	run_p.add_argument(
		"--repeat", "-r", type=int, default=1, help="重复执行次数"
	)
	run_p.add_argument(
		"--timeout", type=int, default=60, help="任务超时时间（秒）"
	)

	# config 子命令，带子子命令 get/set
	cfg_p = subparsers.add_parser("config", help="配置管理（get/set）")
	cfg_sub = cfg_p.add_subparsers(dest="action", required=True)

	cfg_get = cfg_sub.add_parser("get", help="读取配置项")
	cfg_get.add_argument("key", help="配置项键名")

	cfg_set = cfg_sub.add_parser("set", help="设置配置项")
	cfg_set.add_argument("key", help="配置项键名")
	cfg_set.add_argument("value", help="配置项值")

	# version 子命令
	subparsers.add_parser("version", help="显示工具版本并退出")

	return parser


def handle_run(args: argparse.Namespace) -> int:
	"""处理 run 子命令的逻辑。返回退出码。"""
	if args.dry_run:
		print(f"[dry-run] 将运行任务: {args.task}, repeat={args.repeat}, timeout={args.timeout}")
		return 0

	# 模拟执行
	for i in range(1, args.repeat + 1):
		if args.verbose:
			print(f"[run] 第 {i}/{args.repeat} 次执行任务 '{args.task}' (timeout={args.timeout})")
		else:
			print(f"运行: {args.task} ({i}/{args.repeat})")
	return 0


def handle_config(args: argparse.Namespace) -> int:
	"""处理 config 子命令 (get/set)。这里仅做示例，不持久化。"""
	if args.action == "get":
		# 示例返回一个固定值
		print(f"{args.key} = 42")
		return 0

	if args.action == "set":
		# 在真实程序中应保存到文件或其它存储
		print(f"已设置 {args.key} = {args.value}")
		return 0

	print("未知的 config 操作", file=sys.stderr)
	return 2


def main(argv: List[str] | None = None) -> int:
	"""程序入口，解析参数并分派到具体处理函数。返回进程退出码。"""
	argv = argv if argv is not None else sys.argv[1:]
	parser = build_parser()
	args = parser.parse_args(argv)

	# 调试/上下文信息
	if args.verbose:
		print(f"[debug] 已解析参数: {args}")
		if args.config:
			print(f"[debug] 使用配置文件: {args.config}")

	if args.cmd == "run":
		return handle_run(args)

	if args.cmd == "config":
		return handle_config(args)

	if args.cmd == "version":
		print(__version__)
		return 0

	parser.print_help()
	return 1


if __name__ == "__main__":
	raise SystemExit(main())


