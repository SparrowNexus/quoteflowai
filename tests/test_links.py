from pathlib import Path
from html.parser import HTMLParser
import unittest
ROOT=Path(__file__).resolve().parents[1]/'public'
class LinkParser(HTMLParser):
    def __init__(self): super().__init__(); self.hrefs=[]; self.srcs=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'href' in a: self.hrefs.append(a['href'])
        if 'src' in a: self.srcs.append(a['src'])
class StaticLinkTests(unittest.TestCase):
    def test_local_links_resolve(self):
        route_files={'/':'index.html','/features':'features.html','/how-it-works':'how-it-works.html','/solutions':'solutions.html','/about':'about.html','/contact':'contact.html','/terms':'terms.html','/privacy':'privacy.html','/software-license':'software-license.html','/refunds':'refunds.html','/intellectual-property':'intellectual-property.html','/customer-exit':'customer-exit.html','/security':'security.html','/accessibility':'accessibility.html','/login':'login.html'}
        missing=[]
        for f in ROOT.glob('*.html'):
            parser=LinkParser(); parser.feed(f.read_text(encoding='utf-8'))
            for url in parser.hrefs+parser.srcs:
                if url.startswith(('#','mailto:','tel:','https://','http://','data:')): continue
                path=url.split('?')[0].split('#')[0]
                if not path: continue
                if path in route_files:
                    target=ROOT/route_files[path]
                else:
                    target=ROOT/path.lstrip('/')
                    if path.endswith('/') and path!='/': target=ROOT/(path.strip('/')+'.html')
                if not target.exists(): missing.append(f'{f.name}: {url}')
        self.assertEqual(missing,[], '\n'.join(missing))
if __name__=='__main__': unittest.main(verbosity=2)
