# simonvalentine.com

Personal website of Simon Valentine. A plain static site (HTML, CSS, a few lines of JavaScript) published with GitHub Pages.

## Editing

All page text, links and the three articles live in one file: `_build/build.py`.

1. Edit the text in `_build/build.py` (or the styles in `assets/css/site.css`).
2. Run `python3 _build/build.py` from the repository root. It regenerates every page.
3. Commit and push to `main`. GitHub Pages publishes within a minute or two.

Folders starting with `_` are not published, so the build script stays private to the repo.

## Structure

| Path | Page |
| --- | --- |
| `index.html` | Home |
| `about/`, `work/`, `ventures/`, `articles/`, `contact/` | Main pages |
| `go/` | Link-in-bio page |
| `<article-slug>/` | Articles (same addresses as the old WordPress site) |
| `privacy-policy/`, `terms-of-service/` | Legal |
| `assets/` | Stylesheet, script and photos |

## Contact details policy

The site lists LinkedIn and email only. No phone number, WhatsApp or Instagram.

## Custom domain

To serve this at simonvalentine.com: in the repository's **Settings → Pages**, set the custom domain to `simonvalentine.com`, then point the domain's DNS at GitHub Pages:

- `A` records for `simonvalentine.com`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- `CNAME` record for `www`: `simonvalentine.github.io`

Then tick **Enforce HTTPS** once the certificate is issued.
