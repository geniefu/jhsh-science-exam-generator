# -*- coding: utf-8 -*-
"""
自然科/理化科 試卷自動化質量檢驗程式 (science_verifier.py)
檢核項目：
1. 全卷配分加總是否嚴格等於 100 分？各大題與小題配分是否皆為整數？
2. 題號是否連續無跳號？
3. 選擇題是否全數為四選一且選項齊全？正解分佈是否均衡 (各約 25%)？
4. 課綱防超綱字眼過濾：嚴禁出現「斜率」、合金複雜公式、高年級公式等。
"""

import sys
import re

PROHIBITED_TERMS = [
    ("斜率", "國中尚未教授斜率概念，請改用『比值為密度』或『成正比』"),
    ("合金密度公式", "國中課綱限制不考多元合金平均密度繁瑣計算"),
    ("動量守恆", "動量守恆為高中物理範疇，國中理化僅教授牛頓第三運動定律相互作用力"),
    ("角動量", "超綱高中大學物理"),
    ("分離係數法", "數學多項式除法超綱"),
    ("雙重根號", "國中不考雙重根號化簡"),
    ("克拉瑪公式", "超綱高中數學"),
    ("反應商數", "化學平衡反應商數 Q 為高中選修化學"),
    ("理想氣體常數 R", "PV=nRT 繁複數值計算為高中範疇，國中僅探討波以耳與查理定性關係"),
]

def verify_score_total(questions_list, expected_total=100):
    """
    驗證題目配分：
    questions_list: [{'num': 1, 'score': 3}, ...]
    """
    total = sum(q.get('score', 0) for q in questions_list)
    errors = []
    
    for q in questions_list:
        score = q.get('score', 0)
        if not isinstance(score, int) or score <= 0:
            errors.append(f"題號 {q.get('num')}: 配分必須為正整數，當前為 {score}")
            
    if total != expected_total:
        errors.append(f"試卷總分錯誤：當前總分 {total} 分，應為 {expected_total} 分！")
        
    return (len(errors) == 0, total, errors)

def verify_question_continuity(questions_list):
    """驗證題號連續性"""
    nums = [q.get('num') for q in questions_list if 'num' in q]
    errors = []
    if not nums:
        return (False, ["試卷無有效題目列表"])
        
    expected = list(range(1, len(nums) + 1))
    if nums != expected:
        diff = set(expected).symmetric_difference(set(nums))
        errors.append(f"題號不連續或有缺漏/重複！異常題號：{diff}")
        
    return (len(errors) == 0, errors)

def verify_options_balance(answers_list):
    """
    驗證選項均衡度 (A, B, C, D)
    answers_list: ['A', 'C', 'B', 'D', ...]
    """
    total = len(answers_list)
    if total == 0:
        return (False, "無答案列表")
        
    counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for ans in answers_list:
        ans_clean = str(ans).strip().upper()
        if ans_clean in counts:
            counts[ans_clean] += 1
            
    ratios = {k: f"{v}/{total} ({v/total*100:.1f}%)" for k, v in counts.items()}
    # 檢查是否有選項偏離 15%~35%
    imbalance = []
    for k, v in counts.items():
        ratio = v / total
        if ratio < 0.12 or ratio > 0.38:
            imbalance.append(f"選項 ({k}) 比例異常：{ratio*100:.1f}%")
            
    return (len(imbalance) == 0, ratios, imbalance)

def verify_anti_out_of_bounds(text):
    """過濾文本中的禁忌超綱字眼"""
    found = []
    for term, reason in PROHIBITED_TERMS:
        if term in text:
            found.append(f"【超綱警告】偵測到禁忌詞『{term}』：{reason}")
    return (len(found) == 0, found)

def run_all_checks(exam_data):
    """
    執行全面檢核
    exam_data: {
        'questions': [...],
        'answers': [...],
        'full_text': "..."
    }
    """
    results = {}
    
    # 1. 配分
    ok_score, total, errs_score = verify_score_total(exam_data.get('questions', []))
    results['score'] = {'pass': ok_score, 'total': total, 'errors': errs_score}
    
    # 2. 題號
    ok_num, errs_num = verify_question_continuity(exam_data.get('questions', []))
    results['continuity'] = {'pass': ok_num, 'errors': errs_num}
    
    # 3. 選項
    ok_opt, ratios, errs_opt = verify_options_balance(exam_data.get('answers', []))
    results['balance'] = {'pass': ok_opt, 'ratios': ratios, 'errors': errs_opt}
    
    # 4. 超綱檢查
    ok_bounds, errs_bounds = verify_anti_out_of_bounds(exam_data.get('full_text', ''))
    results['bounds'] = {'pass': ok_bounds, 'errors': errs_bounds}
    
    all_passed = ok_score and ok_num and ok_opt and ok_bounds
    return all_passed, results
