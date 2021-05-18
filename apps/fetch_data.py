import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm 
import mysql.connector
from mysql.connector import errorcode
import sqlalchemy as db

def prem_year_mapper():
    return {
        'PREM_20_21': 667,
        'PREM_19_20':639,
        'PREM_18_19':614,
        'PREM_17_18':586,
        'PREM_16_17':556,
    }

def prem_team_mapper2():
    return {
        'Manchester City':14,
        'Manchester United':3,
        'Leicester City': 13,
        'Chelsea':8,    
        'Liverpool':4,
        'West Ham United':21,
        'Tottenham Hotspur':19,
        'Everton':10,
        'Arsenal':5,
        'Leeds United':12,
        'Aston Villa':24,
        'Wolverhampton Wanderers':63,
        'Southampton':18,
        'Burnley':54,
        'Newcastle United':16,
        'Crystal Palace':35,
        'Brighton & Hove Albion':749,
        'Fulham':55,
        'West Bromwich Albion':64,
        'Sheffield United':27
    }

def get_data(year,team):
    base_url = f'https://www.statbunker.com/competitions/TopGoalScorers?comp_id={year}&club_id={team}'
    html = requests.get(base_url).content
    df_list = pd.read_html(html)
    return df_list

def main():
    res = pd.DataFrame()
    years = prem_year_mapper()
    teams = prem_team_mapper2()
    for m,s in years.items():
        for k,v in tqdm(teams.items()):
            try:
                data = get_data(s,v)[0]
                data['team'] = [k for x in range(len(data))]
                res = pd.concat([res,data],ignore_index=True)
            except ValueError:
                print('THIS DID NOT WORK:',k,m)
    return res

def mysql_writer(data):
    engine = db.create_engine('mysql+mysqldb://root:mulberry.1206@127.0.0.1:3306/Kindred')
    data.to_sql('Top_Goal_Scorers',con=engine,if_exists='append')
    return None

if __name__=="__main__":
    res = main()
    db = mysql_writer(res)
    print('Complete')

