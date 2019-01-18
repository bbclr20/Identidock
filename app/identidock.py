from flask import Flask, Response, request
import hashlib
import requests
import redis

app = Flask(__name__)
cache = redis.StrictRedis(host="redis", port=6379, db=0)
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
<img src=/monster/{} name="md5"/>
<img src=/monster/{} name="sha224"/>
<img src=/monster/{} name="sha256"/>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def mainpage():
    name = default_name
    if request.method == "POST":
        name = request.form["name"]

    salted_name = salt + name
    name_md5 = hashlib.md5(salted_name.encode()).hexdigest()
    name_sha224 = hashlib.sha224(name_md5.encode()).hexdigest()
    name_sha256 = hashlib.sha256(name_sha224.encode()).hexdigest()

    return doc.format(name, name_md5, name_sha224, name_sha256)


@app.route("/monster/<name>")
def get_identicon(name):
    image = cache.get(name)
    if image is None:
        print("{} is not cached".format(name))
        res = requests.get("http://dnmonster:8080/monster/" + name + "?size=120")
        image = res.content
        cache.set(name, image)
    return Response(image, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
