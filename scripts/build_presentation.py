import os
from pathlib import Path
import subprocess

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Initialize paths
PROJECT_ROOT = Path(".").resolve()
FIG_DIR = PROJECT_ROOT / "reports" / "presentation" / "figures"
OUTPUT_DIR = PROJECT_ROOT / "reports" / "presentation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PPTX_PATH = OUTPUT_DIR / "greenlens_presentation.pptx"
PDF_PATH = OUTPUT_DIR / "greenlens_presentation.pdf"

# Initialize presentation with 16:9 widescreen
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Theme Colors
COLOR_BG = RGBColor(248, 250, 249)          # Clean soft sage tint
COLOR_PRIMARY = RGBColor(27, 67, 50)        # Deep Forest Green (#1B4332)
COLOR_SECONDARY = RGBColor(45, 106, 79)     # Emerald Green (#2D6A4F)
COLOR_TEXT_DARK = RGBColor(45, 55, 72)      # Slate Charcoal (#2D3748)
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)  # Slate Grey (#64748B)
COLOR_CARD_BG = RGBColor(255, 255, 255)     # Crisp White
COLOR_CARD_BORDER = RGBColor(216, 243, 220) # Soft Mint Border (#D8F3DC)
COLOR_ACCENT_BG = RGBColor(232, 245, 233)   # Light Sage Tint
COLOR_WHITE = RGBColor(255, 255, 255)

def apply_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

def add_header(slide, title_text, category_text="GreenLens Project Presentation"):
    # Category / Tracker
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_SECONDARY
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_PRIMARY

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    return shape

# ==============================================================================
# SLIDE 1: TITLE SLIDE
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
apply_slide_background(s1)

# Left Column: Project Identity & Metadata
left_margin = Inches(0.9)
title_box = s1.shapes.add_textbox(left_margin, Inches(1.2), Inches(6.0), Inches(4.5))
tf = title_box.text_frame
tf.word_wrap = True

p0 = tf.paragraphs[0]
p0.text = "INTRODUCTION TO ALGORITHMS  |  FINAL PROJECT"
p0.font.size = Pt(11)
p0.font.bold = True
p0.font.color.rgb = COLOR_SECONDARY
p0.space_after = Pt(14)

p1 = tf.add_paragraph()
p1.text = "GreenLens"
p1.font.size = Pt(44)
p1.font.bold = True
p1.font.color.rgb = COLOR_PRIMARY
p1.space_after = Pt(8)

p2 = tf.add_paragraph()
p2.text = "Intelligent Plant Pathology Diagnosis\n& Actionable Decision Support"
p2.font.size = Pt(16)
p2.font.bold = True
p2.font.color.rgb = COLOR_SECONDARY
p2.space_after = Pt(18)

p3 = tf.add_paragraph()
p3.text = "Deep Learning Classification & Treatment Recommendation\nfor Sustainable Agriculture"
p3.font.size = Pt(12)
p3.font.color.rgb = COLOR_TEXT_MUTED
p3.space_after = Pt(36)

# Metadata Card
meta_card = add_card(s1, left_margin, Inches(4.6), Inches(6.0), Inches(2.25), bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER)
meta_box = s1.shapes.add_textbox(left_margin + Inches(0.2), Inches(4.7), Inches(5.6), Inches(2.05))
tf_m = meta_box.text_frame
tf_m.word_wrap = True

m_p1 = tf_m.paragraphs[0]
m_p1.text = "Author / Presenter:  Abdelaziz Ahmed Elbanna"
m_p1.font.size = Pt(12.5)
m_p1.font.bold = True
m_p1.font.color.rgb = COLOR_PRIMARY
m_p1.space_after = Pt(4)

m_p2 = tf_m.add_paragraph()
m_p2.text = "Team:  TerraGreen"
m_p2.font.size = Pt(11.5)
m_p2.font.bold = True
m_p2.font.color.rgb = COLOR_SECONDARY
m_p2.space_after = Pt(4)

m_p3 = tf_m.add_paragraph()
m_p3.text = "Supervisor:  Dr. Fatma Talaat"
m_p3.font.size = Pt(11.5)
m_p3.font.color.rgb = COLOR_TEXT_DARK
m_p3.space_after = Pt(4)

m_p4 = tf_m.add_paragraph()
m_p4.text = "Course:  Introduction to Algorithms (Year 3, Semester 1)"
m_p4.font.size = Pt(11)
m_p4.font.color.rgb = COLOR_TEXT_MUTED
m_p4.space_after = Pt(5)

m_p5 = tf_m.add_paragraph()
r_label = m_p5.add_run()
r_label.text = "Repository:  "
r_label.font.size = Pt(10.5)
r_label.font.bold = True
r_label.font.color.rgb = COLOR_TEXT_DARK

r_link = m_p5.add_run()
r_link.text = "https://github.com/AbdelazizElbanna/greenlens"
r_link.font.size = Pt(10)
r_link.font.bold = True
r_link.font.color.rgb = COLOR_SECONDARY
r_link.hyperlink.address = "https://github.com/AbdelazizElbanna/greenlens"

# Right Column: Visual Graphic
if (FIG_DIR / "title_cover.png").exists():
    s1.shapes.add_picture(str(FIG_DIR / "title_cover.png"), Inches(7.3), Inches(1.4), Inches(5.2), Inches(4.8))

# ==============================================================================
# SLIDE 2: PROBLEM STATEMENT & MOTIVATION
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
apply_slide_background(s2)
add_header(s2, "Agricultural Pathology: The Problem & Motivation", "Context & Impact")

# 3 Concept Cards across top
col_w = Inches(3.64)
col_gap = Inches(0.39)
card_top = Inches(1.6)
card_h = Inches(4.8)

# Card 1: Economic & Yield Loss
add_card(s2, Inches(0.8), card_top, col_w, card_h)
tb1 = s2.shapes.add_textbox(Inches(0.95), card_top + Inches(0.2), col_w - Inches(0.3), card_h - Inches(0.4))
tf1 = tb1.text_frame
tf1.word_wrap = True

p = tf1.paragraphs[0]
p.text = "Severe Crop Yield Losses"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(14)

bullets1 = [
    "Plant pathogens (fungi, bacteria, viruses) cause an estimated 20% to 40% loss of global agricultural production annually.",
    "Smallholder farmers and amateur growers frequently lack rapid access to plant pathology experts or agricultural extension services.",
    "Early leaf symptoms are often subtle, easily confused with physiological stress or nutrient deficiencies."
]
for b in bullets1:
    bp = tf1.add_paragraph()
    bp.text = "- " + b
    bp.font.size = Pt(11.5)
    bp.font.color.rgb = COLOR_TEXT_DARK
    bp.space_after = Pt(12)

# Card 2: Pesticide Misuse
add_card(s2, Inches(0.8) + col_w + col_gap, card_top, col_w, card_h)
tb2 = s2.shapes.add_textbox(Inches(0.95) + col_w + col_gap, card_top + Inches(0.2), col_w - Inches(0.3), card_h - Inches(0.4))
tf2 = tb2.text_frame
tf2.word_wrap = True

p = tf2.paragraphs[0]
p.text = "Chemical Overuse & Impact"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(14)

bullets2 = [
    "Misdiagnosis leads to inappropriate pesticide selection (e.g., applying fungicides against bacterial or viral pathogens).",
    "Excessive and broad-spectrum chemical application contaminates soil biomes and groundwater reservoirs.",
    "Improper chemical regimens accelerate pesticide resistance in pathogen populations and elevate farmer input costs."
]
for b in bullets2:
    bp = tf2.add_paragraph()
    bp.text = "- " + b
    bp.font.size = Pt(11.5)
    bp.font.color.rgb = COLOR_TEXT_DARK
    bp.space_after = Pt(12)

# Card 3: GreenLens Objective
add_card(s2, Inches(0.8) + (col_w + col_gap)*2, card_top, col_w, card_h, bg_color=COLOR_ACCENT_BG)
tb3 = s2.shapes.add_textbox(Inches(0.95) + (col_w + col_gap)*2, card_top + Inches(0.2), col_w - Inches(0.3), card_h - Inches(0.4))
tf3 = tb3.text_frame
tf3.word_wrap = True

p = tf3.paragraphs[0]
p.text = "The GreenLens Objective"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(14)

bullets3 = [
    "Deliver instant, high-accuracy disease diagnosis from simple mobile leaf photographs.",
    "Formulate an edge-capable deep learning algorithm capable of rapid inference on constrained hardware.",
    "Bridge the gap between detection and action by generating automated, actionable treatment and prevention protocols."
]
for b in bullets3:
    bp = tf3.add_paragraph()
    bp.text = "- " + b
    bp.font.size = Pt(11.5)
    bp.font.color.rgb = COLOR_TEXT_DARK
    bp.space_after = Pt(12)

# Bottom note
bn = s2.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.7), Inches(0.5))
p_bn = bn.text_frame.paragraphs[0]
p_bn.text = "Goal: Reduce diagnosis time from days to milliseconds while achieving over 98% diagnostic accuracy."
p_bn.font.size = Pt(11)
p_bn.font.bold = True
p_bn.font.color.rgb = COLOR_SECONDARY

# ==============================================================================
# SLIDE 3: DATASET & EXPLORATORY ANALYSIS
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
apply_slide_background(s3)
add_header(s3, "Dataset Corpus & Exploratory Data Analysis", "Data Understanding")

# Left Column: Key Facts & Stratification
left_w = Inches(5.6)
add_card(s3, Inches(0.8), Inches(1.6), left_w, Inches(4.8))
tb_d = s3.shapes.add_textbox(Inches(1.0), Inches(1.8), left_w - Inches(0.4), Inches(4.4))
tf_d = tb_d.text_frame
tf_d.word_wrap = True

p = tf_d.paragraphs[0]
p.text = "PlantVillage Benchmark Dataset"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(12)

d_points = [
    ("Total Images Cataloged:", "20,639 high-resolution leaf images (256x256 RGB)."),
    ("Target Pathology Classes:", "15 distinct conditions across 3 vital staple crops:"),
    ("  - Pepper (Bell):", "Bacterial Spot, Healthy (2 classes)."),
    ("  - Potato:", "Early Blight, Late Blight, Healthy (3 classes)."),
    ("  - Tomato:", "8 Disease conditions + Healthy foliage (10 classes)."),
    ("Data Distribution:", "86.7% diseased specimens, 13.3% healthy baseline leaves."),
    ("Class Cardinality:", "Ranges from 152 samples (Potato Healthy) to 3,209 samples (Tomato Yellow Leaf Curl Virus)."),
    ("Rigorous Partitioning:", "Stratified 80% Train (16,511), 10% Val (2,064), 10% Test (2,064) ensuring exact class ratios.")
]

for label, desc in d_points:
    dp = tf_d.add_paragraph()
    dp.text = f"{label} {desc}"
    dp.font.size = Pt(11)
    dp.font.color.rgb = COLOR_TEXT_DARK
    dp.space_after = Pt(6)

# Right Column: Embedded Figure
if (FIG_DIR / "leaf_samples.png").exists():
    s3.shapes.add_picture(str(FIG_DIR / "leaf_samples.png"), Inches(6.7), Inches(1.6), Inches(5.8), Inches(4.8))

# Bottom note
bn3 = s3.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.7), Inches(0.5))
p_bn3 = bn3.text_frame.paragraphs[0]
p_bn3.text = "Stratified sampling ensures balanced evaluation so that minority disease classes are represented equally in the test set."
p_bn3.font.size = Pt(11)
p_bn3.font.color.rgb = COLOR_TEXT_MUTED

# ==============================================================================
# SLIDE 4: PROPOSED SOLUTION & SYSTEM ARCHITECTURE
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
apply_slide_background(s4)
add_header(s4, "GreenLens Closed-Loop Diagnostic Architecture", "System Solution")

# Top: Horizontal Pipeline Diagram
if (FIG_DIR / "architecture_pipeline.png").exists():
    s4.shapes.add_picture(str(FIG_DIR / "architecture_pipeline.png"), Inches(0.8), Inches(1.5), Inches(11.7), Inches(2.6))

# Bottom: 3 Detail Cards
detail_w = Inches(3.64)
detail_gap = Inches(0.39)
card_top4 = Inches(4.35)
card_h4 = Inches(2.45)

# Card 1: Data Augmentation
add_card(s4, Inches(0.8), card_top4, detail_w, card_h4)
tb_c1 = s4.shapes.add_textbox(Inches(0.95), card_top4 + Inches(0.15), detail_w - Inches(0.3), card_h4 - Inches(0.3))
tf_c1 = tb_c1.text_frame
tf_c1.word_wrap = True

p = tf_c1.paragraphs[0]
p.text = "1. Preprocessing & Augmentation"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(8)

b_c1 = [
    "Geometric Transforms: Random Horizontal & Vertical Flips (p=0.5).",
    "Spatial Scaling: Standardized to 224x224 RGB.",
    "Color Normalization: ImageNet channel mean and variance alignment."
]
for b in b_c1:
    bp = tf_c1.add_paragraph()
    bp.text = "- " + b
    bp.font.size = Pt(10)
    bp.font.color.rgb = COLOR_TEXT_DARK
    bp.space_after = Pt(4)

# Card 2: Feature Representation
add_card(s4, Inches(0.8) + detail_w + detail_gap, card_top4, detail_w, card_h4)
tb_c2 = s4.shapes.add_textbox(Inches(0.95) + detail_w + detail_gap, card_top4 + Inches(0.15), detail_w - Inches(0.3), card_h4 - Inches(0.3))
tf_c2 = tb_c2.text_frame
tf_c2.word_wrap = True

p = tf_c2.paragraphs[0]
p.text = "2. Deep Representation Learning"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(8)

b_c2 = [
    "Pretrained Feature Extractor: MobileNetV2 with inverted residual bottlenecks.",
    "Automatic Mixed Precision (AMP): Fast FP16/FP32 training with low memory usage.",
    "Optimization: AdamW with Cosine Annealing learning rate schedule."
]
for b in b_c2:
    bp = tf_c2.add_paragraph()
    bp.text = "- " + b
    bp.font.size = Pt(10)
    bp.font.color.rgb = COLOR_TEXT_DARK
    bp.space_after = Pt(4)

# Card 3: Decision Engine
add_card(s4, Inches(0.8) + (detail_w + detail_gap)*2, card_top4, detail_w, card_h4, bg_color=COLOR_ACCENT_BG)
tb_c3 = s4.shapes.add_textbox(Inches(0.95) + (detail_w + detail_gap)*2, card_top4 + Inches(0.15), detail_w - Inches(0.3), card_h4 - Inches(0.3))
tf_c3 = tb_c3.text_frame
tf_c3.word_wrap = True

p = tf_c3.paragraphs[0]
p.text = "3. Agronomic Decision Engine"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(8)

b_c3 = [
    "Clinical Mapping: Instant lookup from predicted class to agronomic regimen.",
    "Three-Tier Protocols: Immediate curative chemical, cultural prevention, and organic bio-control.",
    "Actionable Output: Direct confidence score and diagnostic treatment card."
]
for b in b_c3:
    bp = tf_c3.add_paragraph()
    bp.text = "- " + b
    bp.font.size = Pt(10)
    bp.font.color.rgb = COLOR_TEXT_DARK
    bp.space_after = Pt(4)

# ==============================================================================
# SLIDE 5: ALGORITHMIC MODELING & COMPLEXITY COMPARISON
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
apply_slide_background(s5)
add_header(s5, "Algorithmic Modeling: From Scratch vs. Transfer Learning", "Algorithm Design")

col_w5 = Inches(5.6)
# Left Column: Custom CNN Baseline
add_card(s5, Inches(0.8), Inches(1.6), col_w5, Inches(4.8))
tb_m1 = s5.shapes.add_textbox(Inches(1.0), Inches(1.8), col_w5 - Inches(0.4), Inches(4.4))
tf_m1 = tb_m1.text_frame
tf_m1.word_wrap = True

p = tf_m1.paragraphs[0]
p.text = "Model 1: Custom CNN (From Scratch)"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(10)

m1_desc = [
    ("Architecture:", "4-stage sequential Convolutional network."),
    ("Layer Hierarchy:", "Conv2D(32) -> Conv2D(64) -> Conv2D(128) -> Conv2D(256) with BatchNorm, ReLU, and 2x2 MaxPool."),
    ("Classifier Head:", "AdaptiveAvgPool(4x4) -> Flatten -> Dropout(0.4) -> Dense(256) -> Dropout(0.3) -> Dense(15)."),
    ("Trainable Parameters:", "~1.39 Million parameters."),
    ("Inductive Bias:", "Learned strictly from 16,511 agricultural images without external priors."),
    ("Baseline Test Accuracy:", "84.25% (Macro F1: 77.47%)."),
    ("Bottleneck:", "Prone to lower sensitivity on rare classes (<200 samples).")
]
for label, desc in m1_desc:
    mp = tf_m1.add_paragraph()
    mp.text = f"- {label} {desc}"
    mp.font.size = Pt(10.5)
    mp.font.color.rgb = COLOR_TEXT_DARK
    mp.space_after = Pt(6)

# Right Column: Transfer Learning (MobileNetV2)
add_card(s5, Inches(6.9), Inches(1.6), col_w5, Inches(4.8), bg_color=COLOR_ACCENT_BG)
tb_m2 = s5.shapes.add_textbox(Inches(7.1), Inches(1.8), col_w5 - Inches(0.4), Inches(4.4))
tf_m2 = tb_m2.text_frame
tf_m2.word_wrap = True

p = tf_m2.paragraphs[0]
p.text = "Model 2: MobileNetV2 (Transfer Learning)"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(10)

m2_desc = [
    ("Pretrained Backbone:", "ImageNet feature representation (1.4M natural images)."),
    ("Core Innovation:", "Depthwise Separable Convolutions & Inverted Residuals with linear bottlenecks."),
    ("Algorithmic Efficiency:", "Reduces computational complexity from O(Dk^2 * M * N * Df^2) to O(Dk^2 * M * Df^2 + M * N * Df^2)."),
    ("Compute Savings:", "8x to 9x fewer multiply-accumulate operations (MACs)."),
    ("Trainable Parameters:", "~2.24 Million parameters (optimized for edge devices)."),
    ("Convergence Speed:", "Reaches 98.69% in epoch 1, 99.37% in epoch 2."),
    ("Final Test Accuracy:", "99.13% across all 15 classes (Macro F1: 99.13%).")
]
for label, desc in m2_desc:
    mp = tf_m2.add_paragraph()
    mp.text = f"- {label} {desc}"
    mp.font.size = Pt(10.5)
    mp.font.color.rgb = COLOR_TEXT_DARK
    mp.space_after = Pt(6)

# Bottom note
bn5 = s5.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.7), Inches(0.5))
p_bn5 = bn5.text_frame.paragraphs[0]
p_bn5.text = "Key Algorithmic Finding: Transfer learning resolves data scarcity in minority pathology classes by leveraging generalized low-level visual priors."
p_bn5.font.size = Pt(11)
p_bn5.font.bold = True
p_bn5.font.color.rgb = COLOR_SECONDARY

# ==============================================================================
# SLIDE 6: BENCHMARK EVALUATION & INFERENCE DEMO
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
apply_slide_background(s6)
add_header(s6, "Experimental Evaluation & Clinical Diagnostic Demo", "Results & Inference")

# Left Column: Metrics Table & Training Curves
left_w6 = Inches(5.6)

# Metrics Summary Card
add_card(s6, Inches(0.8), Inches(1.5), left_w6, Inches(1.8))
tb_met = s6.shapes.add_textbox(Inches(0.95), Inches(1.55), left_w6 - Inches(0.3), Inches(1.7))
tf_met = tb_met.text_frame
tf_met.word_wrap = True

p = tf_met.paragraphs[0]
p.text = "Unseen Test Set Benchmark (2,064 Samples)"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(4)

metrics_lines = [
    "Overall Test Accuracy:    Custom CNN: 84.25%  |  MobileNetV2: 99.13%",
    "Macro-Averaged Precision: Custom CNN: 87.35%  |  MobileNetV2: 99.12%",
    "Macro-Averaged Recall:    Custom CNN: 76.19%  |  MobileNetV2: 99.16%",
    "Macro-Averaged F1-Score:  Custom CNN: 77.47%  |  MobileNetV2: 99.13%"
]
for ml in metrics_lines:
    mlp = tf_met.add_paragraph()
    mlp.text = ml
    mlp.font.size = Pt(10)
    mlp.font.bold = "99.13%" in ml
    mlp.font.color.rgb = COLOR_PRIMARY if "99.13%" in ml else COLOR_TEXT_DARK

# Embedded Curves Figure
if (FIG_DIR / "training_curves.png").exists():
    s6.shapes.add_picture(str(FIG_DIR / "training_curves.png"), Inches(0.8), Inches(3.45), left_w6, Inches(2.95))

# Right Column: Confusion Matrix & Inference Card
right_w6 = Inches(5.8)
if (FIG_DIR / "confusion_matrix.png").exists():
    s6.shapes.add_picture(str(FIG_DIR / "confusion_matrix.png"), Inches(6.7), Inches(1.5), right_w6, Inches(3.3))

if (FIG_DIR / "test_inference_card.png").exists():
    s6.shapes.add_picture(str(FIG_DIR / "test_inference_card.png"), Inches(6.7), Inches(4.9), right_w6, Inches(1.65))

# ==============================================================================
# SLIDE 7: CONCLUSION, ALGORITHMIC TAKEAWAYS & THANK YOU
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
apply_slide_background(s7)
add_header(s7, "Conclusion, Algorithmic Takeaways & Next Steps", "Summary & Close")

# 3 Horizontal Cards
c_w7 = Inches(3.64)
c_gap7 = Inches(0.39)
c_top7 = Inches(1.6)
c_h7 = Inches(3.6)

# Card 1: Key Achievements
add_card(s7, Inches(0.8), c_top7, c_w7, c_h7)
tb_con1 = s7.shapes.add_textbox(Inches(0.95), c_top7 + Inches(0.15), c_w7 - Inches(0.3), c_h7 - Inches(0.3))
tf_con1 = tb_con1.text_frame
tf_con1.word_wrap = True

p = tf_con1.paragraphs[0]
p.text = "Key Project Achievements"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(10)

achievements = [
    "Developed GreenLens, an end-to-end plant disease diagnosis pipeline for 15 foliar conditions.",
    "Achieved 99.13% test accuracy and 99.13% macro F1-score across 2,064 unseen test images.",
    "Seamlessly integrated automated diagnostic decision support offering tailored treatment protocols."
]
for a in achievements:
    ap = tf_con1.add_paragraph()
    ap.text = "- " + a
    ap.font.size = Pt(10.5)
    ap.font.color.rgb = COLOR_TEXT_DARK
    ap.space_after = Pt(6)

# Card 2: Algorithmic Takeaways
add_card(s7, Inches(0.8) + c_w7 + c_gap7, c_top7, c_w7, c_h7)
tb_con2 = s7.shapes.add_textbox(Inches(0.95) + c_w7 + c_gap7, c_top7 + Inches(0.15), c_w7 - Inches(0.3), c_h7 - Inches(0.3))
tf_con2 = tb_con2.text_frame
tf_con2.word_wrap = True

p = tf_con2.paragraphs[0]
p.text = "Algorithmic Insights"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(10)

insights = [
    "Complexity Reduction: Depthwise separable convolution achieves 8-9x FLOP savings, proving ideal for mobile deployment.",
    "Inductive Bias Transfer: Pretrained representations eliminate class imbalance penalties on minority pathology classes.",
    "Convergence Velocity: Reached near-optimal validation performance in just 2 epochs of fine-tuning."
]
for ins in insights:
    ip = tf_con2.add_paragraph()
    ip.text = "- " + ins
    ip.font.size = Pt(10.5)
    ip.font.color.rgb = COLOR_TEXT_DARK
    ip.space_after = Pt(6)

# Card 3: Future Roadmap
add_card(s7, Inches(0.8) + (c_w7 + c_gap7)*2, c_top7, c_w7, c_h7)
tb_con3 = s7.shapes.add_textbox(Inches(0.95) + (c_w7 + c_gap7)*2, c_top7 + Inches(0.15), c_w7 - Inches(0.3), c_h7 - Inches(0.3))
tf_con3 = tb_con3.text_frame
tf_con3.word_wrap = True

p = tf_con3.paragraphs[0]
p.text = "Future Roadmap"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.space_after = Pt(10)

roadmap = [
    "Edge Mobile App: Package model into ONNX / TFLite for real-time offline field inference.",
    "Multi-Leaf Segmentation: Integrate YOLO/Mask R-CNN to localize multiple diseased leaves per plant.",
    "Continuous Learning: Implement active learning pipeline from farmer feedback and verified field samples."
]
for rm in roadmap:
    rp = tf_con3.add_paragraph()
    rp.text = "- " + rm
    rp.font.size = Pt(10.5)
    rp.font.color.rgb = COLOR_TEXT_DARK
    rp.space_after = Pt(6)

# Bottom Thank You Banner
ty_card = add_card(s7, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.4), bg_color=COLOR_PRIMARY, border_color=COLOR_SECONDARY)
tb_ty = s7.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.3), Inches(1.3))
tf_ty = tb_ty.text_frame
tf_ty.word_wrap = True

p_ty1 = tf_ty.paragraphs[0]
p_ty1.text = "Thank You! Questions & Discussion"
p_ty1.font.size = Pt(22)
p_ty1.font.bold = True
p_ty1.font.color.rgb = COLOR_WHITE
p_ty1.alignment = PP_ALIGN.CENTER
p_ty1.space_after = Pt(4)

p_ty2 = tf_ty.add_paragraph()
p_ty2.text = "GreenLens  |  Team TerraGreen  |  Presenter: Abdelaziz Ahmed Elbanna  |  Supervisor: Dr. Fatma Talaat"
p_ty2.font.size = Pt(12)
p_ty2.font.color.rgb = RGBColor(216, 243, 220)
p_ty2.alignment = PP_ALIGN.CENTER

# Save PowerPoint
prs.save(PPTX_PATH)
print(f"PowerPoint Presentation successfully saved: {PPTX_PATH}")

# Convert to PDF using LibreOffice
print("Converting presentation to PDF via headless LibreOffice...")
cmd = [
    "libreoffice",
    "--headless",
    "--convert-to", "pdf",
    "--outdir", str(OUTPUT_DIR),
    str(PPTX_PATH)
]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print(f"PDF Presentation successfully exported: {PDF_PATH}")
else:
    print("LibreOffice conversion output:", result.stdout)
    print("LibreOffice conversion error:", result.stderr)

print("Build complete!")
