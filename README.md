# multi-agent-simple

このリポジトリは、複数のAIエージェントが協調して開発・運用・品質保証・セキュリティ管理を行う「シンプル」なマルチエージェント組織のサンプル実装です。

---

## 特徴
- **MCPプラグインベース**：各エージェント（開発/QA/セキュリティ/運用）は独立したMCPサーバーとして動作
- **品質ゲート**：QA承認なしに顧客報告不可
- **シンプルな構成**：エージェント追加・設定が容易

---

## ディレクトリ構成
```
multi-agent-simple/
├── agents/              # 各エージェントのプラグイン定義
│   ├── development/     # 開発担当
│   ├── qa/              # QA担当
│   ├── security/        # セキュリティ担当
│   └── operations/      # 運用担当
├── scripts/             # ユーティリティスクリプト
│   └── generate_config.py
├── claude_config.json   # エージェント設定（自動生成）
├── .gitignore           # Git管理除外ファイル
└── README.md            # このファイル
```

---

## セットアップ手順
1. 必要なエージェントディレクトリ（`agents/`配下）を用意
2. 各エージェントに `agent.json`（MCPサーバー設定）と `CLAUDE.md`（役割定義）を配置
3. 設定ファイル生成スクリプトを実行

```bash
python scripts/generate_config.py
```

- `claude_config.json` が自動生成されます

---

## 起動

```bash
claude --mcp-config ./claude_config.json \
--mcp-debug
```

---

## 確認

```
/mcp

# 以下のようになっていればOK
╭─────────────────────────────────────────────────────────
│ Manage MCP servers
│
│ ❯ 1. development  ✔ connected · Enter to view details
│   2. operations   ✔ connected · Enter to view details
│   3. qa           ✔ connected · Enter to view details
│   4. security     ✔ connected · Enter to view details
╰───────────────────────────────────────────────────────── 
```

---

## 使い方

- 依頼内容をプロンプトで入力する
- 依頼内容をマークダウン形式のファイルにしてそれを読み込ませてタスクを実行させる
- 等々

---

## 各エージェントの役割例

### 開発担当（development）
- 高品質で保守性の高いコード実装
- Lint/UnitTest/レビュー準備/QAへの引き継ぎ

### QA担当（qa）
- 独立した視点でのテスト・E2E自動化
- Playwright MCPによるブラウザテストも可能

### セキュリティ担当（security）
- 脆弱性診断・リスク評価・修正案提示

> セキュリティ担当のプロンプトは [MIXI DEVELOPERS Tech BlogのZenn記事](https://zenn.dev/mixi/articles/79831816f9fd22) を参考にしています。記事執筆者・関係者の皆様に感謝いたします。

### 運用担当（operations）
- 安全なデプロイ・監視・障害対応

---

## 履歴管理のルール
- すべての依頼・対応結果は `history/` 以下に時系列で記録
- 依頼記録・各担当の対応・サマリーを分割管理
- 記録例やフォーマットは `CLAUDE.md` を参照

---

## エージェント追加・拡張方法
1. `agents/` に新ディレクトリを作成
2. `agent.json` と `CLAUDE.md` を配置
3. `python scripts/generate_config.py` を再実行

---

## サンプル設定ファイル
### agent.json
```json
{
  "command": "claude",
  "args": ["mcp", "serve"]
}
```

### claude_config.json（自動生成例）
```json
{
  "mcpServers": {
    "development": {
      "command": "claude",
      "args": ["mcp", "serve"],
      "cwd": ".../agents/development",
      "env": {"CLAUDE_ROLE": "# 開発担当の役割 ..."}
    },
    ...
  }
}
```

---

## 注意事項
- `.credentials` など機密情報は `.gitignore` で管理し、リポジトリに含めないでください
- 回答・運用は日本語が前提です

---

## ライセンス
MIT License 