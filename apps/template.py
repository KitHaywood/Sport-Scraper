import dash
import dash_core_components as dcc 
import dash_html_components as html 
import dash_table

def app_layout():
    return html.Div(style={
        'backgroundColor':'#303030'
    },children=[
        dcc.Store(id='get_store'),
        dcc.Store(id='check_store'),
        html.H1(
            children='Sample Scraper of StatsBunker',
            style={'textAlign':'center','color':'white'}
            ),
        html.Div(className='row',children=[
            html.Label(['Get/Load Goal Data'],style={'text-align':'center','color':'white'}),
            html.Button('Get Data',id='get_data',n_clicks=0),
            html.Div(id='get_success',children='Was the database write successful?'),
            html.Div(style={'margin':'20px'},children=[
            dcc.Loading(id='get_data_loading',children=[
                dash_table.DataTable(
                    id='get_data_table',
                    style_table={
                        'border': '1px solid white',
                        'borderRadius': '15px',
                        'overflow': 'hidden'
                    },
                    style_header={'backgroundColor':'rgb(30,30,30)'},
                    style_cell={
                        'backgroundColor':'rgb(50,50,50)',
                        'color':'white',
                        'margin':'2px'
                    }
                )
                ])]),
            html.Label(['Check Against Existing Database'],style={'text-align':'center','color':'white'}),
            html.Button('Check Data',id='check_data',n_clicks=0),
            html.Div(id='check_success',children='Was the check successful?'),
            html.Div(style={'margin':'20px'},children=[
            dcc.Loading(id='get_check_loading',children=[
                dash_table.DataTable(
                    id='check_data_table',
                    style_table={
                        'border': '1px solid white',
                        'borderRadius': '15px',
                        'overflow': 'hidden'
                    },
                    style_header={'backgroundColor':'rgb(30,30,30)'},
                    style_cell={
                        'backgroundColor':'rgb(50,50,50)',
                        'color':'white',
                        'margin':'2px'
                    }
                )
                ])]),
            html.Button('Write Data', id='write_data',n_clicks=0),
            html.Div(id='data_write',children='was the write successful?')
            ])

    ])