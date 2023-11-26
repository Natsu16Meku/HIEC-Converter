from flask import Flask, request, send_file
from PIL import Image
import pillow_heif
import io

app = Flask(__name__)

@app.route('/')
def upload_file():
    # HTMLコードを直接埋め込む
    return '''
    <!doctype html>
    <html>
    <head>
        <title>HEIC to JPEG Converter</title>
    </head>
    <body>
        <h1>HEICファイルをJPEGに変換</h1>
        <form action="/convert" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>
    </body>
    </html>
    '''

@app.route('/convert', methods=['POST'])
def convert_heic_to_jpeg():
    if 'file' not in request.files:
        return 'ファイルがありません'
    file = request.files['file']
    if file.filename == '':
        return 'ファイルが選択されていません'
    if file:
        heif_file = pillow_heif.read_heif(file.stream)  # HEICファイルを読み込み
        image = Image.frombytes(
            "RGB", 
            heif_file.size, 
            heif_file.data,
            "raw",
            "RGB",
            heif_file.stride,
        )
        output = io.BytesIO()
        image.save(output, format='JPEG')  # JPEG形式で保存
        output.seek(0)
        return send_file(output, download_name='converted_image.jpeg', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
