import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

# 현재 파일 (예: service.py 또는 controller.py)의 절대경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class AnalysisService:

    # 럭셔리 아파트
    def expensiveApt(self):
        # 1. CSV 파일 경로 설정
        csv_path = os.path.join(BASE_DIR, '..', 'resources', 'csv', 'data.csv')

        # 2. CSV 파일 불러오기
        df = pd.read_csv(csv_path)

        # 3. 결측치 및 공백 제거 (문제 방지용)
        # df = df.dropna(subset=['price', 'name'])  # 가격과 아파트명 없으면 제거
        # df = df[df['price'].astype(str).str.strip() != '']  # 공백 제거
        df['price'] = df['price'].astype(float)

        # 4. 아파트 이름 기준으로 중복 제거
        df = df.drop_duplicates(subset='name')

        # 5. 가격 기준으로 상위 10개 추출
        top10_price = df.sort_values(by='price', ascending=False).head(10)

        # 6. 결과 출력
        # print(top10_price)
        return top10_price.to_dict(orient='records')

    # 아파트 가격예측 회기분석
    def regressionApt(self):
        csv_path = os.path.join(BASE_DIR, '..','resources', 'csv', 'data.csv')
        df = pd.read_csv(csv_path)

        # 2. 인코딩 (구, 동: 범주형)
        le_gu = LabelEncoder()
        le_dong = LabelEncoder()
        df['gu'] = le_gu.fit_transform(df['gu'])
        df['dong'] = le_dong.fit_transform(df['dong'])

        # 3. 독립 변수 (X), 종속 변수 (y)
        X = df[['gu', 'dong', 'pyung', 'years', 'household', 'subway']]
        y = df['price']

        # 4. 회귀 모델 학습
        model = LinearRegression()
        model.fit(X, y)

        # 5. 예측
        df['pred'] = model.predict(X)

        # 6. 오차 계산
        df['devi'] = abs(df['price'] - df['pred'])

        # 7. 오차가 가장 작은 10개 샘플 추출
        top10 = df.sort_values(by='devi').head(10)
        
        #다시 한글로 변경
        top10['gu'] = le_gu.inverse_transform(top10['gu'])
        top10['dong'] = le_dong.inverse_transform(top10['dong'])

        # JSON 형식으로 변환
        top10_json = top10[[
            'gu', 'dong', 'name', 'pyung', 'years', 'household', 'subway',
            'price', 'pred', 'devi'
        ]].to_dict(orient='records')

        return top10_json

    

analysisService = AnalysisService()
