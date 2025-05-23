import streamlit as st
import requests

API_BASE = "http://localhost:8000"  # FastAPI must be running locally

st.set_page_config(page_title="🌤️ Weather Tracker with Login", layout="centered")

# === Session state init ===
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# === Login / Register ===
if not st.session_state.logged_in:
    st.title("🔐 Login to Weather Tracker")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            res = requests.post(f"{API_BASE}/login", json={"username": username, "password": password})
            if res.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Logged in!")
            else:
                st.error("❌ Invalid credentials.")

    with col2:
        if st.button("Register"):
            res = requests.post(f"{API_BASE}/register", json={"username": username, "password": password})
            if res.status_code == 200:
                st.success("✅ Registered successfully. Now log in.")
            else:
                st.error("❌ Could not register.")

else:
    st.sidebar.write(f"👤 Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""

    st.title("🌤️ Weather Tracker")
    city = st.text_input("🌍 Enter city name")

    if st.button("Get Weather") and city:
        with st.spinner("Fetching weather data..."):
            res = requests.get(f"{API_BASE}/weather", params={
                "city": city,
                "username": st.session_state.username
            })

            if res.status_code == 200:
                data = res.json()
                st.metric("Temperature", f"{data['current']['temp_c']} °C")
                st.write("**Condition:**", data["current"]["condition"]["text"])
                st.image(f"https:{data['current']['condition']['icon']}")
                st.write("**Humidity:**", f"{data['current']['humidity']}%")
                st.write("**Wind:**", f"{data['current']['wind_kph']} kph")
            else:
                st.error("⚠️ Could not retrieve weather data.")

    st.markdown("🕘 **Recent Searches**")
    res = requests.get(f"{API_BASE}/searches", params={"username": st.session_state.username})
    if res.status_code == 200:
        searches = res.json().get("recent_searches", [])
        if searches:
            for city in searches:
                st.write(f"- {city}")
        else:
            st.info("No recent searches yet.")
    else:
        st.error("⚠️ Could not load search history.")

    if st.button("Clear Search History"):
        res = requests.delete(f"{API_BASE}/searches", params={"username": st.session_state.username})
        if res.status_code == 200:
            st.success("🗑️ History cleared.")
