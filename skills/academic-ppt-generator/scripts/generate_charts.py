#!/usr/bin/env python3
"""
学术PPT图表生成脚本模板
使用matplotlib生成学术发表级图表（300DPI）
"""

import matplotlib
matplotlib.use('Agg')  # 非交互式后端，无需GUI
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ========== 全局配置 ==========
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'ppt_charts')
os.makedirs(OUTPUT_DIR, exist_ok=True)

DPI = 300

# 学术配色（Nature/Science风格，色盲友好）
COLORS = {
    'navy':   '#17375E',   # 深蓝-主色
    'blue':   '#3276CB',   # 蓝-辅色
    'red':    '#C0392B',   # 红-强调
    'green':  '#27AE60',   # 绿-强调
    'purple': '#6C5B7B',   # 紫-强调
    'gold':   '#C9A84C',   # 金-装饰
    'lt_blue':'#DBEEF4',   # 浅蓝-背景
    'gray':   '#F2F2F2',   # 浅灰-背景
}

PALETTE = [COLORS['blue'], COLORS['red'], COLORS['green'], COLORS['purple'], COLORS['gold']]

# 中文字体配置
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Microsoft YaHei', 'SimHei', 'Arial'],
    'axes.unicode_minus': False,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': '#333333',
    'axes.linewidth': 0.8,
    'xtick.labelsize': 9.5,
    'ytick.labelsize': 9.5,
    'axes.labelsize': 11,
    'axes.titlesize': 14,
    'legend.fontsize': 9,
})


def academic_style(ax):
    """应用学术风格：去除顶部和右侧spine"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.8)
    ax.spines['bottom'].set_linewidth(0.8)


def add_source_note(fig, text, y=0.01):
    """添加数据来源脚注"""
    fig.text(0.12, y, text, fontsize=8, color='#666666', style='italic')


# ========== 图表1: 水平柱状图 ==========
def gen_barh_chart():
    """生成水平柱状图+目标参考线+差距区间"""
    fig, ax = plt.subplots(figsize=(10, 4.8))

    categories = ['专业匹配度', '转化率', '人才缺口', '校企合作数']
    current = [58, 12.6, 12, 36]  # 现状值
    target = [85, 40, 0, 200]     # 目标值

    y_pos = np.arange(len(categories))
    bar_height = 0.35

    # 现状柱
    bars1 = ax.barh(y_pos + bar_height/2, current, bar_height,
                     color=COLORS['blue'], label='现状', edgecolor='white', linewidth=0.5)

    # 目标柱（半透明）
    bars2 = ax.barh(y_pos - bar_height/2, target, bar_height,
                     color=COLORS['green'], alpha=0.3, label='目标', edgecolor=COLORS['green'], linewidth=0.8)

    # 差距区间（斜线填充）
    for i, (c, t) in enumerate(zip(current, target)):
        if c < t:
            ax.barh(y_pos[i] + bar_height/2, t - c, bar_height,
                     left=c, color=COLORS['red'], alpha=0.15, hatch='///', edgecolor=COLORS['red'], linewidth=0.5)

    # 目标参考线
    for i, t in enumerate(target):
        ax.plot([t, t], [y_pos[i] - 0.4, y_pos[i] + 0.4],
                color=COLORS['green'], linewidth=1.5, linestyle='--', alpha=0.6)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)
    ax.set_xlabel('数值')
    ax.set_title('关键指标现状与目标对比', fontweight='bold', pad=15)
    ax.legend(loc='lower right', frameon=True, framealpha=0.9)
    academic_style(ax)

    add_source_note(fig, '数据来源：黑龙江省教育厅2024年度报告 / 广厦学院产教融合年报')
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(os.path.join(OUTPUT_DIR, 'fig1_data_gap.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('✅ fig1_data_gap.png generated')


# ========== 图表2: 概念框架图 ==========
def gen_framework_chart():
    """生成中心辐射式概念框架图"""
    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # 中心圆
    center = (5, 3.1)
    circle_outer = plt.Circle(center, 1.2, color=COLORS['lt_blue'], alpha=0.3)
    circle_inner = plt.Circle(center, 0.8, color=COLORS['navy'], alpha=0.9)
    ax.add_patch(circle_outer)
    ax.add_patch(circle_inner)
    ax.text(5, 3.1, '深度融合', fontsize=14, fontweight='bold', color='white',
            ha='center', va='center')

    # 四链节点
    chains = [
        (2.0, 4.5, '教育链', COLORS['blue']),
        (8.0, 4.5, '人才链', COLORS['green']),
        (2.0, 1.7, '产业链', COLORS['red']),
        (8.0, 1.7, '创新链', COLORS['purple']),
    ]

    for x, y, label, color in chains:
        rect = FancyBboxPatch((x-0.8, y-0.35), 1.6, 0.7,
                               boxstyle="round,pad=0.1", facecolor=color, alpha=0.85,
                               edgecolor='white', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y, label, fontsize=12, fontweight='bold', color='white',
                ha='center', va='center')

        # 连线到中心（双向箭头）
        ax.annotate('', xy=(5 + (x-5)*0.25, 3.1 + (y-3.1)*0.25),
                     xytext=(x - (x-5)*0.15, y - (y-3.1)*0.15),
                     arrowprops=dict(arrowstyle='<->', color=color, lw=1.8, alpha=0.6))

    # 连接标签
    labels_pos = [
        (3.2, 4.1, '精准耦合', COLORS['blue']),
        (6.8, 4.1, '供需对接', COLORS['green']),
        (3.2, 2.2, '资源协同', COLORS['red']),
        (6.8, 2.2, '创新驱动', COLORS['purple']),
    ]
    for x, y, label, color in labels_pos:
        bbox = dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, alpha=0.9)
        ax.text(x, y, label, fontsize=9, color=color, ha='center', va='center', bbox=bbox)

    ax.set_title('"四链"深度融合机制框架', fontweight='bold', fontsize=14, pad=10)
    add_source_note(fig, '框架设计：基于黑龙江省"四链"深度融合政策文件')

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(os.path.join(OUTPUT_DIR, 'fig2_four_chains.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('✅ fig2_four_chains.png generated')


# ========== 图表3: 层次架构图 ==========
def gen_model_chart():
    """生成层次架构模型图"""
    fig, ax = plt.subplots(figsize=(10, 5.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.8)
    ax.axis('off')

    layers = [
        (5, 5.0, 4.0, 0.6, '"一体"\n命运共同体', COLORS['navy'], 13),
        (2.8, 3.8, 2.2, 0.6, '"两翼"之\n数字化赋能', COLORS['blue'], 11),
        (7.2, 3.8, 2.2, 0.6, '"两翼"之\n制度创新', COLORS['green'], 11),
    ]

    # 一体层
    x, y, w, h, label, color, fs = layers[0]
    rect = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.08",
                           facecolor=color, edgecolor='white', linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y, label, fontsize=fs, fontweight='bold', color='white', ha='center', va='center')

    # 两翼层
    for x, y, w, h, label, color, fs in layers[1:]:
        rect = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.08",
                               facecolor=color, alpha=0.85, edgecolor='white', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, y, label, fontsize=fs, fontweight='bold', color='white', ha='center', va='center')

    # 金色连线
    ax.plot([3.5, 5], [4.15, 4.7], color=COLORS['gold'], linewidth=2, marker='v', markersize=6)
    ax.plot([6.5, 5], [4.15, 4.7], color=COLORS['gold'], linewidth=2, marker='v', markersize=6)

    # 三平台层
    platforms = [
        (1.5, 2.3, '产教融合\n协同平台', COLORS['blue']),
        (5.0, 2.3, '数字化\n支撑平台', COLORS['green']),
        (8.5, 2.3, '质量保障\n评价平台', COLORS['purple']),
    ]

    for x, y, label, color in platforms:
        rect = FancyBboxPatch((x-1.1, y-0.45), 2.2, 0.9, boxstyle="round,pad=0.08",
                               facecolor='white', edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        # 彩色头部条
        header = FancyBboxPatch((x-1.1, y+0.25), 2.2, 0.2, boxstyle="round,pad=0.02",
                                 facecolor=color, edgecolor=color, linewidth=0)
        ax.add_patch(header)
        ax.text(x, y-0.05, label, fontsize=10, color='#333333', ha='center', va='center')

    # 连线到两翼
    ax.plot([1.5, 2.8], [2.8, 3.5], color=COLORS['gold'], linewidth=1.5, alpha=0.6)
    ax.plot([5.0, 5.0], [2.8, 3.5], color=COLORS['gold'], linewidth=1.5, alpha=0.6)
    ax.plot([8.5, 7.2], [2.8, 3.5], color=COLORS['gold'], linewidth=1.5, alpha=0.6)

    # 技术底座
    base = FancyBboxPatch((0.5, 0.8), 9.0, 0.6, boxstyle="round,pad=0.08",
                           facecolor='#E8E8E8', edgecolor='#999999', linewidth=1)
    ax.add_patch(base)
    ax.text(5, 1.1, '技术底座：大数据 · 云计算 · 人工智能 · 区块链', fontsize=10,
            color='#555555', ha='center', va='center')

    # 虚线反馈
    ax.annotate('', xy=(5, 1.5), xytext=(5, 2.3),
                arrowprops=dict(arrowstyle='->', color=COLORS['gold'], lw=1.2, linestyle='--'))

    ax.set_title('"一体两翼三平台"实践模型', fontweight='bold', fontsize=14, pad=10)
    add_source_note(fig, '模型设计：基于产教融合命运共同体理论框架')

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    fig.savefig(os.path.join(OUTPUT_DIR, 'fig3_model.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('✅ fig3_model.png generated')


# ========== 图表4: 保障体系图 ==========
def gen_guarantee_chart():
    """生成三重保障体系图"""
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    pillars = [
        (1.5, 0.5, '制度保障', COLORS['blue'],
         ['政策法规体系', '产教融合联席制度', '利益分配机制']),
        (5.0, 0.5, '资源保障', COLORS['green'],
         ['专项资金投入', '共享实训基地', '双师型教师队伍']),
        (8.5, 0.5, '评价保障', COLORS['purple'],
         ['多元评价体系', '质量监测平台', '动态反馈机制']),
    ]

    for x, y, title, color, items in pillars:
        # 主体矩形
        rect = FancyBboxPatch((x-1.3, y), 2.6, 3.2, boxstyle="round,pad=0.08",
                               facecolor='white', edgecolor=color, linewidth=2)
        ax.add_patch(rect)

        # 标题头
        header = FancyBboxPatch((x-1.3, y+2.6), 2.6, 0.6, boxstyle="round,pad=0.05",
                                 facecolor=color, edgecolor=color, linewidth=0)
        ax.add_patch(header)
        ax.text(x, y+2.9, title, fontsize=12, fontweight='bold', color='white',
                ha='center', va='center')

        # 左侧色条
        accent = FancyBboxPatch((x-1.3, y), 0.06, 2.6, boxstyle="round,pad=0",
                                 facecolor=color, edgecolor=color, linewidth=0)
        ax.add_patch(accent)

        # 列表项
        for i, item in enumerate(items):
            ax.text(x-0.9, y+2.1-i*0.7, f'● {item}', fontsize=10, color='#333333',
                    ha='left', va='center')

    ax.set_title('三重保障机制体系', fontweight='bold', fontsize=14, pad=10)
    add_source_note(fig, '保障体系设计：基于产教融合政策框架与实践经验')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(os.path.join(OUTPUT_DIR, 'fig4_guarantee.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('✅ fig4_guarantee.png generated')


# ========== 图表5: 对比表图 ==========
def gen_paradigm_chart():
    """生成范式对比表图"""
    fig, ax = plt.subplots(figsize=(10, 4.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.0)
    ax.axis('off')

    # 表头
    headers = ['维度', '传统模式', '命运共同体模式']
    header_colors = ['#E8E8E8', COLORS['red'], COLORS['green']]
    for i, (header, hcolor) in enumerate(zip(headers, header_colors)):
        x = 0.3 + i * 3.2
        rect = FancyBboxPatch((x, 3.2), 2.8, 0.5, boxstyle="round,pad=0.02",
                               facecolor=hcolor, edgecolor='white', linewidth=1)
        ax.add_patch(rect)
        ax.text(x+1.4, 3.45, header, fontsize=11, fontweight='bold',
                color='white' if i > 0 else '#333333', ha='center', va='center')

    # 数据行
    rows = [
        ('关系定位', '甲方乙方', '共生共赢'),
        ('资源流动', '单向输出', '双向赋能'),
        ('利益分配', '零和博弈', '共享增值'),
        ('合作深度', '浅层协作', '深度融合'),
        ('持续时间', '项目制', '长效机制'),
    ]

    for j, (dim, old, new) in enumerate(rows):
        y = 2.6 - j * 0.5
        bg_color = '#F8F8F8' if j % 2 == 0 else 'white'

        # 维度列
        rect = FancyBboxPatch((0.3, y-0.2), 2.8, 0.45, boxstyle="round,pad=0.01",
                               facecolor=bg_color, edgecolor='#E0E0E0', linewidth=0.5)
        ax.add_patch(rect)
        ax.text(1.7, y, dim, fontsize=10, color='#333333', ha='center', va='center', fontweight='bold')

        # 传统列
        rect = FancyBboxPatch((3.5, y-0.2), 2.8, 0.45, boxstyle="round,pad=0.01",
                               facecolor=bg_color, edgecolor='#E0E0E0', linewidth=0.5)
        ax.add_patch(rect)
        ax.text(4.9, y, old, fontsize=10, color=COLORS['red'], ha='center', va='center')

        # 新模式列
        rect = FancyBboxPatch((6.7, y-0.2), 2.8, 0.45, boxstyle="round,pad=0.01",
                               facecolor=bg_color, edgecolor='#E0E0E0', linewidth=0.5)
        ax.add_patch(rect)
        ax.text(8.1, y, new, fontsize=10, color=COLORS['green'], ha='center', va='center')

        # 箭头
        ax.annotate('', xy=(6.7, y), xytext=(6.3, y),
                     arrowprops=dict(arrowstyle='->', color=COLORS['gold'], lw=2))

    ax.set_title('范式转型：从"资源互补"到"命运共同体"', fontweight='bold', fontsize=14, pad=10)
    add_source_note(fig, '对比分析：基于产教融合理论研究与实践探索')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(os.path.join(OUTPUT_DIR, 'fig5_paradigm.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('✅ fig5_paradigm.png generated')


# ========== 图表6: 时间线图 ==========
def gen_timeline_chart():
    """生成实践时间线图"""
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.5)
    ax.axis('off')

    events = [
        (1.5, 2021, '启动探索', COLORS['blue']),
        (3.5, 2022, '模式构建', COLORS['green']),
        (5.5, 2023, '平台建设', COLORS['purple']),
        (7.5, 2024, '深化拓展', COLORS['red']),
        (9.0, 2025, '示范推广', COLORS['gold']),
    ]

    # 主时间轴
    ax.plot([0.5, 9.8], [1.5, 1.5], color='#999999', linewidth=2, solid_capstyle='butt')
    ax.annotate('', xy=(9.8, 1.5), xytext=(9.5, 1.5),
                arrowprops=dict(arrowstyle='->', color='#999999', lw=2))

    for x, year, label, color in events:
        # 节点圆
        circle = plt.Circle((x, 1.5), 0.15, color=color, zorder=5)
        ax.add_patch(circle)

        # 年份
        ax.text(x, 0.8, str(year), fontsize=11, fontweight='bold', color=color,
                ha='center', va='center')

        # 事件标签
        ax.text(x, 2.2, label, fontsize=10, color='#333333',
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=color, linewidth=1.2))

        # 连线
        ax.plot([x, x], [1.7, 1.95], color=color, linewidth=1.2)

    ax.set_title('产教融合实践发展历程', fontweight='bold', fontsize=14, pad=10)
    add_source_note(fig, '时间线：基于广厦学院产教融合实践年报')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(os.path.join(OUTPUT_DIR, 'fig6_timeline.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('✅ fig6_timeline.png generated')


# ========== 主函数 ==========
if __name__ == '__main__':
    print('🔬 Generating academic charts (300 DPI)...')
    gen_barh_chart()
    gen_framework_chart()
    gen_model_chart()
    gen_guarantee_chart()
    gen_paradigm_chart()
    gen_timeline_chart()
    print('✅ All 6 charts generated successfully!')
