from flask import Flask, request, send_file, render_template
from PIL import Image
import pillow_heif
import io
import os

app = Flask(__name__)

@app.route('/')
def upload_file():
    return render_template("upload.html")

@app.route('/convert', methods=['POST'])
def convert_image():
    if 'file' not in request.files:
        return 'ファイルがありません'
    file = request.files['file']
    output_format = request.form.get('format', 'JPEG')
    custom_filename = request.form.get('custom_filename', 'converted_image')
    filename, file_extension = os.path.splitext(file.filename)
    if file.filename == '':
        return 'ファイルが選択されていません'
    if file:
        if file_extension.lower() in ['.heic', '.heif']:
            # HEIC/HEIFファイルを指定された形式に変換
            heif_file = pillow_heif.read_heif(file.stream)
            image = Image.frombytes(
                "RGB", 
                heif_file.size, 
                heif_file.data,
                "raw",
                "RGB",
                heif_file.stride,
            )
        else:
            # 他の形式のファイルを選択された形式に変換
            image = Image.open(file.stream)

        output = io.BytesIO()
        image.save(output, format=output_format)
        output.seek(0)
        return send_file(
            output,
            as_attachment=True,
            download_name=f'{custom_filename}.{output_format.lower()}'
        )

if __name__ == '__main__':
    app.run(debug=True)