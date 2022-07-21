import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import dash
from dash import dcc
from dash import html

suffix_strings = ["_0-2", "_2-4", "_4-6", "_6+"]
dataframes = []


def displayData(df, suffix_string):
    df['3FG Freq'+suffix_string] = df['3FG Freq'+suffix_string].str.rstrip('%').astype('float')
    fig = make_subplots(rows=2, cols=1,  subplot_titles=("3P% vs Frequency on" +suffix_string+ "ft separation", "Frequency(%) of 3P FGA w/"+suffix_string+ "ft separation"))
    fig.add_trace(
        go.Scatter(y=df['3FG Freq'+suffix_string], x=df['3P%'+suffix_string], mode= 'markers', hovertext=df['Team'], hovertemplate='%{hovertext}<extra></extra>', showlegend = False),
        row = 1, col = 1
    )
    df2 = df[['Team', '3FG Freq'+suffix_string]]
    df2 = df2.sort_values(by= '3FG Freq'+suffix_string, ascending = False)
    fig.add_trace(
        go.Bar(x= df2['Team'], y=df2['3FG Freq'+suffix_string], showlegend= False),
        row=2, col=1
    )
    fig.update_xaxes(tickangle=90, row=2, col=1)
    fig.update_yaxes(title_text="3P FG Freq"+suffix_string+"(%)")
    fig.update_xaxes(title_text="3P% "+suffix_string +"ft sep", row = 1, col = 1)
    return fig



def makeVisualization():
    app = dash.Dash()
    fig_dropdown = html.Div([
        dcc.Dropdown(
            id='fig_dropdown',
            options=[{'label': x, 'value': x} for x in suffix_strings],
            value=None
        )])
    fig_plot = html.Div(id='fig_plot')
    app.layout = html.Div([fig_dropdown, fig_plot])

    @app.callback(
        dash.dependencies.Output('fig_plot', 'children'),
        [dash.dependencies.Input('fig_dropdown', 'value')])
    def update_output(fig_name):
        return name_to_figure(fig_name)

    def name_to_figure(fig_name):
        index = suffix_strings.index(fig_name)
        figure = displayData(dataframes[index], suffix_strings[index])
        return dcc.Graph(figure=figure)

    app.run_server(debug=True, use_reloader=False)


if __name__ == '__main__':
    for i in range(4):
        df = pd.read_csv("nba_shooting" + suffix_strings[i] + ".csv")
        dataframes.append(df)
    makeVisualization()
