"""Render the CER source index. The input contains descriptions and DOI links only."""
from html import escape


def bilingual(text):
    return escape(text['en']) + '<span class="zh" lang="zh-CN">' + escape(text['zh']) + '</span>'


def source_link(source):
    label = bilingual(source)
    if source.get('url'):
        return '<a href="' + escape(source['url'], quote=True) + '">' + label + '</a>'
    return label


def render_index(catalog):
    references = catalog['references']
    categories = catalog['categories']
    navigation = ''.join('<a href="#' + category['id'] + '">' + bilingual(category['title']) + '</a>'
                         for category in categories)
    intro = {'en': 'Data sources used in China Economic Review research, with access information and paired links to each article and its Dataverse replication package.',
             'zh': 'China Economic Review研究的数据来源索引，列出获取条件，并逐篇配对文章与Dataverse复现包链接。'}
    sections = []
    headings = [('Dataset', '数据名称'), ('Source', '来源'), ('Access', '开放情况'),
                ('Article DOI', '文章 DOI'), ('Dataverse DOI', '复现包 DOI')]
    table_head = '<thead><tr>' + ''.join('<th scope="col">' + bilingual({'en': en, 'zh': zh}) + '</th>'
                                        for en, zh in headings) + '</tr></thead>'
    for category in categories:
        groups = []
        for dataset in category['datasets']:
            uses = dataset['uses']
            assert uses and len({row['paper'] for row in uses}) == len(uses)
            # Share identical cells; preserve study-specific distributors and access conditions.
            shared_source = all(row['source'] == uses[0]['source'] for row in uses)
            shared_access = all(row['access'] == uses[0]['access'] for row in uses)
            rows = []
            for index, row in enumerate(uses):
                paper = row['paper']
                ref = references[paper]
                cells = ''
                if index == 0:
                    description = dataset['description']
                    cells += f'<th scope="rowgroup" rowspan="{len(uses)}"><details class="dataset-details"><summary>'
                    cells += bilingual(dataset['name']) + '</summary><div class="dataset-description"><p>'
                    cells += escape(description['en']) + '</p><p class="zh" lang="zh-CN">'
                    cells += escape(description['zh']) + '</p></div></details></th>'
                if not shared_source or index == 0:
                    span = f' rowspan="{len(uses)}"' if shared_source else ''
                    cells += '<td' + span + '>' + source_link(row['source']) + '</td>'
                if not shared_access or index == 0:
                    span = f' rowspan="{len(uses)}"' if shared_access else ''
                    cells += '<td' + span + '>' + bilingual(row['access']) + '</td>'
                title = escape(ref['title'], quote=True)
                article_doi = escape(ref['article_doi'], quote=True)
                package_doi = escape(ref['dataverse_doi'], quote=True)
                cells += '<td class="study"><span class="citation">' + escape(ref['citation']) + '</span>'
                cells += f'<a class="doi" href="https://doi.org/{article_doi}" title="{title}">{article_doi}</a></td>'
                cells += f'<td class="study"><a class="doi" href="https://doi.org/{package_doi}" title="Replication package: {title}">{package_doi}</a></td>'
                rows.append(f'<tr data-paper="{paper}">' + cells + '</tr>')
            groups.append('<tbody class="dataset" data-dataset="' + dataset['id'] + '">' + ''.join(rows) + '</tbody>')
        heading_id = category['id'] + '-heading'
        sections.append('<section id="' + category['id'] + '" aria-labelledby="' + heading_id + '"><h2 id="' + heading_id + '">'
                        + bilingual(category['title']) + '</h2><div class="table-wrap" role="region" tabindex="0" aria-labelledby="'
                        + heading_id + '"><table>' + table_head + ''.join(groups) + '</table></div></section>')
    note = {'en': 'Access describes the source versions used in the studies. A public replication package may rely on restricted inputs. This site hosts descriptions and links only, not research data.',
            'zh': '开放情况指论文所用来源的获取条件；公开复现包仍可能使用受限原始数据。本站仅提供说明与链接，不存储研究数据。'}
    return ('<main id="main" class="cer-page"><div class="page-heading"><h1>CER Open Data</h1><p>'
            + bilingual(intro) + '</p><p class="expand-hint">'
            + bilingual({'en': 'Select a dataset name to read a brief description.', 'zh': '点击数据名称展开简介。'})
            + '</p><nav class="category-nav" aria-label="Data categories">' + navigation
            + '</nav></div>' + ''.join(sections) + '<div class="index-note"><p>' + bilingual(note)
            + '</p><p>Updated ' + escape(catalog['updated']) + '</p></div></main>')
