# -*- coding: utf-8 -*-
"""docx 定向修改工具：保持原格式的段落/单元格文本替换、段落与表格原位插入、列宽重设。"""
import copy
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from docx.table import Table

LOG = []


def log(msg):
    LOG.append(msg)
    print(msg)


# ---------------------------------------------------------------- 段落文本
def _run_text(r):
    return ''.join(t.text or '' for t in r._r.findall(qn('w:t')))


def _set_run_text(r, text):
    ts = r._r.findall(qn('w:t'))
    for t in ts[1:]:
        r._r.remove(t)
    if ts:
        ts[0].text = text
        ts[0].set(qn('xml:space'), 'preserve')
    else:
        e = OxmlElement('w:t')
        e.text = text
        e.set(qn('xml:space'), 'preserve')
        r._r.append(e)


def repl_para(p, old, new, expect=1):
    """段落内精确子串替换，尽量保持原 run 边界与字符格式。"""
    runs = list(p.runs)
    if not runs:
        ts = p._p.findall('.//' + qn('w:t'))
        joined = ''.join(t.text or '' for t in ts)
        cnt = joined.count(old)
        if cnt != expect:
            log('WARN 非run段落命中 %d(期望%d): %s' % (cnt, expect, old[:26]))
            return False
        idx = joined.find(old)
        newj = joined[:idx] + new + joined[idx + len(old):]
        for i, t in enumerate(ts):
            t.text = newj if i == 0 else ''
        return True
    texts = [_run_text(r) for r in runs]
    joined = ''.join(texts)
    cnt = joined.count(old)
    if cnt != expect:
        log('WARN 段落命中 %d(期望%d): %s | %s' % (cnt, expect, old[:26], joined[:40]))
        return False
    idx = joined.find(old)
    end = idx + len(old)
    pos = 0
    for r, tx in zip(runs, texts):
        s, e = pos, pos + len(tx)
        pos = e
        if e <= idx or s >= end:
            continue
        # 匹配起始所在 run 保留前缀并放入新文本；跨越匹配终点的 run 必须保留其尾部
        pre = tx[:idx - s] if s < idx else ''
        post = tx[end - s:] if e > end else ''
        _set_run_text(r, pre + (new if s <= idx else '') + post)
    return True


def set_para(p, text):
    runs = list(p.runs)
    if not runs:
        ts = p._p.findall('.//' + qn('w:t'))
        if ts:
            ts[0].text = text
            for t in ts[1:]:
                t.text = ''
            return True
        # 段落内没有任何 run（空单元格等）：补建一个 run，否则静默失败
        r = OxmlElement('w:r')
        e = OxmlElement('w:t')
        e.text = text
        e.set(qn('xml:space'), 'preserve')
        r.append(e)
        p._p.append(r)
        return True
    _set_run_text(runs[0], text)
    for r in runs[1:]:
        r._r.getparent().remove(r._r)
    return True


def append_para(p, text):
    runs = list(p.runs)
    if not runs:
        ts = p._p.findall('.//' + qn('w:t'))
        if ts:
            ts[-1].text = (ts[-1].text or '') + text
            return True
        return False
    nr_el = copy.deepcopy(runs[-1]._r)
    from docx.text.run import Run
    _set_run_text(Run(nr_el, p), text)
    runs[-1]._r.addnext(nr_el)
    return True


# ---------------------------------------------------------------- 单元格
def cell_replace(cell, old, new, expect=1):
    found = 0
    for p in cell.paragraphs:
        if old in p.text:
            n = p.text.count(old)
            repl_para(p, old, new, expect=n)
            found += n
    if found != expect:
        log('WARN 单元格命中 %d(期望%d): %s' % (found, expect, old[:26]))
        return False
    return True


def set_cell(cell, text):
    ps = cell.paragraphs
    for extra in ps[1:]:
        extra._p.getparent().remove(extra._p)
    set_para(ps[0], text)
    return True


# ---------------------------------------------------------------- 插入段落
def _as_el(anchor):
    return anchor._p if isinstance(anchor, Paragraph) else anchor


def clone_para(template_p, text):
    new_p = copy.deepcopy(template_p._p)
    for tag in ('w:r', 'w:hyperlink', 'w:bookmarkStart', 'w:bookmarkEnd'):
        for el in new_p.findall(qn(tag)):
            new_p.remove(el)
    src_runs = template_p._p.findall(qn('w:r'))
    if not src_runs:
        src_runs = template_p._p.findall('.//' + qn('w:r'))
    if src_runs:
        nr = copy.deepcopy(src_runs[0])
        _set_run_text(nr if hasattr(nr,'_r') else Run(nr, template_p), text)
    else:
        nr = OxmlElement('w:r')
        _set_run_text(nr, text)
    new_p.append(nr)
    return new_p


def insert_para(anchor, template_p, text, after=True):
    new_p = clone_para(template_p, text)
    el = _as_el(anchor)
    if after:
        el.addnext(new_p)
    else:
        el.addprevious(new_p)
    return Paragraph(new_p, template_p._parent)


def chain_insert(anchor, items):
    """items: [('p', template_p, text) | ('t', tbl_el)]，按顺序插入。"""
    cur = _as_el(anchor)
    out = []
    for it in items:
        if it[0] == 'p':
            new_p = clone_para(it[1], it[2])
            cur.addnext(new_p)
            cur = new_p
            out.append(Paragraph(new_p, it[1]._parent))
        else:
            cur.addnext(it[1])
            cur = it[1]
            out.append(it[1])
    return out


# ---------------------------------------------------------------- 表格
def table_rows(tbl):
    return tbl._tbl.findall(qn('w:tr'))


def insert_rows_after(tbl, row_index, rows_values):
    """在 row_index 之后插入若干行，values 中 None 表示该列（多为竖向合并列）不填。"""
    trs = table_rows(tbl)
    anchor = trs[row_index]
    for vals in reversed(rows_values):
        new_tr = copy.deepcopy(anchor)
        anchor.addnext(new_tr)
    rows = list(tbl.rows)
    for k, vals in enumerate(rows_values):
        row = rows[row_index + 1 + k]
        for ci, v in enumerate(vals):
            if v is None or ci >= len(row.cells):
                continue
            set_cell(row.cells[ci], v)
    return rows[row_index + 1: row_index + 1 + len(rows_values)]


def insert_row_after_clone(tbl, src_row_index, values):
    return insert_rows_after(tbl, src_row_index, [values])


def make_table(template_tbl, data, widths=None):
    tbl_el = copy.deepcopy(template_tbl._tbl)
    trs = tbl_el.findall(qn('w:tr'))
    need = len(data)
    while len(trs) < need:
        new_tr = copy.deepcopy(trs[-1])
        trs[-1].addnext(new_tr)
        trs = tbl_el.findall(qn('w:tr'))
    while len(trs) > need:
        tbl_el.remove(trs[-1])
        trs = tbl_el.findall(qn('w:tr'))
    tbl = Table(tbl_el, template_tbl._parent)
    for ri, vals in enumerate(data):
        for ci, v in enumerate(vals):
            if v is None or ci >= len(tbl.rows[ri].cells):
                continue
            set_cell(tbl.rows[ri].cells[ci], v)
    if widths:
        set_col_widths(tbl_el, widths)
    return tbl_el


def set_col_widths(tbl_el, fractions):
    tbl = Table(tbl_el, None)
    grid = tbl_el.find(qn('w:tblGrid'))
    cols = grid.findall(qn('w:gridCol'))
    if not cols:
        return
    total = 0
    for c in cols:
        try:
            total += int(c.get(qn('w:w')))
        except (TypeError, ValueError):
            total = 0
            break
    if total <= 0:
        total = 9000
    n = min(len(cols), len(fractions))
    for i in range(n):
        cols[i].set(qn('w:w'), str(int(total * fractions[i])))
    for row in tbl.rows:
        for i, cell in enumerate(row.cells):
            if i >= n:
                continue
            tcPr = cell._tc.get_or_add_tcPr()
            tcW = tcPr.find(qn('w:tcW'))
            if tcW is None:
                tcW = OxmlElement('w:tcW')
                tcPr.append(tcW)
            tcW.set(qn('w:w'), str(int(total * fractions[i])))
            tcW.set(qn('w:type'), 'dxa')


def mount_table(tbl_el, anchor_el, after=True):
    if after:
        anchor_el.addnext(tbl_el)
    else:
        anchor_el.addprevious(tbl_el)
