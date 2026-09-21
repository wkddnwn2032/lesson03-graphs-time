import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("박스오피스 데이터를 날짜의 흐름에 따라 살펴보는 그래프 도감입니다.")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# =========================================================
# 데이터 불러오기
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    return df


df = load_data()


# =========================================================
# 데이터 확인
# =========================================================

st.caption(
    f"데이터 기간: {df['날짜'].min().strftime('%Y-%m-%d')} ~ "
    f"{df['날짜'].max().strftime('%Y-%m-%d')} | "
    f"총 {len(df):,}개 기록"
)


# =========================================================
# 그래프 1
# =========================================================

st.divider()
st.header("📈 그래프 1. 영화별 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화의 날짜별 일관객 변화를 확인할 수 있습니다."
)

# 영화 목록
movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
    key="movie_selector"
)

# 선택한 영화 데이터
movie_df = df[df["영화명"] == selected_movie].copy()

# 날짜순 정렬
movie_df = movie_df.sort_values("날짜")


# Plotly 선 그래프
fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,.0f"
    }
)

fig.update_traces(
    hovertemplate=
    "<b>날짜</b>: %{x|%Y-%m-%d}<br>"
    "<b>일관객</b>: %{y:,.0f}명"
    "<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# 그래프 해석 문구
# =========================================================

st.subheader("💡 이 그래프로 알 수 있는 것")

st.info(
    "이 그래프로 알 수 있는 것: "
    f"「{selected_movie}」의 일관객 수가 날짜에 따라 어떻게 증가하거나 감소했는지 확인할 수 있다."
)


# =========================================================
# 앞으로 추가할 그래프 영역
# =========================================================

st.divider()

st.header("📊 그래프 2")
st.caption("앞으로 추가할 그래프를 위한 공간입니다.")

st.info("다음 그래프가 이 구역에 추가될 예정입니다.")


st.divider()

st.header("📊 그래프 3")
st.caption("앞으로 추가할 그래프를 위한 공간입니다.")

st.info("다음 그래프가 이 구역에 추가될 예정입니다.")
