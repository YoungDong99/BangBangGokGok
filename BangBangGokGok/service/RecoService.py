import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# 아파트 데이터 불러오기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class RecoService:
    @staticmethod
    def recommend_by_similarity(user_input):
        apartments = pd.read_csv(os.path.join(BASE_DIR, '..', 'resources', 'csv', 'data.csv'), encoding='utf-8-sig')
        """
        user_input: dict 형태 예시
            {
            'district': '강남구',z
            'price': 50000,     # 단위: 천만원
            'pyung': 30,
            'years': True,
            'ignore': {
                'price': False,
                'pyung': True,
                'years': False
            }
        }
        """

        # 필터링 조건 - 자치구 필터
        district = user_input.get('gu')
        if district == "서울 전체":
            df = apartments.copy()  # 전체 데이터 사용
        else:
            df = apartments[apartments['gu'] == district].copy()
        
        if df.empty:
            return []

        # 사용할 feature 구성
        features = []
        input_values = []
        result_columns = ['name', 'gu', 'dong', 'similarity', 'sub_dist']  # 기본 컬럼

        # 가격 feature 추가
        if not user_input['ignore'].get('price'):
            features.append('price')
            input_values.append(user_input['price'])
            result_columns.append('price')
            
            # 입력 금액의 2배를 초과하는 매물만 제외
            max_price = user_input['price'] * 2
            
            # 가격이 입력 금액의 2배 이하인 매물만 필터링
            df = df[df['price'] <= max_price]
        else:
            # '상관없음'인 경우 해당 컬럼 제외
            df = df.drop('price', axis=1)

        # 평수 feature 추가
        if not user_input['ignore'].get('pyung'):
            features.append('pyung')
            input_values.append(user_input['pyung'])
            result_columns.append('pyung')
            
            # 평수 타입에 따른 필터링
            pyung_type = user_input.get('pyung_type')
            if pyung_type == "4": 
                df = df[df['pyung'] >= 33]
            elif pyung_type == "3": 
                df = df[(df['pyung'] >= 24) & (df['pyung'] < 33)]
            elif pyung_type == "2": 
                df = df[(df['pyung'] >= 16) & (df['pyung'] < 24)]
            elif pyung_type == "1": 
                df = df[df['pyung'] < 16]
        else:
            # '상관없음'인 경우 해당 컬럼 제외
            df = df.drop('pyung', axis=1)

        # 아파트 연식 처리
        if not user_input['ignore'].get('years'):
            df['years'] = pd.to_numeric(df['years'], errors='coerce')  # 문자열을 숫자로 변환

            if user_input['years']:  # True인 경우 (신축 선택)
                df = df[df['years'] <= 5]  # 신축만 필터링

            # 유사도 계산에도 연식 반영
            features.append('years')
            input_values.append(0 if user_input['years'] else df['years'].median())  
            # 신축을 원하는 경우 0으로 설정 (0년에 가까울수록 더 신축임), 아니면 중간값 사용

            result_columns.append('years')
        else:
            df = df.drop('years', axis=1)

        # 역세권 처리
        if not user_input['ignore'].get('station'):
            df['sub_dist'] = pd.to_numeric(df['sub_dist'], errors='coerce')  # 문자열을 숫자로 변환
            
            if user_input['station_dist'] == 5:  # 도보 5분 이내
                df = df[df['sub_dist'] <= 400]
            elif user_input['station_dist'] == 15:  # 도보 15분 이내
                df = df[(df['sub_dist'] > 400) & (df['sub_dist'] <= 1000)]

            # 유사도 계산에도 역세권 반영
            features.append('sub_dist')
            input_values.append(0)  # 거리가 가까울수록 더 좋은 점수
        else:
            # '상관없음'인 경우에도 sub_dist는 결과에 포함
            df['sub_dist'] = pd.to_numeric(df['sub_dist'], errors='coerce')

        if not features:
            # 모든 조건이 '상관없음'이거나 feature가 없는 경우
            if df.empty:
                return []  # 필터링 후 데이터가 없는 경우
            # 랜덤으로 10개 추출하고 similarity를 0.8로 설정
            result = df.sample(n=min(10, len(df)))
            result['similarity'] = 0.8
            return result[result_columns].to_dict(orient='records')

        # NaN 값 처리
        df = df.dropna(subset=features)
        
        if df.empty:
            return []

        # 정규화
        combined = df[features].copy()
        combined.loc['user'] = input_values
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(combined)
        df_scaled = scaled[:-1]
        user_vector = scaled[-1].reshape(1, -1)

        # 정규화 변경 전전
        # scaler = MinMaxScaler()
        # df_scaled = scaler.fit_transform(df[features])
        # user_vector = scaler.transform([input_values])

        # 유사도 계산
        similarities = cosine_similarity(user_vector, df_scaled)[0]
        df['similarity'] = similarities

        # 유사한 항목 상위 10개 추천
        result = df.sort_values(by='similarity', ascending=False)
        return result[result_columns].head(10).to_dict(orient='records')



recoService = RecoService()