def output():
    #학습, 테스트 데이터 분포 확인
    from sklearn.model_selection import train_test_split

    import pandas as pd

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

    #(Graph 그리기용)
    df.drop(columns='MIXA_PASTEUR_STATE', inplace=True)
    df.drop(columns='MIXB_PASTEUR_STATE', inplace=True)

    df = df.sample(250)

    #데이터 분리

    #측정데이터와 레이블(정답)을 분리
    #X = df.iloc[:, 1:5].values
    X = df.iloc[:, 1:3].values

    y = df.iloc[:, -1:].values

    #'OK'이면 1, 아니면 0
#    y = np.where(y == 'OK', 'OK', 'NG')
    #1차원으로 변경(flatten)
    y = y.ravel()

    trace_spaces = [
        [X, y, 'NG', '', 'square'],
        [X, y, 'OK', '', 'circle']
    ]

    fig = go.Figure(data=[
        go.Scatter(
            x=X[y==label, 0], y=X[y==label, 1],
            name=f'{split} Split, Label {label}',
            mode='markers', marker_symbol=marker
        )
        for X, y, label, split, marker in trace_spaces
    ])

    # fig.update_traces(
    #     marker_size=12, marker_line_width=1.5,
    #     marker_color="lightyellow"
    # )

    fig.update_traces(marker=dict(size=12,
                    line=dict(width=2,
                    color='lightyellow')),
                    selector=dict(mode='markers'))    


    return fig