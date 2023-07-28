# 세계 인구수 시각화를 위한 데이터 수집 및 시각화 과정
### REST Countries API, Google Sheets, 그리고 Google Data Studio 활용하기

## 1. 프로젝트 개요

이 프로젝트는 세계 각국의 인구 데이터를 수집하여 이를 Google Sheets에 저장하고, 이후에 Google Data Studio를 활용하여 데이터를 시각화하는 것입니다. 여기서 사용된 주요 도구와 라이브러리는 Python, REST Countries API, Google Sheets API, Google Data Studio, gspread, requests, oauth2client, 그리고 ThreadPoolExecutor입니다. 

아래는 이들 라이브러리를 설치하는 데 사용할 수 있는 Python `pip` 명령

```bash
pip install gspread oauth2client requests
```

### 사용된 도구 및 라이브러리:

- Python
- REST Countries API
- Google Sheets API
- Google Data Studio
- gspread
- requests
- oauth2client



## 2. 프로젝트 구현
### 2.1. 데이터 수집
데이터 수집 단계에서는 REST Countries API를 사용하여 세계 각국의 정보를 수집합니다. Python의 requests 라이브러리를 활용하여 API를 호출하고 JSON 형식의 응답을 파싱합니다. 수집되는 데이터는 국가 이름, 지역, 인구 등의 정보입니다.

```python
import requests

# REST Countries API로부터 데이터 가져오기
response = requests.get('https://restcountries.com/v2/all')
data = response.json()

```

### 2.2. Google Sheets에 데이터 저장
데이터 수집 후에는 Google Sheets에 데이터를 저장하는 작업이 이루어집니다. Google Sheets API와 gspread 라이브러리를 사용하여 Google Sheets와의 연동 및 데이터 입력을 수행합니다. 이때, Google Sheets API를 사용하기 위해서는 Google Cloud Console에서 API Key를 발급받아야 합니다. 발급받은 API Key는 client_secret.json 파일에 저장되어 있어야 합니다.

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets 인증 및 접속
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Google Sheets 문서 열기
sheet = client.open('Your-Google-Sheet-Name').sheet1

```

### 2.3. 데이터 저장 함수 생성
이제, 각 국가의 정보를 Google Sheets에 저장하는 함수를 정의하고 이를 실행합니다. 함수는 각 국가의 이름, 국가 코드, 대륙 코드, 지역, 지역 상세, 인구수 그리고 위도와 경도를 받아 Google Sheets에 저장, 이 때, 위도와 경도 정보가 없는 경우에는 None으로 처리한다

```python
import time

# 첫 번째 행에 가져오는 데이터 정보를 입력
header_row = ['국가명', '국가코드', '대륙코드', '지역', '지역상세', '인구수', '위도, 경도']
sheet.insert_row(header_row, 1)  # 첫 번째 행에 삽입

# 각 국가의 정보를 Google Sheets에 저장하는 함수
def save_to_google_sheets(country):
    row = [country['name'], country.get('alpha2Code'), country.get('alpha3Code'), country['region'], country['subregion'], country['population']]
    if 'latlng' in country:
        row.append(','.join(str(coord) for coord in country['latlng']))  # 위도와 경도를 하나의 문자열로 합쳐서 추가
    else:
        row.append(None)  # 위도와 경도가 없는 경우 None으로 채워집니다.
    sheet.append_row(row)
    time.sleep(1)  # 1초 대기

# 데이터 저장에 시간 간격을 두면서 Google Sheets에 저장
for country in data:
    save_to_google_sheets(country)

print("Data has been saved to Google Sheets successfully.")

```
### 2.4. 데이터 저장 및 정렬
각 국가의 정보를 Google Sheets에 저장하고, 저장된 데이터를 인구수를 기준으로 내림차순 정렬합니다.

```python
# 첫 번째 행을 제외하고, 인구수(population) 열을 기준으로 내림차순으로 정렬
sheet.sort(6, 'desc', False, 2)

print("인구수 기준으로 정렬되었습니다.")

```
## 3. Google Data Studio로 시각화
마지막으로 Google Data Studio를 활용하여 Google Sheets에 저장된 데이터를 시각화합니다. 이를 통해 국가별 인구 통계를 한눈에 볼 수 있게 됩니다. Google Data Studio에서는 다양한 차트와 그래프 형태로 데이터를 시각화할 수 있으며, 원하는 시각화 형태를 선택하고 데이터 소스를 연결하면 된다. 그리고 해당 시각화 자료에서 원하는 자료에 대해 클릭하면 드롭다운 되어 원하는 정보 확인이 가능하다

![image](https://github.com/plintAn/World-Population/assets/124107186/85a9be25-8535-4352-8209-ee9705d876b3)


## 4. 결론
이 프로젝트를 통해 REST Countries API에서 세계 각국의 인구 데이터를 가져오는 방법, 그리고 Google Sheets에 데이터를 저장하고 정렬하는 방법, 마지막으로 Google Data Studio를 통해 데이터를 시각화하는 방법을 소개하였습니다. 이렇게 수집 및 시각화된 세계 인구 통계 데이터는 각 국가의 인구 통계 및 분포를 파악하는 데 유용한 정보를 제공한다.





















