# -*- coding: utf-8 -*-
"""
自然科/理化科 300 DPI 高清考卷插圖繪製引擎 (science_plotter.py)
嚴格遵守：
1. +8 Pt 特大字級標準 (標題 19.5~21pt、物件代號 18~19.5pt、刻度 16.5~17.5pt、尺寸標註 17~18.5pt)
2. 黑白灰階印刷優化 (實線/虛線/點線/不同灰階/網格填充，嚴禁依賴顏色區分)
3. 國中不超綱原則 (圖形與題幹嚴禁用「斜率」字眼，回歸比值與正比定義)
4. 圖例文字精簡，詳細敘述移至題幹
5. 零重疊、零遮擋、視角邊界主動外擴
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 中文字型設定
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'DFKai-SB', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def create_figure(figsize=(5.5, 4.2), dpi=300):
    """建立白底高清 300 DPI 畫布"""
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    return fig, ax

def plot_mv_density(materials, output_path="mv_density.png", title="圖(一) 質量與體積關係圖"):
    """
    繪製 M-V 質量體積關係圖
    materials: [{'name': '甲', 'density': 2.0, 'linestyle': '-'}, {'name': '乙', 'density': 1.0, 'linestyle': '--'}]
    """
    fig, ax = create_figure(figsize=(5.5, 4.2))
    
    v_max = 50
    v = np.linspace(0, v_max, 100)
    
    for mat in materials:
        name = mat.get('name', '')
        d = mat.get('density', 1.0)
        ls = mat.get('linestyle', '-')
        m = d * v
        ax.plot(v, m, color='black', linestyle=ls, linewidth=2.2, label=f"物質{name}")
        # 在曲線末端直接標註名稱，避免覆蓋圖面
        ax.text(v[-1] + 1, m[-1], f"{name}", fontsize=18, fontweight='bold', va='center')

    ax.set_xlim(0, v_max * 1.15)
    ax.set_ylim(0, max(mat.get('density', 1.0) * v_max for mat in materials) * 1.15)
    
    ax.set_xlabel("體積 $V$ (cm$^3$)", fontsize=18, fontweight='bold')
    ax.set_ylabel("質量 $M$ (g)", fontsize=18, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=16.5)
    ax.set_title(title, fontsize=20, fontweight='bold', pad=12)
    ax.grid(True, linestyle=':', alpha=0.6, color='gray')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    return output_path

def plot_cylinder_intercept(density, empty_mass, output_path="cylinder_intercept.png", title="圖(二) 量筒與液體總質量關係圖"):
    """
    繪製量筒加液體截距圖 (縱軸截距為空量筒質量，直線上升幅度代表液體密度)
    """
    fig, ax = create_figure(figsize=(5.5, 4.2))
    
    v = np.array([0, 10, 20, 30, 40, 50])
    m = empty_mass + density * v
    
    ax.plot(v, m, color='black', linestyle='-', linewidth=2.2, marker='o', markersize=7, markerfacecolor='black')
    
    # 標註截距點
    ax.plot(0, empty_mass, marker='s', markersize=8, color='black')
    ax.annotate(f"空量筒質量\n({empty_mass} g)", xy=(0, empty_mass), xytext=(8, empty_mass + 5),
                fontsize=17, fontweight='bold',
                arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=6))
    
    ax.set_xlim(-2, 58)
    ax.set_ylim(0, max(m) * 1.2)
    ax.set_xlabel("液體體積 $V$ (cm$^3$)", fontsize=18, fontweight='bold')
    ax.set_ylabel("總質量 $M$ (g)", fontsize=18, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=16.5)
    ax.set_title(title, fontsize=20, fontweight='bold', pad=12)
    ax.grid(True, linestyle=':', alpha=0.6, color='gray')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    return output_path

def plot_transverse_wave(wavelength=20, amplitude=5, num_periods=2, output_path="transverse_wave.png", title="圖(三) 橫波波形示意圖"):
    """
    繪製橫波波形構造圖 (波峰、波谷、振幅 A、波長 λ)
    """
    fig, ax = create_figure(figsize=(6.2, 3.8))
    
    x = np.linspace(0, wavelength * num_periods, 400)
    y = amplitude * np.sin(2 * np.pi * x / wavelength)
    
    # 平衡位置
    ax.axhline(0, color='gray', linestyle='--', linewidth=1.5)
    ax.text(x[-1] + 1, 0, "平衡位置", fontsize=15.5, va='center')
    
    # 波動曲線
    ax.plot(x, y, color='black', linewidth=2.2)
    
    # 標註波峰與波谷
    crest_x = wavelength / 4
    trough_x = 3 * wavelength / 4
    ax.plot(crest_x, amplitude, 'o', color='black', markersize=6)
    ax.text(crest_x, amplitude + 0.8, "波峰", fontsize=18, fontweight='bold', ha='center')
    
    ax.plot(trough_x, -amplitude, 'o', color='black', markersize=6)
    ax.text(trough_x, -amplitude - 1.5, "波谷", fontsize=18, fontweight='bold', ha='center')
    
    # 標註波長 λ
    ax.annotate('', xy=(crest_x, amplitude + 0.3), xytext=(crest_x + wavelength, amplitude + 0.3),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.8))
    ax.text(crest_x + wavelength / 2, amplitude + 0.7, f"波長 $\\lambda = {wavelength}$ cm",
            fontsize=17, fontweight='bold', ha='center')
    
    # 標註振幅 A
    ax.annotate('', xy=(wavelength / 2, 0), xytext=(wavelength / 2, amplitude),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.8))
    ax.text(wavelength / 2 - 1.5, amplitude / 2, f"$A={amplitude}$ cm", fontsize=16.5, fontweight='bold', ha='right')

    ax.set_xlim(-2, wavelength * num_periods + 8)
    ax.set_ylim(-amplitude * 1.6, amplitude * 1.6)
    ax.set_xlabel("位置 $x$ (cm)", fontsize=18, fontweight='bold')
    ax.set_ylabel("位移 $y$ (cm)", fontsize=18, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=16.5)
    ax.set_title(title, fontsize=20, fontweight='bold', pad=12)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    return output_path

def plot_balance_scale(pointer_angle=5, output_path="balance_scale.png", title="圖(四) 上皿天平示意圖"):
    """
    繪製上皿天平示意圖
    pointer_angle: >0 偏右, <0 偏左, =0 平衡
    """
    fig, ax = create_figure(figsize=(5.8, 4.2))
    ax.axis('off')
    
    # 底座與支柱
    ax.plot([-3, 3], [0, 0], color='black', lw=3) # 底座
    ax.plot([0, 0], [0, 3], color='black', lw=3)  # 支柱
    
    # 橫梁
    beam_tilt = np.radians(pointer_angle * 0.5)
    bx = np.array([-2.5, 2.5]) * np.cos(beam_tilt)
    by = 3.0 + np.array([-2.5, 2.5]) * np.sin(beam_tilt)
    ax.plot(bx, by, color='black', lw=2.5)
    
    # 兩盤
    left_pan_x, left_pan_y = bx[0], by[0]
    right_pan_x, right_pan_y = bx[1], by[1]
    
    # 左盤支柱與秤盤
    ax.plot([left_pan_x, left_pan_x], [left_pan_y, left_pan_y + 0.6], color='black', lw=2)
    ax.plot([left_pan_x - 0.8, left_pan_x + 0.8], [left_pan_y + 0.6, left_pan_y + 0.6], color='black', lw=2.5)
    
    # 右盤支柱與秤盤
    ax.plot([right_pan_x, right_pan_x], [right_pan_y, right_pan_y + 0.6], color='black', lw=2)
    ax.plot([right_pan_x - 0.8, right_pan_x + 0.8], [right_pan_y + 0.6, right_pan_y + 0.6], color='black', lw=2.5)
    
    # 校準螺絲 A 與 B
    ax.plot(bx[0] + 0.2, by[0], 's', color='gray', markersize=8)
    ax.text(bx[0] - 0.3, by[0] - 0.4, "左校準螺絲 A", fontsize=17, fontweight='bold', ha='right')
    
    ax.plot(bx[1] - 0.2, by[1], 's', color='gray', markersize=8)
    ax.text(bx[1] + 0.3, by[1] - 0.4, "右校準螺絲 B", fontsize=17, fontweight='bold', ha='left')
    
    # 指針與刻度板
    p_rad = np.radians(-pointer_angle)
    px = 1.8 * np.sin(p_rad)
    py = 3.0 - 1.8 * np.cos(p_rad)
    ax.plot([0, px], [3.0, py], color='black', lw=2) # 指針向下
    
    # 刻度盤 (小弧線)
    arc_x = np.linspace(-0.6, 0.6, 20)
    arc_y = 3.0 - 1.8 + 0.05 * (arc_x**2)
    ax.plot(arc_x, arc_y, color='black', lw=1.5)
    ax.text(0, 0.9, "刻度盤 (0)", fontsize=16.5, ha='center', fontweight='bold')
    
    # 標題與圖名
    ax.text(0, -0.6, title, fontsize=19.5, fontweight='bold', ha='center')
    
    ax.set_xlim(-4.2, 4.2)
    ax.set_ylim(-0.9, 4.5)
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, facecolor='white', bbox_inches='tight')
    plt.close()
    return output_path
