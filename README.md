# 세계 인구수 시각화
### REST Countries에서 Google Sheets로, 그리고 Google Data Studio로

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
- ThreadPoolExecutor



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
각 국가의 정보를 Google Sheets에 저장하기 위한 함수를 생성합니다. 함수는 각 국가의 이름, 지역, 인구수를 입력 받아 이를 Google Sheets에 추가합니다.

```python
# 각 국가의 정보를 Google Sheets에 저장하는 함수
def save_to_google_sheets(country):
    row = [country['name'], country['region'], country['subregion'], country['population']]
    sheet.append_row(row)
```
### 2.4. 데이터 저장 및 정렬
각 국가의 정보를 Google Sheets에 저장하고, 저장된 데이터를 인구수를 기준으로 내림차순 정렬합니다.

```python
from concurrent.futures import ThreadPoolExecutor

# 코드 시작 행에 구분 추가
header_row = ['이름', '지역', '하위지역', '인구수']
sheet.insert_row(header_row, index=1)

# ThreadPoolExecutor를 사용하여 병렬 처리
with ThreadPoolExecutor() as executor:
    executor.map(save_to_google_sheets, data)

# 시트를 인구수(population) 열을 기준으로 내림차순으로 정렬
sheet.sort((4, 'des'))

print("데이터가 구글 스프레드시트에 저장되고 정렬되었습니다.")
```
## 3. Google Data Studio로 시각화
마지막으로 Google Data Studio를 활용하여 Google Sheets에 저장된 데이터를 시각화합니다. 이를 통해 국가별 인구 통계를 한눈에 볼 수 있게 됩니다. Google Data Studio에서는 다양한 차트와 그래프 형태로 데이터를 시각화할 수 있으며, 원하는 시각화 형태를 선택하고 데이터 소스를 연결하면 됩니다.

## 4. 결론
이 프로젝트를 통해, REST Countries API에서 데이터를 가져오는 방법, Google Sheets에 데이터를 저장하고 정렬하는 방법, 그리고 Google Data Studio를 활용한 시각화에 대해 배울 수 있었습니다. 이렇게 얻어진 세계 인구 통계 데이터는 국가별 인구 통계 및 분포를 파악하는데 유용한 정보를 제공합니다.





















