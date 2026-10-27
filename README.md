# Ruochen Dai — academic website

Personal academic website for GitHub Pages, inspired by the clear research layout of [Xianglong Sean Kong](https://www.xianglong-kong.com/research).

## 本地查看

在项目文件夹运行：

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

浏览器打开 http://127.0.0.1:8765 。按 Ctrl+C 停止。

## 修改内容

- `content/profile.json`：简介、职位、邮箱和 CV 文件路径。
- `content/papers.json`：论文标题、作者（保留论文署名顺序）、期刊、年份、卷（`volume`）、期（`number`）、页码（`pages`，用 `--` 连接）、文章编号（`article_number`）、摘要、PDF 和 DOI。
- `content/grants.json`：主页与 CV 共用的两个基金项目，保留可核实的名称、类别、编号和执行期；新项目英文标题为中文标题的译名。
- `papers/`：对外提供的论文 PDF 与 BibTeX。
- `cv/ruochen-dai-cv.pdf`：2026 年 10 月公开 CV。论文与网页共用 `content/papers.json`，仅保留作者确认的 16 篇；手机号和具体办公室不公开。旧的 2025 PDF 地址也提供同一份更新内容，以兼容已分享链接。
- `cv/source/`：公开 CV 的排版模板、生成后的 LaTeX 和样式文件，不含隐私信息。
- `assets/style.css`：字号、颜色、间距与手机布局。
- `scripts/build.py`：用 Python 标准库生成首页、三个独立论文分类页和 BibTeX。网站运行不依赖 Python 或 JavaScript。

修改内容后运行：

```sh
python3 scripts/build.py
```

将内容文件与生成的 HTML、BibTeX 一起提交。新增论文时在 `content/papers.json` 增加一条记录，并将 PDF 放入 `papers/`。`status` 只使用 `publication` 或 `working-paper`。`language` 使用 `en` 或 `zh`。`id` 必须唯一，并与 PDF 文件名对应。没有 DOI 时保留空字符串；不编造期刊或复制材料链接。

## 内容核对

本次收到 19 个 PDF，按标题、作者、DOI 和页数识别并合并 3 组重复论文，列出 16 篇：14 篇 Publications（含 forthcoming）与 2 篇 Working Papers。分组按作者本人确认：

- `Community Networks and Entrepreneurship in a Developing Economy`：Working Paper。
- `Export Destinations, Quality, and Automation: Evidence from China`：Working Paper；文件名中的 JIE 不作为发表信息。
- `Serial Entrepreneurship in China`：Publications，AEJ: Macroeconomics, forthcoming。

标题、署名与摘要以用户提供的论文为准，PDF 本身未修改。摘要仅整理 PDF 换行、断词和排版字符，不改写研究内容。任职与研究兴趣参考用户的 CV 和 [中央财经大学教师页](https://econ.cufe.edu.cn/info/1033/6641.htm)。教师页与论文标题存在差异时使用论文首页标题。中文论文保留中文标题和摘要。

`.work/` 保存本地原始 CV 源码、解析结果和验证记录，已被 Git 忽略，不上传到网站。原始 Dropbox 文件不作修改。网页只包含明确准备好的公开文件。

## GitHub Pages

目标仓库为 `RuochenDai-Econ/RuochenDai-Econ.github.io`。在仓库 Settings → Pages 中选择 Deploy from a branch，分支 `main`，目录 `/ (root)`。`.nojekyll` 允许直接提供这些静态文件。

目标地址：https://ruochendai-econ.github.io/

作者论文与照片的相关权利保留；本仓库不对这些材料授予额外使用许可。

## 论文分类与引文

Research 下的 English Publications、中文发表、Working Papers 分别显示 6、8、2 篇论文；摘要用原生 HTML details 默认收起，不依赖 JavaScript。

BibTeX 将卷、期、页码分别输出为 `volume`、`number`、`pages`。为兼容传统 BibTeX 样式，Elsevier 文章编号也输出在 `pages` 中；`note` 只记录 Forthcoming / Working paper。没有正式卷期的论文不编造卷期。网页与 BibTeX 共用这些结构化字段。

本轮核对以所提供 PDF 为基础，并补充 [JLEO 正式卷期 42(3):906–933](https://academic.oup.com/jleo/issue/42/3)、[AEJ 论文 DOI 与 forthcoming 状态](https://www.aeaweb.org/articles?id=10.1257/mac.20240030)、[经济管理学刊 3(2):55–82](https://ccj.pku.edu.cn/article/info?id=581530139787333)。

## 同步更新 CV

论文记录修改后，依次运行 `python3 scripts/build.py` 和 `python3 scripts/build_cv.py`。后者需要 XeLaTeX 和 ctex/Fandol 字体，生成公开 PDF；编译临时文件保存在 `.work/cv-build/`。`cv/source/template.tex` 保留原 CV 的非论文履历，论文条目自动插入生成 `main.tex`。Overleaf 原始项目未修改。

## Google 收录

网站允许搜索引擎抓取，四个页面在 `sitemap.xml` 中列出，页面有 canonical 地址。首页标题包含英文名、中文名、经济学家身份和 CUFE，并提供 Person 结构化信息。

目前未在本任务中验证 Google Search Console 或提交收录请求。网站所有者可添加 URL-prefix 属性 `https://ruochendai-econ.github.io/`，完成 HTML 文件或 meta 标签验证后提交 `sitemap.xml`，并用 URL Inspection 请求首页收录。抓取与排名由 Google 决定，不能保证时点或名次。
