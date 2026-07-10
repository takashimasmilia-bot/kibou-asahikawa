# デプロイ構成メモ

## 本番環境（2026-07-10確認）

- **本番ドメイン**: `kibou-asahikawa.com`
- **ホスティング**: Cloudflare Pages（`main`ブランチへのpushで自動デプロイ）
- Cloudflare Pages側の設定（ビルド設定・ドメイン接続）はCloudflareダッシュボード側にあり、このリポジトリにはCloudflare関連の設定ファイルはない。

## kibou.online について

- 旧ドメイン。今もWixのネームサーバー（`ns6.wixdns.net` / `ns7.wixdns.net`）を使用しており、Wix上の旧サイトが表示される。
- 本サイトのコード内（canonical、og:url、JSON-LD、sitemap.xml、robots.txt等）は`kibou-asahikawa.com`を参照するよう統一済み（2026-07-10、以前は誤って`kibou.online`を参照していた）。
- 今後 `kibou.online` を使う予定はない、または別用途（2026-07-10時点の認識）。

## GitHub Pagesについて

- 2026-07-10に誤って有効化・`kibou.online`をカスタムドメイン設定してしまったが、本番はCloudflare Pagesのため不要と判明。カスタムドメイン設定は解除済み。
- `https://takashimasmilia-bot.github.io/kibou-asahikawa/` として引き続き有効だが、実運用では使用しない（重複ミラー）。
