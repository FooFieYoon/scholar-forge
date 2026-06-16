# Grading Criteria Reference (Generic - Update per Course)

This file serves as a template. After reading the user's uploaded course materials (考核方案, 附件1, etc.), update this file with the specific rules extracted from those documents.

## Scoring Dimension Template

Extract from the course scoring quantification table. Common structure:

### Dimension N: [Name] ([Weight]%)
| Score | Criteria |
|-------|----------|
| 9-10 | [Top-level description] |
| 7-8 | [Mid-level description] |
| 5-6 | [Low-level description] |
| <5 | [Failure description] |

## Common Hard Penalty Rules

These patterns apply across many courses. Verify against the user's specific materials.

### Word Count Penalties
- Requirement: [N] words (±[M] acceptable)
- < [threshold]: deduct [X-Y] points on dimension [Z]

### Missing Elements Penalties
| Missing Item | Penalty |
|-------------|---------|
| No source code submitted | Functional dimension = 3, Knowledge dimension = 2 |
| No X discussion | Related dimension ≤ 6 |
| Mock/sample data used | Functional dimension ≤ 5 |
| No error handling | Functional + Logic dimensions ≤ 6 |
| No diagrams/flowcharts | Thinking tools dimension ≤ 6 |
| Cover page shows wrong class/name | Format dimension deduct 1 |

### Special Cases
| Case | Action |
|------|--------|
| Non-course project (严重偏题) | May give 0 |
| Embedded scoring table in report | Skip, no penalty |
| Extreme failure | ≤ [N] students below 60 |

## Distribution Requirements

| Level | Score Range | Target % |
|-------|-------------|----------|
| 优秀 | 90-100 | ~15% |
| 良好 | 80-89 | ~35% |
| 中等 | 70-79 | ~35% |
| 及格 | 60-69 | ~15% |
| 不及格 | <60 | ≤[N] |

## Output Format

Excel columns: 学号 | 姓名 | 总分 | 等级 | [dim1] | [dim2] | ... | [dimN] | 优点([X]字以上) | 缺点([Y]字以上) | 指导教师评语([Z]字)

---

## Example: Python爬虫技术 Course

### Dimensions (10 × 10pts)
1. 项目功能实现与运行效果 — 9-10: 完整正确稳定合规; 7-8: 核心功能实现; 5-6: 不完整; <5: 无法运行
2. 知识整合应用 — 9-10: 综合运用; 7-8: 关键知识整合; 5-6: 简单使用; <5: 原则性错误
3. 编码及报告规范 — 9-10: 规范完整; 7-8: 基本规范; 5-6: 规范性差; <5: 混乱
4. 逻辑严谨性 — 9-10: 闭环完整; 7-8: 通顺; 5-6: 有断点; <5: 混乱
5. 思维链工具使用 — 9-10: 流程图清晰; 7-8: 有表达; 5-6: 形式化; <5: 无
6. 迭代优化痕迹 — 9-10: 完整链条; 7-8: 有过程; 5-6: 简单对比; <5: 无
7. 人机协同调试 — 9-10: 深入提问; 7-8: 较具体; 5-6: 宽泛; <5: 低质量
8. 演示表达 — 9-10: 专业完整; 7-8: 流畅; 5-6: 表面; <5: 中断
9. 批判甄别+合规 — 9-10: 明确理由; 7-8: 较浅; 5-6: 无分析; <5: 无甄别
10. 心得反思 — 9-10: 深刻; 7-8: 较浅; 5-6: 空泛; <5: 无

### Hard Rules
- No HTTP → dim1≤4; Mock → dim1≤5; No source → dim1=3,dim2=2
- No robots → dim9≤6; No DB → dim2≤7; No try/except → dim1≤6,dim4≤6
- Words <2000 → dim3≤5; <2700 → dim3≤6
- Wrong class on cover → dim3-1
