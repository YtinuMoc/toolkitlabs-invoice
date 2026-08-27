#!/usr/bin/env python3
"""Programmatic SEO engine — clone of Orion datcxy seo_engine.py shape."""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


def render_pages(dataset: list[dict], template: str) -> dict[str, str]:
    """Turn one dataset into indexable long-tail pages."""
    pages: dict[str, str] = {}
    for row in dataset:
        slug = row.get("slug") or row.get("id", "page")
        body = template
        for k, v in row.items():
            body = body.replace(f"{{{{{k}}}}}", str(v))
        pages[f"{slug}.html"] = body
    return pages


def write_sitemap(pages: dict[str, str], base_url: str, out: Path) -> Path:
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for name in sorted(pages):
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = f"{base_url.rstrip('/')}/{name}"
    path = out / "sitemap.xml"
    ET.ElementTree(urlset).write(path, encoding="utf-8", xml_declaration=True)
    return path


def write_robots(base_url: str, out: Path) -> Path:
    path = out / "robots.txt"
    path.write_text(f"User-agent: *\nAllow: /\nSitemap: {base_url.rstrip('/')}/sitemap.xml\n")
    return path


def indexnow_payload(host: str, key: str, urls: list[str]) -> dict:
    return {"host": host, "key": key, "urlList": urls}


def self_test() -> None:
    tpl = "<h1>{{title}}</h1><p>{{desc}}</p>"
    data = [{"slug": "csv-invoice", "title": "CSV Invoice", "desc": "Batch invoices from CSV."}]
    pages = render_pages(data, tpl)
    assert "csv-invoice.html" in pages
    assert "CSV Invoice" in pages["csv-invoice.html"]
    tmp = Path("/tmp/seo_engine_test")
    tmp.mkdir(exist_ok=True)
    write_sitemap(pages, "https://example.com", tmp)
    write_robots("https://example.com", tmp)
    assert (tmp / "sitemap.xml").exists()
    payload = indexnow_payload("example.com", "abc", ["https://example.com/csv-invoice.html"])
    assert payload["urlList"]
    print("seo_engine.py self-test OK")


if __name__ == "__main__":
    self_test()
