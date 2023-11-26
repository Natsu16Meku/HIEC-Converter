from flask import Flask, request, send_file
from PIL import Image
import pillow_heif
import io
import os

app = Flask(__name__)

@app.route('/')
def upload_file():
    # 出力形式を選択できるフォーム
    return '''
    <!doctype html>
    <html>
    <head>
        <title>Image Converter</title>
    </head>
    <body>
        <h1>画像ファイルを変換</h1>
        <form action="/convert" method="post" enctype="multipart/form-data">
            <input type="file" name="file"><br><br>
            <label for="format">出力形式を選択:</label>
            <select name="format">
                <option value="JPEG">JPEG</option>
                <option value="PNG">PNG</option>
                <option value="BMP">BMP</option>
                <option value="GIF">GIF</option>
                <option value="TIFF">TIFF</option>
                <option value="WebP">WebP</option>
            </select><br><br>
            <input type="submit" value="Upload">
        </form>
    </body>
    </html>
    '''

@app.route('/convert', methods=['POST'])
def convert_image():
    if 'file' not in request.files:
        return 'ファイルがありません'
    file = request.files['file']
    output_format = request.form.get('format', 'JPEG')  # デフォルトはJPEG
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
            download_name=f'converted_image.{output_format.lower()}'
        )

if __name__ == '__main__':
    app.run(debug=True)