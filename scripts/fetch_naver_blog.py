#!/usr/bin/env python3
from __future__ import annotations
import json, re, html, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from email.utils import parsedate_to_datetime

BLOG_ID = "songdo1000miso"
RSS_URL = f"https://rss.blog.naver.com/{BLOG_ID}.xml"
OUT = Path("data/blog-posts.json")
MAX_POSTS = 18

def clean_html(value: str) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value

def first_image(value: str) -> str:
    if not value:
        return ""
    # Supports both normal HTML and escaped HTML commonly found in RSS descriptions.
    decoded = html.unescape(value)
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', decoded, flags=re.I)
    return m.group(1) if m else ""

def get_text(item, tags):
    for tag in tags:
        el = item.find(tag)
        if el is not None and el.text:
            return el.text.strip()
    return ""

req = urllib.request.Request(
    RSS_URL,
    headers={
        "User-Agent": "Mozilla/5.0 (compatible; Songdo1000MisoSite/1.0)",
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
    },
)
with urllib.request.urlopen(req, timeout=30) as response:
    xml_bytes = response.read()

root = ET.fromstring(xml_bytes)
items = root.findall(".//item")

posts = []
for item in items[:MAX_POSTS]:
    title = clean_html(get_text(item, ["title"]))
    link = get_text(item, ["link"])
    desc_raw = get_text(item, ["description", "{http://purl.org/rss/1.0/modules/content/}encoded"])
    description = clean_html(desc_raw)
    if len(description) > 180:
        description = description[:177].rstrip() + "…"

    pub = get_text(item, ["pubDate", "{http://purl.org/dc/elements/1.1/}date"])
    display_date = pub
    if pub:
        try:
            dt = parsedate_to_datetime(pub)
            display_date = dt.astimezone(timezone.utc).strftime("%Y.%m.%d")
        except Exception:
            try:
                display_date = datetime.fromisoformat(pub.replace("Z","+00:00")).strftime("%Y.%m.%d")
            except Exception:
                pass

    category = get_text(item, ["category"]) or "BLOG"

    posts.append({
        "title": title,
        "link": link,
        "date": display_date,
        "category": clean_html(category),
        "description": description,
        "thumbnail": first_image(desc_raw),
    })

payload = {
    "blogId": BLOG_ID,
    "rss": RSS_URL,
    "updatedAt": datetime.now(timezone.utc).isoformat(),
    "posts": posts,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Fetched {len(posts)} posts from {RSS_URL}")
