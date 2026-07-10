#!/usr/bin/env python3
"""
合同会社きぼう 毎日ブログ自動生成スクリプト
実行方法: python scripts/generate_post.py
必要な環境変数: ANTHROPIC_API_KEY
"""

import os
import json
import datetime
import re
from pathlib import Path
import anthropic

# ============================================================
# テーマリスト（順番に使用、ループする）
# ============================================================
TOPICS = [
    {"keyword": "旭川 老人ホーム 種類 費用 比較 選び方",              "category": "facility"},
    {"keyword": "住宅型有料老人ホーム 特徴 メリット デメリット",       "category": "facility"},
    {"keyword": "介護保険 要介護認定 申請 流れ 手続き",               "category": "insurance"},
    {"keyword": "介護保険 1割負担 2割負担 サービス 何が使える",        "category": "insurance"},
    {"keyword": "認知症 介護 自宅 限界 施設入居 タイミング",           "category": "care"},
    {"keyword": "老人ホーム 見学 チェックリスト ポイント 注意点",      "category": "facility"},
    {"keyword": "在宅介護 施設入居 費用 比較 どちらが得",             "category": "family"},
    {"keyword": "老人ホーム 入居費用 月額 相場 内訳",                 "category": "facility"},
    {"keyword": "高齢者 食事 栄養 老人ホーム 食生活 管理",            "category": "care"},
    {"keyword": "介護保険 ケアマネジャー 役割 相談 活用方法",          "category": "insurance"},
    {"keyword": "老人ホーム 入居 準備 持ち物 必要なもの",             "category": "facility"},
    {"keyword": "看取りケア ターミナルケア 老人ホーム 旭川 対応",      "category": "care"},
    {"keyword": "認知症 種類 アルツハイマー レビー小体 違い 対応",     "category": "care"},
    {"keyword": "老人ホーム 退去 条件 身体状況 悪化 対応",            "category": "facility"},
    {"keyword": "老人ホーム 面会 頻度 外泊 ルール 家族",              "category": "family"},
    {"keyword": "特養 待機 長い 老人ホーム 民間 選択肢",              "category": "facility"},
    {"keyword": "高齢者 転倒 予防 施設 環境 安全対策",               "category": "care"},
    {"keyword": "介護保険 区分変更 手続き 必要 タイミング",            "category": "insurance"},
    {"keyword": "旭川市 高齢化 介護 現状 将来 課題",                  "category": "care"},
    {"keyword": "老人ホーム スタッフ 人員配置 基準 確認方法",          "category": "facility"},
    {"keyword": "介護 兄弟 役割分担 トラブル 解決 方法",              "category": "family"},
    {"keyword": "高齢者 うつ 孤独 施設入居 改善 事例",               "category": "care"},
    {"keyword": "グループホーム 認知症 住宅型有料 違い 比較",          "category": "facility"},
    {"keyword": "介護 医療 連携 かかりつけ医 老人ホーム 対応",         "category": "care"},
    {"keyword": "老人ホーム 選び方 失敗しない 後悔 ポイント",          "category": "facility"},
    {"keyword": "介護保険 施設サービス 居宅サービス 違い 活用",        "category": "insurance"},
    {"keyword": "老人ホーム 入居後 生活 一日 スケジュール 様子",       "category": "care"},
    {"keyword": "高齢者 資金計画 老人ホーム 費用 準備 貯金",          "category": "family"},
    {"keyword": "老人ホーム リハビリ 機能訓練 回復 目標",             "category": "care"},
    {"keyword": "認知症 家族 対応 コミュニケーション 方法",           "category": "family"},
    {"keyword": "介護 不動産 自宅売却 老人ホーム費用 資金計画",        "category": "family"},
    {"keyword": "老人ホーム 入浴 排泄 日常生活 介助 基準",            "category": "care"},
    {"keyword": "旭川 介護 相談窓口 地域包括支援センター 活用",        "category": "insurance"},
    {"keyword": "住宅型有料老人ホーム 契約 重要事項説明書 確認",       "category": "facility"},
    {"keyword": "老人ホーム 感染症 対策 面会 制限 ルール",            "category": "care"},
    {"keyword": "高齢者 薬 管理 服薬 老人ホーム 支援",               "category": "care"},
    {"keyword": "介護 仕事 両立 離職 解決策 制度活用",               "category": "family"},
    {"keyword": "老人ホーム 入居 断られた 理由 対処法",               "category": "facility"},
    {"keyword": "高齢者 熱中症 冬 低体温 施設 体温管理",             "category": "care"},
    {"keyword": "介護保険 限度額 超えた 全額自費 費用 どうする",       "category": "insurance"},
]


def get_today_topic(posts_json_path: Path) -> dict:
    try:
        with open(posts_json_path, encoding="utf-8") as f:
            posts = json.load(f)
        idx = len(posts) % len(TOPICS)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        idx = 0
    return TOPICS[idx]


def generate_article(topic: dict, client: anthropic.Anthropic) -> str:
    prompt = f"""あなたは北海道旭川市で住宅型有料老人ホーム「うらら」「セラヴィ豊岡」を運営する「合同会社きぼう」のブログライターです。
代表の髙嶋裕紀は不動産業（ハウスドゥ澄川 / 合同会社スミリア）も営んでおり、介護と不動産のワンストップ相談が特徴です。

## テーマキーワード
{topic['keyword']}

## 執筆ルール
- 読者：介護施設への入居を検討している家族（40〜60代）と、本人（65歳以上の高齢者）
- 文体：丁寧だが親しみやすい。専門用語は必ず平易に説明する。
- 地域：旭川市に関連した内容を必ず1箇所以上含める
- 施設名：記事のテーマに合う場合、「うらら」または「セラヴィ豊岡」を自然な形で言及する
- 本文：1200〜1800字
- 構成：リード文（100〜150字）→ H2見出し3〜4個 → 各見出しに本文 → まとめ
- 末尾：「合同会社きぼうへご相談ください」という自然な誘導文（1〜2文）で締める

## 出力形式（HTMLタグのみ）
<h1>（タイトル）</h1>
<p class="post-lead">（リード文）</p>
<h2>（見出し）</h2>
<p>（本文）</p>
（以下繰り返し）

使用可能なタグ：h1, h2, h3, p, ul, li, strong
マークダウン記法は使用しないこと。コードブロックも不要。HTMLタグのみで出力。"""

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def extract_title(html_content: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html_content, re.DOTALL)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return "介護のお役立ちコラム"


def extract_excerpt(html_content: str, length: int = 120) -> str:
    text = re.sub(r"<[^>]+>", "", html_content)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= length:
        return text
    cut = text[:length]
    boundary = max(cut.rfind("。"), cut.rfind("、"))
    if boundary > length * 0.5:
        cut = cut[:boundary + 1]
    return cut + "…"


def make_slug(date_str: str, keyword: str) -> str:
    kw = re.sub(r"[^\w]", "-", keyword[:20]).strip("-")
    kw = re.sub(r"-+", "-", kw)
    return f"{date_str}-{kw}"


def build_related_posts_html(existing_posts: list, category: str, current_slug: str) -> str:
    related = [p for p in existing_posts
               if p.get("category") == category and current_slug not in (p.get("url") or "")][:3]
    if not related:
        return ""
    cat_icons = {"care": "🤝", "facility": "🏠", "insurance": "📋", "family": "👪"}
    icon = cat_icons.get(category, "📝")
    items = "\n".join(
        f'          <li><a href="/{p["url"]}" style="color:var(--primary);text-decoration:none;">'
        f'{icon} {p["title"]}</a><span style="color:var(--text-muted);font-size:.85rem;margin-left:8px;">{p["date"]}</span></li>'
        for p in related
    )
    return f"""
        <div style="margin-top:48px;padding:28px;background:var(--primary-light);border-radius:12px;">
          <p style="font-weight:700;font-size:1rem;margin-bottom:16px;">関連コラム</p>
          <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:12px;">
{items}
          </ul>
        </div>"""


def build_html_page(title: str, body_html: str, date_display: str,
                    category: str, slug: str = "", excerpt: str = "",
                    date_str: str = "", existing_posts: list = None) -> str:
    cat_map = {
        "care":      ("介護のこと",  "badge-green"),
        "facility":  ("施設について", "badge-blue"),
        "insurance": ("介護保険",    "badge-orange"),
        "family":    ("ご家族へ",    "badge-beige"),
    }
    cat_label, cat_cls = cat_map.get(category, ("介護のこと", "badge-green"))

    body = re.sub(r"<h1[^>]*>.*?</h1>", "", body_html, flags=re.DOTALL).strip()

    canonical_url = f"https://kibou-asahikawa.com/posts/{slug}.html" if slug else ""
    desc = excerpt if excerpt else f"{title}｜合同会社きぼうの介護コラム"

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{desc}">
  <title>{title} | 合同会社きぼう（旭川）</title>
  {f'<link rel="canonical" href="{canonical_url}">' if canonical_url else ''}
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title} | 合同会社きぼう（旭川）">
  <meta property="og:description" content="{desc}">
  {f'<meta property="og:url" content="{canonical_url}">' if canonical_url else ''}
  <meta property="og:site_name" content="合同会社きぼう">
  <meta property="og:locale" content="ja_JP">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{desc}",
    "datePublished": "{date_str}",
    "dateModified": "{date_str}",
    "author": {{
      "@type": "Organization",
      "name": "合同会社きぼう",
      "url": "https://kibou-asahikawa.com/"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "合同会社きぼう",
      "url": "https://kibou-asahikawa.com/"
    }},
    "url": "{canonical_url}"
  }}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <header class="header" id="header">
    <div class="header-inner">
      <a href="/" class="logo">
        <span class="logo-sub">旭川市 住宅型有料老人ホーム</span>
        <span class="logo-main">合同会社<span>きぼう</span></span>
      </a>
      <nav class="nav">
        <ul class="nav-links">
          <li><a href="/"        class="nav-link">トップ</a></li>
          <li><a href="/urara"   class="nav-link">うらら</a></li>
          <li><a href="/celavie" class="nav-link">セラヴィ豊岡</a></li>
          <li><a href="/blog"    class="nav-link active">ブログ</a></li>
          <li><a href="/recruit" class="nav-link">求人</a></li>
          <li><a href="/contact" class="nav-link">お問い合わせ</a></li>
        </ul>
        <a href="/contact" class="btn btn-primary nav-cta">入居相談（無料）</a>
        <button class="hamburger" id="hamburger" aria-label="メニューを開く">
          <span></span><span></span><span></span>
        </button>
      </nav>
    </div>
  </header>
  <div class="mobile-menu" id="mobileMenu">
    <ul class="mobile-nav-links">
      <li><a href="/"        class="mobile-nav-link">🏠 トップ</a></li>
      <li><a href="/urara"   class="mobile-nav-link">🌸 うらら</a></li>
      <li><a href="/celavie" class="mobile-nav-link">🌿 セラヴィ豊岡</a></li>
      <li><a href="/blog"    class="mobile-nav-link">📝 ブログ</a></li>
      <li><a href="/recruit" class="mobile-nav-link">💼 求人</a></li>
      <li><a href="/contact" class="mobile-nav-link">✉️ お問い合わせ</a></li>
    </ul>
    <a href="/contact" class="btn btn-primary mobile-nav-cta">入居相談（無料）</a>
  </div>

  <div class="page-hero">
    <div class="page-hero-content">
      <p class="page-hero-breadcrumb">
        <a href="/">トップ</a> &gt;
        <a href="/blog">ブログ</a> &gt;
        {title}
      </p>
      <h1 class="page-hero-title" style="font-size:clamp(1.2rem,3vw,1.75rem);line-height:1.5;">{title}</h1>
      <p class="page-hero-subtitle">
        <span class="badge {cat_cls}">{cat_label}</span>&nbsp; {date_display}
      </p>
    </div>
  </div>

  <main>
    <section class="section">
      <div class="container">
        <div class="post-body">
{body}
        </div>

{build_related_posts_html(existing_posts or [], category, slug)}

        <div class="post-cta-box">
          <p class="post-cta-title">入居相談・見学は無料です</p>
          <p class="post-cta-text">
            「うちの場合はどうすればいい？」そんな疑問も、ぜひそのままお持ちください。<br>
            旭川市の住宅型有料老人ホーム「うらら」「セラヴィ豊岡」を運営する合同会社きぼうが丁寧にお応えします。
          </p>
          <div style="display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin-top:20px;">
            <a href="/contact" class="btn btn-primary btn-lg">📩 無料相談フォーム</a>
            <a href="tel:0166548388" class="btn btn-secondary btn-lg">📞 0166-54-8388</a>
          </div>
        </div>

        <p style="text-align:center;margin-top:32px;">
          <a href="/blog" style="color:var(--primary);">← ブログ一覧に戻る</a>
        </p>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-logo">合同会社<span>きぼう</span></div>
          <div class="footer-company">旭川市 住宅型有料老人ホーム</div>
          <address class="footer-address" style="font-style:normal;">
            <strong style="color:#fff;">うらら</strong><br>
            北海道旭川市春光町12番地2（〒070-0902）<br>
            TEL：0166-54-8388<br>
            <strong style="color:#fff;display:inline-block;margin-top:8px;">セラヴィ豊岡</strong><br>
            北海道旭川市豊岡4条3丁目4-12（〒078-8234）<br>
            TEL：0166-73-7395<br>
            <span style="display:inline-block;margin-top:8px;">受付時間：9:00〜18:00</span>
          </address>
        </div>
        <div>
          <div class="footer-nav-title">サイトマップ</div>
          <ul class="footer-nav-links">
            <li><a href="/"        class="footer-nav-link">トップページ</a></li>
            <li><a href="/urara"   class="footer-nav-link">うらら</a></li>
            <li><a href="/celavie" class="footer-nav-link">セラヴィ豊岡</a></li>
            <li><a href="/blog"    class="footer-nav-link">ブログ</a></li>
            <li><a href="/recruit" class="footer-nav-link">求人</a></li>
            <li><a href="/contact" class="footer-nav-link">お問い合わせ</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 合同会社きぼう All Rights Reserved.</span>
      </div>
    </div>
  </footer>

  <script src="../script.js"></script>
</body>
</html>"""


def update_sitemap(posts: list, base: Path, today_str: str = "") -> None:
    today = today_str or datetime.date.today().isoformat()
    static_urls = [
        ("https://kibou-asahikawa.com/",        today,        "weekly",  "1.0"),
        ("https://kibou-asahikawa.com/urara",   today,        "monthly", "0.9"),
        ("https://kibou-asahikawa.com/celavie", today,        "monthly", "0.9"),
        ("https://kibou-asahikawa.com/about",   "2026-07-05", "monthly", "0.7"),
        ("https://kibou-asahikawa.com/blog",    today,        "weekly",  "0.7"),
        ("https://kibou-asahikawa.com/recruit", "2026-07-05", "monthly", "0.6"),
        ("https://kibou-asahikawa.com/contact", "2026-07-05", "monthly", "0.6"),
    ]
    entries = []
    for loc, lastmod, changefreq, priority in static_urls:
        entries.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n    <priority>{priority}</priority>\n  </url>"
        )
    for post in posts:
        if post.get("url"):
            loc = f"https://kibou-asahikawa.com/{post['url']}"
            lastmod = post.get("dateISO", "2026-07-05")
            entries.append(
                f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n"
                f"    <changefreq>never</changefreq>\n    <priority>0.6</priority>\n  </url>"
            )
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "\n".join(entries) + "\n</urlset>\n"
    (base / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"sitemap.xml を更新しました（合計 {len(entries)} URL）")


def main():
    base = Path(__file__).resolve().parent.parent
    posts_dir = base / "posts"
    posts_dir.mkdir(exist_ok=True)
    posts_json = base / "posts.json"

    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    date_display = today.strftime("%Y年%m月%d日")

    topic = get_today_topic(posts_json)
    print(f"[{date_str}] テーマ: {topic['keyword']}")

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    content = generate_article(topic, client)

    title = extract_title(content)
    excerpt = extract_excerpt(content)
    slug = make_slug(date_str, topic["keyword"])
    filename = f"{slug}.html"

    try:
        existing = json.loads(posts_json.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []

    html = build_html_page(title, content, date_display, topic["category"], slug, excerpt,
                           date_str=date_str, existing_posts=existing)
    article_path = posts_dir / filename
    article_path.write_text(html, encoding="utf-8")
    print(f"記事を生成しました: posts/{filename}")

    new_entry = {
        "title":    title,
        "category": topic["category"],
        "date":     date_display,
        "dateISO":  date_str,
        "excerpt":  excerpt,
        "url":      f"posts/{filename}",
    }
    existing.insert(0, new_entry)
    posts_json.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"posts.json を更新しました（合計 {len(existing)} 記事）")

    update_sitemap(existing, base, today_str=date_str)


if __name__ == "__main__":
    main()
