import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("일별 박스오피스 데이터를 이용해 영화의 시간에 따른 관객 변화를 살펴봅니다.")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str).str.zfill(8),
        format="%Y%m%d",
        errors="coerce"
    )

    numeric_columns = [
        "순위", "영화코드", "일관객", "누적관객", "스크린수", "상영횟수"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


df = load_data().sort_values("날짜")


# ─────────────────────────────────────────────
# 1. 영화별 날짜별 일관객 변화
# ─────────────────────────────────────────────
st.header("1. 영화별 날짜별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique().tolist())
selected_movie = st.selectbox("영화를 선택하세요.", movie_list)

movie_df = (
    df[df["영화명"] == selected_movie]
    .copy()
    .sort_values("날짜")
)

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}'의 날짜별 일관객 변화",
    labels={"날짜": "날짜", "일관객": "일관객 수"},
)

fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig1.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info(
    "영화가 날짜에 따라 하루 동안 얼마나 많은 관객을 끌어모았는지와 관객 수의 증가·감소 추세를 확인할 수 있습니다."
)

st.divider()


# ─────────────────────────────────────────────
# 2. 기간 일관객 TOP 5 영화의 날짜별 변화
# ─────────────────────────────────────────────
st.header("2. 기간 일관객 TOP 5 영화의 날짜별 변화")

top_5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .nlargest(5)
    .index
    .tolist()
)

top_5_df = (
    df[df["영화명"].isin(top_5_movies)]
    .copy()
    .sort_values(["날짜", "영화명"])
)

fig2 = px.line(
    top_5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="기간 일관객 합계 TOP 5 영화의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    },
)

fig2.update_traces(
    hovertemplate="영화: %{fullData.name}<br>날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)

fig2.update_layout(
    hovermode="x unified",
    legend_title_text="영화"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info(
    "기간 동안 관객이 많았던 영화 5편의 날짜별 흥행 추이와 영화 간 관객 변화를 비교할 수 있습니다."
)

st.divider()


# ─────────────────────────────────────────────
# 3. 날짜별 10위권 일관객 합계
# ─────────────────────────────────────────────
st.header("3. 날짜별 10위권 일관객 합계")

daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

top_3_days = daily_total.nlargest(3, "일관객").sort_values("날짜")

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)

fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>10위권 일관객 합계: %{y:,}명<extra></extra>"
)

for _, row in top_3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=f"{row['날짜'].strftime('%Y-%m-%d')}<br>{row['일관객']:,}명",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-45,
        bgcolor="white",
        bordercolor="gray",
        borderwidth=1
    )

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)"
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info(
    "날짜에 따라 박스오피스 10위권 전체의 관객 규모가 어떻게 변했는지와 관객이 가장 많이 몰린 날짜를 확인할 수 있습니다."
)

st.divider()


# ─────────────────────────────────────────────
# 4. 영화별 기간 일관객 TOP 10
# ─────────────────────────────────────────────
st.header("4. 영화별 기간 일관객 TOP 10")

movie_summary = (
    df.dropna(subset=["영화명", "일관객", "날짜"])
    .groupby("영화명")
    .agg(
        기간_일관객=("일관객", "sum"),
        10위권_등장일수=("날짜", "nunique")
    )
    .nlargest(10, "기간_일관객")
    .sort_values("기간_일관객", ascending=True)
    .reset_index()
)

fig4 = px.bar(
    movie_summary,
    x="기간_일관객",
    y="영화명",
    orientation="h",
    title="영화별 기간 일관객 TOP 10",
    labels={
        "영화명": "영화",
        "기간_일관객": "기간 일관객 합계"
    },
    custom_data=["10위권_등장일수"]
)

fig4.update_traces(
    hovertemplate=(
        "영화: %{y}<br>"
        "기간 일관객 합계: %{x:,}명<br>"
        "개봉 후 10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="기간 일관객 합계(명)",
    yaxis_title="영화",
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info(
    "이 기간 동안 일관객 합계가 많았던 영화 10편과 각 영화가 10위권에 등장한 날수를 함께 비교할 수 있습니다."
)

st.divider()


# ─────────────────────────────────────────────
# 5. 월 × 요일별 일관객 합계 히트맵
# ─────────────────────────────────────────────
st.header("5. 월 × 요일별 일관객 합계 히트맵")

heatmap_df = df.dropna(subset=["날짜", "일관객"]).copy()
heatmap_df["월"] = heatmap_df["날짜"].dt.month

weekday_order = [
    "월요일", "화요일", "수요일", "목요일",
    "금요일", "토요일", "일요일"
]

weekday_map = dict(enumerate(weekday_order))
heatmap_df["요일"] = heatmap_df["날짜"].dt.dayofweek.map(weekday_map)

heatmap_data = (
    heatmap_df.groupby(["월", "요일"])["일관객"]
    .sum()
    .unstack(fill_value=0)
    .reindex(columns=weekday_order)
    .sort_index()
)

heatmap_data.index = [f"{month}월" for month in heatmap_data.index]

fig5 = px.imshow(
    heatmap_data,
    labels={
        "x": "요일",
        "y": "월",
        "color": "일관객 합계"
    },
    aspect="auto",
    color_continuous_scale="Blues",
    title="월 × 요일별 10위권 일관객 합계"
)

fig5.update_traces(
    hovertemplate="%{y} %{x}<br>일관객 합계: %{z:,}명<extra></extra>"
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    coloraxis_colorbar_title="일관객 합계"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info(
    "어떤 월과 요일 조합에서 박스오피스 10위권 영화들의 일관객 합계가 많이 나타났는지 한눈에 비교할 수 있습니다."
)

st.divider()

st.header("6. 추가 그래프")
st.write("앞으로 시간에 관한 다른 그래프를 추가할 수 있습니다.")
