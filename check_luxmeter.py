#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = [
#   "requests>=2.32.0",
# ]
# ///
"""照度計動作確認スクリプト。

Usage:
    uv run check_luxmeter.py --url http://<host>:<port>
    uv run check_luxmeter.py --url http://<host>:<port> --count 5 --interval 2
"""

import argparse
import sys
import time
from datetime import datetime

import requests

LUXMETER_PATH = "/api/v1/sensors/luxmeter/value"


def fetch_lux(url: str, timeout: float) -> float:
    response = requests.get(url, timeout=timeout)
    if response.status_code != 200:
        raise RuntimeError(f"HTTP {response.status_code}: {response.text}")
    body = response.json()
    if "value" not in body:
        raise RuntimeError(f"レスポンスに 'value' キーがありません: {body}")
    value = body["value"]
    if not isinstance(value, (int, float)):
        raise TypeError(f"照度値が数値ではありません: {value!r}")
    return float(value)


def main() -> None:
    parser = argparse.ArgumentParser(description="照度計動作確認スクリプト")
    parser.add_argument(
        "--url",
        required=True,
        help="センサーのベース URL (例: http://192.168.1.100:8080)",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="計測回数 (デフォルト: 1)",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="計測間隔（秒）(デフォルト: 1.0)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="HTTP タイムアウト（秒）(デフォルト: 10.0)",
    )
    args = parser.parse_args()

    endpoint = args.url.rstrip("/") + LUXMETER_PATH

    print("照度計確認スクリプト")
    print(f"URL: {endpoint}")
    print("---")

    success_count = 0
    for i in range(args.count):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            lux = fetch_lux(endpoint, timeout=args.timeout)
            print(f"[{timestamp}] 照度: {lux:.1f} lux")
            success_count += 1
        except requests.exceptions.ConnectionError:
            print(f"[{timestamp}] エラー: 接続できません ({endpoint})")
        except requests.exceptions.Timeout:
            print(f"[{timestamp}] エラー: タイムアウト ({args.timeout}秒)")
        except requests.exceptions.RequestException as e:
            print(f"[{timestamp}] エラー: {e}")
        except (RuntimeError, TypeError) as e:
            print(f"[{timestamp}] エラー: {e}")

        if i < args.count - 1:
            time.sleep(args.interval)

    print("---")
    if args.count == 1:
        print("計測完了")
    else:
        print(f"計測完了 ({success_count}/{args.count}回 成功)")

    if success_count == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
