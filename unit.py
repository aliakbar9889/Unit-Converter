import streamlit as st
import sqlite3

st.set_page_config(page_title="Unit Converter", page_icon="⚡", layout="centered")

# Database Setup
conn = sqlite3.connect("conversions.db", check_same_thread=False)


cursor = conn.cursor()
cursor.execute("DELETE FROM history")
cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    input_value FLOAT,
                    from_unit TEXT,
                    to_unit TEXT,
                    result FLOAT)''')
conn.commit()

# Main Page
st.title("⚡ Unit Converter")
st.write("🔹 A simple unit converter app built with Streamlit and SQLite.")

# Category Icons
category_icons = {
    "Weight": "⚖️",
    "Height": "📏",
    "Speed": "🚀"
}

# Sidebar Category Selection
categories = list(category_icons.keys())
selected_option = st.sidebar.selectbox(" Select a Category:", categories)

# Show selected category as heading on the main page with an icon
st.subheader(f"{category_icons[selected_option]} {selected_option} Conversion")

# Conversion Functions
def convert_weight(value, from_unit, to_unit):
    weight_units = {"kg": 1, "g": 1000, "lb": 2.20462, "oz": 35.274}
    return value * (weight_units[to_unit] / weight_units[from_unit])

def convert_height(value, from_unit, to_unit):
    height_units = {"m": 1, "cm": 100, "inch": 39.3701, "ft": 3.28084}
    return value * (height_units[to_unit] / height_units[from_unit])

def convert_speed(value, from_unit, to_unit):
    speed_units = {"m/s": 1, "km/h": 3.6, "mph": 2.23694, "knot": 1.94384}
    return value * (speed_units[to_unit] / speed_units[from_unit])

def show_history():
    """Display conversion history."""
    cursor.execute("SELECT * FROM history")
    history = cursor.fetchall()
    return history

# Input Value (Increases by 1.00 on tap)
value = st.number_input("Enter value:", min_value=0.0, step=1.0, format="%.2f")

# Unit Selection & Conversion
if selected_option == "Weight":
    from_unit = st.selectbox("From:", ["kg", "g", "lb", "oz"])
    to_unit = st.selectbox("To:", ["kg", "g", "lb", "oz"])
    result = convert_weight(value, from_unit, to_unit) if value > 0 else None

elif selected_option == "Height":
    from_unit = st.selectbox("From:", ["m", "cm", "inch", "ft"])
    to_unit = st.selectbox("To:", ["m", "cm", "inch", "ft"])
    result = convert_height(value, from_unit, to_unit) if value > 0 else None

elif selected_option == "Speed":
    from_unit = st.selectbox("From:", ["m/s", "km/h", "mph", "knot"])
    to_unit = st.selectbox("To:", ["m/s", "km/h", "mph", "knot"])
    result = convert_speed(value, from_unit, to_unit) if value > 0 else None

# Convert Button
if st.button("🔄 Convert"):
    if result is None:
        st.error("⚠️ Input not found! Please enter a value before converting.")
    else:
        st.success(f"✅ Converted Value: {result:.2f} {to_unit}")

        # **Save conversion to database**
        cursor.execute("INSERT INTO history (input_value, from_unit, to_unit, result) VALUES (?, ?, ?, ?)", 
                       (value, from_unit, to_unit, result))
        conn.commit()

# Show History
st.subheader("📜 Your Conversion History")
history = show_history() 
for record in history:
    st.write(f"{record[1]} {record[2]} → {record[4]} {record[3]}")
