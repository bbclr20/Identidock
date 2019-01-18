from flask import Flask, Response, request
import hashlib
import requests

app = Flask(__name__)
salt = "SALT"
default_name = "ben"

doc = """
<html>
<head>
    <title>
        Identidock
    </title>
</head>
<body>
<form method="POST">
    Hello <input type="text" name="name" value="{}">
    <input type="submit" value="submit">
</form>
<p>You look like a:</p>
<img src=/monster/{} />
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def mainpage():
    name = default_name
    if request.method == "POST":
        name = request.form["name"]

    salted_name = salt + name
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

    return doc.format(name, name_hash)

@app.route("/monster/<name>")
def get_identicon(name):
    res = requests.get("http://dnmonster:8080/monster/" + name + "?size=120")
    image = res.content
    return Response(image, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
