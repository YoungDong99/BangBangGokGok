import urllib.request
from urllib.request import urlopen
import json

class MainService:
    #구 번호(cortarNo) 가져오기
    def getcortarGu(self, guName):
        cortarObj={}
        if guName == "강남구":
            cortarObj={"cortarNo":"1168000000","centerLat":37.517408,"centerLon":127.047313,"cortarName":"강남구","cortarType":"dvsn"}
        elif guName == "강동구":
            cortarObj={"cortarNo":"1174000000","centerLat":37.530126,"centerLon":127.123771,"cortarName":"강동구","cortarType":"dvsn"}
        elif guName == "강북구":
            cortarObj={"cortarNo":"1130500000","centerLat":37.63974,"centerLon":127.025488,"cortarName":"강북구","cortarType":"dvsn"}
        elif guName == "강서구":
            cortarObj={"cortarNo":"1150000000","centerLat":37.550985,"centerLon":126.849534,"cortarName":"강서구","cortarType":"dvsn"}
        elif guName == "관악구":
            cortarObj={"cortarNo":"1162000000","centerLat":37.481021,"centerLon":126.951601,"cortarName":"관악구","cortarType":"dvsn"}
        elif guName == "광진구":
            cortarObj={"cortarNo":"1121500000","centerLat":37.538617,"centerLon":127.082375,"cortarName":"광진구","cortarType":"dvsn"}
        elif guName == "구로구":
            cortarObj={"cortarNo":"1153000000","centerLat":37.49551,"centerLon":126.887532,"cortarName":"구로구","cortarType":"dvsn"}
        elif guName == "금천구":
            cortarObj={"cortarNo":"1154500000","centerLat":37.45196,"centerLon":126.902075,"cortarName":"금천구","cortarType":"dvsn"}
        elif guName == "노원구":
            cortarObj={"cortarNo":"1135000000","centerLat":37.654286,"centerLon":127.056411,"cortarName":"노원구","cortarType":"dvsn"}
        elif guName == "도봉구":
            cortarObj={"cortarNo":"1132000000","centerLat":37.668768,"centerLon":127.047163,"cortarName":"도봉구","cortarType":"dvsn"}
        elif guName == "동대문구":
            cortarObj={"cortarNo":"1123000000","centerLat":37.574493,"centerLon":127.039765,"cortarName":"동대문구","cortarType":"dvsn"}
        elif guName == "동작구":
            cortarObj={"cortarNo":"1159000000","centerLat":37.51245,"centerLon":126.9395,"cortarName":"동작구","cortarType":"dvsn"}
        elif guName == "마포구구":
            cortarObj={"cortarNo":"1144000000","centerLat":37.563517,"centerLon":126.9084,"cortarName":"마포구","cortarType":"dvsn"}
        elif guName == "서대문구":
            cortarObj={"cortarNo":"1141000000","centerLat":37.579225,"centerLon":126.9368,"cortarName":"서대문구","cortarType":"dvsn"}
        elif guName == "서초구":
            cortarObj={"cortarNo":"1165000000","centerLat":37.483564,"centerLon":127.032594,"cortarName":"서초구","cortarType":"dvsn"}
        elif guName == "성동구구":
            cortarObj={"cortarNo":"1120000000","centerLat":37.563475,"centerLon":127.036838,"cortarName":"성동구","cortarType":"dvsn"}
        elif guName == "성북구":
            cortarObj={"cortarNo":"1129000000","centerLat":37.5874,"centerLon":127.020729,"cortarName":"성북구","cortarType":"dvsn"}
        elif guName == "송파구":
            cortarObj={"cortarNo":"1171000000","centerLat":37.514592,"centerLon":127.105863,"cortarName":"송파구","cortarType":"dvsn"}
        elif guName == "양천구":
            cortarObj={"cortarNo":"1147000000","centerLat":37.517007,"centerLon":126.866546,"cortarName":"양천구","cortarType":"dvsn"}
        elif guName == "영등포구":
            cortarObj={"cortarNo":"1156000000","centerLat":37.526367,"centerLon":126.896213,"cortarName":"영등포구","cortarType":"dvsn"}
        elif guName == "용산구":
            cortarObj={"cortarNo":"1117000000","centerLat":37.538825,"centerLon":126.96535,"cortarName":"용산구","cortarType":"dvsn"}
        elif guName == "은평구":
            cortarObj={"cortarNo":"1138000000","centerLat":37.60278,"centerLon":126.929163,"cortarName":"은평구","cortarType":"dvsn"}
        elif guName == "종로구":
            cortarObj={"cortarNo":"1111000000","centerLat":37.573025,"centerLon":126.979638,"cortarName":"종로구","cortarType":"dvsn"}
        elif guName == "중구":
            cortarObj={"cortarNo":"1114000000","centerLat":37.563842,"centerLon":126.9976,"cortarName":"중구","cortarType":"dvsn"}
        elif guName == "중랑구":
            cortarObj={"cortarNo":"1126000000","centerLat":37.606324,"centerLon":127.092584,"cortarName":"중랑구","cortarType":"dvsn"}
        return cortarObj
    
    #구 번호로 동 cortarNo 가져오기
    def getcortarDong(self, cortarNo, dongNm):
        dong_list = []
        url = r"https://new.land.naver.com/api/regions/list?cortarNo=" + cortarNo
        #해당 url은 봇 접근을 차단하고있음 -> 헤더 정보를 추가해서 bot이 아닌것처럼 행동하기
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req) as response:
                byte_data = response.read()
                text_data = byte_data.decode("utf-8")
                json_data = json.loads(text_data)
                dong_list = json_data.get("regionList", [])
                for d in dong_list :
                    if d['cortarName'] == dongNm :
                        return d
                return {'cortarNo': '-1', 'abnomalData' : dongNm}

        except urllib.error.HTTPError as e:
            print("getcortarDong - HTTPError:", e.code, e.reason)
        except urllib.error.URLError as e:
            print("getcortarDong - URLError:", e.reason)
    
    #해당 동의 위치정보 가져오기
    def getLatLon(self, cortarDong):
        url = f"https://new.land.naver.com/api/cortars?zoom=16&centerLat={cortarDong['centerLat']}&centerLon={cortarDong['centerLon']}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req) as response:
                byte_data = response.read()
                text_data = byte_data.decode("utf-8")
                json_data = json.loads(text_data)
               
                return json_data.get("cortarVertexLists", [])[0]

        except urllib.error.HTTPError as e:
            print("getlatLon - HTTPError:", e.code, e.reason)
        except urllib.error.URLError as e:
            print("getlatLon - URLError:", e.reason)
 
    #위치정보 기반으로 최종 아파트 매물 리스트 가져오기
    def getAptList(self, aptCon, coords):     
        
        latitudes = [lat for lat, lon in coords]
        longitudes = [lon for lat, lon in coords]

        # 최댓값과 최솟값 계산
        min_lat = min(latitudes)
        max_lat = max(latitudes)
        min_lon = min(longitudes)
        max_lon = max(longitudes)

        # 결과 출력
        # print(f"최소 위도: {min_lat}")
        # print(f"최대 위도: {max_lat}")
        # print(f"최소 경도: {min_lon}")
        # print(f"최대 경도: {max_lon}")
        
        #최종 파라미터
        base_url = "https://new.land.naver.com/api/complexes/single-markers/2.0"
        # 파라미터 정의 (JSON 형태 + 설명 주석)
        params = {
            "cortarNo": aptCon['cortarNo'],              # 행정동 코드 (예: 서울 강남구 역삼동)
            "zoom": 16,                            # 지도 줌 레벨
            "priceType": "RETAIL",                 # 가격 타입: RETAIL = 일반매매
            "markerId": "",                        # 마커 ID (선택된 마커가 있을 경우 지정)
            "markerType": "",                      # 마커 타입 (ex: 단지, 건물 등)
            "selectedComplexNo": "",              # 선택된 단지 번호
            "selectedComplexBuildingNo": "",      # 선택된 건물 번호
            "fakeComplexMarker": "",              # 가상 단지 마커 여부
            "realEstateType": "APT",              # 부동산 유형: APT = 아파트
            "tradeType": "A1",                    # 거래 유형: A1 = 매매, B1 = 전세, B2 = 월세
            "tag": "::::::::",                    # 태그 필터 (URL 인코딩된 상태, 비워두면 필터 없음)
            "rentPriceMin": 0,                    # 최소 임대 가격
            "rentPriceMax": aptCon['priceMax'],          # 최대 임대 가격
            "priceMin": aptCon['priceMin'],                        # 최소 매매가 (단위: 만 원 → 5억 원)
            "priceMax": aptCon['priceMax'],                   # 최대 매매가 (단위: 만 원 → 12억 원)
            "areaMin": aptCon['areaMin'],                       # 최소 전용면적 (㎡)
            "areaMax": aptCon['areaMax'],                       # 최대 전용면적 (㎡)
            "oldBuildYears": aptCon['years'],                  # 오래된 건물 기준 필터 (미지정)
            "recentlyBuildYears": "",            # 최근 건축 연도 필터 (미지정)
            "minHouseHoldCount": "" ,            # 최소 세대 수
            "maxHouseHoldCount": "",             # 최대 세대 수 (미지정)
            "showArticle": "false",              # 매물 정보 표시 여부
            "sameAddressGroup": "false",         # 동일 주소 그룹 여부
            "minMaintenanceCost": "",            # 최소 관리비 (미지정)
            "maxMaintenanceCost": "",            # 최대 관리비 (미지정)
            "directions": "",                    # 방향 (동향, 남향 등 필터, 미지정)
            "leftLon": {min_lon},              # 지도 좌측 경도
            "rightLon": {max_lon},             # 지도 우측 경도
            "topLat": {max_lat},                # 지도 상단 위도
            "bottomLat": {min_lat},             # 지도 하단 위도
            "isPresale": "false"                 # 분양 여부: false는 기존 매물
        }
        
        query_string = urllib.parse.urlencode(params, doseq=True)
        final_url = f"{base_url}?{query_string}"
        # print(final_url)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        fin_req = urllib.request.Request(final_url, headers=headers)
        
        try:
            with urllib.request.urlopen(fin_req) as response:
                byte_data = response.read()
                text_data = byte_data.decode("utf-8")
                json_data = json.loads(text_data)
                
                return json_data
        
        except urllib.error.HTTPError as e:
            print("getAptList - HTTPError:", e.code, e.reason)
        except urllib.error.URLError as e:
            print("getAptList - URLError:", e.reason)

    # 아파트 매물 상세 정보 가져오기
    def getAptSaleInfo(self, complexNo):
        url = f"https://new.land.naver.com/api/complexes/overview/{complexNo}?complexNo={complexNo}&isClickedMarker=true"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        req = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(req) as response:
                byte_data = response.read()
                text_data = byte_data.decode("utf-8")
                json_data = json.loads(text_data)
                
                return json_data

        except urllib.error.HTTPError as e:
            print("getAptSaleInfo - HTTPError:", e.code, e.reason)
        except urllib.error.URLError as e:
            print("getAptSaleInfo - URLError:", e.reason)


    

mainService = MainService()