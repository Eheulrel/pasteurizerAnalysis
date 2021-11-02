#학습, 테스트 데이터 분포 확인

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np

import plotly.graph_objects as go

raw_data = 'F:/40_20211005_ML/project/raw_data/pasteurizer.csv'

df = pd.read_csv(raw_data)

#결측치 존재하는 행 전부 제거
df = df.dropna()

#DataFrame간 비트연산 가능함
condition_MIXA_PASTEUR_STATE = (df['MIXA_PASTEUR_STATE'] == 0) | (df['MIXA_PASTEUR_STATE'] == 1)
#condition_MIXA_PASTEUR_STATE = df.MIXA_PASTEUR_STATE < 2
df = df[condition_MIXA_PASTEUR_STATE]

#온도가 0인 행 제거
condition_temp_zero = (df['MIXA_PASTEUR_TEMP'] != 0) & (df['MIXB_PASTEUR_TEMP'] != 0)
df = df[condition_temp_zero]

#우선 Pasteur 상태 Column Drop
#(Graph 그리기용)
df.drop(columns='MIXA_PASTEUR_STATE', inplace=True)
df.drop(columns='MIXB_PASTEUR_STATE', inplace=True)

#데이터 분리

#측정데이터와 레이블(정답)을 분리
#X = df.iloc[:, 1:5].values
X = df.iloc[:, 1:3].values

y = df.iloc[:, -1:].values

#'OK'이면 1, 아니면 0
y = np.where(y == 'OK', 1, 0)
#1차원으로 변경(flatten)
y = y.ravel()

#Train set, test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

trace_spaces = [
    [X_train, y_train, 0, 'Train', 'square'],
    [X_train, y_train, 1, 'Train', 'circle'],
    [X_test, y_test, 0, 'Test', 'square-dot'],
    [X_test, y_test, 1, 'Test', 'circle-dot']
]

fig = go.Figure(data=[
    go.Scatter(
        x=X[y==label, 0], y=X[y==label, 1],
        name=f'{split} Split, Label {label}',
        mode='markers', marker_symbol=marker
    )
    for X, y, label, split, marker in trace_spaces
])

fig.update_traces(
    marker_size=12, marker_line_width=1.5,
    marker_color="lightyellow"
)

#dash로 띄우기
import dash
#import dash_core_components as dcc #Deprecated
from dash import dcc
#import dash_html_components as html #Deprecated
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)