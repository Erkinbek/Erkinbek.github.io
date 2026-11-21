#!/usr/bin/env python3
"""Sends changed pages to IndexNow (Bing, Yandex, Seznam, Naver share what one of them gets).

    python tools/indexnow.py SITEMAP_OR_URL [...]
    python tools/indexnow.py --dry-run https://erkinbek.github.io/bigtext/sitemap.xml

A sitemap argument (ending in .xml) is fetched and every <loc> in it is sent; any other
argument is sent as a page URL. Only URLs on erkinbek.github.io are accepted: the key file
at the root of this repository proves the host is ours.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HOST = "erkinbek.github.io"
ENDPOINT = "https://api.indexnow.org/indexnow"
ROOT = Path(__file__).resolve().parent.parent
UA = "indexnow-submit/1.0"


def key():
    found = [p for p in ROOT.glob("*.txt") if re.fullmatch(r"[0-9a-f]{32}", p.stem)]
    if len(found) != 1:
        sys.exit(f"expected one <32 hex>.txt key file in {ROOT}, found {len(found)}")
    k = found[0].read_text(encoding="utf-8").strip()
    if k != found[0].stem:
        sys.exit(f"{found[0].name} must contain its own name")
    return k


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def urls_from(args):
    out = []
    for a in args:
        if a.endswith(".xml"):
            out += [u.strip() for u in re.findall(r"<loc>([^<]+)</loc>", fetch(a))]
        else:
            out.append(a)
    bad = [u for u in out if not u.startswith(f"https://{HOST}/")]
    if bad:
        sys.exit("not on " + HOST + ": " + ", ".join(bad))
    return list(dict.fromkeys(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    k = key()
    urls = urls_from(a.targets)
    body = {"host": HOST, "key": k, "keyLocation": f"https://{HOST}/{k}.txt", "urlList": urls}
    print(f"{len(urls)} URLs")
    for u in urls:
        print(" ", u)
    if a.dry_run:
        return
    if fetch(body["keyLocation"]).strip() != k:
        sys.exit(f"{body['keyLocation']} is not live yet (or holds another key)")
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps(body).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("IndexNow:", r.status, r.reason)
    except urllib.error.HTTPError as err:
        # 200 and 202 are success; 403 = key not found at keyLocation, 422 = URL/host mismatch.
        sys.exit(f"IndexNow: {err.code} {err.reason} {err.read().decode('utf-8', 'replace')}")


if __name__ == "__main__":
    main()
