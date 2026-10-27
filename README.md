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
- `content/papers.json`：论文标题、作者（保留论文署名顺序）、期刊、年份、摘要、PDF 和 DOI。
- `papers/`：对外提供的论文 PDF 与 BibTeX。
- `cv/ruochen-dai-cv-2025.pdf`：用户提供的 Overleaf 项目中 `cv2025.tex` 的公开版本，已按作者要求删除手机号和具体办公室信息。此文件含早期论文状态；网页列表独立使用最新材料。
- `assets/style.css`：字号、颜色、间距与手机布局。
- `scripts/build.py`：用 Python 标准库生成静态 HTML 和 BibTeX。网站运行不依赖 Python 或 JavaScript。

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
