import json, os, subprocess, sys, time, unittest, urllib.request, urllib.error, socket
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class WebsiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sock=socket.socket(); sock.bind(('127.0.0.1',0)); cls.port=sock.getsockname()[1]; sock.close()
        env=os.environ.copy(); env.update({'HOST':'127.0.0.1','PORT':str(cls.port),'APP_URL':'','SMTP_HOST':'','SMTP_USER':'','SMTP_PASSWORD':''})
        cls.proc=subprocess.Popen([sys.executable,str(ROOT/'server.py')],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        cls.base=f'http://127.0.0.1:{cls.port}'
        for _ in range(50):
            try:
                urllib.request.urlopen(cls.base+'/health',timeout=.2); break
            except Exception: time.sleep(.1)
        else: raise RuntimeError('Test server did not start')
    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate(); cls.proc.wait(timeout=3)
    def get(self,path):
        return urllib.request.urlopen(self.base+path,timeout=2)
    def test_all_pages_render(self):
        for route in ['/','/features','/how-it-works','/solutions','/about','/contact','/terms','/privacy','/software-license','/refunds','/intellectual-property','/customer-exit','/security','/accessibility','/login']:
            with self.subTest(route=route):
                r=self.get(route); self.assertEqual(r.status,200); body=r.read().decode(); self.assertIn('<main id="main">',body); self.assertIn('A product of Sparrow Nexus',body)
    def test_static_assets(self):
        for path in ['/assets/site.css','/assets/site.js','/assets/favicon.svg','/assets/quoteflow-logo.png','/assets/app-interface-reference.png','/robots.txt','/sitemap.xml']:
            with self.subTest(path=path): self.assertEqual(self.get(path).status,200)
    def test_security_headers(self):
        r=self.get('/'); self.assertEqual(r.headers['X-Content-Type-Options'],'nosniff'); self.assertEqual(r.headers['X-Frame-Options'],'DENY'); self.assertIn('Content-Security-Policy',r.headers)
    def test_unknown_route_returns_custom_404(self):
        with self.assertRaises(urllib.error.HTTPError) as err: self.get('/does-not-exist')
        self.assertEqual(err.exception.code,404); self.assertIn(b'This page could not be found',err.exception.read())
    def post(self,payload):
        req=urllib.request.Request(self.base+'/api/enquiry',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST')
        try: return urllib.request.urlopen(req,timeout=3)
        except urllib.error.HTTPError as e: return e
    def test_form_validates_server_side(self):
        r=self.post({'name':'','email':'bad','company':'','type':'Nope','message':'x','privacy':False})
        self.assertEqual(r.code,400); self.assertFalse(json.loads(r.read())['ok'])
    def test_form_reports_missing_email_configuration(self):
        r=self.post({'name':'Taylor','email':'taylor@example.com','company':'Example Co','type':'Product enquiry','message':'Please tell me more about this product.','privacy':True,'phone':'','website':''})
        self.assertEqual(r.code,503); self.assertIn('not configured',json.loads(r.read())['message'])
    def test_health(self): self.assertEqual(json.loads(self.get('/health').read())['status'],'ok')
if __name__=='__main__': unittest.main(verbosity=2)
