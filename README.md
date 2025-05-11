## 📦 How to Run Locally
git clone https://github.com/yourusername/leosimlab.git ,
cd leosimlab ,
pip install -r requirements.txt  ,
streamlit run app.py  ,
Note: You can create virtual environment in anaconda powershell for streamlit installation and then try to run the app

# LeoSimlab-OaaS
LeoSimlab + OaaS is a web-based Simulation-as-a-Service prototype that enables carbon- and cost-aware mission planning for Low Earth Orbit (LEO) infrastructure. Built using Python and Streamlit, it offers orbital simulations, mission booking, CSV report generation, —designed to democratize access to commercial space planning tools.

LeoSimlab + OaaS: Platform Workflow Overview

The following steps summarize the workflow for users:

Login & Authentication
Users begin by logging in through a secure interface. The platform verifies credentials to ensure authorized access to the simulator, booking system, and market data modules.

Mission Simulation
Upon successful login, users access the Mission Feasibility Simulator, where they input mission parameters such as payload mass, orbit type (LEO, Polar), and mission duration.
The platform then calculates:
Estimated mission cost,
Preparation timeline,
Carbon footprint (in tons CO₂),
Cost breakdown visualizations.

Mission Report Generation
After simulation, the platform generates a downloadable CSV report containing the input parameters and estimated outputs. This file can be used for academic, regulatory, or commercial planning.

Orbit Slot Booking
Users proceed to the Orbit Booking Interface to choose a launch window. The system:
Checks for date conflicts,
Confirms and stores the reservation in a central CSV database,
Displays existing reserved slots.

Market Insights Access
Users can explore curated insights on the commercial LEO market

Logout & Session Management
The platform provides a logout option that securely ends the session, preserving data integrity and privacy.

This structured workflow integrates mission planning, commercial foresight, and sustainability tracking—making LeoSimlab + OaaS an enabler for education, research, and commercial ventures in LEO.
