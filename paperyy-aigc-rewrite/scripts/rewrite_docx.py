"""
PaperYY AIGC降重工具 - docx段落替换脚本

用法:
  python rewrite_docx.py <input.docx> <output.docx> <replacements.json>

功能:
  1. 解包docx为XML
  2. 读取replacements.json中的段落索引→新文本映射
  3. 逐段替换，保留首个run的格式属性(rPr)
  4. 重新打包为docx

依赖:
  Python 3.7+ (标准库即可: xml.etree.ElementTree, zipfile, shutil, json, copy, os, sys)

注意:
  - 段落索引从0开始，仅计算w:p标签
  - 替换时会保留第一个w:r的rPr格式
  - tables中的段落也会被计入索引
"""

import xml.etree.ElementTree as ET
import copy
import zipfile
import shutil
import json
import os
import sys

# Word XML 命名空间
ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
xml_ns = 'http://www.w3.org/XML/1998/namespace'

# 注册所有常见命名空间，防止打包时丢失前缀声明
_NAMESPACES = {
    'w': ns,
    'wpc': 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'o': 'urn:schemas-microsoft-com:office:office',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'v': 'urn:schemas-microsoft-com:vml',
    'wp14': 'http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'w10': 'urn:schemas-microsoft-com:office:word',
    'w15': 'http://schemas.microsoft.com/office/word/2012/wordml',
    'wpg': 'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup',
    'wpi': 'http://schemas.microsoft.com/office/word/2010/wordprocessingInk',
    'wne': 'http://schemas.microsoft.com/office/word/2006/wordml',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
    'wpsCustomData': 'http://www.wps.cn/officeDocument/2013/wpsCustomData',
    'xml': xml_ns,
}

for prefix, uri in _NAMESPACES.items():
    ET.register_namespace(prefix, uri)


def get_para_text(para):
    """提取段落中所有w:t的文本"""
    parts = []
    for t in para.iter(f'{{{ns}}}t'):
        if t.text:
            parts.append(t.text)
    return ''.join(parts)


def replace_para_content(para, new_text):
    """
    替换段落文本，保留第一个w:r的格式(rPr)。
    删除所有原run，插入新的单run + xml:space="preserve"。
    """
    runs = [c for c in para if c.tag == f'{{{ns}}}r']
    if not runs:
        return False

    first_run = runs[0]
    rPr = first_run.find(f'{{{ns}}}rPr')
    rPr_copy = copy.deepcopy(rPr) if rPr is not None else None

    for r in runs:
        para.remove(r)

    new_run = ET.SubElement(para, f'{{{ns}}}r')
    if rPr_copy is not None:
        new_run.append(rPr_copy)

    new_t = ET.SubElement(new_run, f'{{{ns}}}t')
    new_t.text = new_text
    new_t.set(f'{{{xml_ns}}}space', 'preserve')
    return True


def unpack_docx(docx_path, unpack_dir):
    """解包docx到指定目录"""
    with zipfile.ZipFile(docx_path, 'r') as z:
        z.extractall(unpack_dir)


def pack_docx(unpack_dir, output_path):
    """将目录重新打包为docx"""
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(unpack_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, unpack_dir)
                zf.write(file_path, arcname)


def rewrite(docx_path, output_path, replacements_dict):
    """
    主函数：解包→修改XML→打包

    Args:
        docx_path: 输入docx文件路径
        output_path: 输出docx文件路径
        replacements_dict: {段落索引(int): 新文本(str), ...}
    """
    # 使用临时目录解包
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        unpack_docx(docx_path, tmpdir)
        xml_path = os.path.join(tmpdir, 'word', 'document.xml')

        tree = ET.parse(xml_path)
        root = tree.getroot()

        body = root.find(f'{{{ns}}}body')
        all_paras = list(body.iter(f'{{{ns}}}p'))

        print(f"文档共 {len(all_paras)} 个段落")
        print(f"待替换 {len(replacements_dict)} 个段落\n")

        success_count = 0
        for idx, new_text in replacements_dict.items():
            if idx < len(all_paras):
                old_text = get_para_text(all_paras[idx])
                if replace_para_content(all_paras[idx], new_text):
                    success_count += 1
                    preview = old_text[:30] if old_text else "(空段落)"
                    print(f"[OK] 段落 {idx}: \"{preview}...\"")
                else:
                    print(f"[SKIP] 段落 {idx}: 无run元素")
            else:
                print(f"[WARN] 段落 {idx}: 索引超出范围(共{len(all_paras)}段)")

        print(f"\n成功替换 {success_count}/{len(replacements_dict)} 个段落")

        # 保存修改后的XML
        tree.write(xml_path, encoding='UTF-8', xml_declaration=True)

        # 打包为docx
        pack_docx(tmpdir, output_path)

    # 验证输出文件
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"\n输出文件: {output_path}")
        print(f"文件大小: {size:,} 字节")
    else:
        print(f"\n[ERROR] 输出文件未生成: {output_path}")


def main():
    if len(sys.argv) < 4:
        print("用法: python rewrite_docx.py <input.docx> <output.docx> <replacements.json>")
        print("\nreplacements.json 格式:")
        print('{')
        print('  "6": "替换后的段落文本...",')
        print('  "8": "另一段替换文本..."')
        print('}')
        sys.exit(1)

    input_docx = sys.argv[1]
    output_docx = sys.argv[2]
    replacements_file = sys.argv[3]

    if not os.path.exists(input_docx):
        print(f"[ERROR] 输入文件不存在: {input_docx}")
        sys.exit(1)

    if not os.path.exists(replacements_file):
        print(f"[ERROR] 替换配置文件不存在: {replacements_file}")
        sys.exit(1)

    with open(replacements_file, 'r', encoding='utf-8') as f:
        replacements = json.load(f)

    # 将JSON的字符串key转为int
    replacements_int = {int(k): v for k, v in replacements.items()}

    rewrite(input_docx, output_docx, replacements_int)


if __name__ == '__main__':
    main()
