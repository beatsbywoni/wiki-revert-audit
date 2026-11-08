"""원고 Markdown → JASIST 제출용 Word(.docx) 변환.

- HTML 주석 제거, "[Figure N here]" 자리에 figures/FigureN.png 삽입(300 dpi, 폭 6 in)
- pandoc → docx, 이후 python-docx 로 본문 Times New Roman 12pt 1.5 줄간격, 표 9pt, 캡션·제목 서식
- JASIST: 제목은 번호 없음(pandoc 기본), 미주는 본문 끝 섹션으로 유지(ScholarOne 요구 시 Word 미주로 전환)
사용법: python build_docx.py <in.md> <out.docx> [--figdir DIR] [--pdf]
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Pt, Inches


def preprocess(md, figdir):
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    def fig(m):
        n = m.group(1); p = os.path.join(figdir, f"Figure{n}.png")
        return f"![]({p})" if os.path.exists(p) else f"[Figure {n} here]"
    md = re.sub(r"\[Figure (\w+) here\]", fig, md)
    md = re.sub(r"!\[\]\(figures/(Figure\w+)\.png\)", lambda m: f"![]({os.path.join(figdir, m.group(1))}.png)", md)
    md = re.sub(r"\n\[Abstract: \d+ words\]\n", "\n", md)
    return md


def set_run_font(run, name="Times New Roman", size=None):
    run.font.name = name
    r = run._element.rPr
    if r is not None:
        rf = r.find(qn("w:rFonts"))
        if rf is None:
            rf = r.makeelement(qn("w:rFonts"), {}); r.append(rf)
        for k in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            rf.set(qn(k), name)
    if size: run.font.size = Pt(size)


def get_style(d, name):
    for st in d.styles:
        if st.name == name:
            return st
    raise KeyError(name)


def style_doc(path):
    d = Document(path)
    for sname, size, bold in [("Normal", 12, None), ("Body Text", 12, None), ("First Paragraph", 12, None), ("Compact", 12, None),
                              ("Title", 16, True), ("Heading 1", 14, True), ("Heading 2", 12, True), ("Heading 3", 12, True)]:
        try:
            st = get_style(d, sname)
        except KeyError:
            continue
        st.font.name = "Times New Roman"; st.font.size = Pt(size)
        if bold is not None: st.font.bold = bold
        rpr = st.element.get_or_add_rPr(); rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = rpr.makeelement(qn("w:rFonts"), {}); rpr.append(rf)
        for k in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"): rf.set(qn(k), "Times New Roman")
        for k in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            if rf.get(qn(k)) is not None: del rf.attrib[qn(k)]
        pf = st.paragraph_format
        if sname in ("Normal", "Body Text", "First Paragraph"):
            pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE; pf.space_after = Pt(6); pf.first_line_indent = None
        if sname.startswith("Heading"):
            pf.space_before = Pt(12); pf.space_after = Pt(6); pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
            st.font.italic = sname == "Heading 3"
    # 제목 색: 검정
    from docx.shared import RGBColor
    for sname in ("Title", "Heading 1", "Heading 2", "Heading 3"):
        try:
            st = get_style(d, sname); st.font.color.rgb = RGBColor(0, 0, 0)
            rpr = st.element.get_or_add_rPr(); col = rpr.find(qn("w:color"))
            if col is None:
                col = rpr.makeelement(qn("w:color"), {}); rpr.append(col)
            col.set(qn("w:val"), "000000")
            for k in ("w:themeColor", "w:themeShade", "w:themeTint"):
                if col.get(qn(k)) is not None: del col.attrib[qn(k)]
        except KeyError: pass
    # 표: 열 폭을 내용 길이에 비례해 고정(총 6.5 in), 넓은 표는 8pt, 얇은 테두리
    for t in d.tables:
        ncol = len(t.columns)
        lens = []
        for ci in range(ncol):
            mx = 1
            for row in t.rows:
                try: txt = row.cells[ci].text
                except IndexError: continue
                mx = max(mx, max((len(w) for w in txt.split()), default=1) + 1, min(len(txt), 28) * 0.6)
            lens.append(mx)
        tot = sum(lens); widths = [max(0.42, 6.5 * l / tot) for l in lens]
        scale = 6.5 / sum(widths); widths = [w * scale for w in widths]
        size = 8 if ncol >= 10 else 9
        tblPr = t._tbl.tblPr
        layout = tblPr.makeelement(qn("w:tblLayout"), {qn("w:type"): "fixed"}); tblPr.append(layout)
        tblW = tblPr.find(qn("w:tblW"))
        if tblW is None:
            tblW = tblPr.makeelement(qn("w:tblW"), {}); tblPr.append(tblW)
        tblW.set(qn("w:type"), "dxa"); tblW.set(qn("w:w"), str(int(6.5 * 1440)))
        borders = tblPr.makeelement(qn("w:tblBorders"), {})
        for edge in ("top", "bottom", "insideH"):
            el = borders.makeelement(qn(f"w:{edge}"), {qn("w:val"): "single", qn("w:sz"): "4", qn("w:color"): "000000"}); borders.append(el)
        tblPr.append(borders)
        grid = t._tbl.tblGrid
        for gc, w in zip(grid.findall(qn("w:gridCol")), widths): gc.set(qn("w:w"), str(int(w * 1440)))
        for row in t.rows:
            for ci, cell in enumerate(row.cells):
                if ci < len(widths): cell.width = Inches(widths[ci])
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE; p.paragraph_format.space_after = Pt(0)
                    for r in p.runs: set_run_font(r, size=size)
    # 캡션(**Table n.** / **Figure n.** 로 시작하는 단락): 10pt 단일 간격
    for p in d.paragraphs:
        txt = p.text.strip()
        if re.match(r"^(Table|Figure) S?\d+\.", txt):
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            for r in p.runs: set_run_font(r, size=10)
        for r in p.runs:
            if r.font.name is None: set_run_font(r)
    for s in d.sections:
        s.left_margin = s.right_margin = Inches(1); s.top_margin = s.bottom_margin = Inches(1)
    d.save(path)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--figdir", default=None); ap.add_argument("--pdf", action="store_true"); a = ap.parse_args()
    figdir = a.figdir or os.path.join(os.path.dirname(os.path.abspath(a.inp)), "figures")
    md = preprocess(open(a.inp, encoding="utf-8").read(), figdir)
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
        fh.write(md); tmp = fh.name
    subprocess.run(["pandoc", tmp, "-o", a.out, "--from", "markdown+pipe_tables", "--to", "docx", "--dpi=300"], check=True)
    style_doc(a.out)
    if a.pdf:
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(os.path.abspath(a.out)), a.out],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("written", a.out)


if __name__ == "__main__":
    main()
