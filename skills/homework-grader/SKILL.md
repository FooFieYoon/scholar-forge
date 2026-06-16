---
name: homework-grader
description: >
  Generic multi-step homework grading system for university courses. Supports batch document extraction (.doc/.docx/.pdf), source code analysis (.py/.ipynb), rubric-based scoring with normal distribution curves, and Excel report generation. Scoring criteria and deduction rules are dynamically derived from course-specific grading materials uploaded by the user (考核方案, 附件, 评分量化表). Triggers on requests like "批改作业", "grade homework", "评分", or when user provides student submissions directory with grading rubric documents.
agent_created: true
---

# Homework Grader — Generic Course Grading

This skill grades student homework for ANY course. All grading criteria are derived dynamically from the user's uploaded course materials — not hardcoded for a specific course.

## Phase 0: Read Grading Materials (MANDATORY FIRST STEP)

Before any grading, the user MUST provide course-specific grading materials. These are typically:
- `考核方案.docx` / `考核方案.doc` — Assessment plan with scoring table and requirements
- `附件1-项目报告模板.doc` — Report template with embedded scoring criteria
- Any additional course-specific grading documents

**From these documents, extract and store:**
1. **Grading dimensions** (N dimensions × M points each) — read from the scoring quantification table
2. **Scoring levels** per dimension (e.g., 9-10: 完整实现, 7-8: 基本实现, 5-6: 不完整, <5: 失败)
3. **Word count requirement** (e.g., ≥3000 words, ±300 acceptable, <2000 penalty)
4. **Distribution requirement** (e.g., 优秀15%, 良好35%, 中等35%, 及格15%)
5. **Penalty rules** (e.g., missing X → deduct on dimY, no source → fail)
6. **Special rules** (e.g., auto-skip embedded scoring tables, no perfect score, max failing count)
7. **Output format** (e.g., Excel columns, advantages/disadvantages length)

**Confirm understanding by listing all extracted rules before proceeding.**

## Phase 1: Discovery

1. Explore student submission directory to map `{student_id} → {name, report_path, source_path}`
2. Count total students (N)
3. For each student, compile: report file (.doc/.docx), source code (.py/.ipynb or other), video files, data files

## Phase 2: Report Extraction

For each report file:
- `.docx` → use `python-docx` (paragraphs + tables)
- `.doc` (OLE2 binary) → use PowerShell Word COM: `$w=New-Object -ComObject Word.Application; $w.Visible=$false; $d=$w.Documents.Open(path); $t=$d.Content.Text; $d.Close(); $w.Quit()`
- `.pdf` → use `markitdown` or pdf skill
- Store extracted text in a dedicated output directory with naming `{id}-{name}.txt`

## Phase 3: Source Code Analysis

For each source code file, detect:
- Language and framework features relevant to the course (e.g., for Python爬虫: requests, BeautifulSoup, Selenium, Scrapy, SQLite, MySQL, matplotlib, jieba, wordcloud; for other courses: adapt detection accordingly)
- Key quality indicators: line count, function count, import count
- Feature flags: database usage, visualization, error handling, compliance checks, mock/sample data detection
- For `.ipynb` files, read as JSON and extract code cells

## Phase 4: Auto-Skip Rules

**Embedded Scoring Tables:** Students often mistakenly paste the course scoring quantification table into their reports. When detected (typically on page 2 of the report, matching the structure from the reference materials):
- Skip the entire table page from word count
- Do NOT deduct points for this formatting error

**Code blocks and references:** Exclude from word count.

## Phase 5: Dimension Scoring

Score each student on every dimension from the extracted rubric. Apply ALL penalty rules from the grading materials.

**General scoring principles (apply regardless of course):**
- Read the report text AND source code for every student
- Apply hard penalty rules from the grading materials
- Differentiate scores — avoid uniform [7,7,7,7,7,7,7,7,7,7] patterns
- Score based on actual content, not formulas alone

## Phase 6: Advantages, Disadvantages, Comments

For each student, generate:
- **Advantages**: Specific to actual code snippets, specific charts, specific analysis points. Must reference concrete elements from the student's work.
- **Disadvantages**: Specific, targeted improvement suggestions with concrete examples.
- **Teacher Comment**: Formal 20-30 character instructor evaluation.

Character count requirements as specified in the grading materials (typically 100+/150+/20-30).

## Phase 7: Normal Distribution Curve

Apply curve to match the distribution specified in grading materials.

Standard curve function:
```python
def apply_curve(rank, n, top_pct=0.15, good_pct=0.35, mid_pct=0.35):
    top_n = round(n * top_pct)
    good_n = round(n * good_pct)
    mid_n = round(n * mid_pct)
    if rank < top_n: return round(93 - (rank/max(1,top_n-1))*3)
    elif rank < top_n+good_n: return round(89 - ((rank-top_n)/max(1,good_n-1))*9)
    elif rank < top_n+good_n+mid_n: return round(79 - ((rank-top_n-good_n)/max(1,mid_n-1))*9)
    else: return round(69 - ((rank-top_n-good_n-mid_n)/max(1,n-top_n-good_n-mid_n-1))*9)
```

Adjust curve parameters based on course requirements.

## Phase 8: Excel Output

Generate Excel with columns matching the user's specified output format.

Apply color coding: 优秀=green, 良好=blue, 中等=yellow, 及格=light red, 不及格=dark red.

## Phase 9: Quality Audit

After generating all grades:
1. Verify NO student has all identical scores (no placeholder [7,7,7,7,7,7,7,7,7,7])
2. Verify NO impossible score combinations (e.g., dim1=9 but dim9=3)
3. Verify distribution matches target within reasonable tolerance
4. Verify all advantages/disadvantages/comments meet length requirements
5. Re-read a sample of reports to cross-check scores
6. Fix any issues found before delivering final output

## Scripts

### `scripts/extract_reports.py`
Batch extraction of .doc/.docx student reports to text files.
Usage: `python scripts/extract_reports.py <student_base_dir> <output_dir> [student_list.json]`

### `scripts/generate_excel.py`
Generate final graded Excel from JSON grading data with curve.
Usage: `python scripts/generate_excel.py <grades.json> <output.xlsx>`

## References

### `references/grading_criteria.md`
Generic grading criteria reference. Update this file with course-specific rules after reading the user's grading materials. Contains common penalty patterns applicable across courses.
