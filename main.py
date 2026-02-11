import os
import subprocess
from flask import Flask, request, send_file, render_template
from docxtpl import DocxTemplate

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Getting the data from the form
    selected_subject_code = request.form.get('subject_code')
    selected_subject_name = request.form.get('subject_name')
    student_name = request.form.get('student_name')

    # Load template
    doc = DocxTemplate("template.docx")
    
    # Placeholders must match exactly in your Word Doc: {{NAME}}, {{CODE}}, {{SUBJECT}}
    context = {
        'NAME': student_name,
        'CODE': selected_subject_code,
        'SUBJECT': selected_subject_name
    }
    
    doc.render(context)
    docx_path = "/tmp/temp.docx"
    pdf_path = "/tmp/temp.pdf"
    doc.save(docx_path)

    # Convert to PDF via LibreOffice
    subprocess.run([
        'libreoffice', '--headless', '--convert-to', 'pdf',
        '--outdir', '/tmp', docx_path
    ], check=True)

    return send_file(pdf_path, as_attachment=True, download_name=f"{selected_subject_code}.pdf")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
  
