from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import zipfile
import io
import textwrap

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB limit

def convert_text_to_image(text, font_size=12):
    # Calculate image size based on text length
    padding = 20
    font = ImageFont.load_default()
    
    # Wrap text to fit in 800px width
    wrapped_text = textwrap.fill(text, width=80)
    lines = wrapped_text.count('\n') + 1
    
    # Create image with white background
    img_width = 800
    img_height = (lines * (font_size + 4)) + (padding * 2)
    image = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw text
    draw.text((padding, padding), wrapped_text, font=font, fill='black')
    
    return image

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'files' not in request.files:
        return redirect(url_for('home'))
    
    files = request.files.getlist('files')
    if not files or all(file.filename == '' for file in files):
        return redirect(url_for('home'))
    
    dpi = int(request.form.get('dpi', 200))
    font_size = int(request.form.get('font_size', 12))
    
    # Create a BytesIO object to store the zip file
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(file_path)
                
                base_name = os.path.splitext(filename)[0]
                
                try:
                    if filename.lower().endswith('.pdf'):
                        # Convert PDF to images
                        images = convert_from_path(file_path, dpi=dpi)
                        for i, image in enumerate(images):
                            img_byte_arr = io.BytesIO()
                            image.save(img_byte_arr, format='JPEG')
                            img_bytes = img_byte_arr.getvalue()
                            zipf.writestr(f"{base_name}_page_{i+1}.jpg", img_bytes)
                    
                    elif filename.lower().endswith('.txt'):
                        # Convert text file to image
                        with open(file_path, 'r', encoding='utf-8') as txt_file:
                            text_content = txt_file.read()
                            image = convert_text_to_image(text_content, font_size)
                            img_byte_arr = io.BytesIO()
                            image.save(img_byte_arr, format='JPEG')
                            img_bytes = img_byte_arr.getvalue()
                            zipf.writestr(f"{base_name}.jpg", img_bytes)
                    
                    # Clean up uploaded file
                    os.remove(file_path)
                
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
                    continue
    
    zip_io.seek(0)
    return send_file(
        zip_io,
        mimetype='application/zip',
        as_attachment=True,
        download_name='converted_images.zip'
    )

if __name__ == '__main__':
    app.run(debug=True)
