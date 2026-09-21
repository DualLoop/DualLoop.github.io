"""Apply the same primary navigation to every public HTML page."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
LINKS=[('index.html','Overview'),('questions.html','Questions'),('programs.html','Programs'),('steering.html','Image support'),('results.html','Results')]
def sync(root=ROOT):
    site_url=json.loads((root/'data/site.json').read_text()).get('url','').rstrip('/')
    for page in root.glob('*.html'):
        text=page.read_text()
        if not re.search(r'<nav\b[^>]*class="(?:site-nav|inverse-nav)"',text):
            continue
        active='steering.html' if page.name=='steering-gallery.html' else 'programs.html' if page.name=='inverse-programs.html' else page.name
        links=''.join(f'<a href="{url}"'+(' aria-current="page"' if url==active else '')+f'>{label}</a>' for url,label in LINKS)
        nav='<nav class="site-nav" aria-label="Main navigation"><a class="wordmark" href="index.html" aria-label="DualLoop home">DualLoop</a><div class="nav-links">'+links+'</div></nav>'
        text=re.sub(r'<nav\b[^>]*class="(?:site-nav|inverse-nav)"[^>]*>.*?</nav>',nav,text,count=1,flags=re.S)
        if 'static/css/navigation.css' not in text:
            text=text.replace('</head>','<link rel="stylesheet" href="static/css/navigation.css"></head>')
        # Keep primary navigation outside the article on the legacy examples page.
        if page.name == 'inverse-programs.html':
            text=text.replace(nav,'',1)
            text=re.sub(r'(<body[^>]*>)',lambda m:m.group(1)+nav,text,count=1)
        text=re.sub(r'<link[^>]*href="static/css/reading.css"[^>]*>', '', text)
        text=text.replace('</head>','<link rel="stylesheet" href="static/css/reading.css"></head>')
        if site_url:
            url=site_url+'/'+('' if page.name=='index.html' else page.name)
            text=re.sub(r'<meta[^>]*property="og:url"[^>]*>\s*', '', text)
            text=re.sub(r'<link[^>]*rel="canonical"[^>]*>\s*', '', text)
            text=text.replace('</head>',f'<meta property="og:url" content="{url}" />\n<link rel="canonical" href="{url}" />\n</head>')
        page.write_text(text)
if __name__=='__main__': sync()
