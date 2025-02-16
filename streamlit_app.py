import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Set up the model
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def generate_content(patient_data, clinical_data):
    prompt = f"""
    Create a colorful, engaging patient education material with emojis and formatting. Use the following patient information:
    
    Patient Details:
    - Age: {patient_data['age']}
    - Preferred Language: {patient_data['language']}
    - Education Level: {patient_data['education']}
    
    Clinical Information:
    - Diagnosis: {clinical_data['diagnosis']}
    - Visual Acuity RE: {clinical_data['va_re']}
    - Visual Acuity LE: {clinical_data['va_le']}
    - OCT Findings: {clinical_data['oct_findings']}
    
    Include these sections: {', '.join(clinical_data['sections'])}
    
    Make the content patient-friendly, using simple language. Add emojis and color indicators using markdown.
    Use different colors for different sections (using markdown).
    Include a summary at the end.
    
    If the language selected is not English, provide content in both English and the selected language.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {str(e)}"

def main():
    st.set_page_config(page_title="Retina Patient Education Generator", page_icon="👁️")
    
    st.title("👁️ Retina Patient Education Generator")
    st.markdown("---")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    # Patient Demographics (Left Column)
    with col1:
        st.subheader("Patient Demographics")
        patient_data = {
            'age': st.number_input("Patient Age", 1, 100, 50),
            'language': st.selectbox(
                "Preferred Language",
                ["English", "Hindi", "Punjabi", "Odiya"]
            ),
            'education': st.selectbox(
                "Education Level",
                ["Primary", "Secondary", "Tertiary"]
            )
        }
    
    # Clinical Information (Right Column)
    with col2:
        st.subheader("Clinical Information")
        clinical_data = {
            'diagnosis': st.selectbox(
                "Diagnosis",
                [
                    "Diabetic Retinopathy",
                    "Age-related Macular Degeneration",
                    "Retinal Detachment",
                    "Central Serous Chorioretinopathy",
                    "Diabetic Macular Edema"
                ]
            ),
            'va_re': st.text_input("Visual Acuity (Right Eye)", "6/6"),
            'va_le': st.text_input("Visual Acuity (Left Eye)", "6/6"),
            'oct_findings': st.text_area("OCT Findings", "")
        }
    
    # Content Sections (Full Width)
    st.subheader("Content Sections")
    clinical_data['sections'] = st.multiselect(
        "Select sections to include:",
        [
            "Disease Overview",
            "Treatment Options",
            "Lifestyle Modifications",
            "Follow-up Care",
            "Emergency Signs",
            "Dietary Recommendations",
            "Visual Aids and Rehabilitation"
        ],
        default=["Disease Overview", "Treatment Options"]
    )
    
    # Generate Button
    if st.button("Generate Education Material", type="primary"):
        with st.spinner("Generating education material..."):
            content = generate_content(patient_data, clinical_data)
            st.markdown("### Generated Education Material")
            st.markdown(content)
            
            # Add download button for the content
            st.download_button(
                label="Download Material",
                data=content,
                file_name="patient_education_downloaded.txt",
                mime="text/plain"
            )
