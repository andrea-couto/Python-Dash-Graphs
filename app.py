'''
This file creates the webpage, connecting the data with Dash graphs
AUTHOR: ANDY COUTO
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from firebase import firebase
import requests
import sys
import plotly.plotly as py


database_url = 'https://hackernewsgraphs.firebaseio.com/'


def get_database(hn_fb_url):
    if requests.get(hn_fb_url).status_code != 200:
        sys.exit("database not found")
    else:
        HN_database = firebase.FirebaseApplication(hn_fb_url, None)
        return HN_database


def get_FB_keys(db_title, database):
    result_get = database.get(db_title, None)
    return result_get, list(result_get)


def cleaned_database_data(result_get, result_keys):
    result_data = []
    for i in range(len(result_get)):
        result_datum = result_get[result_keys[i]]
        result_data.append(result_datum)
    return result_data


def extract_data(result_data):
    result_month = []
    result_comments = []
    for i in result_data:
        month_key = list(i.keys())
        result_commentNum = list(i.values())
        result_comments.append(result_commentNum[0])
        result_month.append(month_key[0])
    return result_month, result_comments


def make_df(result_get, result_keys):
    result_month, result_comments = extract_data(cleaned_database_data(result_get, result_keys))
    result_df = pd.DataFrame({
        "months": result_month, "comments": result_comments
    })
    return result_df


def make_trace(result, dataframe):
    trace = go.Scatter(
        x=dataframe.months,
        y=dataframe.comments,
        mode="lines+markers",
        name=result
    )
    return trace


def make_traces(resultuages, database):
    data = []
    for i in resultuages:
        result_get, result_keys = get_FB_keys(i, database)
        result_df = make_df(result_get, result_keys)
        trace = make_trace(i, result_df)
        data.append(trace)
    return data


#TODO should be three functions
def get_data_for_graphs(database):
    result, result_keys = get_FB_keys('num_comments', database)
    df = make_df(result, result_keys)

    traceList = ['onsite','remote']
    data = make_traces(traceList, database)

    languages = ['python', 'c', 'java', 'cplusplus', 'csharp', 'r', 'javascript', 'php', 'go', 'swift']
    langdata = make_traces(languages, database)

    return df, data, langdata


def main():
    app = dash.Dash()
    database = get_database(database_url)
    df, data, langdata = get_data_for_graphs(database)
    app.config.suppress_callback_exceptions = True
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

    index_page = html.Div([
        html.H1(children='Hacker News Who is Hiring Project'),
        html.Div(children='''By Andy Couto'''),
        html.Br(),
        dcc.Link('Graph 1', href='/page-1'),
        html.P('Valid Comments/Thread by Month (Feb 16 - Feb 18)'),
        html.Br(),
        dcc.Link('Graph 2', href='/page-2'),
        html.P('Onsite vs Remote/Thread by Month (Feb 16 - Feb 18)'),
        html.Br(),
        dcc.Link('Graph 3', href='/page-3'),
        html.P('Prog. Lang. Jobs/Thread by Month (Feb 16 - Feb 18)'),
        html.Br(),
        dcc.Link('Graph 4', href='/page-4'),
        html.P('USA jobs per state March 2018 vs March 2017'),
    ], style={
                'textAlign': 'center',
                'color': '#7FDBFF'
            })

    page_1_layout = html.Div(children=[
        html.H1(children='Hacker News Who is Hiring Project'),

        html.Div(children='''
            By Andy Couto
        '''),

        dcc.Graph(
            id='number_comments',
            figure={
                'data': [
                    go.Bar(
                        x= df.months,
                        y= df.comments,
                        marker=dict(
                        color='rgb(158,202,225)',
                        line=dict(
                            color='rgb(8,48,107)',
                            width=1.5),
                        ),
                        opacity=0.6
                        ),
                ],
                'layout': {
                    'title': 'Valid Comments/Thread by Month (Feb 16 - Feb 18)'
                }
            }
        ),
        html.Div(id='page-1-content'),
        html.Br(),
        dcc.Link('Go to Graph 2', href='/page-2'),
        html.Br(),
        dcc.Link('Go to Graph 3', href='/page-3'),
        html.Br(),
        dcc.Link('Go to Graph 4', href='/page-4'),
        html.Br(),
        dcc.Link('Go back to home', href='/'),
    ])

    page_2_layout = html.Div(children=[
        html.H1(children='Hacker News Who is Hiring Project'),

        html.Div(children='''
            By Andy Couto
        '''),

        dcc.Graph(
            id='onsite_remote',
            figure={
                'data': data,
                'layout': {
                    'title': 'Onsite vs Remote/Thread by Month (Feb 16 - Feb 18)'
                }
            }
        ),
        html.Div(id='page-2-content'),
        html.Br(),
        dcc.Link('Go to Graph 1', href='/page-1'),
        html.Br(),
        dcc.Link('Go to Graph 3', href='/page-3'),
        html.Br(),
        dcc.Link('Go to Graph 4', href='/page-4'),
        html.Br(),
        dcc.Link('Go back to home', href='/')
    ])

    page_3_layout = html.Div(children=[
        html.H1(children='Hacker News Who is Hiring Project'),

        html.Div(children='''
            By Andy Couto
        '''),

        dcc.Graph(
            id='prog_languages',
            figure={
                'data': langdata,
                'layout': {
                    'title': 'Prog. Lang. Jobs/Thread by Month (Feb 16 - Feb 18)'
                }
            }
        ),
        html.Div(id='page-3-content'),
        html.Br(),
        dcc.Link('Go to Graph 1', href='/page-1'),
        html.Br(),
        dcc.Link('Go to Graph 2', href='/page-2'),
        html.Br(),
        dcc.Link('Go to Graph 4', href='/page-4'),
        html.Br(),
        dcc.Link('Go back to home', href='/')
    ])

    df1 = pd.read_csv('location_1.csv')
    df2 = pd.read_csv('location_2.csv')

    scl = [0, "rgb(150,0,90)"], [0.125, "rgb(0, 0, 200)"], [0.25, "rgb(0, 25, 255)"], \
          [0.375, "rgb(0, 152, 255)"], [0.5, "rgb(44, 255, 150)"], [0.625, "rgb(151, 255, 0)"], \
          [0.75, "rgb(255, 234, 0)"], [0.875, "rgb(255, 111, 0)"], [1, "rgb(255, 0, 0)"]

    page_4_layout = html.Div(children=[
        html.H1(children='Hacker News Who is Hiring Project'),

        html.Div(children='''
            By Andy Couto
        '''),

        html.Div(
            dcc.Graph(
            id='2018',
            figure={
                'data': [ dict(
                    lat=df1['latitude'],
                    lon=df1['longitude'],
                    text=df1['city']+" "+df1['occurrences'].astype(str),
                    marker=dict(
                        color=df1['occurrences'],
                        colorscale=scl,
                        reversescale=True,
                        opacity=0.7,
                        size=8+(df1['occurrences']/2),
                        ),
                    type='scattergeo'
                    )
                ],
                'layout': dict(
                    geo=dict(
                        scope='world',
                        showland=True,
                        landcolor="rgb(212, 212, 212)",
                        subunitcolor="rgb(255, 255, 255)",
                        countrycolor="rgb(255, 255, 255)",
                        showlakes=True,
                        lakecolor="rgb(255, 255, 255)",
                        showsubunits=True,
                        showcountries=True,
                        resolution=50,
                        lonaxis=dict(
                            showgrid=True,
                            gridwidth=0.5,
                            range=[-140.0, -55.0],
                            dtick=5
                        ),
                        lataxis=dict(
                            showgrid=True,
                            gridwidth=0.5,
                            range=[20.0, 60.0],
                            dtick=5
                        )
                    ),
                    title='Hacker News Location Data from March 2018',
                ),
            }
        )),

        html.Div(
            dcc.Graph(
            id = '2017',
            figure = {
                'data': [dict(
                    lat=df2['latitude'],
                    lon=df2['longitude'],
                    text=df2['city'] + " " + df2['occurrences'].astype(str),
                    marker=dict(
                        color=df2['occurrences'],
                        colorscale=scl,
                        reversescale=True,
                        opacity=0.7,
                        size=8 + (df2['occurrences'] / 2),
                    ),
                    type='scattergeo'
                )
                ],
                'layout': dict(
                    geo=dict(
                        scope='world',
                        showland=True,
                        landcolor="rgb(212, 212, 212)",
                        subunitcolor="rgb(255, 255, 255)",
                        countrycolor="rgb(255, 255, 255)",
                        showlakes=True,
                        lakecolor="rgb(255, 255, 255)",
                        showsubunits=True,
                        showcountries=True,
                        resolution=50,
                        lonaxis=dict(
                            showgrid=True,
                            gridwidth=0.5,
                            range=[-140.0, -55.0],
                            dtick=5
                        ),
                        lataxis=dict(
                            showgrid=True,
                            gridwidth=0.5,
                            range=[20.0, 60.0],
                            dtick=5
                        )
                    ),
                    title='Hacker News Location Data from March 2017',
                ),
            }
        )),

        html.Div(id='page-4-content'),
        html.Br(),
        dcc.Link('Go to Graph 1', href='/page-1'),
        html.Br(),
        dcc.Link('Go to Graph 2', href='/page-2'),
        html.Br(),
        dcc.Link('Go to Graph 3', href='/page-3'),
        html.Br(),
        dcc.Link('Go back to home', href='/')
    ])

    # Update the index
    @app.callback(dash.dependencies.Output('page-content', 'children'),
                  [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/page-1':
            return page_1_layout
        elif pathname == '/page-2':
            return page_2_layout
        elif pathname == '/page-3':
            return page_3_layout
        elif pathname == '/page-4':
            return page_4_layout
        else:
            return index_page
        # Could also return a 404 "URL not found" page here

    app.css.append_css({
        'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    })

    app.run_server(debug=True)


if __name__ == '__main__':
    main()