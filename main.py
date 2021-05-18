from dash.dependencies import Input, Output, State
import dash
import dash_core_components as dcc 
import dash_html_components as html
import pandas as pd 
import dash_table
import numpy as np
import plotly.express as px 
from apps.app import dash_app
from apps.template import app_layout
import datetime as dt
import requests
from tqdm import tqdm 
import mysql.connector
from mysql.connector import errorcode
import sqlalchemy as db
import sys

engine = db.create_engine('mysql+mysqldb://root:limetree123@127.0.0.1:3306/Kindred')
dash_app = dash_app
dash_app.layout = app_layout()
app = dash_app.server

@dash_app.callback(
    [Output(component_id='get_data_table',component_property='data'),
    Output(component_id='get_data_table',component_property='columns'),
    Output(component_id='get_success',component_property='children'),
    Output(component_id='get_store',component_property='data')],
    Input(component_id='get_data',component_property='n_clicks'),
    prevent_initial_call=True
)
def get_goal_data(n_clicks):
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
        """return dataframe of concated team data"""
        res = pd.DataFrame()
        years = prem_year_mapper()
        teams = prem_team_mapper2()
        for m,s in years.items():
            for k,v in tqdm(teams.items()):
                try:
                    data = get_data(s,v)[0]
                    data['team'] = [k for x in range(len(data))]
                    data['year'] = [m for x in range(len(data))]
                    res = pd.concat([res,data],ignore_index=True)
                except ValueError:
                    pass
        return res

    if n_clicks > 0:
        res = main()
        res_full = res.to_json(orient='records')
        columns = [{'id':str(k),'name':str(k)} for k in res.columns]
        res_red = res.head(30).to_dict(orient='records')
        get_success='Yes'
    else:
        pass
    return res_red, columns, get_success, res_full

@dash_app.callback(
    [Output(component_id='check_data_table',component_property='data'),
    Output(component_id='check_data_table',component_property='columns'),
    Output(component_id='check_success',component_property='children'),
    Output(component_id='check_store',component_property='data')],
    [Input(component_id='check_data',component_property='n_clicks'),
    Input(component_id='get_store',component_property='data')],
    prevent_initial_call=True
)
def get_check_table(n_clicks,data):
    data = pd.read_json(data)
    # need to read from database and check
    old_data = pd.read_sql_table('Top_Goal_Scorers',engine)
    same_cols = [x for x in data.columns if x in old_data.columns]
    diff = pd.concat([data[same_cols],old_data[same_cols]]).drop_duplicates(keep=False)
    diff_store = diff.to_json(orient='records')
    diff_res = diff.to_dict(orient='records')
    diff_cols = [{'id':str(k),'name':str(k)} for k in diff.columns]
    check_success = 'SUCCESS'
    return diff_res, diff_cols, check_success, diff_store

@dash_app.callback(
    Output(component_id='data_write',component_property='children'),
    [Input(component_id='write_data',component_property='n_clicks'),
    Input(component_id='check_store',component_property='data')]
)
def write_to_db(n_clicks,data):
    data = pd.read_json(data)
    if n_clicks > 0:
        data.to_sql('Top_Goal_Scorers',con=engine,if_exists='append')
        check_success = 'SUCCESS'
    else:
        check_success='FAIL'
    return check_success

if __name__=="__main__":
    dash_app.run_server(host='0.0.0.0',threaded=True, debug=True, port=8080)