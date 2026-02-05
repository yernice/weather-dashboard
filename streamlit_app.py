import streamlit as st
from weather import plot_temp_figure

st.set_page_config(page_title="Weather Dashboard", layout="centered")
st.title("🌤️ Weather Dashboard")

city = st.text_input(
    "Enter city name", placeholder="Astana, Almaty, London...")

if city:
    try:
        with st.spinner("Fetching weather data..."):
            fig, min_temp, max_temp = plot_temp_figure(city)
        st.subheader("📈 Hourly Temperature Today")
        st.pyplot(fig)

        col1, col2 = st.columns(2)
        col1.metric("Min Temperature", f"{min_temp} °C")
        col2.metric("Max Temperature", f"{max_temp} °C")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
