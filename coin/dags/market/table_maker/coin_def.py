import requests
import pandas as pd
from sqlalchemy import create_engine

def coin_name():
# MySQL 연결 설정
    engine = create_engine('mysql+pymysql://inseong:Kiminseong!1@coinMysql/coin?charset=utf8mb4')
    '''코인 이름
    형식
    [{"market":"BTC-KRW","korean_name":"비트코인","english_name":"bitcoin"}]
    '''
######## 마켓 코드 가져오기
    url = "https://api.upbit.com/v1/market/all?isDetails=false"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    name_list = pd.DataFrame(response.json())

    print(name_list)
##############마켓코드를 데이터프레임으로 만들어서 sql로 저장
    table_name = 'coin_name' 

    name_list.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

    engine.dispose()
    return name_list

############ 분봉정보 저장
######데이터베이스 테이블 이름은 -가 사용 불가하여 _로 변경
def min_table(name_list):

    engine = create_engine('mysql+pymysql://inseong:Kiminseong!1@coinMysql/coin?charset=utf8mb4')

    name_list['market'].replace('-', '_',inplace=True)

    #확인
    print(name_list)

    #코인별 테이블 만들어서 데이터 넣어두기
    for coin_name in name_list['market']:

        url = (f"https://api.upbit.com/v1/candles/minutes/1?market={coin_name}&count=1")

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        name_list = pd.DataFrame(response.json())

        name_list.to_sql(name=coin_name, con=engine, if_exists='append', index=False)
    engine.dispose()