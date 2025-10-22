# 🦷 Forensic Dental AI System

A comprehensive web application for forensic dental analysis, image enhancement, and dental identification using AI-powered image processing.

![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-ff4b4b) ![Python](https://img.shields.io/badge/Python-3.8+-3776ab) ![Pillow](https://img.shields.io/badge/Pillow-10.2.0-ffffff)

## 📋 Overview

The Forensic Dental AI System assists forensic odontologists and dental professionals in analyzing dental X-rays for identification purposes. It offers advanced image processing, automated tooth detection, and professional forensic reporting capabilities.

## ✨ Features

### 🔍 Image Processing
- **Multiple Degradation Simulations**: Simulate thermal, water, or trauma damage to dental X-rays
- **AI-Powered Enhancement**: Enhance contrast and sharpness for degraded images
- **Real-time Processing**: Instant image transformation and analysis

### 🦷 Dental Analysis
- **Automated Tooth Detection**: Identifies individual teeth in X-rays
- **Condition Assessment**: Classifies teeth (healthy, filled, crowned, root canal, etc.)
- **Confidence Scoring**: Provides confidence levels for all analyses

### 📊 Forensic Reporting
- **Comprehensive Metrics**: Image clarity, forensic utility, identification confidence
- **Professional Reports**: Generates detailed forensic analysis reports
- **Legal Admissibility**: Assesses evidence suitability for legal use

### 🎯 User-Friendly Interface
- **Step-by-Step Workflow**: Evidence preparation → Enhancement → Analysis → Reporting
- **Image Library**: Pre-loaded dental X-ray samples
- **File Upload**: Supports JPG, JPEG, and PNG formats

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- `pip` package manager

### Installation
1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd forensic-dental-ai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Open http://localhost:8501 in your browser.

## 📁 Project Structure
```
forensic-dental-ai/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── LICENSE             # License information
├── bitewing_1.jpg      # Sample dental X-ray
├── degraded_sample.jpg # Sample degraded image
├── panoramic_1.jpg     # Sample panoramic X-ray
└── periapical_1.jpg    # Sample periapical X-ray
```

## 🛠️ Technical Details

### Image Processing
The system uses Pillow and NumPy for advanced image processing:
- Gaussian blur for degradation simulation
- Contrast and sharpness enhancement
- Dynamic analysis based on actual image properties

### AI Analysis
- Unique fingerprint generation for each image
- Dynamic dental condition detection
- Forensic utility scoring algorithms

### Web Interface
- Built with Streamlit for responsive web interface
- Multi-tab workflow for organized analysis
- Real-time feedback and progress indicators

## 📝 Usage Guide

1. **Evidence Preparation**: Load a dental X-ray from the library or upload your own
2. **Apply Degradation**: Simulate various types of damage to the image
3. **AI Enhancement**: Process the degraded image to improve quality
4. **Dental Analysis**: View automated tooth detection and condition assessment
5. **Generate Report**: Create a professional forensic report for legal use

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dental X-ray samples from open-source repositories
- Streamlit for the excellent web framework
- Pillow and NumPy for image processing capabilities