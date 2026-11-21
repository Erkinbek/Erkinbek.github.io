# erkinbek.github.io

The root of https://erkinbek.github.io/: the page that lists the projects whose own sites live
under it ([BigText](https://erkinbek.github.io/bigtext/), [Katak](https://erkinbek.github.io/katak/),
[jsonreshape](https://erkinbek.github.io/jsonreshape/)). Each project's site is served from its
own repository; this one only holds what has to sit at the root of the host:

- `index.html`: Google takes the favicon and the site name for every page under
  erkinbek.github.io from this page, so it must exist (it was a 404 before 2026-11-21).
- `robots.txt`: crawlers read it only at the root; it points them to every project's sitemap.
- `2b24ed08fffacabd79b9d88b56cf09dd.txt`: the [IndexNow](https://www.indexnow.org/) key, so new or changed pages can be
  sent to Bing, Yandex, Seznam and Naver at once (see below).
- `404.html`: shown for paths that no project site serves.
- Search engine verification files (`google*.html`, `BingSiteAuth.xml`, `yandex_*.html`)
  go here too, at the root, so one verification covers all the projects.

`python tools/icons.py` redraws the favicons (needs Pillow).

## Telling search engines about changed pages

```sh
python tools/indexnow.py https://erkinbek.github.io/bigtext/sitemap.xml
```

sends every URL of the given sitemaps (or plain URLs) to IndexNow. Google does not take
IndexNow; it reads the sitemaps listed in Search Console.
