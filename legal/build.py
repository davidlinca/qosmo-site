#!/usr/bin/env python3
"""Generate the hosted legal pages from their markdown sources.

The markdown files in this folder are the single source of truth. Edit those,
re-run this, and the HTML follows — so the published pages can never drift away
from the version you actually reviewed.

    python3 legal/build.py

Writes ../privacy.html and ../terms.html, i.e. straight into the site root
where Vercel serves them as /privacy and /terms. It writes to the deployed
location on purpose: an intermediate copy step is a step someone forgets, and
the failure mode is a live policy that silently lags behind the reviewed one.

Never edit privacy.html or terms.html directly — this overwrites them.
"""

import re
from pathlib import Path

import markdown

HERE = Path(__file__).parent          # legal/ — the markdown sources
OUT  = HERE.parent                    # site root — where Vercel serves from

PAGES = [
    ("privacy-policy.md", "privacy.html", "Privacy Policy — QOSMO"),
    ("terms-of-use.md", "terms.html", "Terms of Use — QOSMO"),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="robots" content="index, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  /* Palette and type matched to qosmoapp.com so the legal pages read as part
     of the same product. A policy that looks like it came from somewhere else
     is one people trust less, and Apple's reviewer follows these links too. */
  :root {{
    --ink-900:#12151A;
    --ink-800:#1B1F26;
    --paper:#EDEEEC;
    --paper-dim:#9CA0A8;
    --amber:#C9915B;
    --amber-soft:#E3B98A;
    --line:rgba(237,238,236,0.10);
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{
    background:var(--ink-900);
    color:var(--paper);
    font-family:'Space Grotesk', sans-serif;
    font-size:16px; line-height:1.65;
    -webkit-font-smoothing:antialiased;
  }}
  nav {{
    position:sticky; top:0; z-index:50;
    background:rgba(18,21,26,0.85);
    backdrop-filter:blur(10px);
    border-bottom:1px solid var(--line);
  }}
  nav .bar {{
    max-width:820px; margin:0 auto; padding:0 24px;
    height:76px; display:flex; align-items:center; justify-content:space-between;
  }}
  .logo {{
    font-family:'Instrument Serif', serif; font-size:26px;
    letter-spacing:0.04em; text-decoration:none; color:var(--paper);
  }}
  .logo span {{ color:var(--amber); }}
  .back {{ font-size:14px; color:var(--paper-dim); text-decoration:none; }}
  .back:hover {{ color:var(--paper); }}

  main {{ max-width:820px; margin:0 auto; padding:64px 24px 96px; }}
  h1 {{
    font-family:'Instrument Serif', serif; font-weight:400;
    font-size:clamp(36px,6vw,52px); line-height:1.1; margin:0 0 8px;
  }}
  h2 {{
    font-family:'Instrument Serif', serif; font-weight:400;
    font-size:28px; line-height:1.25; margin:56px 0 14px;
  }}
  h3 {{ font-size:17px; font-weight:600; margin:32px 0 8px; }}
  p, li {{ color:var(--paper-dim); }}
  strong {{ color:var(--paper); font-weight:600; }}
  a {{ color:var(--amber-soft); }}
  a:hover {{ color:var(--amber); }}
  hr {{ border:0; border-top:1px solid var(--line); margin:48px 0; }}
  table {{
    width:100%; border-collapse:collapse; margin:24px 0; font-size:15px;
    display:block; overflow-x:auto;
  }}
  th, td {{ text-align:left; padding:12px 14px; border-bottom:1px solid var(--line); }}
  th {{ color:var(--paper); font-weight:600; }}
  td {{ color:var(--paper-dim); }}
  ul {{ padding-left:22px; margin:12px 0; }}
  li {{ margin:8px 0; }}
  code {{
    font:13px ui-monospace, SFMono-Regular, Menlo, monospace;
    background:rgba(237,238,236,0.08); padding:2px 6px; border-radius:4px;
    color:var(--paper);
  }}
  footer {{
    margin-top:72px; padding-top:28px; border-top:1px solid var(--line);
    color:var(--paper-dim); font-size:14px;
    display:flex; justify-content:space-between; flex-wrap:wrap; gap:16px;
  }}
  footer .links {{ display:flex; gap:24px; }}
  @media (max-width:600px) {{ h2 {{ font-size:24px; }} }}
</style>
</head>
<body>
<nav>
  <div class="bar">
    <a class="logo" href="/">QOS<span>MO</span></a>
    <a class="back" href="/">&larr; Back to site</a>
  </div>
</nav>
<main>
{body}
<footer>
  <div>&copy; 2026 DAVILEX SOFT S.R.L.</div>
  <div class="links">
    <a href="/privacy">Privacy</a>
    <a href="/terms">Terms</a>
    <a href="mailto:david@qosmoapp.com">Contact</a>
  </div>
</footer>
</main>
</body>
</html>
"""


def build():
    for src_name, out_name, title in PAGES:
        src = (HERE / src_name).read_text(encoding="utf-8")

        # Strip HTML comments — they carry internal TODOs that must not ship.
        src, removed = re.subn(r"<!--.*?-->", "", src, flags=re.DOTALL)

        html = markdown.markdown(src, extensions=["tables", "attr_list"])
        page = TEMPLATE.format(title=title, body=html)
        (OUT / out_name).write_text(page, encoding="utf-8")

        note = f" (stripped {removed} internal comment(s))" if removed else ""
        print(f"  {src_name} → {out_name}{note}")


if __name__ == "__main__":
    print("Building legal pages:")
    build()
    print("Done.")
