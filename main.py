import random, requests, glob, os
from flask import Flask, render_template, request, jsonify
from threading import Thread

app = Flask('DDrive')

def delt():
    files = glob.glob('static/images/*')
    for f in files:
        os.remove(f)

def webSend(msg, filename):
    size = round(os.stat(f'static/images/{filename}').st_size / 1000000, 1)
    if size <= 8.2:
        print(size)  # Print size for debugging purposes
        return True, size
    else:
        print(size)  # Print size for debugging purposes
        return False, size

def webSend2(msg, file, size):
    if size <= 8.2:
        return True
    else:
        return False

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            file = request.files['img']
            file.save(f"static/images/{file.filename}")
            tf, size = webSend(file.filename, file.filename)
            if tf:
                delt()
                return render_template("home.html",
                                       t=file.filename,
                                       size=size,
                                       c="true")
            else:
                delt()
                return render_template("home.html", c="false")
        except Exception as e:
            return f"Something went wrong while uploading, try again!<br>{e}"
    else:
        return render_template("home.html", c="false")

@app.route('/api', methods=["GET", "POST"])
def api():
    if request.method == "POST":
        try:
            file = request.files["file"]
            file.save(f"static/images/{file.filename}")
            tf, size = webSend(file.filename, file.filename)
            if tf:
                delt()
                data = {"size": str(size), "error": None}
                return jsonify(data)
            else:
                delt()
                data = {"size": str(size), "error": "File size exceeds limit!"}
                return jsonify(data)
        except Exception as e:
            data = {"size": None, "error": f"{e}"}
            return jsonify(data)
    else:
        data = {"size": None, "error": "GET Method is not allowed!"}
        return jsonify(data)

@app.route('/api2', methods=["GET", "POST"])
def api2():
    if request.method == "POST":
        try:
            file = request.files["file"]
            filename = str(request.args.get('q'))
            print(filename)
            file.save(f"static/images/{filename}")
            tf, size = webSend(filename, filename)
            if tf:
                delt()
                data = {"size": str(size), "error": None}
                return jsonify(data)
            else:
                delt()
                data = {"size": str(size), "error": "File size exceeds limit!"}
                return jsonify(data)
        except Exception as e:
            data = {"size": None, "error": f"{e}"}
            return jsonify(data)
    else:
        data = {"size": None, "error": "GET Method is not allowed!"}
        return jsonify(data)

@app.route('/sharex', methods=["GET", "POST"])
def sharex():
    if request.method == "POST":
        try:
            file = request.files["file"]
            file.save(f"static/images/{file.filename}")
            tf, size = webSend(file.filename, file.filename)
            if tf:
                delt()
                return "Upload successful"
            else:
                delt()
                return f"Size: {size} MB | File size exceeds limit!"
        except Exception as e:
            return str(e)
    else:
        return "GET Method is not allowed!"

@app.route('/direct', methods=["GET", "POST"])
def direct():
    if request.method == "POST":
        try:
            file = request.files["file"]
            filename = file.filename
            size = float(round(request.content_length / 1000000, 2))
            tf = webSend2(filename, file, size)
            if tf:
                delt()
                data = {"size": str(size), "error": None}
                return jsonify(data)
            else:
                delt()
                data = {"size": str(size), "error": "File size exceeds limit!"}
                return jsonify(data)
        except Exception as e:
            data = {"size": None, "error": f"{e}"}
            return jsonify(data)
    else:
        data = {"size": None, "error": "GET Method is not allowed!"}
        return jsonify(data)

def run():
    app.run(host='0.0.0.0', port=random.randint(2222, 9999))

def keep_alive():
    t = Thread(target=run)
    t.start()
