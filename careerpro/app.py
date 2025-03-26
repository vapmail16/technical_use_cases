import streamlit as st
import os
from dotenv import load_dotenv
import openai
import tempfile
from PyPDF2 import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

# ResumePro Prompt
RESUME_PRO_PROMPT = """
You are ResumePro, an expert resume reviewer.

When a user uploads or pastes a resume:
1. Provide a brief summary of its quality.
2. Highlight 2–3 strengths.
3. Suggest 2–3 improvements in content or format.
4. Evaluate ATS friendliness and keyword usage.
5. Provide examples of improved bullet points if needed.

Do not rewrite the full resume. Instead, guide the user on what to change.

Use a friendly but professional tone.
"""

# ResumeTailor Prompt
RESUME_TAILOR_PROMPT = """
You are ResumeTailor, a specialized GPT that takes two inputs: a resume and a job description.

When both are provided:
1. Identify key requirements from the job description.
2. Compare those to the resume's content.
3. Rewrite the following sections:
   - Resume summary
   - Skills section
   - Key experience bullet points (up to 3 jobs max)
4. Optimize for ATS with relevant keywords.
5. Keep the format readable and professional.

Ensure tone and style match the industry (tech, design, etc.). If any section is missing, add it.

If only one document is provided, ask for the other.
"""

def read_file_content(file_path):
    """Read content from either PDF or TXT file."""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        # Read PDF file
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    else:
        # Read TXT file
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

def create_pdf(text):
    """Create a formatted PDF from text content."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom style for the content
    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceBefore=6,
        spaceAfter=6
    )
    
    # Split text into paragraphs and create PDF elements
    elements = []
    paragraphs = text.split('\n\n')
    
    for para in paragraphs:
        if para.strip():
            elements.append(Paragraph(para, custom_style))
            elements.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def call_openai(system_prompt, user_prompt):
    """Call OpenAI API with system and user prompts."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"OpenAI API Error: {str(e)}")

# Set page config
st.set_page_config(
    page_title="CareerPro - CV Review & Tailoring",
    page_icon="🧠",
    layout="wide"
)

# Title and description
st.title("🧠 CareerPro - CV Review & Tailoring")
st.markdown("""
This app helps you review your CV and tailor it for specific job opportunities using AI.
""")

# File upload section
st.header("Upload Your Documents")
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("📄 Upload your CV (PDF or TXT)", type=["pdf", "txt"])
    if resume_file:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.name)[1]) as tmp_file:
            tmp_file.write(resume_file.getvalue())
            resume_path = tmp_file.name

with col2:
    job_description = st.file_uploader("📝 Upload Job Description (PDF or TXT)", type=["pdf", "txt"])
    if job_description:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(job_description.name)[1]) as tmp_file:
            tmp_file.write(job_description.getvalue())
            job_path = tmp_file.name

# Process button
if resume_file:
    try:
        # Read the resume file
        resume_text = read_file_content(resume_path)

        # Resume Review Button
        if st.button("🔍 Review Resume"):
            with st.spinner("Analyzing your CV..."):
                try:
                    review_result = call_openai(RESUME_PRO_PROMPT, f"My resume:\n{resume_text}")
                    st.subheader("Resume Review")
                    st.write(review_result)
                except Exception as e:
                    st.error(f"Error during CV review: {str(e)}")

        # Resume Tailoring (if job description is provided)
        if job_description:
            job_text = read_file_content(job_path)
            
            if st.button("🎯 Tailor Resume to Job"):
                with st.spinner("Tailoring your CV..."):
                    try:
                        # Get tailored CV
                        tailored_cv = call_openai(
                            RESUME_TAILOR_PROMPT,
                            f"Resume:\n{resume_text}\n\nJob Description:\n{job_text}"
                        )
                        
                        # Create PDF
                        pdf_buffer = create_pdf(tailored_cv)
                        
                        # Display preview
                        st.subheader("Tailored CV Preview")
                        st.text_area("Preview", tailored_cv, height=400)
                        
                        # Download PDF button
                        st.download_button(
                            label="📥 Download Tailored CV (PDF)",
                            data=pdf_buffer.getvalue(),
                            file_name="tailored_cv.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Error during CV tailoring: {str(e)}")
    except Exception as e:
        st.error(f"Error reading files: {str(e)}")

# Cleanup temporary files
if 'resume_path' in locals():
    os.unlink(resume_path)
if 'job_path' in locals():
    os.unlink(job_path)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and OpenAI") 