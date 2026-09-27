# -*- coding: utf-8 -*-
"""按公文格式（参照 GB/T 9704 体例）对既有 .docx 全文重新排版。

用法：
    python gongwen_format.py <文档.docx> [--h1-report]

设计要点（务必先读 SKILL.md）：
  * 不按样式名套版式，按**角色**判定：cover / toc_title / toc_entry / h1 / h2 / h3 /
    exec / caption / tablenote / listnum / body
  * 目录区由「目录段 → 其后第一个 Heading 段落」界定（否则目录里的"附录A"条目会被误判为一级标题）
  * run 遍历必须用 allruns(p)，把 w:hyperlink 内部的 run 也覆盖到
  * 手写 OOXML 时按 ECMA-376 顺序插入（见 *_ORDER），收尾再跑一遍 normalize_ooxml.py
  * 表头判定＝「首行且首格非纯数字」（附录类表格首行常是数据行）
"""
import sys
import os
import re
import argparse
from collections import Counter

import docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.text.run import Run

# ------------------------------------------------------------------ 版式常量
FONT_SONG = '宋体'
FONT_HEI = '黑体'
FONT_LAT = 'Times New Roman'
BLACK = '000000'

SZ_H1, SZ_H2, SZ_H3, SZ_BODY, SZ_TBL, SZ_CAP = 16, 14, 12, 12, 10.5, 10.5
LINE = 1.5

# ------------------------------------------------------------------ 顺序表
RPR_ORDER = ['w:rStyle', 'w:rFonts', 'w:b', 'w:bCs', 'w:i', 'w:iCs', 'w:caps', 'w:smallCaps',
             'w:strike', 'w:dstrike', 'w:outline', 'w:shadow', 'w:emboss', 'w:imprint',
             'w:noProof', 'w:snapToGrid', 'w:vanish', 'w:webHidden', 'w:color', 'w:spacing',
             'w:w', 'w:kern', 'w:position', 'w:sz', 'w:szCs', 'w:highlight', 'w:u', 'w:effect',
             'w:bdr', 'w:shd', 'w:fitText', 'w:vertAlign', 'w:rtl', 'w:cs', 'w:em', 'w:lang',
             'w:eastAsianLayout', 'w:specVanish', 'w:oMath']
PPR_ORDER = ['w:pStyle', 'w:keepNext', 'w:keepLines', 'w:pageBreakBefore', 'w:framePr',
             'w:widowControl', 'w:numPr', 'w:suppressLineNumbers', 'w:pBdr', 'w:shd', 'w:tabs',
             'w:suppressAutoHyphens', 'w:kinsoku', 'w:wordWrap', 'w:overflowPunct',
             'w:topLinePunct', 'w:autoSpaceDE', 'w:autoSpaceDN', 'w:bidi', 'w:adjustRightInd',
             'w:snapToGrid', 'w:spacing', 'w:ind', 'w:contextualSpacing', 'w:mirrorIndents',
             'w:suppressOverlap', 'w:jc', 'w:textDirection', 'w:textAlignment',
             'w:textboxTightWrap', 'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr',
             'w:pPrChange']
TRPR_ORDER = ['w:cnfStyle', 'w:divId', 'w:gridBefore', 'w:gridAfter', 'w:wBefore', 'w:wAfter',
              'w:cantSplit', 'w:trHeight', 'w:tblHeader', 'w:tblCellSpacing', 'w:jc', 'w:hidden']


def _ins(parent, tag, order):
    """按 schema 顺序取或插入子元素。已存在则原样返回（位置由 normalize_ooxml.py 收尾重排）。"""
    el = parent.find(qn(tag))
    if el is not None:
        return el
    el = OxmlElement(tag)
    idx = order.index(tag)
    for ch in parent:
        nm = next((t for t in order if qn(t) == ch.tag), None)
        if nm is None:
            continue
        if order.index(nm) > idx:
            ch.addprevious(el)
            return el
    parent.append(el)
    return el


def allruns(p):
    """段落内全部 run，含 w:hyperlink 内部的 run（目录条目即为此类，p.runs 取不到）。"""
    rs = list(p.runs)
    for hl in p._p.findall(qn('w:hyperlink')):
        for r in hl.findall(qn('w:r')):
            rs.append(Run(r, p))
    return rs


def set_run(r, ea=None, lat=None, size=None, bold=None, color=None):
    rPr = r._r.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr')
        r._r.insert(0, rPr)
    if ea or lat:
        rf = _ins(rPr, 'w:rFonts', RPR_ORDER)
        if ea:
            rf.set(qn('w:eastAsia'), ea)
        if lat:
            rf.set(qn('w:ascii'), lat)
            rf.set(qn('w:hAnsi'), lat)
            rf.set(qn('w:cs'), lat)
    if bold is not None:
        if bold:
            _ins(rPr, 'w:b', RPR_ORDER).set(qn('w:val'), '1')
            _ins(rPr, 'w:bCs', RPR_ORDER).set(qn('w:val'), '1')
        else:
            for t in ('w:b', 'w:bCs'):
                e = rPr.find(qn(t))
                if e is not None:
                    rPr.remove(e)
    if color is not None:
        _ins(rPr, 'w:color', RPR_ORDER).set(qn('w:val'), color)
    if size is not None:
        for t in ('w:sz', 'w:szCs'):
            _ins(rPr, t, RPR_ORDER).set(qn('w:val'), str(int(round(size * 2))))


def set_mark(p, ea, lat, size):
    """段落标记字体（决定空段落行高与 Normal 兜底）。"""
    pPr = p._p.get_or_add_pPr()
    rPr = _ins(pPr, 'w:rPr', PPR_ORDER)
    rf = _ins(rPr, 'w:rFonts', RPR_ORDER)
    rf.set(qn('w:eastAsia'), ea)
    rf.set(qn('w:ascii'), lat)
    rf.set(qn('w:hAnsi'), lat)
    for t in ('w:sz', 'w:szCs'):
        _ins(rPr, t, RPR_ORDER).set(qn('w:val'), str(int(round(size * 2))))


def sp(p, first_pt=None, left_pt=None, line=None, align=None, before=None, after=None,
       page_break=None, keep_next=None):
    """段落格式。first_pt/left_pt 为磅；line 传 'single' 或浮点倍数。"""
    pPr = p._p.get_or_add_pPr()
    if page_break is not None:
        if page_break:
            _ins(pPr, 'w:pageBreakBefore', PPR_ORDER).set(qn('w:val'), '1')
        else:
            e = pPr.find(qn('w:pageBreakBefore'))
            if e is not None:
                pPr.remove(e)
    if keep_next is not None:
        if keep_next:
            _ins(pPr, 'w:keepNext', PPR_ORDER)
        else:
            e = pPr.find(qn('w:keepNext'))
            if e is not None:
                pPr.remove(e)
    if line is not None or before is not None or after is not None:
        e = _ins(pPr, 'w:spacing', PPR_ORDER)
        if line == 'single':
            e.set(qn('w:line'), '240')
            e.set(qn('w:lineRule'), 'auto')
        elif line is not None:
            e.set(qn('w:line'), str(int(round(line * 240))))
            e.set(qn('w:lineRule'), 'auto')
        if before is not None:
            e.set(qn('w:before'), str(int(round(before * 20))))
            e.set(qn('w:beforeLines'), '0')
        if after is not None:
            e.set(qn('w:after'), str(int(round(after * 20))))
            e.set(qn('w:afterLines'), '0')
    if first_pt is not None or left_pt is not None:
        e = _ins(pPr, 'w:ind', PPR_ORDER)
        for bad in ('w:hanging', 'w:hangingChars'):
            e.attrib.pop(qn(bad), None)
        if first_pt is not None:
            e.set(qn('w:firstLine'), str(int(round(first_pt * 20))))
            e.set(qn('w:firstLineChars'), '0' if first_pt == 0 else '200')
        if left_pt is not None:
            e.set(qn('w:left'), str(int(round(left_pt * 20))))
            e.set(qn('w:leftChars'), '0' if left_pt == 0 else '200')
    if align is not None:
        _ins(pPr, 'w:jc', PPR_ORDER).set(qn('w:val'), align)


# ------------------------------------------------------------------ 角色判定
def classify(doc, cover_n=11, toc_word='目录'):
    paras = list(doc.paragraphs)
    seq = []
    for ch in doc.element.body.iterchildren():
        if ch.tag == qn('w:p'):
            seq.append(('p', ch))
        elif ch.tag == qn('w:tbl'):
            seq.append(('t', ch))
    # 表前导语（跳过空段后紧邻表格的那一段）
    pre_el = set()
    for i, (k, el) in enumerate(seq):
        if k == 't':
            j = i - 1
            while j >= 0:
                if seq[j][0] == 'p':
                    if Paragraph(seq[j][1], doc).text.strip():
                        pre_el.add(id(seq[j][1]))
                    break
                j -= 1
    pre_i = set(i for i, p in enumerate(paras) if id(p._p) in pre_el)

    toc_i = next((i for i, p in enumerate(paras) if p.text.strip() == toc_word), None)
    toc_end = None
    if toc_i is not None:
        for j in range(toc_i + 1, len(paras)):
            if paras[j].style.name.startswith('Heading'):
                toc_end = j
                break
    if toc_end is None:
        toc_end = toc_i + 1 if toc_i is not None else None

    def is_h1(p):
        t = p.text.strip()
        if p.style.name == 'Heading 2':
            return True
        if re.match(r'^附录[A-Z]', t):
            return True
        if p.style.name == 'Heading 3' and t in ('编制说明',):
            return True
        return False

    roles = {}
    for i, p in enumerate(paras):
        t = p.text.strip()
        st = p.style.name
        if i < cover_n:
            r = 'cover'
        elif toc_i is not None and i == toc_i:
            r = 'toc_title'
        elif toc_i is not None and toc_end is not None and toc_i < i < toc_end:
            r = 'toc_entry'
        elif is_h1(p):
            r = 'h1'
        elif st == 'Heading 3' and t.startswith('（'):
            r = 'h2'
        elif re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', t):          # 如 Executive Summary
            r = 'exec'
        elif re.match(r'^表\s*[0-9A-Fa-f]', t):
            r = 'tablenote' if re.match(r'^表\s*[0-9A-Fa-f]+[-－]?[0-9]*\s*注[（(：:]', t) else 'caption'
        elif t.startswith('说明：') or t.startswith('注：'):
            r = 'tablenote'
        elif i in pre_i and re.match(r'^第[一二三四五六七八九十]+轮', t):
            r = 'h3'
        elif i in pre_i and re.match(r'^[0-9]+[.．、]', t):
            r = 'h3'
        elif st == 'List Number':
            r = 'listnum'
        else:
            r = 'body'
        roles[i] = r
        if r != 'h1':                     # 清除非一级标题上的残留分页
            pPr = p._p.find(qn('w:pPr'))
            if pPr is not None:
                pe = pPr.find(qn('w:pageBreakBefore'))
                if pe is not None:
                    pPr.remove(pe)
    return paras, roles


def apply_paragraphs(doc):
    paras, roles = classify(doc)
    for i, p in enumerate(paras):
        r = roles[i]
        empty = not p.text.strip()
        line = 'single' if empty else LINE
        if r == 'cover':
            size = 26 if i == 1 else (22 if i == 2 else (18 if i == 0 else (16 if i == 4 else (22 if i == 3 else 12))))
            fam = FONT_HEI if size >= 16 else FONT_SONG
            sp(p, 0, 0, line, 'center', 0, 0)
            set_mark(p, fam, FONT_LAT, size)
        elif r == 'toc_title':
            sp(p, 0, 0, LINE, 'center', 0, 12)
            set_mark(p, FONT_HEI, FONT_LAT, 22)
            size, fam = 22, FONT_HEI
        elif r == 'toc_entry':
            sp(p, 0, 0, LINE, 'left', 0, 0)
            set_mark(p, FONT_SONG, FONT_LAT, 12)
            size, fam = 12, FONT_SONG
        elif r == 'h1':
            sp(p, SZ_H1 * 2, 0, LINE, 'left', 12, 6, True, True)
            set_mark(p, FONT_HEI, FONT_LAT, SZ_H1)
            size, fam = SZ_H1, FONT_HEI
            for run in allruns(p):
                set_run(run, ea=fam, lat=FONT_LAT, size=size, bold=False, color=BLACK)
            continue
        elif r == 'h2':
            sp(p, SZ_H2 * 2, 0, LINE, 'left', 6, 3, False, True)
            set_mark(p, FONT_HEI, FONT_LAT, SZ_H2)
            size, fam = SZ_H2, FONT_HEI
        elif r == 'h3':
            sp(p, SZ_H3 * 2, 0, LINE, 'left', 3, 3, False, True)
            set_mark(p, FONT_HEI, FONT_LAT, SZ_H3)
            size, fam = SZ_H3, FONT_HEI
        elif r == 'exec':
            sp(p, 0, 0, LINE, 'center', 6, 6)
            set_mark(p, FONT_HEI, FONT_LAT, 12)
            size, fam = 12, FONT_HEI
        elif r == 'caption':
            sp(p, 0, 0, 'single', 'center', 6, 3, None, True)
            set_mark(p, FONT_HEI, FONT_LAT, SZ_CAP)
            size, fam = SZ_CAP, FONT_HEI
        elif r == 'tablenote':
            sp(p, 0, 0, 'single', 'both', 3, 6)
            set_mark(p, FONT_SONG, FONT_LAT, SZ_CAP)
            size, fam = SZ_CAP, FONT_SONG
        elif r == 'listnum':
            sp(p, 0, 24, LINE, 'both', 0, 0)
            set_mark(p, FONT_SONG, FONT_LAT, 12)
            size, fam = 12, FONT_SONG
        else:                              # body
            if p.style.name in ('List Bullet', 'List Number'):
                try:
                    p.style = doc.styles['Normal']
                except Exception:
                    pass
                pPr = p._p.find(qn('w:pPr'))
                if pPr is not None and pPr.find(qn('w:numPr')) is not None:
                    pPr.remove(pPr.find(qn('w:numPr')))
            sp(p, 0 if empty else SZ_BODY * 2, 0, line, 'both', 0, 0, False)
            set_mark(p, FONT_SONG, FONT_LAT, 12)
            size, fam = SZ_BODY, FONT_SONG
        for run in allruns(p):
            set_run(run, ea=fam, lat=FONT_LAT, size=size, color=BLACK)
    return Counter(roles.values())


def apply_tables(doc):
    n_head = 0
    for t in doc.tables:
        one_col = len(t.columns) == 1
        for ri, row in enumerate(t.rows):
            header = False
            if ri == 0 and not one_col:
                header = not re.match(r'^[0-9０-９]+$', row.cells[0].text.strip())
            if header:
                n_head += 1
                trPr = row._tr.get_or_add_trPr()
                _ins(trPr, 'w:tblHeader', TRPR_ORDER).set(qn('w:val'), '1')
            for c in row.cells:
                c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                for p in c.paragraphs:
                    if one_col:
                        set_mark(p, FONT_SONG, FONT_LAT, SZ_TBL)
                        for run in allruns(p):
                            set_run(run, ea=FONT_SONG, lat=FONT_LAT, color=BLACK)
                    else:
                        sp(p, 0, 0, 'single', 'center' if header else 'both', 0, 0)
                        set_mark(p, FONT_SONG, FONT_LAT, SZ_TBL)
                        for run in allruns(p):
                            set_run(run, ea=FONT_SONG, lat=FONT_LAT, size=SZ_TBL,
                                    bold=True if header else None, color=BLACK)
    return n_head


def apply_styles(doc):
    st = doc.styles['Normal']
    st.font.name = FONT_LAT
    st.font.size = Pt(12)
    rpr = st.element.get_or_add_rPr()
    rf = _ins(rpr, 'w:rFonts', RPR_ORDER)
    for k, v in (('w:ascii', FONT_LAT), ('w:hAnsi', FONT_LAT),
                 ('w:eastAsia', FONT_SONG), ('w:cs', FONT_LAT)):
        rf.set(qn(k), v)
    stp = st.element.get_or_add_pPr()
    e = _ins(stp, 'w:spacing', PPR_ORDER)
    e.set(qn('w:line'), '360')
    e.set(qn('w:lineRule'), 'auto')
    _ins(stp, 'w:jc', PPR_ORDER).set(qn('w:val'), 'both')
    dd = doc.styles.element.find(qn('w:docDefaults'))
    if dd is not None:
        rpd = dd.find(qn('w:rPrDefault'))
        if rpd is not None:
            rprd = rpd.find(qn('w:rPr'))
            if rprd is None:
                rprd = OxmlElement('w:rPr')
                rpd.append(rprd)
            rf2 = _ins(rprd, 'w:rFonts', RPR_ORDER)
            rf2.set(qn('w:ascii'), FONT_LAT)
            rf2.set(qn('w:hAnsi'), FONT_LAT)
            rf2.set(qn('w:eastAsia'), FONT_SONG)
            rf2.set(qn('w:cs'), FONT_LAT)
            for tg in ('w:sz', 'w:szCs'):
                _ins(rprd, tg, RPR_ORDER).set(qn('w:val'), '24')


def apply_sections(doc, marg=(3.7, 3.5, 2.8, 2.6)):
    for si, s in enumerate(doc.sections):
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.top_margin, s.bottom_margin = Cm(marg[0]), Cm(marg[1])
        s.left_margin, s.right_margin = Cm(marg[2]), Cm(marg[3])
        s.header_distance, s.footer_distance = Cm(2.0), Cm(2.5)
        if si < len(doc.sections) - 1:
            sectPr = s._sectPr
            tp = sectPr.find(qn('w:type'))
            if tp is None:
                tp = OxmlElement('w:type')
                sectPr.insert(0, tp)
            tp.set(qn('w:val'), 'nextPage')
    # 末节页脚居中页码（首节＝封面，不编号）
    f = doc.sections[-1].footer
    f.is_linked_to_previous = False
    for p in list(f.paragraphs):
        p._p.getparent().remove(p._p)
    fp = f.add_paragraph()
    sp(fp, 0, 0, 'single', 'center', 0, 0)
    set_mark(fp, FONT_SONG, FONT_LAT, 12)
    run = fp.add_run()
    for kind, txt in (('begin', None), ('instr', ' PAGE '), ('separate', None),
                      ('text', '1'), ('end', None)):
        if kind == 'instr':
            e = OxmlElement('w:instrText')
            e.set(qn('xml:space'), 'preserve')
            e.text = txt
        elif kind == 'text':
            e = OxmlElement('w:t')
            e.text = txt
        else:
            e = OxmlElement('w:fldChar')
            e.set(qn('w:fldCharType'), kind)
        run._r.append(e)
    set_run(run, ea=FONT_SONG, lat=FONT_LAT, size=12, color=BLACK)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('docx_path')
    ap.add_argument('--cover-n', type=int, default=11, help='封面段落数（默认 11）')
    args = ap.parse_args()
    doc = docx.Document(args.docx_path)
    print('段落 %d 表 %d' % (len(doc.paragraphs), len(doc.tables)))
    cnt = apply_paragraphs(doc)
    print('角色分布:', dict(cnt))
    print('表头行 %d 张' % apply_tables(doc))
    apply_styles(doc)
    apply_sections(doc)
    doc.save(args.docx_path)
    print('已保存:', args.docx_path)
    print('提示：接着跑 normalize_ooxml.py 收尾（子元素顺序重排＋补 eastAsia）。')


if __name__ == '__main__':
    main()
