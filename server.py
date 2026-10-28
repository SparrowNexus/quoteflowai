"""QuoteFlow AI public website and enquiry endpoint. Python 3.11+; no runtime dependencies."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from email.message import EmailMessage
import json, os, re, smtplib, time, html

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / 'public'
HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', '8000'))
CONTACT_EMAIL = os.getenv('CONTACT_EMAIL', 'quoteflowai@gmail.com')
SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', 'info@sparrownexus.in')
APP_URL = os.getenv('APP_URL', '')
CANONICAL_ORIGIN = os.getenv('PUBLIC_SITE_URL', 'http://localhost:8000').rstrip('/')
SPARROW_URL = os.getenv('SPARROW_AI_URL', 'https://ai.sparrownexus.in/').strip()
SMTP_HOST = os.getenv('SMTP_HOST', '')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SMTP_FROM = os.getenv('SMTP_FROM', SMTP_USER or CONTACT_EMAIL)

RATE = {}
EMAIL_RE = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
PAGES = {'/':'index.html','/features':'features.html','/how-it-works':'how-it-works.html','/solutions':'solutions.html','/about':'about.html','/contact':'contact.html','/terms':'terms.html','/privacy':'privacy.html','/software-license':'software-license.html','/refunds':'refunds.html','/intellectual-property':'intellectual-property.html','/customer-exit':'customer-exit.html','/security':'security.html','/accessibility':'accessibility.html'}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','strict-origin-when-cross-origin')
        self.send_header('Permissions-Policy','camera=(), microphone=(), geolocation=()')
        self.send_header('Content-Security-Policy', "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; form-action 'self'; base-uri 'self'; frame-ancestors 'none'")
        self.send_header('X-Frame-Options','DENY')
        super().end_headers()
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/health':
            return self._json(200, {'status':'ok','service':'quoteflow-public-site'})
        if path == '/robots.txt':
            self.path = '/robots.txt'; return super().do_GET()
        if path == '/sitemap.xml':
            self.path = '/sitemap.xml'; return super().do_GET()
        if path in PAGES:
            self.path = '/' + PAGES[path]; return super().do_GET()
        if path == '/login':
            if APP_URL:
                self.send_response(302); self.send_header('Location', APP_URL); self.end_headers(); return
            self.path = '/login-unavailable.html'; return super().do_GET()
        if path == '/favicon.ico': self.path = '/assets/favicon.svg'; return super().do_GET()
        if path.startswith('/assets/'):
            return super().do_GET()
        self.send_response(404)
        self.send_header('Content-Type','text/html; charset=utf-8')
        body = (PUBLIC / '404.html').read_bytes()
        self.send_header('Content-Length', str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        if urlparse(self.path).path != '/api/enquiry':
            return self._json(404, {'ok':False,'message':'Endpoint not found.'})
        ip = self.client_address[0]
        now = time.time(); hits = [t for t in RATE.get(ip, []) if now-t < 600]
        if len(hits) >= 5:
            RATE[ip] = hits; return self._json(429, {'ok':False,'message':'Too many requests. Please try again later or email us directly.'})
        hits.append(now); RATE[ip] = hits
        try:
            length = int(self.headers.get('Content-Length','0'))
            if length <= 0 or length > 16000: return self._json(413, {'ok':False,'message':'The message is too large.'})
            data = json.loads(self.rfile.read(length))
            # Honeypot field: return a generic success without sending.
            if str(data.get('website','')).strip(): return self._json(200, {'ok':True,'message':'Thank you. Your enquiry has been received.'})
            name = clean(data.get('name'), 100); email = clean(data.get('email'), 254)
            company = clean(data.get('company'), 150); kind = clean(data.get('type'), 80)
            phone = clean(data.get('phone'), 40); message = clean(data.get('message'), 4000)
            consent = data.get('privacy') is True
            if not name or not EMAIL_RE.match(email) or not company or kind not in {'Product enquiry','Licence enquiry','Request a demo','Support','Other'} or len(message) < 10 or not consent:
                return self._json(400, {'ok':False,'message':'Please check the required fields and privacy acknowledgement.'})
            if not SMTP_HOST or not SMTP_USER or not SMTP_PASSWORD:
                return self._json(503, {'ok':False,'message':'The enquiry form is not configured yet. Please email quoteflowai@gmail.com directly.'})
            msg = EmailMessage(); msg['Subject'] = f'QuoteFlow AI website enquiry — {kind}'; msg['From'] = SMTP_FROM; msg['To'] = CONTACT_EMAIL; msg['Reply-To'] = email
            msg.set_content(f"New QuoteFlow AI website enquiry\n\nName: {name}\nBusiness email: {email}\nCompany: {company}\nEnquiry type: {kind}\nPhone: {phone or 'Not provided'}\n\nMessage:\n{message}\n")
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=12) as server:
                server.starttls(); server.login(SMTP_USER, SMTP_PASSWORD); server.send_message(msg)
            return self._json(200, {'ok':True,'message':'Thank you. Your enquiry has been sent.'})
        except (ValueError, json.JSONDecodeError): return self._json(400, {'ok':False,'message':'Please submit a valid enquiry.'})
        except Exception:
            return self._json(502, {'ok':False,'message':'We could not send your enquiry right now. Please email quoteflowai@gmail.com directly.'})
    def _json(self, status, obj):
        body = json.dumps(obj).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self, fmt, *args):
        # Keep routine logs useful without logging submitted form bodies.
        super().log_message(fmt, *args)

def clean(value, limit):
    if not isinstance(value, str): return ''
    value = ''.join(ch for ch in value.strip() if ch in '\n\r\t' or ord(ch) >= 32)
    return value[:limit]

if __name__ == '__main__':
    print(f'QuoteFlow AI website running at http://{HOST}:{PORT}')
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
