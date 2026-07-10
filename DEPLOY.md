# kibou.online 公開手順（Wix → GitHub Pages 移行）

## 現状（2026-07-10時点）

- 本番ドメイン `kibou.online` は今も **Wixのネームサーバー**（`ns6.wixdns.net` / `ns7.wixdns.net`）を使用しており、実際に表示されるのは旧Wixサイト。
- このリポジトリの静的サイトは **GitHub Pagesを有効化済み**：
  - 公開URL（GitHub Pages既定）: https://takashimasmilia-bot.github.io/kibou-asahikawa/
  - カスタムドメイン設定: `kibou.online`（リポジトリに`CNAME`ファイルを追加済み）
  - 現時点ではDNSがWix側を向いたままなので、`kibou.online`へのアクセスはまだWixサイトに届く。

## 残っている作業：WixのDNS設定変更

Wixの管理画面（ドメイン管理 / DNS設定）で、`kibou.online`のDNSレコードを以下の内容に変更する。

### 1. Aレコード（ルートドメイン `kibou.online` 用）

既存のWixホスティング用Aレコード（`185.230.63.x`系）を削除し、GitHub Pagesの4つのIPに置き換える：

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

### 2. www サブドメイン（使っている場合）

`www.kibou.online` のCNAMEレコードを以下に変更：

```
takashimasmilia-bot.github.io
```

### 3. 変更してはいけないもの

- メール関連のレコード（MXレコード、SPF/DKIM等のTXTレコード）が存在する場合は**そのまま残す**（今回の調査ではMXレコードは見当たらなかったが、念のため変更前に確認）。
- Web/独自ドメイン検証以外のTXTレコードも触らない。

## DNS変更後の確認

1. 反映まで数分〜最大24時間程度かかる場合がある。
2. `kibou.online` にブラウザでアクセスし、Wixサイトではなく新サイト（合同会社きぼうの新デザイン）が表示されることを確認。
3. GitHubリポジトリの Settings → Pages で、ドメインの検証が完了し「Enforce HTTPS」が有効化できる状態になっているか確認する（DNS反映後に自動で証明書が発行される）。

## 参考：現在のPages設定

```
source: main ブランチ / ルート（/）
custom domain: kibou.online
https_enforced: DNS反映待ちのため現在false（反映後に有効化推奨）
```
