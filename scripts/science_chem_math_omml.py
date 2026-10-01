# -*- coding: utf-8 -*-
"""
Word 原生 OMML 數學與化學方程式引擎 (science_chem_math_omml.py)
專為自然科/理化科打造：
1. 化學式下標與離子價數上標 (如 H₂SO₄, Cu²⁺, SO₄²⁻)
2. 化學反應方程式箭頭 (→, ⇌) 與反應條件標註
3. 同位素標記 (如 ²³⁵₉₂U)
4. 物態標記 ((s), (l), (g), (aq))
5. 科學單位與數值結合 (如 g/cm³, m/s², kg·m/s, Ω)
6. 純 Python 產生 OMML XML，無外部編譯器依賴，Word 內雙擊即可直接編輯
"""

import re
from docx.oxml import parse_xml

MATH_NS = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

def m_run(text, italic=False):
    """
    建立 OMML 文字節點 <m:r>
    化學符號、數字、單位預設正體 (italic=False)；純數學變數設為斜體 (italic=True)
    """
    sty = '' if italic else '<m:rPr><m:sty m:val="p"/></m:rPr>'
    esc = str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<m:r>{sty}<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math" w:eastAsia="標楷體"/><w:sz w:val="22"/></w:rPr><m:t>{esc}</m:t></m:r>'

def m_frac(num_xml, den_xml):
    """原生分數 <m:f>：num / den"""
    return f'<m:f><m:num>{num_xml}</m:num><m:den>{den_xml}</m:den></m:f>'

def m_sqrt(base_xml, deg_xml=None):
    """原生根號 <m:rad>"""
    if deg_xml is None:
        return f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>{base_xml}</m:e></m:rad>'
    return f'<m:rad><m:radPr><m:degHide m:val="0"/></m:radPr><m:deg>{deg_xml}</m:deg><m:e>{base_xml}</m:e></m:rad>'

def m_sup(base_xml, sup_xml):
    """原生上標 <m:sSup>：如離子價數 Cu²⁺ 或次方 x²"""
    return f'<m:sSup><m:e>{base_xml}</m:e><m:sup>{sup_xml}</m:sup></m:sSup>'

def m_sub(base_xml, sub_xml):
    """原生下標 <m:sSub>：如化學原子個數 H₂O"""
    return f'<m:sSub><m:e>{base_xml}</m:e><m:sub>{sub_xml}</m:sub></m:sSub>'

def m_subsup(base_xml, sub_xml, sup_xml):
    """原生上下標 <m:sSubSup>：同位素或上下標符號"""
    return f'<m:sSubSup><m:e>{base_xml}</m:e><m:sub>{sub_xml}</m:sub><m:sup>{sup_xml}</m:sup></m:sSubSup>'

def chem_formula(formula):
    """
    將標準化學式字串 (如 'H2SO4', 'Ca(OH)2', 'Cu2+', 'SO4^2-') 解析為原生 OMML XML
    """
    xml_parts = []
    # 正則切分元素、括號、數字、電荷
    tokens = re.findall(r'([A-Z][a-z]?|\(|\)|\d+|\^[-+]?\d*|[-+]\d*|\^|\+|-)', formula)
    
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        
        # 若是元素或括號
        if re.match(r'^[A-Za-z\(\)]+$', tok):
            # 檢查後面是否接數字 (下標) 或電荷 (上標)
            has_sub = False
            has_sup = False
            sub_val = ""
            sup_val = ""
            
            if i + 1 < len(tokens) and re.match(r'^\d+$', tokens[i+1]):
                has_sub = True
                sub_val = tokens[i+1]
                i += 1
            
            if i + 1 < len(tokens) and (tokens[i+1].startswith('^') or tokens[i+1] in ['+', '-'] or re.match(r'^\d*[\+\-]$', tokens[i+1])):
                has_sup = True
                sup_val = tokens[i+1].lstrip('^')
                i += 1
                
            base_r = m_run(tok, italic=False)
            if has_sub and has_sup:
                xml_parts.append(m_subsup(base_r, m_run(sub_val, italic=False), m_run(sup_val, italic=False)))
            elif has_sub:
                xml_parts.append(m_sub(base_r, m_run(sub_val, italic=False)))
            elif has_sup:
                xml_parts.append(m_sup(base_r, m_run(sup_val, italic=False)))
            else:
                xml_parts.append(base_r)
        elif tok in ['+', '＋']:
            xml_parts.append(m_run(" + ", italic=False))
        elif tok in ['-', '－']:
            xml_parts.append(m_run(" - ", italic=False))
        else:
            xml_parts.append(m_run(tok, italic=False))
        i += 1
        
    return "".join(xml_parts)

def chem_equation(reactants, products, condition=None, reversible=False):
    """
    產生化學反應方程式 OMML XML
    例如：chem_equation("2H2 + O2", "2H2O", condition="點燃")
    """
    arrow = " ⇌ " if reversible else " → "
    r_xml = chem_formula(reactants)
    p_xml = chem_formula(products)
    
    if condition:
        # 箭頭上方加條件
        arrow_node = f'<m:limUpp><m:e>{m_run(arrow, italic=False)}</m:e><m:lim>{m_run(condition, italic=False)}</m:lim></m:limUpp>'
    else:
        arrow_node = m_run(arrow, italic=False)
        
    return f"{r_xml}{arrow_node}{p_xml}"

def chem_isotope(element, mass_num, atomic_num):
    """
    同位素標記：左側上下標 (如 ²³⁵₉₂U)
    Word OMML 中使用前置上下標模擬
    """
    left_subsup = f'<m:sSubSup><m:e>{m_run(" ", italic=False)}</m:e><m:sub>{m_run(atomic_num, italic=False)}</m:sub><m:sup>{m_run(mass_num, italic=False)}</m:sup></m:sSubSup>'
    elem_node = m_run(element, italic=False)
    return f"{left_subsup}{elem_node}"

def science_unit(value_str, unit_str):
    """產生包含數值與物理量單位的 OMML，如 2.5 g/cm³ 或 9.8 m/s²"""
    v_xml = m_run(f"{value_str} ", italic=False)
    # 解析單位中的斜線與次方
    if "/" in unit_str:
        num_u, den_u = unit_str.split("/", 1)
        den_part = re.sub(r'(\d+)', lambda m: m_sup("", m_run(m.group(1), False)), den_u)
        num_part = re.sub(r'(\d+)', lambda m: m_sup("", m_run(m.group(1), False)), num_u)
        u_xml = m_frac(m_run(num_part, False), m_run(den_part, False))
    else:
        u_xml = m_run(unit_str, italic=False)
    return f"{v_xml}{u_xml}"

def append_omath(paragraph, inner_omml_xml):
    """將 OMML XML 注入 docx 段落中"""
    omath_str = f'<m:oMath {MATH_NS}>{inner_omml_xml}</m:oMath>'
    paragraph._p.append(parse_xml(omath_str))
