"""Replace deployment-domain placeholders across static SEO files."""
from pathlib import Path
import sys
root=Path(__file__).resolve().parent/'public'
if len(sys.argv)!=2 or not sys.argv[1].startswith('https://'):
    print('Usage: python configure_site.py https://your-real-domain.example'); raise SystemExit(2)
origin=sys.argv[1].rstrip('/')
for path in root.rglob('*'):
    if path.is_file() and path.suffix in {'.html','.xml','.txt'}:
        data=path.read_text(encoding='utf-8')
        path.write_text(data.replace('https://YOUR-DOMAIN.example',origin),encoding='utf-8')
print(f'Configured canonical URLs, schema and sitemap for {origin}')
