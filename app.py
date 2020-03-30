import hashlib
import sqlite3

import pytesseract
from PIL import Image

from flask import Flask, request, jsonify, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect('/ocr')


@app.errorhandler(404)
def page_not_found(error):
    return redirect('/ocr/404')


@app.route('/ocr/404')
def page_404():
    return "<h1>OCR : 404</h1>"


@app.route('/ocr', methods=['POST'])
def ocr():
    try:
        file = request.files.get('file')
        lang = request.form.get('lang')
        md5 = hashlib.md5(file.read()).hexdigest()
        conn = sqlite3.connect('./db.sqlite3')
        c = conn.cursor()
        c.execute('''select `text` from `ocr` where `md5`=? and `lang`=?''', (md5, lang))
        values = c.fetchone()
        if values:
            return jsonify({'code': 200, 'msg': 'success', 'data': values[0]})
        img = Image.open(file)
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        text = pytesseract.image_to_string(img, lang=lang)

        c.execute('''insert into `ocr`(`md5`, `text`, `lang`) values(?, ?, ?)''', (md5, text, lang))
        c.close()
        conn.commit()
        conn.close()
        return jsonify({'code': 200, 'msg': 'success', 'data': text})
    except Exception as ex:
        print(ex)
        return jsonify({'code': 500, 'msg': str(ex), 'data': None})


@app.route('/ocr/clear')
def clear():
    try:
        conn = sqlite3.connect('./db.sqlite3')
        c = conn.cursor()
        c.execute('''delete from `ocr` ''')
        c.close()
        conn.commit()
        conn.close()
        return jsonify({'code': 200, 'msg': 'success', 'data': None})
    except Exception as ex:
        print(ex)
        return jsonify({'code': 500, 'msg': str(ex), 'data': None})


if __name__ == '__main__':
    app.run()
