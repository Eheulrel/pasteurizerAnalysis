#Dash로 URL Routing 해보기

import dash
from dash import dcc
from dash import html

import rawData
import preProcess
import heatMap
import kNN

external_scripts = [
    {
        'src':'https://use.fontawesome.com/releases/v5.15.3/js/all.js',
        'crossorigin':'anonymous'
    },
    {
        'src':'https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js'
    }
]

external_stylesheets = [
    {
        'href': 'https://fonts.googleapis.com/css?family=Lora:400,700,400italic,700italic',
        'rel': 'stylesheet',
        'type': 'text/css'
    },
    {
        'href': 'https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800',
        'rel': 'stylesheet',
        'type': 'text/css'
    }
]

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = [
    html.Nav(
        className='navbar navbar-expand-lg navbar-light',
        id='mainNav',
        children=html.Div(
            className='container px-4 px-lg-5',
            children=[
                html.A(
                    className='navbar-brand',
                    href='/',
                    children='미니 프로젝트 2조'                    
                ),
                html.Button(
                    className='navbar-toggler',
                    type='button',
                    **{
                        'data-bs-toggle':"collapse",
                        'data-bs-target':"#navbarResponsive",
                        'aria-controls':"navbarResponsive",
                        'aria-expanded':"false",
                        'aria-label':"Toggle navigation"
                    },
                    children=[
                        '메뉴  ',
                        html.I(className="fas fa-bars")
                    ]
                ),
                html.Div(
                    className="collapse navbar-collapse",
                    id="navbarResponsive",
                    children=[
                        html.Ul(
                            className="navbar-nav ms-auto py-4 py-lg-0",
                            children=[
                                html.Li(
                                    className='nav-item',
                                    children=html.A(
                                        className="nav-link px-lg-3 py-3 py-lg-4",
                                        href='/assets/html/Project_code.html',
                                        children='분석코드'
                                    )
                                ),
                                html.Li(
                                    className='nav-item',
                                    children=html.A(
                                        className="nav-link px-lg-3 py-3 py-lg-4",
                                        href='/assets/ppt/00. 양식_미니프로젝트_2조.pdf',
                                        children='Presentation'
                                    )
                                ),
                                html.Li(
                                    className='nav-item',
                                    children=html.A(
                                        className="nav-link px-lg-3 py-3 py-lg-4",
                                        href='https://www.kamp-ai.kr/front/dataset/AiDataDetail.jsp?AI_SEARCH=&page=1&DATASET_SEQ=10&EQUIP_SEL=&FILE_TYPE_SEL=&GUBUN_SEL=&WDATE_SEL=',
                                        children='데이터셋'
                                    )
                                )
                            ]
                        ),
                    ]
                )

            ],
        )
    ),
    html.Header(
        className='masthead',
        style={'backgroundImage': "url('/assets/img/pasteur.png')"},
        children=html.Div(
            className='container position-relative px-4 px-lg-5',
            children=html.Div(
                className='row gx-4 gx-lg-5 justify-content-center',
                children=html.Div(
                    className="col-md-10 col-lg-8 col-xl-7",
                    children=html.Div(
                        className="site-heading",
                        children=[
                            html.H2('살균기 AI 데이터셋을 이용한'),
                            html.H2('기계학습 및 분석'),

                            html.Span(
                                className="subheading",
                                style={'fontSize':'15px'},
                                children='(의사결정나무 및 kNN 알고리즘을 중심으로)'
                            )
                        ]
                    )
                )
            )
        )
    ),
    html.Div(
        className="container px-4 px-lg-5",
        children=html.Div(
            className="row gx-4 gx-lg-5 justify-content-center",
            children=html.Div(
                className="col-md-10 col-lg-8 col-xl-7",
                children=[
                    html.Div(
                        className="post-preview",
                        children=[
                            html.H2(
                                className='post-title',
                                children='1. 분석 배경 및 목적',
                            ),
                            html.P(
                                className="post-subtitle",
                                children='　가열살균공정은 식품제조 공정 중 하나로, HACCP(식품안전관리인증기준)과 별개로 생산품 품질 유지에 어려움이 있음.'
                            ),
                            html.P(
                                className="post-subtitle",
                                children='　품질에 영향을 미치는 독립변수를 식별하고, 품질검사 결과를 종속변수로 하여, 수집된 데이터를 기반으로 원인 분석 뿐만 아니라 기계학습 모델을 이용하여 예견된 불량을 효율적으로 방지하고자 함.'
                            ),
                        ]
                        
                    ),
                    html.Br(),
                    html.Br(),
                    html.Hr(),
                    html.Div()
                ]
            )

        )
    ),
    html.Div(
        className="container px-4 px-lg-5",
        children=html.Div(
            className="row gx-4 gx-lg-5 justify-content-center",
            children=html.Div(
                className="col-md-10 col-lg-8 col-xl-7",
                children=[
                    html.Div(
                        className="post-preview",
                        children=[
                            html.H2(
                                className='post-title',
                                children='2. 데이터 확인 및 전처리',
                            ),
                            html.P(
                                className="post-subtitle",
                                children='독립변수 : 살균기 작동상태, 작동온도'
                            ),
                            html.P(
                                className="post-subtitle",
                                children='종속변수 : 불량여부'
                            ),
                            html.P(
                                className="post-subtitle",
                                children='결측값 식별 및 처리 : 0, NaN => Drop'
                            ),

                            html.Pre('''
df.info()
Last executed at 2021-11-03 06:29:07 in 947ms
class pandas.core.frame.DataFrame
RangeIndex: 210794 entries, 0 to 210793
Data columns (total 6 columns):
#   Column              Non-Null Count   Dtype  
---  ------              --------------   -----  
0   STD_DT              210794 non-null  object 
1   MIXA_PASTEUR_STATE  11135 non-null   float64 
2   MIXB_PASTEUR_STATE  10255 non-null   float64 
3   MIXA_PASTEUR_TEMP   201423 non-null  float64 
4   MIXB_PASTEUR_TEMP   198802 non-null  float64 
5   INSP                210794 non-null  object  
dtypes: float64(4), object(2) 
memory usage: 9.6+ MB 
                            '''),
                            html.Br(),

                            '(전처리 전)',
                            html.Br(),
                            'PasteurizerB 비정상값 확인 外',
                            dcc.Graph(figure=rawData.output()),
                            '(전처리 후)',
                            dcc.Graph(figure=preProcess.output()),
                            'Correlation Coefficient Analysis',
                            html.Br(),
                            ' =>살균기A 온도, 살균기B 온도의 상관관계 높음',
                            html.Br(),
                            '(상관계수가 높다고 하여 인과관계가 있다고 볼 수는 없음)',
                            dcc.Graph(figure=heatMap.output(1)),
                            # html.Iframe(
                            #     src='/assets/html/chart/heatmap_a.html',
                            #     width='550',
                            #     height='600'
                            # ),
                            html.Br(),
                            '=>산점도 매트릭스',
                            dcc.Graph(figure=heatMap.output(2))
                            # html.Iframe(
                            #         src='/assets/html/chart/scatter_a.html',
                            #         width='880',
                            #         height='880',
                            #         )
                        ]
                    ),
                    html.Hr(),
                    html.Div()
                ]
            )
        )
    ),
    html.Div(
        className="container px-4 px-lg-5",
        children=html.Div(
            className="row gx-4 gx-lg-5 justify-content-center",
            children=html.Div(
                className="col-md-10 col-lg-8 col-xl-7",
                children=[
                    html.Div(
                        className="post-preview",
                        children=[
                            html.H2(
                                className='post-title',
                                children='3. DecisionTree 분석',
                            ),
                            html.Img(
                                src='/assets/img/dtree.png',
                                width='100%',
                                height='100%'
                            )
                        ]
                    ),
                    html.Hr(),
                    html.Div()
                ]
            )
        )
    ),
    html.Div(
        className="container px-4 px-lg-5",
        children=html.Div(
            className="row gx-4 gx-lg-5 justify-content-center",
            children=html.Div(
                className="col-md-10 col-lg-8 col-xl-7",
                children=[
                    html.Div(
                        className="post-preview",
                        children=[
                            html.H2(
                                className='post-title',
                                children='4. kNN 분석',
                            ),
                            '데이터로부터 가장 가까운 k개의 다른 데이터의 레이블을 참조하는 방식의 알고리즘',
                            html.Br(),
                            '(k=5)',
                            dcc.Graph(figure=kNN.output())
                        ]
                    ),
                    html.Hr(),
                    html.Div()
                ]
            )
        )
    ),
    html.Div(
        className="container px-4 px-lg-5",
        children=html.Div(
            className="row gx-4 gx-lg-5 justify-content-center",
            children=html.Div(
                className="col-md-10 col-lg-8 col-xl-7",
                children=[
                    html.Div(
                        className="post-preview",
                        children=[
                            html.H2(
                                className='post-title',
                                children='5. 느낀점',
                            )
                        ]
                    ),
                    html.Div()
                ]
            )
        )
    ),

    html.Footer(
        className='border-top',
        children=html.Div(
            className="container px-4 px-lg-5",
            children=html.Div(
                className="row gx-4 gx-lg-5 justify-content-center",
                children=html.Div(
                    className="col-md-10 col-lg-8 col-xl-7",
                    children=html.Ul(
                        className="list-inline text-center",
                        children=[
                            html.Span('김태형 김현성'),
                            html.Div(
                                className="small text-center text-muted fst-italic",
                                children='미니프로젝트 2조'
                            )
                        ]
                    )
                )
            )
        )
    )
]

error_no_page_assigned = html.Div([
    html.H1('Error'),
    html.Br(),
    html.Div(['Unknown Page - try another URL']),
    html.Br(),
    dcc.Link('Go to home', href='/')
])


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index_page
    else:
        return error_no_page_assigned
    # You could also return a 404 "URL not found" page here

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')