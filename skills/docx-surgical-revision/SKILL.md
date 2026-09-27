---
name: docx-surgical-revision
description: 对既有的 .docx 长文档（规划、报告、方案、讲话稿）做"保持原格式"的定向修订，并按锚点定位、逐段 diff 验收。当用户要求"按某份评审/审阅意见修改 Word 文档""改稿并另存新文档""在既有 Word 里补齐表格行/新增附注/更正口径/统一数字"时触发。核心是文本锚点定位＋克隆既有元素继承格式＋difflib 逐段验收，避免正文静默丢失。
agent_created: true
---

# docx 定向修订（保持格式、可验收）

## 适用场景

- 已有一份排版完成的 .docx（几十万字、几十张表），要依据一份评审意见 / 会议意见 / 口径更正清单做**局部修订**，并另存为新文档。
- 要求：不重建文档、不改动原有排版与样式，新增内容与原文风格一致。

不适用：从零生成文档（用 tencent-docx 那套 HTML→DOCX 流程）。

## 附：设置大纲级别（不改版式）

用户常要求"给文档设一级/二级标题大纲级别"（用于导航窗格与自动目录）。**不要套用 Heading 1/2 内置样式**——
那会把字体、颜色、字号全改掉。正确做法是只写 `w:outlineLvl` 直接格式（0=1级、1=2级…），版式一字不动：

```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_outline(p, lvl):            # lvl 从 1 起
    pPr = p._p.get_or_add_pPr()
    for e in pPr.findall(qn('w:outlineLvl')):
        pPr.remove(e)               # 幂等：先删旧的
    el = OxmlElement('w:outlineLvl'); el.set(qn('w:val'), str(lvl - 1))
    # 关键：pPr 子元素有严格顺序，outlineLvl 必须在 rPr / sectPr / pPrChange 之前，
    # 直接 append 到末尾会排到 rPr 之后 → 顺序非法，Word 可能忽略或报错
    for tag in ('w:rPr', 'w:sectPr', 'w:pPrChange'):
        f = pPr.find(qn(tag))
        if f is not None:
            f.addprevious(el); return
    pPr.append(el)
```

识别标题用正则 + 长度护栏，避免把**目录行**当成标题：
- 一级：`^[一二三四五六七八九十]{1,3}、` 且 `len(text) <= 40`（不加长度护栏会把
  "一、编制背景…；二、现状诊断；…；附：主要数据来源。" 这种单行目录整段设成 1 级）
- 二级：`^（[一二三四五六七八九十]{1,3}）` 且 `len(text) <= 40`
- **附录内的"一、二、三…"是小节而非章**：遍历时记一个 `in_after_appendix` 开关，
  遇到 `^附[:：　]` 之后，把 `^[一二三四五六七八九十]+、` 一律降到 2 级。

验收：① 前后段落文本列表必须**完全相等**（`ta == tb` 为 True）；② 读回每个 `w:outlineLvl` 统计
1/2 级数量并打印大纲树；③ 抽查 pPr 子元素顺序；④ `zipfile.testzip()`。

## 变体：以另一份同类稿为参照校订本稿（回填 + 校对）

出现场景：同一主题存在两份稿子（如"建议稿"与"修订稿·依审议意见修订"），要求"参考 B 稿和公开数据，
对 A 稿进行检查修订"。B 稿里往往已经沉淀了几十上百条已核实的事实与口径，可当权威参照物——
**但 B 稿不是 ground truth**，必须逐条复核，本次实测就发现 B 稿有两处比 A 稿更错（微专业现状数、
省级课程思政示范课门数）。流程：

1. 两份 docx 各自按 body 顺序导出全文（表格展开成 `[[TABLE n]]` 块），逐段通读，标出结构差异。
2. **先做内部勾稽自动核查**：写脚本把所有"占比／比值／上下限合计／人数勾稽"用算式复算一遍
   （80+ 项一次跑完，比肉眼快且不会漏），得到"内部自洽"还是"内部矛盾"的结论。
3. **再联网逐条核验外部数据**，每条归入四类之一：①已证实（保留并补来源与检索日期）；
   ②与 B 稿冲突（查原始出处后择一，必要时并列两口径）；③无出处（删除或改定性表述）；
   ④**主体归属有误**（最高价值的一类，如把某学院/某校区的成果误挂到另一主体，最难自查出来）。
4. 落盘顺序固定为：**段落子串替换 → 段末追加 → 单元格设值 → 结构插入**（新增段／新增来源条目／
   新增校订记录表）。先做无结构变化的编辑，再做插入，可避免锚点漂移。
   **删段必须用"段首前缀 + startswith"精确匹配，且替换一律先于删除**：本次实测用
   `if anchor in p.text` 删"附　本轮校订记录"标题，结果把**内容提要段**也删了——因为该段末尾
   被追加过一句"……明细见文末"附　本轮校订记录"。"。凡是"文末标题"类的锚点，正文里几乎总被
   引用过，`in` 匹配必然误伤。
4.5 **判定"内部矛盾"前必须先在同稿内 grep 定位**（本技能最贵的一次教训）：同时处理两份同类稿时，
   极易把 B 稿某章的句子记成 A 稿的内容，据此判出"内部自相矛盾"并去改 A 稿——实测发生过一次，
   误改已落盘、事后才靠"该短语在本稿命中 0 段"发现。做法：写核查清单时，**每条"矛盾"都先跑
   `sum(1 for p in d.paragraphs if key in p.text)` 并打印命中段号**；命中 0 或只命中 1 处而不能
   与另一处并列的，一律不得判为内部矛盾（只能标为"与另一稿的口径冲突"，并写在校订记录里交决策人）。
   同理，改完要**回头看被改段的全文**，确认没有把自己臆造的"补充事实"塞进去。

5. 修订记录表（在 B 稿体系里通常叫"事实校订记录"）要一并产出，四列：
   `序号 | 原表述（问题） | 处理方式 | 现行表述与依据`，并在文首"修订说明"里同步修订计数。
6. 两稿之间**无法调和的系统性分歧**（如师资总量路径、生师比分母口径），不要擅自动目标体系，
   在文末校订记录里如实并列两种口径 + 给出取舍建议，交决策人判断——擅自改掉目标值反而会
   让不同章节口径互相矛盾。
7. 用户事后常会要求"删掉修订记录和修订说明，回到干净稿"。所以：**修订痕迹要能一键剥离**——
   新增内容集中成整段／整条（如来源清单新增条目），"本轮修订新增引用。"这类尾注统一措辞，
   剥离时只需 3~5 条 `find_and_replace` + 删除 3 个段落（说明段、标题段、记录表）。
   注意"引用了修订说明那句话"的段落（通常是内容提要）要先替换再删段。



## 环境（本机）

- 读改 docx 用带 python-docx 的解释器：
  `C:/Users/foofi/.workbuddy/binaries/python/envs/html-to-docx/Scripts/python.exe`
  （托管版 python 3.13.12 **没有** docx 模块）
- Bash 每条命令开头必须加：`export PATH="/usr/bin:/bin:/mingw64/bin:$PATH"`
- 脚本一律 Write 成 .py 再执行，**不要用 heredoc**（本机 shell 包装下会解析异常）。

## ⚠️ 走 editor_sdk 通道会丢内容（实测，2026-09）

宿主若提示"本地 docx 请改用 `tencent-docs-routing` → `tencent-local-office-edit`"，可以先用它试，
但**必须做落盘前后的段落级 diff 验收**。实测（414 段的稿子）：

- `present_files` 注册的 UUID 实例，`doc_find` 报 `document is not open`；需
  `open_file file_path=... open_with_existing=true` 才真正加载（返回的 file_id 是路径字符串本身）。
- **加载→save_file 一轮之后，某段的开头 15 字与另一整段文本凭空消失**（该文本在 python-docx
  打开的原文件中确实存在，`zipfile.testzip()` 也正常）。`doc_find` 对丢失文本返回 0 命中，
  不会报错，极易静默通过。
- 结论：**能用 python-docx 就用 python-docx**；editor_sdk 只适合结构性弱的小改（改一两个单元格）。
  走 editor_sdk 后务必：① 改前把文件另存一份基准；② 改后用 python-docx 重新读取，与本 skill
  第 5 步的 difflib 做块级比对；③ 改完 `close_file` 掉自己开的实例，避免宿主预览的旧内存
  再次覆盖。一旦发现丢失，直接从"原稿 + 修订脚本"重建（见下"变体"节第 4 步的分段保存设计，
  重建成本很低）。


## 五步流程

### 1. 导出全文与结构，建立定位基准

按 `document.element.body` 顺序展开段落与表格（表格用 `[[TABLE n]]` 占位），输出 `_fulltext.txt`；
另导出每个目标表的逐格内容到 `_tabledump.txt`。
**先读全文**，把改点逐条落到"某段原文片段 / 某表的某行某列"，再动手。

### 2. 用文本锚点写修订脚本，按篇分段串行

每段脚本只处理一个区块（篇首→综述章→实施章→附录），段末 `d.save()`。
这样单段失败不会污染已完成部分，且能重跑。

锚点定位函数（**不要用段落序号**，序号会因插入而漂移）：

```python
def fp(sub, occurrence=1):          # 按内容找段落
    n = 0
    for p in d.paragraphs:
        if sub in p.text:
            n += 1
            if n == occurrence:
                return p
    log('WARN 未定位段落: %s' % sub[:34])   # 必须告警，不静默跳过

def ft(marker, n=1, ncols=None):    # 按内容找表格；ncols 用于排除同名的题注/说明
    k = 0
    for t in d.tables:
        if ncols is not None and len(t.columns) != ncols:
            continue
        if any(marker in c.text for row in t.rows for c in row.cells):
            k += 1
            if k == n:
                return t
    log('WARN 未定位表: %s' % marker)
```

单元格行定位：**先确认序号列在第几列**。风险表、指标表等首列常是"序号"，风险名/指标名在第 2 列，
`find_row(tbl, '某风险', 1)` 才对；用 0 会"找不到行"并抛 AttributeError。

### 3. 新增内容一律克隆既有同类元素（格式自动继承）

- 新增段：`insert_para(锚点段, 模板段, 文本)` / `chain_insert(锚点, [('p',模板段,文本), ('t',表元素)])`
  —— 模板段取同层级、同体例的既有段落（如"表 N 附注"题注、说明段）。
- 新增表：`make_table(以既有表为模板克隆, data, widths=[...])` ＋ `chain_insert`。
- 新增行：`insert_rows_after(表, 行号, [行值, ...])`，克隆首行/末行。
- 单元格设值：`set_cell(cell, text)`（会删掉多余段落）；单元内局部替换：`cell_replace`。

**表内插行的体例修正（易漏）**：多数中文表格的"类别/维度"列只在**组首行**标注，组内其他行为空。
插行后：插入的行首列须留空；若插行把原组打断，须在被打断组的下一行**重新标注组名**。
另：组标签单元格通常为**粗体**，补写时要连 `w:rPr` 一起从同类单元格复制。

### 4. 关键：三个工具函数的坑（务必用下列实现）

```python
# ① 跨 run 替换：必须保留"匹配终点所在 run 的尾部"，否则静默丢正文
def repl_para(p, old, new, expect=1):
    runs = list(p.runs)
    texts = [_run_text(r) for r in runs]
    joined = ''.join(texts)
    if joined.count(old) != expect:
        log('WARN 段落命中 %d(期望%d): %s' % (joined.count(old), expect, old[:26]))
        return False
    idx = joined.find(old)
    end = idx + len(old)
    pos = 0
    for r, tx in zip(runs, texts):
        s, e = pos, pos + len(tx)
        pos = e
        if e <= idx or s >= end:
            continue
        pre = tx[:idx - s] if s < idx else ''
        post = tx[end - s:] if e > end else ''      # ← 这一行是纠错关键
        _set_run_text(r, pre + (new if s <= idx else '') + post)
    return True

# ② 整段替换：空单元格（无任何 run）必须补建 run，否则静默返回 False
def set_para(p, text):
    runs = list(p.runs)
    if not runs:
        ts = p._p.findall('.//' + qn('w:t'))
        if ts:
            ts[0].text = text
            for t in ts[1:]:
                t.text = ''
            return True
        r = OxmlElement('w:r'); e = OxmlElement('w:t')
        e.text = text; e.set(qn('xml:space'), 'preserve')
        r.append(e); p._p.append(r)
        return True
    _set_run_text(runs[0], text)
    for r in runs[1:]:
        r._r.getparent().remove(r._r)
    return True

# ③ 追加文本到段末：克隆末 run 的元素后 addnext（不要用 run.text +=，会丢格式或失效）
```

同目录 `scripts/docxlib.py` 是完整可用的工具库（含 `make_table` / `chain_insert` /
`insert_rows_after` / `set_col_widths`）。

### 4.5 三个必踩的导入/API 坑（python-docx 1.2.0）

```python
# ① Cell 不再从 docx.table 导出，直接 import 会 ImportError
from docx.table import Table, _Cell as Cell   # ← 正确写法

# ② 全量单元格改写 vs 单元格内片段替换是两个函数，别混用
#    全量改写（覆盖整格文字）：定位到 Cell → set_cell(cell, text)
#    片段替换（格内改几个字）：定位到 Cell → cell_replace(cell, old, new, expect=1)
#    常见错误：把 Table 直接传给 cell_replace → AttributeError: 'Table' object
#    has no attribute 'paragraphs'。定位助手必须返回具体 Cell，不是 Table。
def ftab(marker, ncol, row_kw, col=0):
    for t in d.tables:
        if len(t.columns) != ncol:
            continue
        for r in t.rows:
            if row_kw in r.cells[col].text:      # 先命中行
                return t, r                        # 返回 (表, 行)，再取 r.cells[c]
    log('WARN 未定位表行: %s' % row_kw)

# ③ 批量改号（如"表18→表9"）在合并单元格处会漏网
#    paragraph.runs / cell.paragraphs 只能取到可见的首现；被合并/复制的格子取不到。
#    → 必须再做一遍 XML 文本节点直改，并复核残留计数为 0。
for tnode in d.element.body.iter(qn('w:t')):
    if tnode.text and '表18' in tnode.text:
        tnode.text = tnode.text.replace('表18', '表9')
```

### 4.6 锚点必须唯一（否则会改错段）

`setp('定位对标说明', ...)` 这类短锚点极易**命中另一个含同串的段落**（本轮就误覆盖了"总体定位"段）。
处置：锚点取到**足以区分的最长唯一前缀**（`'定位对标说明（关于'`），改完立刻回读该段与相邻段确认。
同理 `ft(marker)` 要带 `ncols` 或行内容二次过滤，避免命中同名题注/说明段。

### 5. 验收三件套（缺一不可）

1. **段落级 difflib 比对**（最重要）：把原稿与修订稿的段落文本列表做 `SequenceMatcher`，
   对每对配再逐字符 diff，**打印所有 ≥4 字的被删片段**。逐条确认"每一处删除都是有意替换"。
   —— 只跑关键词断言是查不出文本静默丢失的（本技能的形成就源于一次 3 处正文被吞）。
   **两个坑**：① 比对列表若把表格展开成多行（每行一个 `[表] ...`），**block 索引 ≠ 段落索引**，
   定位删除片段时按内容判断，不要按索引回查 `d.paragraphs`；② 段末追加（`append_para`）型修订
   只会产生"删除"片段而不会产生"新增"片段（新文本在另一块里），出现少量删除片段属正常。
2. **关键词／算式断言**：把每个改点写成 PASS/FAIL 清单（含勾稽算式，如 `2300÷130＝17.7`）。
   比对前先把文本中的空格去掉归一化，否则表格里的"2026 年 8 月 31 日"这种加空写法会漏判。
   **反面断言的陷阱**：若本次修订在文末新增了"校订记录表"，表内会**引用**被替换掉的旧表述，
   此时"旧表述已消除"类断言必然 FAIL。处置：反面断言只在**正文段落**（`d.paragraphs`）里检索，
   不要用把表格行也拼进来的全文串；同时应正面断言新表存在（行数、表头）。
3. **表格结构核对**：逐表打印行数×列数、前几行与关键行，确认新行落位、组标签体例、列宽。
   新增表时核对文末 `body` 子元素顺序（`p → p → tbl → sectPr`），确保表在 `sectPr` 之前。
4. 另外校验 `zipfile.ZipFile(path).testzip() is True`，并统计段落/表格数变化
   （预期增量可先算好：如 4 个新增段＋标题 1＋来源 N 条＋说明 1 = 段落增量）。


## 常见陷阱速查

| 现象 | 原因 | 处置 |
|---|---|---|
| 正文片段凭空消失 | `repl_para` 未保留终点 run 的尾部 | 用第 4 步①的写法；并用 difflib 验收 |
| 单元格设值无效、无报错 | 该单元格无任何 run | 用第 4 步②的写法 |
| 表里"找不到行" | 序号在第 0 列，名称在第 1 列 | `find_row(tbl, name, 1)` |
| 补写的标签不带粗体 | 新 run 无 rPr | 从同类单元格复制 `w:rPr` 后 `insert(0, ...)` |
| 表格宽度异常 | 克隆模板表列数不同 | `set_col_widths(tbl_el, fractions)` 按比例重设 |
| 关键词断言"通过"但仍丢字 | 断言只看存在性 | 必须做段落级 diff |
| `ImportError: cannot import name 'Cell'` | python-docx 1.2.0 不导出 `Cell` | `from docx.table import Table, _Cell as Cell` |
| `'Table' object has no attribute 'paragraphs'` | 把 Table 传给了 `cell_replace` | 定位助手返回具体 `Cell`，不是 `Table` |
| 批量改号后仍能搜到旧表号 | 合并/复制单元格未被 `cell.paragraphs` 覆盖 | XML 层 `w:t` 节点直改 ＋ 残留计数复核为 0 |
| 改完发现改错了段 | 锚点串在两段都出现（非唯一） | 锚点取最长唯一前缀，改后回读比邻段 |
| 修订史里的旧数字被误"改正" | 附录修订记录会引用旧口径 | 保留历史引述，只改正文现行口径，并加"该计数已更新为…"互见 |

## 收尾

- 修订记录要写进文档自身（如"附录 D 校订记录"增列本轮条目、"附录 F 意见采纳对照表"），
  并在内容提要与编制说明处同步更新计数（否则不同章节的处数/项数会互相矛盾）。
- 交付：`present_files` 给出新文档；过程文件留在 `<项目>/审议过程文件/` 便于复核与重跑。
