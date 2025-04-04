import streamlit as st
from fpdf import FPDF
from PIL import Image

st.set_page_config(page_title="Dump Truck Calculator", layout="centered")

# --- DISPLAY LOGO ---
logo = Image.open("DirtyBiz-Black.png")  # Make sure this file is uploaded to GitHub too
st.image(logo, width=250)

st.title("🚛 Dump Truck Profitability Calculator")

# --- JOB TYPE SELECTION ---
st.header("🔧 Job Type")
job_type = st.selectbox("Is this an hourly job or a tonnage job?", ["Hourly", "Tonnage"])

if job_type == "Tonnage":
    # --- SECTION 1: Cost Per Mile / Load Breakdown ---
    st.header("🚚 Cost Per Mile / Load")
    haul_distance = st.number_input("Haul Distance (miles)", value=20.0)
    mpg = st.number_input("Miles Per Gallon (MPG)", value=5.0)
    fuel_cost_per_gal = st.number_input("Fuel Cost ($/gal)", value=4.25)
    driver_wage = st.number_input("Driver Wage ($/hour)", value=35.0)
    operating_cost_per_load = st.number_input("Operating Cost per Load ($)", value=50.0)

    # --- SECTION 2: Multi-Truck Job Calculator ---
    st.header("🧮 Multi-Truck Job Calculator")
    num_trucks = st.number_input("Number of Trucks", value=3)
    truck_type = st.selectbox("Select Truck Type", ["Single-axle", "Tandem", "Tri-axle", "Quad", "Quint", "Dump-Trailer"])
    load_capacity = st.number_input("Load Capacity per Truck (tons)", value=16.0)
    loads_per_day = st.number_input("Estimated Loads per Day (per truck)", value=10)
    job_length_days = st.number_input("Job Length (days)", value=5)
    daily_hours = st.number_input("Daily Hours Worked (per truck)", value=8.0)

    # --- SECTION 3: Material Type ---
    st.header("📦 Material Type")
    material_type = st.selectbox("Select Material Type", ["Dirt", "Gravel", "Sand", "Millings", "Asphalt", "Tear-out"])

    # --- SECTION 4: Profit Margin Estimator ---
    st.header("💰 Profit Margin Estimator")
    total_job_payout = st.number_input("Total Job Payout ($)", value=25000.0)

    # --- CALCULATIONS ---
    total_loads = num_trucks * loads_per_day * job_length_days
    fuel_cost_per_mile = fuel_cost_per_gal / mpg
    trip_fuel_cost = haul_distance * 2 * fuel_cost_per_mile  # round trip

    cost_per_load = trip_fuel_cost + operating_cost_per_load
    cost_per_mile = trip_fuel_cost / (haul_distance * 2)
    total_hours = daily_hours * job_length_days * num_trucks
    labor_cost = driver_wage * total_hours

    all_in_cost = (cost_per_load * total_loads) + labor_cost
    total_project_hours = total_hours
    total_project_miles = haul_distance * 2 * total_loads

    cost_per_hour = all_in_cost / total_project_hours if total_project_hours else 0
    cost_per_mile_final = all_in_cost / total_project_miles if total_project_miles else 0
    profit = total_job_payout - all_in_cost
    profit_margin = (profit / total_job_payout) * 100 if total_job_payout else 0

    # --- RESULTS ---
    st.subheader("📊 Job Summary")
    st.write(f"**Truck Type:** {truck_type}")
    st.write(f"**Material Type:** {material_type}")
    st.write(f"**Total Loads:** {total_loads}")
    st.write(f"**Total Hours (All Trucks):** {total_project_hours:.2f}")
    st.write(f"**Total Miles (Round Trip x Loads):** {total_project_miles:.2f}")
    st.write(f"**All-In Cost:** ${all_in_cost:,.2f}")
    st.write(f"**Cost per Load:** ${cost_per_load:,.2f}")
    st.write(f"**Cost per Mile:** ${cost_per_mile_final:,.2f}")
    st.write(f"**Cost per Hour:** ${cost_per_hour:,.2f}")

    st.subheader("💼 Profit Analysis")
    st.write(f"**Total Payout:** ${total_job_payout:,.2f}")
    st.write(f"**Profit:** ${profit:,.2f}")
    st.write(f"**Profit Margin:** {profit_margin:.2f}%")

    # --- GENERATE PDF ---
    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, txt="Hauling Services Bid Summary", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Truck Type: {truck_type}", ln=True)
        pdf.cell(200, 10, txt=f"Material Type: {material_type}", ln=True)
        pdf.cell(200, 10, txt=f"Total Loads: {total_loads}", ln=True)
        pdf.cell(200, 10, txt=f"Total Hours: {total_project_hours:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Miles: {total_project_miles:.2f}", ln=True)
        pdf.cell(200, 10, txt=f"All-In Cost: ${all_in_cost:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Cost per Load: ${cost_per_load:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Cost per Mile: ${cost_per_mile_final:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Cost per Hour: ${cost_per_hour:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Total Payout: ${total_job_payout:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Profit: ${profit:,.2f}", ln=True)
        pdf.cell(200, 10, txt=f"Profit Margin: {profit_margin:.2f}%", ln=True)

        return pdf.output(dest="S").encode("latin1")

    pdf_data = generate_pdf()
    st.download_button(
        label="📄 Download Bid as PDF",
        data=pdf_data,
        file_name="hauling_services_bid_summary.pdf",
        mime="application/pdf"
    )

elif job_type == "Hourly":
    st.header("⏱️ Hourly Job Calculator")
    truck_type = st.selectbox("Select Truck Type", ["Single-axle", "Tandem", "Tri-axle", "Quad", "Quint", "Dump-Trailer"])
    material_type = st.selectbox("Select Material Type", ["Dirt", "Gravel", "Sand", "Millings", "Asphalt", "Tear-out"])
    num_trucks = st.number_input("Number of Trucks", value=1)
    hours_per_day = st.number_input("Hours per Day", value=8.0)
    job_length_days = st.number_input("Job Length (days)", value=5)
    hourly_rate_per_truck = st.number_input("Hourly Rate per Truck ($)", value=95.0)

    total_hours = num_trucks * hours_per_day * job_length_days
    total_payout = total_hours * hourly_rate_per_truck

    st.subheader("📊 Hourly Job Summary")
    st.write(f"**Truck Type:** {truck_type}")
    st.write(f"**Material Type:** {material_type}")
    st.write(f"**Total Trucks:** {num_trucks}")
    st.write(f"**Total Hours:** {total_hours}")
    st.write(f"**Hourly Rate per Truck:** ${hourly_rate_per_truck:.2f}")
    st.write(f"**Total Payout:** ${total_payout:,.2f}")
