import os
from flask import Flask, Blueprint
from flask import redirect, url_for
from controller.MainController import main

app = Flask(__name__)
app.register_blueprint(main)

# 기본 페이지
@app.route('/')
def home():
    return redirect(url_for("main.index"))


# 서버 실행
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

