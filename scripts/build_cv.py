"""Build the public CV from the same paper records as the website.

Requires XeLaTeX with ctex/Fandol fonts. Intermediate files stay in .work/.
"""
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
papers = json.loads((ROOT / 'content/papers.json').read_text())

def tex(text):
    replacements = {'&': r'\&', '%': r'\%', '_': r'\_', '#': r'\#',
                    '$': r'\$', '–': '--', '—': '---'}
    return ''.join(replacements.get(char, char) for char in str(text))

def entry(paper):
    authors = ', '.join(r'\textbf{' + tex(name) + '}' if name in ('Ruochen Dai', '戴若尘')
                        else tex(name) for name in paper['authors'])
    citation = authors + '. (' + str(paper['year']) + '). '
    citation += r'\href{https://ruochendai-econ.github.io/' + paper['pdf'] + '}{' + tex(paper['title']) + '}. '
    if paper['journal']:
        citation += r'\emph{' + tex(paper['journal']) + '}'
        if paper.get('volume'):
            citation += ', ' + paper['volume']
        if paper.get('number'):
            citation += '(' + paper['number'] + ')'
        locator = paper.get('pages') or paper.get('article_number')
        if locator:
            citation += ', ' + locator
        if paper.get('note'):
            citation += ', ' + paper['note'].lower()
        citation += '.'
    return r'\item ' + citation

def section(title, status, language):
    selected = [p for p in papers if p['status'] == status and p['language'] == language]
    return ('\\begin{rSection}{' + title + '}\n\\begin{enumerate}\n'
            + '\n\n'.join(entry(p) for p in selected)
            + '\n\\end{enumerate}\n\\end{rSection}\n')

grants = json.loads((ROOT / 'content/grants.json').read_text())
grant_entries = []
for grant in grants:
    heading = grant['type'] + ', ' + grant['funder']
    description = tex(grant['title']) + '.'
    if grant['title_zh']:
        description += r'\\ {\small ' + tex(grant['title_zh']) + '}'
    description += r'\\ Grant No. ' + grant['number']
    if grant['period']:
        description += '; ' + tex(grant['period'])
    grant_entries.append(r'\item \textbf{' + tex(heading) + '}. ' + description + '.')
grant_section = (r'\begin{rSection}{Research Grants}' + '\n' + r'\begin{enumerate}'
                 + '\n' + '\n\n'.join(grant_entries) + '\n'
                 + r'\end{enumerate}\end{rSection}')

source = (ROOT / 'cv/source/template.tex').read_text()
source = source.replace('%% RESEARCH_GRANTS %%', grant_section)
for marker, title, status, language in [
    ('ENGLISH_PUBLICATIONS', 'English Publications', 'publication', 'en'),
    ('CHINESE_PUBLICATIONS', 'Publications in Chinese', 'publication', 'zh'),
    ('WORKING_PAPERS', 'Working Papers', 'working-paper', 'en'),
]:
    source = source.replace('%% ' + marker + ' %%', section(title, status, language))
for private in ('18500186696', 'Room 406', 'Building 11'):
    assert private not in source
(ROOT / 'cv/source/main.tex').write_text(source)
build = ROOT / '.work/cv-build'
build.mkdir(parents=True, exist_ok=True)
engine = shutil.which('xelatex') or '/Library/TeX/texbin/xelatex'
command = [engine, '-no-shell-escape', '-interaction=nonstopmode', '-halt-on-error',
           '-output-directory=' + str(build), 'main.tex']
for _ in range(2):
    result = subprocess.run(command, cwd=ROOT / 'cv/source', capture_output=True, text=True)
    (build / 'build-output.txt').write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError('CV compilation failed; see .work/cv-build/build-output.txt')
shutil.copyfile(build / 'main.pdf', ROOT / 'cv/ruochen-dai-cv.pdf')
# Keep previously shared URLs working, with the same updated public content.
shutil.copyfile(build / 'main.pdf', ROOT / 'cv/ruochen-dai-cv-2025.pdf')
print('Built public CV from all 16 website entries.')
