import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import base64
import os
from io import StringIO

#--- Authentication Logic ---
def check_login(username, password):
    valid_username = "user123"
    valid_password = "password123"
    return username == valid_username and password == valid_password

# --- Get base64 image ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        base64_str = base64.b64encode(img_file.read()).decode("utf-8")
    return base64_str

# Convert logo to Base64
logo_base64 = get_base64_image(r"C:\Users\sgt17\Downloads\leoOaaS\leoOaas_logo.jpg")

# --- Login Page ---
def login_page():
    st.set_page_config(page_title="Login to the LeoSimlab + OaaS Platform", layout="centered")

    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{logo_base64}" width="150">
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.title("LeoSimlab + OaaS")
    st.markdown("Please enter your credentials to log in and access the platform.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state["logged_in"] = True
            st.session_state["page"] = "Simulator"
            st.rerun()
        else:
            st.error("Invalid username or password.")

# --- Logout Logic ---
def logout():
    st.session_state["logged_in"] = False
    st.session_state["page"] = "Login"
    st.rerun()

# --- Simulator Page ---
def simulator_page():
    st.header("\U0001F680 Mission Feasibility Simulator")
    mission_name = st.text_input("Mission Name")
    payload_mass = st.number_input("Payload Mass (kg)", min_value=1)
    duration = st.number_input("Duration (days)", min_value=1)
    orbit_type = st.selectbox("Orbit Type", ["LEO", "Polar"])

    if st.button("Simulate Mission"):
        base_cost = 100000
        cost_per_kg = 5000
        orbit_multiplier = 1.2 if orbit_type == "Polar" else 1.0
        total_cost = base_cost + payload_mass * cost_per_kg * orbit_multiplier
        timeline = "6-12 months" if duration > 30 else "3-6 months"
        carbon_footprint = payload_mass * 0.1  # Simplified estimation

        st.success(f"Estimated Cost: €{total_cost:,.2f}")
        st.info(f"Expected Prep Time: {timeline}")
        st.warning(f"Estimated Carbon Footprint: {carbon_footprint:.2f} tons CO₂")

        # Save mission data
        mission_data = {
            "Mission Name": mission_name,
            "Payload Mass (kg)": payload_mass,
            "Duration (days)": duration,
            "Orbit Type": orbit_type,
            "Estimated Cost (€)": total_cost,
            "Prep Time": timeline,
            "Carbon Footprint (tons CO₂)": carbon_footprint
        }
        save_mission_data(mission_data)
        st.session_state["last_mission"] = mission_data

        # Visualizations
        st.subheader("\U0001F4CA Cost Breakdown")
        fig1, ax1 = plt.subplots()
        labels = ['Base Cost', 'Payload Cost', 'Orbit Multiplier']
        values = [base_cost, payload_mass * cost_per_kg, (payload_mass * cost_per_kg) * orbit_multiplier]
        ax1.bar(labels, values, color=['blue', 'green', 'red'])
        ax1.set_ylabel('Cost (€)')
        ax1.set_title('Mission Cost Breakdown')
        st.pyplot(fig1)

        st.subheader("🌍 Carbon Footprint")
        fig2, ax2 = plt.subplots()
        ax2.pie([carbon_footprint, 100 - carbon_footprint], labels=['Mission', 'Remaining'], autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)

        report_df = pd.DataFrame([mission_data])
        csv_buffer = StringIO()
        report_df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label="Download Report",
            data=csv_data,
            file_name="mission_report.csv",
            mime="text/csv"
        )

# --- Market Insights Page ---
def market_insight_page():
    st.header("📈 Commercial LEO Market Insights")
    st.markdown("""
        - NASA CLD Program: Aims to maintain presence in LEO post-ISS.
        - Key Players: SpaceX, Axiom, Blue Origin.
        - Growth: $1 trillion global space economy by 2030.
        - Opportunities: Space tourism, microgravity research, infrastructure-as-a-service.
    """)

# --- Booking Page ---
def booking_page():
    st.header("🗓️ Orbit Booking Interface")

    default_mission_name = st.session_state.get("last_mission", {}).get("Mission Name", "")
    mission_name = st.text_input("Mission Name (for booking)", value=default_mission_name)
    booking_date = st.date_input("Select Launch Window", date(2025, 9, 1))

    booking_df = load_bookings()

    if st.button("Book Orbit Slot"):
        if (booking_df['Date'] == booking_date.strftime('%Y-%m-%d')).any():
            st.error("Selected date is already reserved. Please choose another.")
        else:
            new_row = pd.DataFrame([{"Mission Name": mission_name, "Date": booking_date.strftime('%Y-%m-%d')}])
            booking_df = pd.concat([booking_df, new_row], ignore_index=True)
            booking_df.to_csv("bookings.csv", index=False)
            st.success(f"Orbit slot reserved for **{mission_name}** on {booking_date.strftime('%Y-%m-%d')}.")

    st.subheader("Reserved Slots")
    st.dataframe(booking_df)

# --- Save Mission Data ---
def save_mission_data(data):
    df = pd.DataFrame([data])
    if os.path.exists("missions.csv"):
        df.to_csv("missions.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("missions.csv", index=False)

# --- Load Bookings ---
def load_bookings():
    if os.path.exists("bookings.csv"):
        return pd.read_csv("bookings.csv")
    else:
        return pd.DataFrame(columns=["Mission Name", "Date"])

# --- Main Page ---
def main_page():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Simulator", "Booking", "Market Insights"])
    if st.sidebar.button("Logout"):
        logout()
    if page == "Simulator":
        simulator_page()
    elif page == "Booking":
        booking_page()
    elif page == "Market Insights":
        market_insight_page()

# --- App Entry Point ---
def app():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "Login"
    if not st.session_state["logged_in"]:
        login_page()
    else:
        main_page()

if __name__ == "__main__":
    app()
