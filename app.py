import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="CardioScan | Heart Disease AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

@st.cache_resource
def load_files():
    model = joblib.load("KNN_heart.pkl")
    scaler = joblib.load("scaler.pkl")
    expected_columns = joblib.load("columns.pkl")
    return model, scaler, expected_columns

model, scaler, expected_columns = load_files()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --navy: #07111f;
    --pink: #ff416c;
    --red: #ff1744;
    --cyan: #35d8d0;
    --white: #f7faff;
    --muted: #9eabc0;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #050810 !important;
    color: #f7faff !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #070b12 !important;
}

[data-testid="stHeader"] { background: transparent !important; }
.block-container {
    max-width: 1250px !important;
    padding: 0 1.2rem 3rem !important;
}
#MainMenu, footer { visibility: hidden; }

.navbar {
    height: 64px;
    margin: 0 -1.2rem;
    padding: 0 4.5%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #070b12;
    border-bottom: 1px solid rgba(255,255,255,.14);
    color: white;
}
.brand {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.08rem;
}
.brand span { color: #ff416c; }
.nav-right {
    display: flex;
    gap: 30px;
    font-size: .78rem;
    font-weight: 600;
    letter-spacing: 1px;
    color: #c9d2df;
}
.creator {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-left: 18px;
    color: #f7faff;
    font-size: .76rem;
    font-weight: 700;
    letter-spacing: .3px;
    white-space: nowrap;
}
.creator-name { color: #ff6682; }
.creator-icon {
    width: 28px;
    height: 28px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: rgba(255,65,108,.12);
    border: 1px solid rgba(255,65,108,.35);
}

.hero {
    position: relative;
    min-height: 555px;
    margin: 0 -1.2rem;
    overflow: hidden;
    background:
        radial-gradient(circle at 51% 48%, rgba(255,23,68,.25), transparent 18%),
        radial-gradient(circle at 75% 30%, rgba(53,216,208,.10), transparent 28%),
        linear-gradient(115deg, #03070d 0%, #091322 55%, #05080e 100%);
    display: flex;
    align-items: center;
    padding: 55px 8%;
}
.hero-grid {
    position: relative;
    z-index: 3;
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    gap: 30px;
}
.hero-copy { max-width: 620px; }
.badge {
    display: inline-block;
    padding: 8px 14px;
    border: 1px solid rgba(255,65,108,.45);
    border-radius: 999px;
    color: #ff8da6;
    background: rgba(255,65,108,.08);
    font-size: .72rem;
    font-weight: 700;
    letter-spacing: 1.7px;
    margin-bottom: 20px;
}
.hero h1 {
    color: white !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(2.6rem, 5vw, 5rem) !important;
    line-height: .98 !important;
    margin: 0 0 20px !important;
    font-weight: 700 !important;
}
.hero h1 span { color: #ff416c; }
.hero-text {
    color: #aebbd0;
    max-width: 560px;
    line-height: 1.75;
    font-size: 1rem;
}
.hero-visual {
    min-height: 390px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}
.heart-orb {
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,23,68,.20), rgba(255,23,68,.02) 65%, transparent 70%);
    box-shadow: 0 0 90px rgba(255,23,68,.24);
    display: flex;
    align-items: center;
    justify-content: center;
    animation: pulse 2.2s infinite;
}
.heart {
    font-size: 8rem;
    filter: drop-shadow(0 0 25px rgba(255,23,68,.75));
}
@keyframes pulse {
    0%,100% { transform: scale(1); }
    50% { transform: scale(1.045); }
}
.ecg-line {
    position: absolute;
    width: 120%;
    height: 100px;
    left: -10%;
    top: 50%;
    transform: translateY(-50%);
    opacity: .75;
    pointer-events: none;
}
.ecg-line svg { width: 100%; height: 100%; }
.ecg-path {
    fill: none;
    stroke: #ff416c;
    stroke-width: 3;
    filter: drop-shadow(0 0 8px #ff1744);
    stroke-dasharray: 900;
    stroke-dashoffset: 900;
    animation: ecg 3.2s linear infinite;
}
@keyframes ecg { to { stroke-dashoffset: 0; } }
.hero-stat {
    position: absolute;
    right: 2%;
    bottom: 4%;
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.12);
    backdrop-filter: blur(12px);
    border-radius: 14px;
    padding: 14px 18px;
    color: white;
    font-size: .78rem;
}
.hero-stat strong {
    display: block;
    font-size: 1.15rem;
    color: #55ddd5;
}

.section-heading {
    text-align: center;
    padding: 65px 0 35px;
}
.section-kicker {
    color: #ff416c;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.section-heading h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #ffffff !important;
    font-size: 2.2rem !important;
    margin: 8px 0 !important;
}
.section-heading p { color: #9eabc0; margin: 0; }

.data-shell {
    background:
        radial-gradient(circle at 10% 0%, rgba(255,65,108,.10), transparent 28%),
        radial-gradient(circle at 90% 100%, rgba(53,216,208,.06), transparent 30%),
        linear-gradient(135deg, #0b111c, #0e1725) !important;
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 26px;
    padding: 35px 38px 40px;
    box-shadow: 0 22px 60px rgba(0,0,0,.35);
}
.data-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 25px;
}
.data-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
}
.data-number {
    color: #7f8da1;
    font-size: .75rem;
    font-weight: 700;
    letter-spacing: 1.5px;
}

[data-testid="stSlider"] label,
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    color: #c5cfdd !important;
    font-size: .78rem !important;
    font-weight: 700 !important;
}
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #111a29 !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 10px !important;
    color: #f7faff !important;
}
[data-testid="stSelectbox"] div[data-baseweb="select"] span {
    color: #f7faff !important;
}
[data-testid="stNumberInput"] input {
    background: #111a29 !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 10px !important;
    color: #f7faff !important;
}
[data-testid="stNumberInput"] button {
    background: #172235 !important;
    border-color: rgba(255,255,255,.10) !important;
    color: #dbe5f2 !important;
}
[data-baseweb="popover"] {
    background: #0d1624 !important;
}
[data-baseweb="menu"] {
    background: #0d1624 !important;
}
[data-baseweb="option"] {
    color: #f7faff !important;
}
[data-baseweb="option"]:hover {
    background: #182437 !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] {
    color: #ff416c !important;
}
[data-testid="stSlider"] div[role="slider"] {
    background: #ff416c !important;
}

/* Dark Streamlit controls */
[data-testid="stWidgetLabel"] p,
[data-testid="stMarkdownContainer"] p {
    color: inherit;
}

div.stButton {
    display: flex;
    justify-content: center;
    margin-top: 25px;
}
div.stButton > button {
    min-width: 220px;
    border: 0 !important;
    border-radius: 12px !important;
    padding: 13px 28px !important;
    background: linear-gradient(135deg, #ff416c, #ff1744) !important;
    color: white !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: .95rem !important;
    font-weight: 700 !important;
    box-shadow: 0 12px 28px rgba(255,23,68,.25) !important;
}
div.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 17px 35px rgba(255,23,68,.34) !important;
}

.result-wrap {
    margin-top: 60px;
    border-radius: 26px;
    padding: 42px;
    text-align: center;
    background: #07111f;
    border: 1px solid rgba(255,255,255,.10);
    box-shadow: 0 25px 70px rgba(7,17,31,.25);
    color: white;
}
.result-kicker {
    color: #8fa2bb;
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: 2px;
}
.result-heart {
    font-size: 4.3rem;
    margin: 10px 0;
    filter: drop-shadow(0 0 20px rgba(255,23,68,.45));
}
.result-low, .result-high {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.1rem;
    font-weight: 700;
}
.result-low { color: #48dfad; }
.result-high { color: #ff6682; }
.result-desc {
    color: #9eabc0;
    max-width: 650px;
    margin: 12px auto 0;
    line-height: 1.65;
}
.result-pill {
    display: inline-block;
    margin-top: 22px;
    padding: 8px 15px;
    border-radius: 999px;
    background: rgba(255,255,255,.07);
    color: #c8d3e2;
    font-size: .73rem;
    font-weight: 700;
    letter-spacing: 1px;
}

.advice-wrap {
    margin-top: 24px;
    border-radius: 24px;
    padding: 30px;
    background:
        radial-gradient(circle at 0% 0%, rgba(255,65,108,.09), transparent 28%),
        linear-gradient(135deg, #0b111c, #0f1927) !important;
    border: 1px solid rgba(255,255,255,.10);
    box-shadow: 0 18px 50px rgba(0,0,0,.30);
}
.advice-title {
    text-align: center;
    color: #ffffff;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    margin-bottom: 6px;
}
.advice-subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: .86rem;
    margin-bottom: 22px;
}
.advice-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
}
.advice-card {
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 18px;
    padding: 22px;
}
.advice-icon {
    font-size: 1.8rem;
    margin-bottom: 8px;
}
.advice-card-title {
    color: #ffffff;
    font-family: 'Space Grotesk', sans-serif;
    margin: 0 0 12px;
    font-size: 1.08rem;
    font-weight: 700;
}
.advice-item {
    color: #aebbd0;
    line-height: 1.65;
    font-size: .86rem;
    margin: 8px 0;
}
.advice-note {
    margin-top: 18px;
    padding: 13px 16px;
    border-radius: 12px;
    background: rgba(255,65,108,.07);
    border: 1px solid rgba(255,65,108,.20);
    color: #c9d3df;
    font-size: .78rem;
    line-height: 1.55;
}

@media (max-width: 800px) {
    .advice-grid { grid-template-columns: 1fr; }
}

@media (max-width: 800px) {
    .hero { min-height: auto; padding: 55px 7%; }
    .hero-grid { grid-template-columns: 1fr; }
    .hero-visual { min-height: 280px; }
    .hero h1 { font-size: 3rem !important; }
    .heart { font-size: 6rem; }
    .heart-orb { width: 210px; height: 210px; }
    .data-shell { padding: 25px 18px 30px; }
    .navbar { flex-wrap: wrap; gap: 8px; }
    .nav-right { display: none; }
    .creator {
        margin-left: auto;
        font-size: .68rem;
    }
    .creator-icon {
        width: 24px;
        height: 24px;
        font-size: .75rem;
    }
    .result-wrap { padding: 30px 18px; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="navbar">
<div class="brand">❤️ Cardio<span>Scan</span> AI</div>
<div class="nav-right">
<span>HEART RISK</span>
<span>AI ANALYSIS</span>
<span>ABOUT</span>
</div>
<div class="creator"><span class="creator-icon">👤</span><span>Created by <span class="creator-name">Gautam Karna</span></span></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<section class="hero">
<div class="hero-grid">
<div class="hero-copy">
<div class="badge">AI-POWERED HEART RISK ANALYSIS</div>
<h1>Examining<br><span>Your Heart.</span></h1>
<div class="hero-text">
A machine-learning powered cardiovascular risk assessment
designed to analyze key heart-health indicators and provide
an instant prediction from your selected patient data.
</div>
</div>
<div class="hero-visual">
<div class="ecg-line">
<svg viewBox="0 0 900 120" preserveAspectRatio="none">
<path class="ecg-path" d="M0 62 L90 62 L115 62 L132 58 L145 62 L162 62 L178 62 L195 15 L210 105 L225 62 L300 62 L325 62 L340 54 L352 62 L370 62 L395 62 L420 62 L442 25 L455 96 L470 62 L545 62 L570 62 L585 54 L598 62 L620 62 L645 62 L670 62 L690 18 L704 102 L718 62 L800 62 L825 62 L845 54 L860 62 L900 62"/>
</svg>
</div>
<div class="heart-orb"><div class="heart">❤️</div></div>
<div class="hero-stat"><strong>11</strong>heart-health indicators</div>
</div>
</div>
</section>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-heading">
<div class="section-kicker">01 — Patient assessment</div>
<h2>Heart's Data</h2>
<p>Enter the patient's cardiovascular measurements below.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="data-shell">
<div class="data-top">
<div class="data-title">Patient Information</div>
<div class="data-number">11 PARAMETERS</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    age = st.slider("Age", 18, 100, 40)
    cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)

with c2:
    sex = st.selectbox("Sex", ["M", "F"])
    resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 120)

with c3:
    chest_pain = st.selectbox("Chest Pain Type", ["ATA", "NAP", "TA", "ASY"])
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1])

with c4:
    max_hr = st.slider("Maximum Heart Rate", 60, 220, 150)
    exercise_angina = st.selectbox("Exercise-Induced Angina", ["Y", "N"])

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

c5, c6, c7 = st.columns(3)

with c5:
    resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])

with c6:
    oldpeak = st.slider("Oldpeak (ST Depression)", 0.0, 6.0, 1.0, step=0.1)

with c7:
    st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

st.markdown("</div>", unsafe_allow_html=True)

predict_clicked = st.button("❤️  ANALYZE MY HEART")

if predict_clicked:
    raw_input = {
        "Age": age,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": fasting_bs,
        "MaxHR": max_hr,
        "Oldpeak": oldpeak,
        "Sex_" + sex: 1,
        "ChestPainType_" + chest_pain: 1,
        "RestingECG_" + resting_ecg: 1,
        "ExerciseAngina_" + exercise_angina: 1,
        "ST_Slope_" + st_slope: 1,
    }

    input_df = pd.DataFrame([raw_input])

    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[expected_columns]
    scaled_input = scaler.transform(input_df)
    prediction = model.predict(scaled_input)[0]

    probability_text = ""
    if hasattr(model, "predict_proba"):
        try:
            probabilities = model.predict_proba(scaled_input)[0]
            risk_probability = float(probabilities[1]) * 100
            probability_text = (
                f'<div class="result-pill">MODEL ESTIMATE • '
                f'{risk_probability:.1f}% POSITIVE CLASS PROBABILITY</div>'
            )
        except Exception:
            probability_text = ""

    if prediction == 1:
        result_html = f"""
<div class="result-wrap">
<div class="result-kicker">ANALYSIS COMPLETE</div>
<div class="result-heart">❤️</div>
<div class="result-high">Higher Risk Detected</div>
<div class="result-desc">
The machine-learning model classified the submitted patient data
into the heart-disease positive class. This is a model prediction,
not a medical diagnosis.
</div>
{probability_text}
</div>
"""
    else:
        result_html = f"""
<div class="result-wrap">
<div class="result-kicker">ANALYSIS COMPLETE</div>
<div class="result-heart">💚</div>
<div class="result-low">Lower Risk Detected</div>
<div class="result-desc">
The machine-learning model classified the submitted patient data
into the heart-disease negative class. This is a model prediction,
not a medical diagnosis.
</div>
{probability_text}
</div>
"""

    st.markdown(result_html, unsafe_allow_html=True)

    # General heart-health guidance shown after the model prediction.
    # Educational information only; not individualized medical advice.
    st.markdown("""
<div class="advice-wrap">
  <div class="advice-title">❤️ What to do next</div>
  <div class="advice-subtitle">General heart-health habits for everyday wellbeing.</div>
</div>
""", unsafe_allow_html=True)

    adv1, adv2 = st.columns(2)

    with adv1:
        st.markdown("""
<div class="advice-card">
  <div class="advice-icon">🥗</div>
  <div class="advice-card-title">Eat for heart health</div>
  <div class="advice-item">✓ Choose plenty of vegetables and fruits.</div>
  <div class="advice-item">✓ Prefer whole grains over refined grains.</div>
  <div class="advice-item">✓ Include healthy proteins such as beans, lentils, nuts, fish, and lean options.</div>
  <div class="advice-item">✓ Choose unsaturated fats and limit foods high in saturated fat.</div>
  <div class="advice-item">✓ Reduce highly processed foods, added sugar, and excess sodium.</div>
</div>
""", unsafe_allow_html=True)

    with adv2:
        st.markdown("""
<div class="advice-card">
  <div class="advice-icon">😴</div>
  <div class="advice-card-title">Build a healthy sleep routine</div>
  <div class="advice-item">✓ Adults should generally aim for 7–9 hours of sleep each night.</div>
  <div class="advice-item">✓ Keep a consistent bedtime and wake-up time.</div>
  <div class="advice-item">✓ Dim screens and lights before bed.</div>
  <div class="advice-item">✓ Create a relaxing wind-down routine.</div>
  <div class="advice-item">✓ Keep the phone and other distractions away while sleeping.</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="advice-note"><strong>Important:</strong> This prediction is for educational use and is not a medical diagnosis. A higher-risk result should not be treated as confirmation of heart disease, and a lower-risk result does not rule it out. If this is based on real patient data, discuss the result with a qualified healthcare professional.</div>
""", unsafe_allow_html=True)
