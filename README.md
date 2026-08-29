# qosmoapp.com

Static site for QOSMO. Three pages, no framework, no build step for the site
itself — only the legal pages are generated.

```
index.html      marketing page
privacy.html    generated · served at /privacy
terms.html      generated · served at /terms
vercel.json     clean URLs, redirects, security headers
legal/
  privacy-policy.md   source of truth
  terms-of-use.md     source of truth
  build.py            regenerates the two HTML pages
```

## Deploy

```bash
npm i -g vercel     # once
vercel              # preview deploy, prints a URL to check
vercel --prod       # production
```

Then in the Vercel dashboard: **Settings → Domains → add `qosmoapp.com`**, and
point the domain's DNS at Vercel as instructed there.

Connecting this repo to Vercel via GitHub gives you automatic deploys on push,
plus a preview URL per pull request.

## The URLs are not cosmetic

`app/paywall/SubscriptionRequiredScreen.js` in the app repo links to:

```
https://qosmoapp.com/terms
https://qosmoapp.com/privacy
```

`vercel.json` sets `cleanUrls: true`, which is what makes `/privacy` serve
`privacy.html`. Remove it and both links 404 — and Apple rejects builds whose
legal links do not resolve. Open both in a browser after deploying, before
submitting.

## Editing the legal pages

**Never edit `privacy.html` or `terms.html` directly — they get overwritten.**
Edit the markdown, then:

```bash
python3 legal/build.py
```

It writes straight into the site root, so there is no copy step to forget. The
markdown stays the single source of truth, which is what stops a live policy
from quietly drifting away from the version you actually reviewed. `build.py`
also strips HTML comments, so internal notes in the markdown never ship.

These sources used to live in the app repo, which meant generating there and
copying here. That copy was the weak link, so they moved.

## Things deliberately not on this site

- **No email capture.** The original page had a waitlist form that discarded
  the address while telling people "You're on the list" — and it was broken
  anyway: the success handler looked for an element sitting outside the
  `<form>`, so it threw and nothing happened at all. Collecting emails would
  also bring a GDPR consent duty and a new privacy-policy section. Removed
  rather than fixed, since the app is at submission and there is nothing left
  to wait for.
- **No "accountability partner".** The original third feature card advertised
  private check-ins with a friend. That feature does not exist anywhere in the
  app — the card now describes the crystal streak system, which does.
- **No analytics.** Nothing to disclose, nothing to consent to, no cookie
  banner. Worth keeping that way unless there is a concrete reason not to.

## Contact address

Every route on the site, in the app, and in both legal documents points at
`david@qosmoapp.com`. The site previously advertised `support@qosmoapp.com`,
which appears nowhere else and may not receive mail. Guideline 1.2 requires
published contact information for apps with user-generated content, so this
address has to work. If you set up `support@`, change it in one pass across
`index.html`, both files in `legal/`, and `SettingsScreen.js` in the app repo.
