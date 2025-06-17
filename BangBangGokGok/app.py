import os
from flask import Flask, Blueprint

app = Flask(__name__)

# 기본 페이지
@app.route('/')
def home():
    return "hello world"


# 서버 실행
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

