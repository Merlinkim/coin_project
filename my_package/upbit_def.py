import requests
import pandas as pd
from sqlalchemy import create_engine

#def coin_name():
# MySQL 연결 설정
#    engine = create_engine('mysql+pymysql://inseong:Kiminseong!1@coinMysql/coin?charset=utf8mb4')
#    '''코인 이름
#    형식
#    [{"market":"BTC-KRW","korean_name":"비트코인","english_name":"bitcoin"}]
#    '''
######## 마켓 코드 가져오기
#    url = "https://api.upbit.com/v1/market/all?isDetails=false"
#
#    headers = {"accept": "application/json"}

#    response = requests.get(url, headers=headers)

#    name_list = pd.DataFrame(response.json())

#    print(name_list)
##############마켓코드를 데이터프레임으로 만들어서 sql로 저장
#    table_name = 'coin_name' 

#    name_list.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

#    engine.dispose()
#    return name_list

############ 분봉정보 저장
#####데이터베이스 테이블 이름은 -가 사용 불가하여 _로 변경
def min_data(savePath):
    json_name = f'{savePath}/name.json'
    df = pd.read_json(json_name)

    df.drop(columns=['korean_name','english_name'],axis=1,inplace=True)

    df['market']=df['market'].str.replace("-",'_')

    df.to_csv(f'{savePath}min_name.txt', sep = '\n' , index =False, header=False)

    return df


######### 데이터 비교 및 추가 삭제
def compare_by_df(origin,new):

    origin_df = pd.read_json(origin)

    new_df = pd.read_json(new)

    if not origin_df.equals(new_df):

        temp_df=pd.concat([origin_df,new_df])

        temp_df.drop_duplicates(inplace=True)

        temp_df.to_json('/Users/merlinkim/tmp/data/tmp/name.json')

        return print("name data has been changed. please check the changed data")
    
    else :

        origin_df.to_json('/Users/merlinkim/tmp/data/tmp/name.json')

        return print("name data didn't changed")


