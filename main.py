import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("일별 박스오피스 데이터를 이용해 영화의 시간에 따른 관객 변화를 살펴봅니다.")

# 데이터 불러오기
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜: YYYYMMDD 형식의 숫자/문자열을 실제 날짜형으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str).str.zfill(8),
        format="%Y%m%d",
        errors="coerce"
    )

    # 숫자형 열 변환
    numeric_columns = ["순위", "영화코드", "일관객", "누적관객", "스크린수", "상영횟수"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

df = load_data()

# 날짜순 정렬
df = df.sort_values("날짜")

# --------------------------------------------------
# 그래프 1. 영화별 날짜별 일관객 변화
# --------------------------------------------------
st.header("1. 영화별 날짜별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique().tolist())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}'의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,",
    }
)

fig.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info("영화가 날짜에 따라 하루 동안 얼마나 많은 관객을 끌어모았는지와 관객 수의 증가·감소 추세를 확인할 수 있습니다.")

st.divider()

# --------------------------------------------------
# 그래프 2. 기간 내 일관객 합계 TOP 5 영화
# --------------------------------------------------
st.header("2. 일관객 합계가 가장 큰 영화 TOP 5")
st.caption("이 기간 동안의 일관객을 모두 합산해 관객 수가 가장 많은 5편을 비교합니다.")

top5_movies = (
    df.dropna(subset=["영화명", "일관객"])
    .groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)["영화명"]
    .tolist()
)

top5_df = df[df["영화명"].isin(top5_movies)].copy()
top5_df = top5_df.sort_values(["날짜", "영화명"])

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=False,
    title="일관객 합계 TOP 5 영화의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,",
        "영화명": True
    }
)

fig2.update_traces(
    hovertemplate="영화: %{fullData.name}<br>날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig2.update_layout(
    hovermode="closest",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화",
    legend=dict(
        itemclick="toggle",
        itemdoubleclick="toggleothers"
    )
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info("이 기간 동안 일관객 합계가 가장 큰 5편의 영화가 날짜에 따라 얼마나 많은 관객을 모았는지 서로 비교할 수 있습니다.")

st.divider()

# --------------------------------------------------
# 앞으로 추가할 그래프 구역
# --------------------------------------------------
st.header("3. 추가 그래프")
st.caption("앞으로 시간에 따른 다른 영화 데이터 그래프를 이 구역에 추가할 수 있습니다.")

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info("여기에 추가 그래프를 통해 알 수 있는 내용을 작성하세요.")

st.divider()

st.header("4. 추가 그래프")
st.caption("새로운 그래프를 계속 추가할 수 있는 공간입니다.")

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info("여기에 추가 그래프를 통해 알 수 있는 내용을 작성하세요.")
