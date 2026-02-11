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
    # 1. Get user input
    user_name = request.form.get('student_name')
    subj_code = request.form.get('subject_code')
    subj_name = request.form.get('subject_name')

    # 2. Paths (Required for Cloud Hosting)
    template_path = os.path.join(os.getcwd(), "template.docx")
    output_docx = "/tmp/filled_assignment.docx"
    output_pdf = "/tmp/filled_assignment.pdf"

    try:
        # 3. Fill Template
        doc = DocxTemplate(template_path)
        context = {'NAME': user_name, 'CODE': subj_code, 'SUBJECT': subj_name}
        doc.render(context)
        doc.save(output_docx)

        # 4. Convert to PDF via LibreOffice
        subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'pdf',
            '--outdir', '/tmp', output_docx
        ], check=True)

        return send_file(output_pdf, as_attachment=True, download_name=f"{subj_code}_Assignment.pdf")
    
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    # Koyeb provides the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
