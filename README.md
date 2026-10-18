# GreenLens

### Intelligent Plant Pathology Diagnosis & Actionable Decision Support System

---

## Academic Information

- **Course:** Introduction to Algorithms (Year 3, Semester 1)
- **Academic Supervisor:** Dr. Fatma Talaat
- **Team Name:** TerraGreen
- **Student / Author:** Abdelaziz Ahmed Elbanna
- **Institution:** Faculty of Computer and Information Sciences

---

## Executive Summary & Motivation

Plant diseases pose a severe threat to global food security, causing estimated annual crop yield losses between 20% and 40% across agricultural regions. Smallholder and commercial farmers frequently struggle with timely in-field diagnosis due to:

1. **Scarcity of Field Agronomists:** Rural areas often lack accessible agricultural pathology experts.
2. **Symptom Visual Ambiguity:** Early-stage fungal, bacterial, and viral infections exhibit subtle, overlapping visual patterns (e.g., chlorosis, concentric necrotic lesions, water-soaked margins).
3. **Misdiagnosis Consequences:** Applying incorrect agrochemicals wastes financial resources, exacerbates soil toxicity, and fosters pathogen resistance.

**GreenLens** addresses these challenges by deploying a high-precision, low-latency deep learning vision system coupled with an automated agronomic treatment recommendation engine. The system delivers real-time pathogen classification and actionable cultural, biological, and chemical disease management protocols tailored for sustainable agriculture.

---

## Repository Architecture

```text
greenlens/
│
├── .gitignore                                 # Git exclusion rules (dataset, virtual environments, caches)
├── requirements.txt                           # Project dependencies
├── README.md                                  # Comprehensive English technical documentation
│
├── notebooks/
│   ├── 01_data_understanding_and_exploration.ipynb   # Exploratory data analysis, class distributions, pixel statistics
│   └── 02_preprocessing_and_modeling.ipynb           # Data pipeline, CNN vs MobileNetV2, benchmarking & recommendation engine
│
├── models/
│   └── greenlens_mobilenetv2_best.pth                # Serialized PyTorch state dict of best model (8.8 MB)
│
├── reports/
│   └── presentation/
│       ├── greenlens_presentation.pptx        # Academic presentation (PowerPoint format, 16:9 widescreen)
│       ├── greenlens_presentation.pdf         # Academic presentation (PDF format, publication-ready)
│       └── figures/                           # High-resolution presentation figures and benchmark visualizations
│           ├── title_cover.png                # Presentation title visual graphic
│           ├── leaf_samples.png               # Grid of healthy and diseased plant leaf specimens
│           ├── architecture_pipeline.png      # End-to-end algorithmic flow diagram
│           ├── training_curves.png            # Convergence loss and accuracy curves
│           ├── confusion_matrix.png           # Normalized 15-class evaluation confusion matrix
│           └── test_inference_card.png        # Production-grade inference and treatment advice card
│
└── scripts/
    ├── build_presentation.py                  # Automated PowerPoint builder and PDF exporter script
    └── export_presentation_figures.py         # Figure extraction script for reproducible presentation graphics
```

---

## Dataset & Taxonomic Scope

The project leverages a curated subset of the PlantVillage benchmark dataset, comprising **20,638 high-resolution leaf images** across **15 distinct pathological classes** representing three vital staple crops:

| Index | Crop | Pathological Condition | Pathogen Type | Sample Count |
| :---: | :--- | :--- | :--- | :---: |
| 0 | Bell Pepper | Bacterial Spot (*Xanthomonas campestris*) | Bacterial | 997 |
| 1 | Bell Pepper | Healthy (*Capsicum annuum*) | None (Healthy) | 1,478 |
| 2 | Potato | Early Blight (*Alternaria solani*) | Fungal | 1,000 |
| 3 | Potato | Late Blight (*Phytophthora infestans*) | Oomycete / Fungal | 1,000 |
| 4 | Potato | Healthy (*Solanum tuberosum*) | None (Healthy) | 152 |
| 5 | Tomato | Bacterial Spot (*Xanthomonas vesicatoria*) | Bacterial | 2,127 |
| 6 | Tomato | Early Blight (*Alternaria solani*) | Fungal | 1,000 |
| 7 | Tomato | Late Blight (*Phytophthora infestans*) | Oomycete / Fungal | 1,909 |
| 8 | Tomato | Leaf Mold (*Passalora fulva*) | Fungal | 952 |
| 9 | Tomato | Septoria Leaf Spot (*Septoria lycopersici*) | Fungal | 1,771 |
| 10 | Tomato | Two-Spotted Spider Mite (*Tetranychus urticae*) | Pest / Acari | 1,676 |
| 11 | Tomato | Target Spot (*Corynespora cassiicola*) | Fungal | 1,404 |
| 12 | Tomato | Yellow Leaf Curl Virus (*TYLCV*) | Viral (Begomovirus) | 3,209 |
| 13 | Tomato | Tomato Mosaic Virus (*ToMV*) | Viral (Tobamovirus) | 373 |
| 14 | Tomato | Healthy (*Solanum lycopersicum*) | None (Healthy) | 1,590 |
| **Total** | | | | **20,638** |

### Data Partitioning Strategy

To guarantee zero data contamination across experimental stages, a stratified partition was applied:
- **Training Set (80%):** 16,511 images used for weight optimization with dynamic data augmentation.
- **Validation Set (10%):** 2,064 images used for hyperparameter tuning and model checkpointing.
- **Test Set (10%):** 2,064 unseen images reserved exclusively for final generalization assessment.

---

## Methodology & Algorithmic Architecture

### 1. Data Augmentation & Normalization Pipeline
To prevent overfitting on laboratory backgrounds and enhance real-world invariance, the input pipeline applies:
- Random horizontal and vertical reflections ($p = 0.5$).
- Affine random rotations ($\pm 20^\circ$).
- Color jitter (brightness, contrast, and saturation perturbed by 0.15).
- Resizing to standard $224 \times 224 \times 3$ resolution.
- Channel-wise standardization using ImageNet distribution parameters ($\mu = [0.485, 0.456, 0.406]$, $\sigma = [0.229, 0.224, 0.225]$).

### 2. Deep Learning Models Evaluated
- **Baseline Custom CNN:** A scratch architecture comprising three sequential convolutional blocks (Conv2D $\rightarrow$ BatchNorm $\rightarrow$ ReLU $\rightarrow$ MaxPool2D) followed by a dense classification head with dropout ($p = 0.5$).
- **MobileNetV2 (Optimal Backbone):** Employs inverted residual blocks with linear bottlenecks and depthwise separable convolutions. The depthwise separable design factorizes standard convolution into:
  $$\text{Computational Cost Ratio} = \frac{D_K \cdot D_K \cdot M + M \cdot N}{D_K \cdot D_K \cdot M \cdot N} = \frac{1}{N} + \frac{1}{D_K^2}$$
  This architecture achieves an $8\times$ reduction in computational multiply-accumulate (MAC) operations compared to standard convolutions while preserving fine spatial feature representations.

---

## Experimental Evaluation & Results

Both architectures were benchmarked under identical test conditions on the **2,064 unseen test images**:

| Evaluation Metric | Custom CNN Baseline | MobileNetV2 (GreenLens) | Relative Improvement |
| :--- | :---: | :---: | :---: |
| **Test Accuracy** | 84.25% | **99.13%** | +14.88% |
| **Macro Precision** | 87.35% | **99.12%** | +11.77% |
| **Macro Recall** | 76.19% | **99.16%** | +22.97% |
| **Macro F1-Score** | 77.47% | **99.13%** | +21.66% |
| **Best Validation Accuracy** | 83.87% | **99.37%** | +15.50% |
| **Total Parameters** | ~1.39 Million | **~2.24 Million** | Edge-deployable |
| **Checkpoint Storage Size** | 5.6 MB | **8.8 MB** | Compact mobile footprint |
| **Inference Latency (GPU)** | ~5 ms | **~12 ms** | Real-time capable |

MobileNetV2 achieved near-perfect classification across all 15 classes, effectively resolving difficult visual edge cases such as differentiating between *Early Blight* and *Late Blight* in both Potato and Tomato crops.

---

## Automated Agronomic Decision Support System

GreenLens extends beyond basic categorization by linking model predictions to a structured agronomic advisory protocol:

1. **Prediction Confidence Filtering:** Rejects ambiguous inputs falling below a defined certainty threshold ($T < 0.65$).
2. **Top-3 Differential Diagnosis:** Provides alternative potential conditions and probabilities to assist field agronomists.
3. **Multi-Tiered Treatment Recommendation:**
   - **Organic Management:** Non-toxic biological interventions (e.g., *Bacillus subtilis*, copper octanoate, neem extracts).
   - **Targeted Chemical Control:** Active ingredient specifications (e.g., Chlorothalonil, Mancozeb) with rotation strategies to mitigate fungicide resistance.
   - **Preventive Cultural Practices:** Environmental management including drip irrigation, canopy thinning, sanitized tools, and multi-year crop rotation schedules.

---

## Academic Presentation Deliverables

The project includes a 7-slide academic presentation matching the GreenLens visual identity:

- **PowerPoint Presentation:** [greenlens_presentation.pptx](file:///home/ae/ME/study/College/3rd-Year/sem1/Intro-to-Algorithms/projects/greenlens/reports/presentation/greenlens_presentation.pptx)
- **PDF Document:** [greenlens_presentation.pdf](file:///home/ae/ME/study/College/3rd-Year/sem1/Intro-to-Algorithms/projects/greenlens/reports/presentation/greenlens_presentation.pdf)
- **High-Resolution Figures:** [reports/presentation/figures/](file:///home/ae/ME/study/College/3rd-Year/sem1/Intro-to-Algorithms/projects/greenlens/reports/presentation/figures/)

### Slide Outline:
1. **Title & Project Identity:** Project title, author, team name, supervisor, and course metadata.
2. **Agricultural Pathology Challenge:** Socio-economic impact, global yield losses, and computational opportunities.
3. **Dataset & Preprocessing Pipeline:** Class taxonomy, distribution analysis, and data hygiene.
4. **Methodology & Architectural Pipeline:** Inverted residual convolutions, transfer learning, and system flow diagram.
5. **Experimental Results & Evaluation:** Loss/accuracy convergence curves, confusion matrix, and macro metrics.
6. **Clinical Inference & Actionable Advice:** Unseen sample classification demonstration with structured agronomic treatment cards.
7. **Summary & Strategic Impact:** Performance synthesis, edge feasibility, and academic acknowledgements.

---

## Installation & Reproduction Guide

### Prerequisites
- Python 3.10+
- Conda or virtualenv package manager
- Optional: CUDA-compatible GPU for accelerated training and inference

### 1. Clone the Repository
```bash
git clone git@github.com:AbdelazizElbanna/greenlens.git
cd greenlens
```

### 2. Environment Setup
```bash
# Option A: Conda
conda create -n greenlens python=3.10 -y
conda activate greenlens
pip install -r requirements.txt

# Option B: Standard Virtual Environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Running the Jupyter Notebooks
Launch the interactive environment:
```bash
jupyter lab
```
Execute the notebooks in sequence:
- `notebooks/01_data_understanding_and_exploration.ipynb`
- `notebooks/02_preprocessing_and_modeling.ipynb`

### 4. Rebuilding the Presentation
To regenerate the PowerPoint slides and export a matching PDF:
```bash
python scripts/export_presentation_figures.py
python scripts/build_presentation.py
```

---

## License

This project is developed for educational and academic research purposes as part of the *Introduction to Algorithms* curriculum.