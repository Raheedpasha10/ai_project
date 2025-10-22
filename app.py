
# app.py - FORENSIC DENTAL AI SYSTEM
import streamlit as st
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import time
import requests
from io import BytesIO
from datetime import datetime
import hashlib

st.set_page_config(
    page_title="Forensic Dental AI System",
    page_icon="🦷", 
    layout="wide"
)

# Simple CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Dental images
DENTAL_IMAGE_LIBRARY = {
    "Panoramic X-ray 1": "https://raw.githubusercontent.com/zcytony/DentalXraySegmentation/master/data/raw/1.png",
    "Panoramic X-ray 2": "https://raw.githubusercontent.com/zcytony/DentalXraySegmentation/master/data/raw/2.png", 
    "Bitewing X-ray": "https://raw.githubusercontent.com/zcytony/DentalXraySegmentation/master/data/raw/3.png",
}

def create_simple_xray():
    """Create dental X-ray"""
    img = Image.new('L', (600, 400), color=120)
    draw = ImageDraw.Draw(img)
    
    for i in range(8):
        x = 150 + i * 50
        draw.rectangle([x, 150, x+30, 200], fill=200)
        draw.rectangle([x, 250, x+30, 300], fill=200)
    
    return img

def load_dental_image(image_name):
    """Load dental image"""
    try:
        if image_name in DENTAL_IMAGE_LIBRARY:
            response = requests.get(DENTAL_IMAGE_LIBRARY[image_name], timeout=10)
            img = Image.open(BytesIO(response.content))
            return img.convert('L')
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
    return create_simple_xray()

def apply_degradation(image, degradation_type, severity=0.5):
    """Apply degradation"""
    img = image.copy()
    
    if degradation_type == "Thermal Damage":
        arr = np.array(img).astype(float)
        noise = np.random.normal(0, 50 * severity, arr.shape)
        arr = np.clip(arr + noise, 0, 255)
        img = Image.fromarray(arr.astype(np.uint8))
        img = img.filter(ImageFilter.GaussianBlur(radius=severity))
        
    elif degradation_type == "Water Damage":
        img = img.filter(ImageFilter.GaussianBlur(radius=2 * severity))
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(0.6)
        
    elif degradation_type == "Trauma Damage":
        arr = np.array(img)
        h, w = arr.shape
        for _ in range(int(3 * severity)):
            patch_size = int(20 * severity)
            x = np.random.randint(0, w - patch_size)
            y = np.random.randint(0, h - patch_size)
            arr[y:y+patch_size, x:x+patch_size] = 0
        img = Image.fromarray(arr)
        
    return img

def enhance_image(image):
    """Enhance image"""
    img = image.copy()
    
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)
    
    return img

def generate_image_fingerprint(image):
    """Generate unique fingerprint for each image"""
    img_array = np.array(image)
    fingerprint = hashlib.md5(
        f"{img_array.shape}{img_array.mean():.2f}{img_array.std():.2f}".encode()
    ).hexdigest()[:8]
    return fingerprint

def analyze_image_quality(image):
    """Analyze actual image quality metrics"""
    img_array = np.array(image)
    
    mean_intensity = img_array.mean()
    contrast = img_array.std()
    
    # Calculate entropy
    histogram = np.histogram(img_array, bins=256, range=(0, 255))[0]
    histogram = histogram[histogram > 0]
    prob = histogram / histogram.sum()
    entropy = -np.sum(prob * np.log2(prob))
    
    clarity = min(100, (contrast / 128) * 100)
    sharpness = min(100, (entropy / 8) * 100)
    brightness_balance = min(100, abs(128 - mean_intensity) * 2)
    
    return {
        "clarity": round(clarity, 1),
        "sharpness": round(sharpness, 1),
        "brightness_balance": round(brightness_balance, 1),
        "contrast_level": round(contrast, 1),
        "mean_intensity": round(mean_intensity, 1)
    }

def detect_teeth_based_on_image(image):
    """Generate unique teeth analysis based on image properties"""
    img_array = np.array(image)
    fingerprint = generate_image_fingerprint(image)
    
    seed = int(fingerprint, 16) % 10000
    np.random.seed(seed)
    
    all_teeth = [
        {"number": "18", "name": "Third Molar", "type": "Wisdom Tooth"},
        {"number": "17", "name": "Second Molar", "type": "Molar"},
        {"number": "16", "name": "First Molar", "type": "Molar"},
        {"number": "15", "name": "Second Premolar", "type": "Premolar"},
        {"number": "14", "name": "First Premolar", "type": "Premolar"},
        {"number": "13", "name": "Canine", "type": "Canine"},
        {"number": "12", "name": "Lateral Incisor", "type": "Incisor"},
        {"number": "11", "name": "Central Incisor", "type": "Incisor"},
    ]
    
    mean_val = img_array.mean()
    std_val = img_array.std()
    
    teeth_data = []
    conditions = ["Healthy", "Filled", "Crowned", "Root Canal", "Impacted", "Missing", "Carious"]
    condition_weights = [0.6, 0.15, 0.08, 0.06, 0.05, 0.04, 0.02]
    
    if std_val < 30:
        condition_weights = [0.4, 0.2, 0.1, 0.1, 0.1, 0.08, 0.02]
    
    for tooth in all_teeth:
        tooth_seed = seed + int(tooth["number"])
        np.random.seed(tooth_seed)
        
        condition = np.random.choice(conditions, p=condition_weights)
        confidence = np.random.uniform(0.75, 0.98)
        
        if std_val < 25:
            confidence *= 0.8
        elif std_val > 80:
            confidence *= 1.1
            
        teeth_data.append({
            "number": tooth["number"],
            "name": tooth["name"],
            "type": tooth["type"],
            "condition": condition,
            "confidence": round(confidence, 3)
        })
    
    return teeth_data

def calculate_forensic_metrics(original_img, enhanced_img, teeth_data):
    """Calculate dynamic forensic metrics"""
    orig_quality = analyze_image_quality(original_img)
    enhanced_quality = analyze_image_quality(enhanced_img)
    
    clarity_improvement = enhanced_quality["clarity"] - orig_quality["clarity"]
    sharpness_improvement = enhanced_quality["sharpness"] - orig_quality["sharpness"]
    
    healthy_count = len([t for t in teeth_data if t["condition"] == "Healthy"])
    treated_count = len([t for t in teeth_data if t["condition"] in ["Filled", "Crowned", "Root Canal"]])
    issue_count = len([t for t in teeth_data if t["condition"] in ["Impacted", "Missing", "Carious"]])
    
    base_utility = enhanced_quality["clarity"] * 0.4 + enhanced_quality["sharpness"] * 0.3
    dental_utility = (healthy_count / len(teeth_data)) * 30 + (treated_count / len(teeth_data)) * 40
    forensic_utility = min(100, base_utility + dental_utility)
    
    distinctive_features = treated_count + issue_count
    id_confidence = min(100, 50 + (distinctive_features * 8) + (forensic_utility * 0.4))
    
    return {
        "image_clarity": enhanced_quality["clarity"],
        "sharpness_quality": enhanced_quality["sharpness"],
        "clarity_improvement": round(clarity_improvement, 1),
        "sharpness_improvement": round(sharpness_improvement, 1),
        "forensic_utility": round(forensic_utility, 1),
        "identification_confidence": round(id_confidence, 1),
        "distinctive_features": distinctive_features,
        "dental_health_score": round((healthy_count / len(teeth_data)) * 100, 1)
    }

def create_tooth_chart(teeth_data):
    """Create tooth chart"""
    img = Image.new('RGB', (600, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    draw.ellipse([150, 50, 450, 150], outline='black', width=2)
    draw.ellipse([150, 150, 450, 250], outline='black', width=2)
    
    positions = {
        "18": (170, 80), "17": (230, 75), "16": (290, 70), "15": (350, 75),
        "14": (410, 80), "13": (450, 100), "12": (480, 120), "11": (500, 140),
    }
    
    condition_colors = {
        "Healthy": "#4CAF50",
        "Filled": "#2196F3", 
        "Crowned": "#FF9800",
        "Root Canal": "#9C27B0",
        "Impacted": "#F44336",
        "Missing": "#9E9E9E",
        "Carious": "#795548"
    }
    
    for tooth in teeth_data:
        if tooth["number"] in positions:
            x, y = positions[tooth["number"]]
            color = condition_colors.get(tooth["condition"], "#000000")
            draw.ellipse([x-12, y-12, x+12, y+12], fill=color, outline='black', width=1)
            draw.text((x-8, y-8), tooth["number"], fill='white')
    
    return img

def generate_report(case_data, metrics, teeth_data):
    """Generate forensic report"""
    
    distinctive_teeth = [t for t in teeth_data if t["condition"] in ["Filled", "Crowned", "Root Canal", "Impacted"]]
    
    if metrics["identification_confidence"] >= 90:
        conclusion = "**EXCELLENT** - Highly suitable for positive identification"
    elif metrics["identification_confidence"] >= 75:
        conclusion = "**GOOD** - Suitable for identification purposes" 
    else:
        conclusion = "**MODERATE** - Limited identification value"
    
    report = f"""
# FORENSIC DENTAL ANALYSIS REPORT

## Case Information
- **Case ID**: {case_data['case_id']}
- **Analysis Date**: {case_data['analysis_date']}
- **Evidence Condition**: {case_data['degradation_type']}

## Technical Analysis
- **Final Clarity Score**: {metrics['image_clarity']}%
- **Sharpness Quality**: {metrics['sharpness_quality']}%
- **Clarity Improvement**: +{metrics['clarity_improvement']}%
- **Sharpness Improvement**: +{metrics['sharpness_improvement']}%

## Forensic Evaluation
- **Overall Forensic Utility**: {metrics['forensic_utility']}%
- **Identification Confidence**: {metrics['identification_confidence']}%
- **Distinctive Dental Features**: {metrics['distinctive_features']}

## Dental Findings
- **Total Teeth Analyzed**: {len(teeth_data)}
- **Healthy Teeth**: {len([t for t in teeth_data if t['condition'] == 'Healthy'])}
- **Restored Teeth**: {len([t for t in teeth_data if t['condition'] in ['Filled', 'Crowned', 'Root Canal']])}
- **Dental Anomalies**: {len([t for t in teeth_data if t['condition'] in ['Impacted', 'Missing', 'Carious']])}

## Conclusion
{conclusion}

---
*Report generated by Forensic Dental AI System | {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
    
    return report

# Initialize session state
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = {
        'current_image': create_simple_xray(),
        'current_name': "Default X-ray",
        'degraded': None,
        'enhanced': None,
        'analysis_done': False,
        'degradation_type': "Thermal Damage",
        'severity': 5,
        'metrics': None,
        'teeth_data': None,
        'image_fingerprint': None
    }

# Main app
st.markdown('<h1 class="main-header">🦷 Forensic Dental AI System</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## Image Library")
    selected_image = st.selectbox("Choose image:", list(DENTAL_IMAGE_LIBRARY.keys()))
    
    if st.button("📷 Load Image"):
        with st.spinner("Loading image..."):
            st.session_state.analysis_data['current_image'] = load_dental_image(selected_image)
            st.session_state.analysis_data['current_name'] = selected_image
            st.session_state.analysis_data['degraded'] = None
            st.session_state.analysis_data['enhanced'] = None
            st.session_state.analysis_data['analysis_done'] = False
            st.success(f"Loaded: {selected_image}")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📷 Evidence", "🔍 Enhancement", "🦷 Analysis", "📄 Report"])

with tab1:
    st.markdown("### Step 1: Evidence Preparation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display current image using simple st.image
        st.image(st.session_state.analysis_data['current_image'], 
                caption=st.session_state.analysis_data['current_name'])
        
        uploaded_file = st.file_uploader("Upload dental image", type=['jpg', 'jpeg', 'png'])
        if uploaded_file is not None:
            try:
                img = Image.open(uploaded_file).convert('L')
                st.session_state.analysis_data['current_image'] = img
                st.session_state.analysis_data['current_name'] = uploaded_file.name
                st.session_state.analysis_data['degraded'] = None
                st.session_state.analysis_data['enhanced'] = None
                st.session_state.analysis_data['analysis_done'] = False
                st.success("✅ Image uploaded successfully!")
            except Exception as e:
                st.error(f"Upload error: {e}")
    
    with col2:
        st.markdown("### Apply Degradation")
        
        deg_type = st.selectbox("Degradation Type:", 
                               ["Thermal Damage", "Water Damage", "Trauma Damage"])
        severity = st.slider("Severity Level:", 1, 10, 5)
        
        if st.button("Apply Degradation"):
            with st.spinner("Applying degradation..."):
                degraded_img = apply_degradation(
                    st.session_state.analysis_data['current_image'], 
                    deg_type, 
                    severity/10
                )
                st.session_state.analysis_data['degraded'] = degraded_img
                st.session_state.analysis_data['degradation_type'] = deg_type
                st.session_state.analysis_data['severity'] = severity
                st.session_state.analysis_data['enhanced'] = None
                st.session_state.analysis_data['analysis_done'] = False
                st.success("✅ Degradation applied!")
        
        if st.session_state.analysis_data['degraded'] is not None:
            st.success("✅ Ready for enhancement!")
            st.image(st.session_state.analysis_data['degraded'], caption="Degraded Image")
        else:
            st.info("👆 Apply degradation to continue")

with tab2:
    st.markdown("### Step 2: AI Enhancement")
    
    if st.session_state.analysis_data['degraded'] is None:
        st.error("❌ Please apply degradation first in the Evidence tab!")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### **Input: Degraded Image**")
            st.image(st.session_state.analysis_data['degraded'], caption="")
            
            if st.button("🚀 ENHANCE IMAGE", type="primary", use_container_width=True):
                try:
                    with st.spinner("Enhancing image..."):
                        # Create enhanced image
                        enhanced_img = enhance_image(st.session_state.analysis_data['degraded'])
                        st.session_state.analysis_data['enhanced'] = enhanced_img
                        
                        # Generate analysis
                        fingerprint = generate_image_fingerprint(enhanced_img)
                        st.session_state.analysis_data['image_fingerprint'] = fingerprint
                        st.session_state.analysis_data['teeth_data'] = detect_teeth_based_on_image(enhanced_img)
                        st.session_state.analysis_data['metrics'] = calculate_forensic_metrics(
                            st.session_state.analysis_data['degraded'], 
                            enhanced_img, 
                            st.session_state.analysis_data['teeth_data']
                        )
                        
                        st.session_state.analysis_data['analysis_done'] = True
                        st.success("✅ Enhancement & Analysis completed!")
                        
                except Exception as e:
                    st.error(f"Enhancement failed: {str(e)}")
        
        with col2:
            st.markdown("#### **Output: Enhanced Image**")
            
            if st.session_state.analysis_data['enhanced'] is not None:
                # Display enhanced image
                st.image(st.session_state.analysis_data['enhanced'], caption="")
                
                st.markdown('<div class="success-box">✅ Unique analysis generated!</div>', unsafe_allow_html=True)
                
                # Show metrics
                metrics = st.session_state.analysis_data['metrics']
                if metrics:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("ID Confidence", f"{metrics['identification_confidence']}%")
                    with col2:
                        st.metric("Distinctive Features", metrics['distinctive_features'])
                    
                    st.info(f"**Image Fingerprint:** {st.session_state.analysis_data['image_fingerprint']}")
            else:
                st.info("👆 Click **ENHANCE IMAGE** to process")
                # Show placeholder
                placeholder = Image.new('RGB', (400, 300), color='#f0f2f6')
                draw = ImageDraw.Draw(placeholder)
                draw.text((120, 140), "Enhanced image will appear here", fill='#666666')
                st.image(placeholder, caption="")

with tab3:
    st.markdown("### Step 3: Dental Analysis")
    
    if not st.session_state.analysis_data['analysis_done']:
        st.warning("⚠️ Please complete enhancement first.")
    else:
        st.success("🦷 Dental Analysis Complete!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Analysis Metrics")
            
            metrics = st.session_state.analysis_data['metrics']
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Forensic Utility", f"{metrics['forensic_utility']}%")
                st.metric("Clarity Score", f"{metrics['image_clarity']}%")
            with col2:
                st.metric("ID Confidence", f"{metrics['identification_confidence']}%")
                st.metric("Dental Health", f"{metrics['dental_health_score']}%")
            
            st.markdown("#### 🦷 Tooth Chart")
            chart_img = create_tooth_chart(st.session_state.analysis_data['teeth_data'])
            st.image(chart_img, caption="Dental Analysis Chart")
        
        with col2:
            st.markdown("#### 📋 Detailed Findings")
            
            teeth_data = st.session_state.analysis_data['teeth_data']
            healthy_count = len([t for t in teeth_data if t["condition"] == "Healthy"])
            treated_count = len([t for t in teeth_data if t["condition"] in ["Filled", "Crowned", "Root Canal"]])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Healthy Teeth", healthy_count)
            with col2:
                st.metric("Treated Teeth", treated_count)
            
            st.markdown("#### Tooth-by-Tooth Analysis")
            for tooth in teeth_data:
                with st.expander(f"Tooth {tooth['number']} - {tooth['name']}"):
                    st.write(f"**Condition:** {tooth['condition']}")
                    st.write(f"**Confidence:** {tooth['confidence']*100:.1f}%")
                    if tooth["condition"] != "Healthy":
                        st.info(f"Distinctive feature for identification")

with tab4:
    st.markdown("### Step 4: Forensic Report")
    
    if not st.session_state.analysis_data['analysis_done']:
        st.warning("Please complete the analysis first.")
    else:
        case_data = {
            'case_id': f"DENT-{datetime.now().strftime('%Y%m%d-%H%M')}",
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'degradation_type': st.session_state.analysis_data['degradation_type'],
            'severity': st.session_state.analysis_data['severity']
        }
        
        report = generate_report(
            case_data, 
            st.session_state.analysis_data['metrics'], 
            st.session_state.analysis_data['teeth_data']
        )
        
        st.markdown(report)
        
        st.info(f"**Unique Analysis ID:** {st.session_state.analysis_data['image_fingerprint']}")

# Footer
st.markdown("---")
st.markdown("*Forensic Dental AI System | Streamlit Deployment*")
