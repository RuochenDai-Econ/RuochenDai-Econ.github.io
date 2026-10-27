"""Build the static homepage and three research category pages using Python's standard library.

Edit content/papers.json for research entries and content/profile.json for the
biography. Run python3 scripts/build.py, then commit the generated HTML too.
GitHub Pages serves the files directly; it does not need Python or JavaScript.
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
papers = json.loads((ROOT / 'content/papers.json').read_text())
profile = json.loads((ROOT / 'content/profile.json').read_text())
SITE = 'https://ruochendai-econ.github.io'


def page(title, body, current, prefix='', path='/'):
    navigation = []
    for label, path, key in [('Home', '', 'home'), ('Research', 'research/', 'research'),
                             ('CV (2025)', profile['cv'], 'cv')]:
        active = ' aria-current="page"' if key == current else ''
        navigation.append(f'<a href="{prefix}{path or "./"}"{active}>{label}</a>')
    description = ('Ruochen Dai, economist at the Central University of Finance and Economics. '
                   'Research on entrepreneurship, firm dynamics, and development economics.')
    url = SITE + path
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} | Ruochen Dai</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#8c202a">
  <meta property="og:title" content="{escape(title)} | Ruochen Dai">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/ruochen-dai.jpg">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="wordmark" href="{prefix or './'}">Ruochen Dai <span lang="zh-CN">戴若尘</span></a>
      <nav aria-label="Main navigation">{' '.join(navigation)}</nav>
    </div>
  </header>
  {body}
  <footer class="site-footer">
    <span>Ruochen Dai · Central University of Finance and Economics</span>
    <a href="mailto:{profile['email']}">{profile['email']}</a>
  </footer>
</body>
</html>
'''


def publication_details(paper):
    details = paper.get('volume', '')
    if paper.get('number'):
        details += f'({paper["number"]})'
    locator = paper.get('pages', '').replace('--', '–') or paper.get('article_number', '')
    if locator:
        details += (', ' if details else '') + locator
    return details or paper.get('note', '')


def paper_row(paper, prefix):
    chinese = paper['language'] == 'zh'
    coauthors = [name for name in paper['authors'] if name not in ('Ruochen Dai', '戴若尘')]
    if chinese:
        authors = '与' + '、'.join(coauthors) + '合作'
    elif len(coauthors) > 1:
        authors = 'with ' + ', '.join(coauthors[:-1]) + ' and ' + coauthors[-1]
    else:
        authors = 'with ' + coauthors[0]
    journal = ''
    if paper['journal']:
        journal = (f'<p class="journal"><em>{escape(paper["journal"])}</em>, '
                   f'{paper["year"]}. {escape(publication_details(paper))}.</p>')
    links = [f'<a href="{prefix}{paper["pdf"]}">Paper</a>']
    if paper['doi']:
        links.append(f'<a href="https://doi.org/{escape(paper["doi"])}">Journal</a>')
    links.append(f'<a href="{prefix}papers/{paper["id"]}.bib" download>BibTeX</a>')
    language = 'zh-CN' if chinese else 'en'
    abstract_label = '摘要' if chinese else 'Abstract'
    return f'''<article class="paper" id="{paper['id']}" lang="{language}">
      <div class="paper-info">
        <h3>{escape(paper['title'])}</h3>
        <p class="coauthors">{escape(authors)}</p>
        {journal}
        <p class="paper-links">{' <span aria-hidden="true">|</span> '.join(links)}</p>
      </div>
      <details class="paper-abstract"><summary>{abstract_label}</summary>
        <p class="abstract">{escape(paper['abstract'])}</p>
      </details>
    </article>'''


def write_bibtex(paper):
    fields = {'title': '{' + paper['title'] + '}',
              'author': ' and '.join('{' + a + '}' if paper['language'] == 'zh' else a for a in paper['authors']),
              'year': str(paper['year'])}
    if paper['journal']:
        fields['journal'] = paper['journal']
    if paper['doi']:
        fields['doi'] = paper['doi']
    for key in ('volume', 'number', 'pages', 'note'):
        if paper.get(key):
            fields[key] = paper[key]
    # Standard BibTeX styles print electronic article numbers from pages.
    if paper.get('article_number'):
        fields['pages'] = paper['article_number']
    fields['url'] = SITE + '/' + paper['pdf']
    kind = 'article' if paper['status'] == 'publication' else 'unpublished'
    # Escape TeX special characters without changing author order or title case.
    lines = [f'@{kind}{{{paper["id"]},']
    for key, value in fields.items():
        value = value.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_')
        lines.append(f'  {key} = {{{value}}},')
    lines.append('}')
    (ROOT / 'papers' / (paper['id'] + '.bib')).write_text('\n'.join(lines) + '\n')


for paper in papers:
    assert paper['status'] in ('publication', 'working-paper')
    assert (ROOT / paper['pdf']).is_file(), paper['pdf']
    write_bibtex(paper)
assert len({p['id'] for p in papers}) == len(papers)

categories = [
    ('english', 'English Publications', 'research/', 'publication', 'en'),
    ('chinese', '中文发表', 'research/chinese/', 'publication', 'zh'),
    ('working', 'Working Papers', 'research/working-papers/', 'working-paper', 'en'),
]
for category, label, path, status, language in categories:
    prefix = '../' * path.count('/')
    selected = [p for p in papers if p['status'] == status and p['language'] == language]
    navigation = []
    for key, nav_label, nav_path, _, _ in categories:
        active = ' aria-current="page"' if key == category else ''
        navigation.append(f'<a href="{prefix}{nav_path}"{active}>{nav_label}</a>')
    rows = '\n'.join(paper_row(p, prefix) for p in selected)
    research = f'''<main id="main" class="research-page">
    <div class="page-heading"><h1>Research</h1>
      <nav class="section-nav" aria-label="Research categories">{' '.join(navigation)}</nav>
    </div>
    <section aria-labelledby="category-heading">
      <h2 id="category-heading">{label}</h2>
      {rows}
    </section>
    <p class="back-top"><a href="#main">Back to top ↑</a></p>
  </main>'''
    destination = ROOT / path / 'index.html'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page(label, research, 'research', prefix, '/' + path))

biography = '\n'.join('<p>' + escape(paragraph) + '</p>' for paragraph in profile['biography'])
home = f'''<main id="main" class="home-page">
    <section class="profile" aria-labelledby="name">
      <div class="portrait-column">
        <img class="portrait" src="assets/ruochen-dai.jpg" alt="Ruochen Dai punting on a river" width="768" height="1024" fetchpriority="high">
      </div>
      <div class="biography">
        <h1 id="name">Ruochen Dai <span lang="zh-CN">戴若尘</span></h1>
        <p class="position">{escape(profile['position'])}<br>
          <a href="https://econ.cufe.edu.cn/">School of Economics</a><br>
          Central University of Finance and Economics</p>
        {biography}
        <p>I serve as Data Editor at <em>China Economic Review</em>.</p>
        <p class="contact"><a href="mailto:{profile['email']}">{profile['email']}</a></p>
        <p class="profile-links"><a href="research/">Research</a><span aria-hidden="true"> / </span>
          <a href="{profile['cv']}">CV (2025) <span class="file-type">PDF</span></a><span aria-hidden="true"> / </span>
          <a href="https://econ.cufe.edu.cn/info/1033/6641.htm">University profile</a></p>
      </div>
    </section>
    <section class="home-research" aria-labelledby="research-heading">
      <div><h2 id="research-heading">Research</h2><p>Entrepreneurship · Firm dynamics · Development economics</p></div>
      <div class="research-intro"><p>My work examines how entrepreneurs create and grow firms, and how networks, institutions, and technology shape these decisions.</p>
        <a href="research/">Publications &amp; working papers →</a></div>
    </section>
  </main>'''

(ROOT / 'index.html').write_text(page('Home', home, 'home'))
print(f'Built Home and three research categories with {len(papers)} papers and BibTeX files.')
