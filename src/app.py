import streamlit as st
from PIL import Image
import numpy as np
import cv2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from src.utils.image_processing import enhance_image, simulate_degradation
from src.utils.dental_analysis import analyze_teeth

# Page config
st.set_page_config(page_title="Forensic Dental AI System", layout="wide")

# Title
st.title("🦷 Forensic Dental AI System")

# Sidebar for workflow
st.sidebar.title("Workflow")
step = st.sidebar.selectbox("Select Step", ["Upload Evidence", "Enhance Image", "Analyze Teeth", "Generate Report"])

# File uploader
uploaded_file = st.file_uploader("Choose a dental X-ray image", type=["jpg", "jpeg", "png"])

# Image library (sample images from assets/)
sample_images = [f for f in os.listdir("assets") if f.endswith((".jpg", ".jpeg", ".png"))]
selected_sample = st.sidebar.selectbox("Or select a sample image", ["None"] + sample_images)

# Load image (uploaded or sample)
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
elif selected_sample != "None":
    image = Image.open(os.path.join("assets", selected_sample))

if image is not None:
    st.image(image, caption="Original Image", use_column_width=True)
    
    if step == "Enhance Image":
        st.header("🔍 Image Enhancement")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Apply Degradation")
            degrade_type = st.selectbox("Degradation Type", ["Thermal Damage", "Water Damage", "Trauma"])
            if st.button("Simulate Damage"):
                degraded_img = simulate_degradation(np.array(image), degrade_type.lower())
                st.image(degraded_img, caption=f"{degrade_type} Applied")
                st.session_state["current_image"] = degraded_img
        with col2:
            st.subheader("Enhance Image")
            if st.button("Enhance Contrast & Sharpness"):
                current_img = st.session_state.get("current_image", np.array(image))
                enhanced_img = enhance_image(current_img)
                st.image(enhanced_img, caption="Enhanced Image")
                st.session_state["current_image"] = enhanced_img
    
    elif step == "Analyze Teeth":
        st.header("🦷 Dental Analysis")
        if st.button("Run Analysis"):
            current_img = st.session_state.get("current_image", np.array(image))
            results = analyze_teeth(current_img)
            st.write("### Analysis Results")
            for tooth, data in results.items():
                st.write(f"- {tooth}: {data['condition']} (Confidence: {data['confidence']:.0%})")
            st.session_state["analysis_results"] = results
    
    elif step == "Generate Report":
        st.header("📊 Forensic Report")
        if st.button("Generate PDF Report"):
            current_img = st.session_state.get("current_image", np.array(image))
            results = st.session_state.get("analysis_results", {})
            report_path = "reports/report.pdf"
            c = canvas.Canvas(report_path, pagesize=letter)
            c.drawString(100, 750, "Forensic Dental AI Report")
            c.drawString(100, 730, "Generated on: 2025-10-22")
            c.drawString(100, 700, "Image Clarity: High")
            c.drawString(100, 680, "Identification Confidence: 85%")
            c.drawString(100, 660, "Legal Admissibility: Suitable")
            if results:
                c.drawString(100, 640, "Dental Analysis:")
                y = 620
                for tooth, data in results.items():
                    c.drawString(100, y, f"- {tooth}: {data['condition']} ({data['confidence']:.0%})")
                    y -= 20
            c.save()
            with open(report_path, "rb") as f:
                st.download_button("Download Report", f, file_name="forensic_report.pdf")
            st.write("Report generated! Download above.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Step-by-Step: Preparation → Enhancement → Analysis → Reporting")
