from flask import Flask, render_template, request, jsonify, Blueprint, session
from service.MainService import mainService
from service.AnalysisService import analysisService
import json
import os

main = Blueprint("main", __name__)

#index 
@main.route('/index', methods=['GET'])
def index():
    #럭셔리 아파트
    exp_apt = analysisService.expensiveApt()
    # print(exp_apt)
    #상승 확률 UP 아파트
    reg_apt = analysisService.regressionApt()
    # print(reg_apt)
    return render_template('index.html', exp_apt = exp_apt, reg_apt = reg_apt)

# 아파트 매물 상세
@main.route('/sale', methods=['POST'])
def sale():
    data = request.get_json()
    aptSaleInfo = mainService.getAptSaleInfo(data['markerId'])

    return jsonify({'status': 'success', 'apt': aptSaleInfo})

