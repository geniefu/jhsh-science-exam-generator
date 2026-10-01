# -*- coding: utf-8 -*-
"""
新北市立錦和高中 自然科/理化科 試卷排版與 Word (.docx) 生成模組
嚴格符合：
1. 邊界 1.0 cm (0.3937 inch)
2. 全卷正文嚴格維持 11 點字 (11 Pt)，中文字型標楷體，英文字型 Times New Roman
3. 試題標題粗體加底線、扣 5 分警語
4. 題號凸排 (Hanging Indent) 0.28 inch
5. 試題插圖採右側浮動「矩形文繞圖 (wrapSquare)」(寬度 2.6~2.8 inch)，垂直節省 40%~50% 版面
6. 動態頁尾代碼：〔第 X 頁，共 Y 頁〕
7. 答案卷與詳解卷排版、表格與 0~3 級分規準支援
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_base_style(doc):
    """設定試卷基礎樣式：1cm 邊界與 11 點標楷體/Times New Roman"""
    for s in doc.sections:
        s.top_margin = Inches(0.3937)    # 1.0 cm
        s.bottom_margin = Inches(0.3937) # 1.0 cm
        s.left_margin = Inches(0.3937)   # 1.0 cm
        s.right_margin = Inches(0.3937)  # 1.0 cm
    
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(11) # 嚴格全卷 11 點字
    style._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')
    style._element.rPr.rFonts.set(qn('w:ascii'), 'Times New Roman')
    style._element.rPr.rFonts.set(qn('w:hAnsi'), 'Times New Roman')

def add_header(doc, title, scope=None, student_info=True):
    """
    加入錦和高中標準試卷抬頭
    格式：新北市立錦和高級中學 11X學年度第X學期 [國中/高中]部○年級○○科第○次段考試題
    """
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    run_t = p_title.add_run(title)
    run_t.font.name = 'Times New Roman'
    run_t._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')
    run_t.font.size = Pt(14)
    run_t.font.bold = True
    run_t.font.underline = True

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(3)
    p_sub.paragraph_format.line_spacing = 1.15

    if scope:
        run_s = p_sub.add_run(f"﹝命題範圍：{scope}﹞")
        run_s.font.size = Pt(11)
        run_s.font.bold = True
        run_s.font.name = 'Times New Roman'
        run_s._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')
    
    if student_info:
        # 右側對齊班級座號姓名欄
        p_sub.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run_info = p_sub.add_run("　　班級：______ 座號：____ 姓名：____________")
        run_info.font.size = Pt(11)
        run_info.font.name = 'Times New Roman'
        run_info._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')

def add_warnings(doc, has_answer_card=True, has_non_choice=False, custom_warning=None):
    """加入試務組指定之標準警語"""
    p_warn = doc.add_paragraph()
    p_warn.paragraph_format.space_before = Pt(0)
    p_warn.paragraph_format.space_after = Pt(4)
    p_warn.paragraph_format.line_spacing = 1.15
    
    if has_answer_card:
        run_w1 = p_warn.add_run("※ 注意事項：答案卷(卡)未寫班級、姓名、座號，或畫卡錯誤致電腦無法判讀考生身份者，一律扣 5 分。\n")
        run_w1.font.size = Pt(11)
        run_w1.font.bold = True
        run_w1.font.color.rgb = RGBColor(204, 0, 0) # 紅色警語
        run_w1.font.name = 'Times New Roman'
        run_w1._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')

    if has_non_choice:
        run_w2 = p_warn.add_run("※ 非選擇題請使用黑色墨水筆於規定欄位內作答，違者扣非選擇題總分 5 分；計算題須詳列計算過程始得計分。\n")
        run_w2.font.size = Pt(11)
        run_w2.font.bold = True
        run_w2.font.name = 'Times New Roman'
        run_w2._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')

    if custom_warning:
        run_w3 = p_warn.add_run(custom_warning)
        run_w3.font.size = Pt(11)
        run_w3.font.name = 'Times New Roman'
        run_w3._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')

def add_section_title(doc, title_text):
    """加大題標題（如：【第一部分：單一選擇題...】）"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(title_text)
    run.font.name = 'Times New Roman'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')
    run.font.size = Pt(11.5)
    run.font.bold = True

def make_floating_image(run, img_path, width=Inches(2.7), align="right", wrap="bothSides"):
    """
    將插入圖片轉換為 Word 原生浮動 wrapSquare 錨點，
    使題幹與選項在左側流暢繞行，大幅節省 40%~50% 垂直版面
    """
    if not os.path.exists(img_path):
        return None
    inline_shape = run.add_picture(img_path, width=width)
    inline = inline_shape._inline
    
    extent = inline.find(qn('wp:extent'))
    docPr = inline.find(qn('wp:docPr'))
    cNvGraphicFramePr = inline.find(qn('wp:cNvGraphicFramePr'))
    graphic = inline.find(qn('a:graphic'))
    
    cx = extent.get('cx')
    cy = extent.get('cy')
    docPr_id = docPr.get('id')
    docPr_name = docPr.get('name')
    
    anchor_xml = f'''
    <wp:anchor {nsdecls("wp", "a")} distT="36000" distB="36000" distL="144000" distR="0" simplePos="0" relativeHeight="251658240" behindDoc="0" locked="0" layoutInCell="1" allowOverlap="0">
        <wp:simplePos x="0" y="0"/>
        <wp:positionH relativeFrom="column">
            <wp:align>{align}</wp:align>
        </wp:positionH>
        <wp:positionV relativeFrom="paragraph">
            <wp:posOffset>0</wp:posOffset>
        </wp:positionV>
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:wrapSquare wrapText="{wrap}"/>
        <wp:docPr id="{docPr_id}" name="{docPr_name}"/>
    </wp:anchor>
    '''
    anchor = parse_xml(anchor_xml)
    if cNvGraphicFramePr is not None:
        anchor.append(cNvGraphicFramePr)
    if graphic is not None:
        anchor.append(graphic)
        
    parent = inline.getparent()
    parent.replace(inline, anchor)
    return anchor

def format_options(options, img_present=False):
    """
    選項智慧排版邏輯：
    - 若有右側浮動圖形：四選項一律單列排列 (1 option per line)，避免與浮動圖碰撞
    - 若無附圖且每選項 <= 14 字：四選一列橫排
    - 若無附圖且每選項 <= 24 字：兩選一列 (2x2)
    - 其餘情況：四選各一列
    回傳格式化後的字串清單
    """
    labels = ["(A)", "(B)", "(C)", "(D)"]
    opt_texts = [f"{labels[i]} {options[i]}" for i in range(len(options))]
    max_len = max(len(o) for o in opt_texts) if opt_texts else 0
    
    if img_present:
        return opt_texts # 單列 4 行
    
    if max_len <= 14 and len(opt_texts) == 4:
        return ["　　".join(opt_texts)] # 一列 4 選項
    elif max_len <= 24 and len(opt_texts) == 4:
        return [
            f"{opt_texts[0]}　　　　{opt_texts[1]}",
            f"{opt_texts[2]}　　　　{opt_texts[3]}"
        ] # 兩列 2x2
    else:
        return opt_texts # 四列

def add_question(doc, num, text, options=None, img_path=None, img_width=Inches(2.7), chapter_tag=None):
    """
    加入標準試題段落：
    - 題號凸排 (left_indent 0.28 in, first_line_indent -0.28 in)
    - 題幹末尾章節標記【X-Y】
    - 若有圖片，採用右側浮動矩形文繞圖
    - 緊隨其後加入選項
    """
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.28)
    p.paragraph_format.first_line_indent = Inches(-0.28) # 凸排
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(1)

    run_num = p.add_run(f"({num:>2}) ")
    run_num.font.bold = True
    run_num.font.size = Pt(11)
    run_num.font.name = 'Times New Roman'
    run_num._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')

    # 若有右側浮動圖形，先在題幹開頭綁定錨點
    has_img = False
    if img_path and os.path.exists(img_path):
        make_floating_image(p.add_run(), img_path, width=img_width, align="right", wrap="bothSides")
        has_img = True

    run_text = p.add_run(text)
    run_text.font.size = Pt(11)
    run_text.font.name = 'Times New Roman'
    run_text._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')

    if chapter_tag:
        run_tag = p.add_run(f" 【{chapter_tag}】")
        run_tag.font.size = Pt(10)
        run_tag.font.color.rgb = RGBColor(100, 100, 100)
        run_tag.font.name = 'Times New Roman'
        run_tag._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')

    # 選項排版
    if options:
        opt_lines = format_options(options, img_present=has_img)
        for opt_line in opt_lines:
            p_opt = doc.add_paragraph()
            p_opt.paragraph_format.left_indent = Inches(0.28)
            p_opt.paragraph_format.first_line_indent = Inches(0)
            p_opt.paragraph_format.line_spacing = 1.15
            p_opt.paragraph_format.space_before = Pt(0)
            p_opt.paragraph_format.space_after = Pt(1)
            
            run_o = p_opt.add_run(opt_line)
            run_o.font.size = Pt(11)
            run_o.font.name = 'Times New Roman'
            run_o._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')

def add_page_number_field(doc):
    """在每一節的頁尾置中加入動態頁碼：〔第 X 頁，共 Y 頁〕"""
    for section in doc.sections:
        footer = section.footer
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.text = "" # 清空預設文字
        
        r1 = p.add_run("〔第 ")
        r1.font.name = 'Times New Roman'
        r1._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')
        r1.font.size = Pt(10)

        # 動態頁碼 PAGE
        fld_page = OxmlElement('w:fldSimple')
        fld_page.set(qn('w:instr'), 'PAGE')
        p._p.append(fld_page)

        r2 = p.add_run(" 頁，共 ")
        r2.font.name = 'Times New Roman'
        r2._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')
        r2.font.size = Pt(10)

        # 動態總頁數 NUMPAGES
        fld_numpages = OxmlElement('w:fldSimple')
        fld_numpages.set(qn('w:instr'), 'NUMPAGES')
        p._p.append(fld_numpages)

        r3 = p.add_run(" 頁〕")
        r3.font.name = 'Times New Roman'
        r3._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')
        r3.font.size = Pt(10)

def add_answer_key_table(doc, answers_list, cols=10):
    """
    在答案卷頂部加入精美標準答案表格
    answers_list: [(題號, 答案, 配分), ...]
    """
    total = len(answers_list)
    rows_count = (total + cols - 1) // cols * 2 # 題號列 + 答案列
    table = doc.add_table(rows=rows_count, cols=cols)
    table.style = 'Table Grid'
    
    idx = 0
    row_idx = 0
    while idx < total:
        # 題號列
        for c in range(cols):
            cell = table.cell(row_idx, c)
            if idx + c < total:
                q_num, _, score = answers_list[idx + c]
                cell.text = f"{q_num} ({score}分)" if score else f"{q_num}"
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.size = Pt(9.5)
            else:
                cell.text = ""
        # 答案列
        for c in range(cols):
            cell = table.cell(row_idx + 1, c)
            if idx + c < total:
                _, ans, _ = answers_list[idx + c]
                cell.text = str(ans)
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.size = Pt(11)
            else:
                cell.text = ""
        idx += cols
        row_idx += 2
