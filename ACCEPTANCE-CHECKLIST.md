# QuoteFlow AI website acceptance checklist

## Implemented in source
- [x] Separate public website; no app database or private API connection.
- [x] Supplied QuoteFlow AI logo and application screenshot included.
- [x] Homepage brand/title/subtitle/attribution order matches the approved request.
- [x] Green/teal visual identity, responsive layouts, keyboard focus and reduced-motion handling.
- [x] Multi-page navigation and legal/support page templates.
- [x] One-time licence wording without invented price or implied perpetual rights.
- [x] Configurable login destination; no password collection.
- [x] Server-side enquiry validation, size limit, honeypot, basic rate limiting and optional SMTP.
- [x] Security headers, custom 404, SEO metadata, structured data, robots and sitemap templates.
- [x] Environment-variable example and deployment instructions.

## Must verify before launch
- [ ] Select and configure the production domain.
- [ ] Confirm the official Sparrow Nexus AI destination URL.
- [ ] Confirm `quoteflowai@gmail.com` and `info@sparrownexus.in` are monitored and correct.
- [ ] Configure SMTP credentials and verify real delivery end-to-end.
- [ ] Deploy and verify the private application; configure `APP_URL`.
- [ ] Verify every advertised capability against the exact released app version.
- [ ] Finalise one-time licence duration, permitted users, updates, support, price, taxes, refunds, termination and exit terms.
- [ ] Provide verified contracting entity and address; obtain legal review of all policies.
- [ ] Configure HTTPS, DNS, security headers at the edge, logs, monitoring and backups.
- [ ] Replace domain placeholders in canonical tags, structured data, sitemap and robots.
- [ ] Run deployed route/form/security smoke tests and keyboard/screen reader/mobile accessibility review.
- [ ] Decide whether to enable analytics and implement appropriate consent before doing so.
- [ ] Confirm the chosen host supports the Python enquiry endpoint or migrate it to an appropriate serverless/service architecture.
