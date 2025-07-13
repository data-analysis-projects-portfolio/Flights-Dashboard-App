# ✈️ Flight Routes & Analytics Dashboard

This project is a **Streamlit-based web application** that visualizes flight route data and provides interactive analytics. It allows users to explore all possible flight connections between any two cities and gain insights into flight patterns and airport activity.

---

## 📁 Data Source

- The data is loaded from a cleaned CSV file: `flights_cleaned.csv`
- This data is imported into a **PostgreSQL** database:
  - **Database name:** `flights`
  - **Table name:** `flights_data`

---

## 🛠️ Application Overview

The Streamlit app consists of **two main tabs** in the sidebar:

### 1. 🔍 Check Flights

- Allows users to select:
  - **Source City** (dropdown)
  - **Destination City** (dropdown)
- Displays a **table** of all available flight connections between the selected cities.

### 2. 📊 Analytics

Provides three interactive charts for better understanding of flight trends:

#### a. 🥧 Airline Pie Chart
- Shows the frequency distribution of flights for each airline.

#### b. 🏙️ Busiest Airports Bar Graph
- Displays the busiest cities based on the number of flights (as source or destination).

#### c. 📈 Flights per Day Line Chart
- Visualizes the number of flights operating on each day.

---

## ⚙️ Tech Stack

- **Python**
- **Streamlit** for the web interface
- **Pandas** for data manipulation
- **Plotly / Matplotlib / Seaborn** for visualizations
- **PostgreSQL** for the database

---

## 🚀 How to Run the App Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/data-analysis-projects-portfolio/Flights-Dashboard-App.git
   cd Flights-Dashboard-App
