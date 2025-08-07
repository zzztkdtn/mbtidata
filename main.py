import streamlit as st
import pandas as pd
import altair as alt

st.title("대륙별 MBTI 평균 분포 시각화")

# CSV 파일 업로드
uploaded_file = st.file_uploader("MBTI 데이터 CSV 파일 업로드", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 간단한 대륙 정보 추가 (원하는 국가 추가 가능)
    continent_map = {
        "South Korea": "Asia",
        "Japan": "Asia",
        "China": "Asia",
        "Germany": "Europe",
        "France": "Europe",
        "United States": "North America",
        "Canada": "North America",
        "Brazil": "South America",
        "Argentina": "South America",
        "South Africa": "Africa",
        "Nigeria": "Africa",
        "Australia": "Oceania",
        "New Zealand": "Oceania"
    }

    df["Continent"] = df["Country"].map(continent_map)

    # 지역이 지정된 국가만 필터링
    df_filtered = df.dropna(subset=["Continent"])

    if df_filtered.empty:
        st.warning("대륙 정보가 지정된 국가가 없습니다. 매핑 딕셔너리를 확장해 주세요.")
    else:
        # MBTI 유형 열만 추출
        mbti_types = df.columns[1:-1]  # Country, Continent 제외

        # 대륙별 평균 계산
        mean_by_continent = df_filtered.groupby("Continent")[mbti_types].mean().reset_index()

        # Melt for Altair
        melted = mean_by_continent.melt(id_vars="Continent", var_name="MBTI", value_name="Average")

        st.subheader("📊 대륙별 MBTI 평균 비율")
        chart = alt.Chart(melted).mark_bar().encode(
            x=alt.X("MBTI:N", sort=None),
            y="Average:Q",
            color="Continent:N",
            column="Continent:N"
        ).properties(
            width=120,
            height=300
        )

        st.altair_chart(chart, use_container_width=True)
