# QuoteFlow AI public website

A separate public marketing website for QuoteFlow AI. It does **not** connect to, modify, or expose the private QuoteFlow AI application's database or API. The supplied logo and application screenshot are included as assets.

## What's included

- Homepage, Features, How It Works, Solutions, About, Contact, and legal/support pages.
- The requested homepage hierarchy: **QuoteFlow AI** as the main brand, “Smarter Quotation Management. Better Business Visibility.” as subtitle, and “A product of Sparrow Nexus” directly below it.
- Subtle Sparrow Nexus attribution in the footer, opening `https://ai.sparrownexus.in/` in a new tab. The domain was supplied by the owner but could not be independently confirmed in the web search performed during this build; verify it before launch.
- One-time licence model explained in copy without inventing a price or asserting perpetual rights. Final licence duration and permitted use remain to be defined in the agreement.
- Responsive navigation, reduced-motion support, semantic forms, custom 404, SEO metadata, canonical placeholders, structured data, sitemap and robots file.
- A small Python standard-library server with a server-side enquiry endpoint, field validation, honeypot, request size limit, per-IP rate limit and optional SMTP delivery.
- Tests using Python's built-in `unittest`; no third-party Python packages required for local operation.

## Requirements

- Python 3.11 or newer (tested with Python 3.13).
- No Node/npm build is needed. The website is static HTML/CSS/JS served by Python.

## Run locally on Windows 11 / PowerShell

```powershell
cd path\to\quoteflow-ai-website
py -3 server.py
```

Open `http://127.0.0.1:8000`. Stop with `Ctrl+C`.

To use another port for the current PowerShell session:

```powershell
$env:PORT="8080"
py -3 server.py
```

## Tests

```powershell
py -3 -m unittest discover -s tests -v
```

The tests cover route responses, static assets, security headers, custom 404, server-side form validation, health endpoint and the unconfigured email state. They do **not** verify delivery through a real SMTP account or test a deployed domain.

## Configuration

Copy `.env.example` to `.env` as a reference. The included standard-library server does not automatically parse `.env`; export environment variables in your hosting dashboard or PowerShell. Never commit credentials.

PowerShell example (use credentials from a real provider; do not paste them into source files):

```powershell
$env:CONTACT_EMAIL="quoteflowai@gmail.com"
$env:SUPPORT_EMAIL="info@sparrownexus.in"
$env:APP_URL="https://YOUR-DEPLOYED-APP-URL"
$env:SMTP_HOST="YOUR-SMTP-HOST"
$env:SMTP_PORT="587"
$env:SMTP_USER="YOUR-SMTP-USERNAME"
$env:SMTP_PASSWORD="YOUR-SMTP-APP-PASSWORD"
$env:SMTP_FROM="YOUR-VERIFIED-SENDER"
$env:PUBLIC_SITE_URL="https://YOUR-DOMAIN"
$env:SPARROW_AI_URL="https://ai.sparrownexus.in/"
py -3 server.py
```

`APP_URL` is optional. Until set, Log In displays a clear not-configured page rather than collecting credentials. SMTP must be configured before the form can deliver email. The endpoint returns a helpful 503 message if delivery credentials are absent. Test delivery using a real enquiry before launch.

## Domain / SEO setup

After selecting the final public domain, run this once before deployment:

```powershell
py -3 configure_site.py https://your-real-domain.example
```

This replaces `https://YOUR-DOMAIN.example` in the static HTML, structured data, sitemap and robots file. Review the generated files and commit the configured versions. Do not publish while placeholder canonical URLs remain. The sitemap currently lists the intended indexable routes; `/login` is intentionally excluded.

## Deployment guidance

The provided Python server is a dependency-free reference implementation and is suitable for local testing. For production, deploy behind a reputable HTTPS-enabled host or reverse proxy that supports Python processes, environment variables, health checks and logs. The current site is **not a drop-in Vercel static deployment** because its enquiry endpoint runs in Python. If using Vercel for the static frontend, move `/api/enquiry` into a supported serverless function or host the full Python service separately, then configure CORS/origin and rate limiting carefully. Keep the application and public website as separate deployments.

Before go-live:

1. Choose a domain and configure DNS records at your registrar.
2. Deploy the site/service and force HTTPS; configure HSTS at the trusted HTTPS edge after HTTPS is confirmed.
3. Set environment variables in the hosting dashboard. Do not expose SMTP credentials in client-side JavaScript.
4. Verify the two support email addresses and configure a sender/domain authentication (SPF/DKIM/DMARC as applicable).
5. Send test enquiries and confirm actual delivery, reply-to behaviour, spam filtering, rate limiting and error handling.
6. Configure `APP_URL` only after the private application is deployed and its login path is tested.
7. Verify `https://ai.sparrownexus.in/` is the intended official destination.
8. Replace SEO placeholders, check canonical tags and sitemap, add the final domain to Google Search Console, and submit the sitemap.
9. Decide whether analytics will be enabled; it is not currently implemented or active.
10. Review all legal pages with qualified counsel and replace required legal placeholders before publication.
11. Run the test suite, review accessibility on keyboard/screen reader/mobile, and run a production smoke test.

## Important limitations and launch blockers

- No domain was supplied; SEO canonical/schema/sitemap placeholders need configuration.
- The legal business name and address have not been verified. “QuoteFlow AI — product of Sparrow Nexus” is a brand description, not necessarily the contracting entity.
- Legal documents are drafts and explicitly mark missing commercial/legal inputs. They require review before publication.
- Licence price is intentionally omitted. The one-time model is stated, but duration, permitted users, updates, support, refunds, termination and data exit terms need written confirmation.
- The application URL is not available. Login is intentionally not integrated.
- SMTP credentials are not provided; real form delivery remains unverified until configured and tested.
- `info@sparrownexus.in` and the Sparrow Nexus AI URL were supplied by the owner but should be verified before launch.
- No analytics, payment checkout, automatic provisioning, customer account system or application API integration is implemented.
- The interface screenshot is used as a visual reference. Its displayed counts and monetary values are not copied into marketing copy as claims.
- The existing application's administration, reporting and product editing issues have not been repaired or independently tested by this website build. Those features are not marketed as verified.
- A production deployment requires host-level HTTPS, DNS, logging/monitoring, backup and operational configuration. The local server alone is not a production hosting service.

## Project layout

```text
quoteflow-ai-website/
  server.py
  configure_site.py
  .env.example
  README.md
  build_pages.py
  public/
    *.html
    robots.txt
    sitemap.xml
    assets/
  tests/test_site.py
```

`build_pages.py` is the source generator used to create the static pages. If editing the page templates in that generator, rerun `py -3 build_pages.py`, then rerun the tests and SEO domain configuration.
