# luxmeter-check

照度計（照度センサー）の動作確認用 CLI スクリプト。
HTTP API 経由で照度値を取得し、ターミナルに出力します。

## 前提条件

- Python 3.11 以上（追加パッケージ不要）

## 使い方

```bash
# 1回計測
python3 check_luxmeter.py --url http://<ホスト>:8890

# 5回、2秒間隔で繰り返し計測
python3 check_luxmeter.py --url http://<ホスト>:8890 --count 5 --interval 2
```

> **ポートについて**  
> デフォルトは `8890` ですが、正確な値は AppConfig の設定値を参照してください。

### オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `--url` | センサーサービスのベース URL（必須） | - |
| `--count` | 計測回数 | `1` |
| `--interval` | 計測間隔（秒） | `1.0` |
| `--timeout` | HTTP タイムアウト（秒） | `10.0` |

### 出力例

```
照度計確認スクリプト
URL: http://192.168.4.101:8890/api/v1/sensors/luxmeter/value
---
[2026-05-22 10:30:01] 照度: 523.5 lux
[2026-05-22 10:30:03] 照度: 521.0 lux
[2026-05-22 10:30:05] 照度: 525.3 lux
---
計測完了 (3/3回 成功)
```

接続できない場合は以下のように表示されます。

```
照度計確認スクリプト
URL: http://localhost:9999/api/v1/sensors/luxmeter/value
---
[2026-05-22 10:30:01] エラー: 接続できません (http://localhost:9999/api/v1/sensors/luxmeter/value)
---
計測完了
exit code: 1
```

## API 仕様

センサーサービスは以下のエンドポイントを提供している必要があります。

```
GET /api/v1/sensors/luxmeter/value
```

レスポンス例:

```json
{ "value": 523.5 }
```
