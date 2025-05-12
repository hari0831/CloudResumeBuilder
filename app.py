from flask import Flask, render_template, request, send_file
from xhtml2pdf import pisa
import os
import uuid


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.form.to_dict()
    template = data.get('template', 'resume_template1.html')
    html = render_template(template, data=data)
    filename = f"{uuid.uuid4().hex}.pdf"
    filepath = os.path.join("generated", filename)
    os.makedirs("generated", exist_ok=True)

    with open(filepath, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)

    if pisa_status.err:
        return "Error generating PDF"

    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
