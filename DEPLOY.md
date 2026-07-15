# デプロイ構成メモ

## 本番環境（2026-07-10確認）

- **本番ドメイン**: `kibou-asahikawa.com`
- **ホスティング**: Cloudflare Pages（`main`ブランチへのpushで自動デプロイ）
- Cloudflare Pages側の設定（ビルド設定・ドメイン接続）はCloudflareダッシュボード側にあり、このリポジトリにはCloudflare関連の設定ファイルはない。

## kibou.online について

- 旧ドメイン。今もWixのネームサーバー（`ns6.wixdns.net` / `ns7.wixdns.net`）を使用しており、Wix上の旧サイトが表示される。
- 本サイトのコード内（canonical、og:url、JSON-LD、sitemap.xml、robots.txt等）は`kibou-asahikawa.com`を参照するよう統一済み（2026-07-10、以前は誤って`kibou.online`を参照していた）。
- **2026年8月、Wixとの契約を更新しない予定（ドメイン登録ごと）**。つまり`kibou.online`のドメイン自体もこのタイミングで失効する見込み（2026-07-10時点の方針）。
  - サイトコード側は既に`kibou-asahikawa.com`基準になっているため、失効しても本番サイトへの影響はない。
  - 一点だけ留意：ドメイン失効後は第三者が`kibou.online`を再登録できる状態になる。旧サイトへの被リンクや検索エンジンでの認知を今後どう扱うかは未検討（必要になれば別途判断）。

## GitHub Pagesについて

- 2026-07-10に誤って有効化・`kibou.online`をカスタムドメイン設定してしまったが、本番はCloudflare Pagesのため不要と判明。カスタムドメイン設定は解除済み。
- `https://takashimasmilia-bot.github.io/kibou-asahikawa/` として引き続き有効だが、実運用では使用しない（重複ミラー）。

## 残作業（2026-07-10時点、未着手）

サイトコード・DNS周りは`kibou-asahikawa.com`基準に統一済みだが、Google側の外部設定がまだ`kibou.online`のままになっている可能性が高い。ログインが必要なため対応はユーザー本人作業。

- [x] **Googleビジネスプロフィール**：うらら・セラヴィ豊岡それぞれのプロフィールで、ウェブサイトURLを`kibou.online`→`kibou-asahikawa.com`に変更（2026-07-15完了）
- [ ] **Google Search Console**：
  - [ ] `https://kibou-asahikawa.com/` の新規プロパティを登録・所有権確認
  - [ ] サイトマップ `https://kibou-asahikawa.com/sitemap.xml` を送信
  - [ ] `kibou.online`のプロパティが登録済みの場合、8月のドメイン失効を踏まえて移行するか放置するか判断（アドレス変更ツールを使うか、単に放置でも実害は小さい）
