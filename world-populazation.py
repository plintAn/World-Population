import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# REST Countries API로부터 데이터 가져오기
response = requests.get('https://restcountries.com/v2/all')
data = response.json()

# Google Sheets 인증 및 접속
scope = ['your',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Google Sheets 문서 열기 (해당 코드에서는 문서명을 'Your-Google-Sheet-Name'으로 변경해야 합니다.)
sheet = client.open('feeds').sheet1

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

# 첫 번째 행을 제외하고, 인구수(population) 열을 기준으로 내림차순으로 정렬
sheet.sort(5, 'desc', False, 2)

print("인구수 기준으로 정렬되었습니다.")
