from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree

import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np

raw_data = 'F:/40_20211005_ML/project/raw_data/pasteurizer.csv'

df = pd.read_csv(raw_data)

#결측치 전부 제거
df = df.dropna()

#DataFrame간 비트연산 가능함
condition_MIXA_PASTEUR_STATE = (df['MIXA_PASTEUR_STATE'] == 0) | (df['MIXA_PASTEUR_STATE'] == 1)
#condition_MIXA_PASTEUR_STATE = df.MIXA_PASTEUR_STATE < 2
df = df[condition_MIXA_PASTEUR_STATE]

condition_temp_zero = (df['MIXA_PASTEUR_TEMP'] != 0) & (df['MIXB_PASTEUR_TEMP'] != 0)
df = df[condition_temp_zero]

#우선 Pasteur 상태 Column Drop
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

#feature_names = df.columns[1:5]
feature_names = df.columns[1:3]

target_name = np.array(['0', '1'])

#동일한 조건에서, KNeighborsClassifier 알고리즘 분석해보기
neigh = KNeighborsClassifier(n_neighbors=3)
#neigh = neigh.fit(X_train, y_train)
neigh.fit(X_train, y_train)

#neigh_prediction = neigh.predict(X_test)

#prediction 결과 그래프로 띄우기
y_score = neigh.predict_proba(X_test)[:, 1]

#fig용 split data 따로 만들기
sample_df = df.sample(n=500)
sp_X = sample_df.iloc[:, 1:3].values
sp_y = sample_df.iloc[:, -1:].values
#'OK'이면 1, 아니면 0
sp_y = np.where(sp_y == 'OK', 1, 0)
#1차원으로 변경(flatten)
sp_y = sp_y.ravel()
#Train set, test set
sp_X_train, sp_X_test, sp_y_train, sp_y_test = train_test_split(sp_X, sp_y, test_size=0.3, random_state=1)

#prediction 결과 그래프로 띄우기
sp_y_score = neigh.predict_proba(sp_X_test)[:, 1]

fig = px.scatter(
    sp_X_test, x=0, y=1,
    color=sp_y_score, color_continuous_scale='RdBu',
    symbol=sp_y_test, symbol_map={'0': 'square-dot', '1': 'circle-dot'},
    labels={'symbol': 'label', 'color': 'score of <br>first class'}
)

fig.update_traces(marker_size=12, marker_line_width=1.5)
fig.update_layout(legend_orientation='h')

#dash로 띄우기
import dash
from dash import dcc
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
   dcc.Graph(figure=fig)
])

app.run_server(debug=True)