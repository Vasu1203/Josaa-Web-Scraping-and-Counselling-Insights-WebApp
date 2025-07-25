import streamlit as st
import pandas as pd

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("combined_OR_CR.csv")
    df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')
    df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce')
    df.dropna(subset=['Closing Rank'], inplace=True)
    df.dropna(subset=['Opening Rank'], inplace=True)
    return df
df = load_data()

# --- Load NIRF Ranking 2024 CSV (Engineering Only) ---
@st.cache_data
def load_nirf_data():
    df_nirf = pd.read_csv("NIRF Ranking 2024.csv")
        # Standardize column names if needed
    df_nirf.columns = df_nirf.columns.str.strip()
    # Filter only Engineering discipline
    df_nirf = df_nirf[df_nirf['Field'].str.lower() == 'engineering']
    # Drop Discipline/Field column
    df_nirf.drop(columns=[col for col in ['Field'] if col in df_nirf.columns], inplace=True)
    # Convert to numeric
    df_nirf['Rank'] = pd.to_numeric(df_nirf['Rank'], errors='coerce')
    df_nirf['Score'] = pd.to_numeric(df_nirf['Score'], errors='coerce')
    # Sort by Ranking
    df_nirf.sort_values(by='Rank', inplace=True)
    return df_nirf
df_nirf = load_nirf_data()

# --- Page Config ---
st.set_page_config(page_title="JoSAA Counselling Insights", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
        }
        .main-title {
            font-size: 48px;
            font-weight: bold;
            color: #00FFFF;
            text-align: center;
            margin-bottom: 30px;
        }
        .sidebar .stSelectbox label, .sidebar .stNumberInput label, .sidebar .stMultiSelect label {
            font-weight: bold;
            color: #004080;
        }
        .css-1d391kg {
            background-color: #f0f8ff;
        }
        .reportview-container .markdown-text-container {
            padding-top: 2rem;
        }
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="main-title">🎓 JoSAA Counselling Insights Dashboard</div>', unsafe_allow_html=True)

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")

# Rank 
rank_input = st.sidebar.number_input("Enter Your Rank (JEE MAINS/ADVANCED)", min_value=1, step=1, key="rank_input")

# Institute                               
Institute_Type = st.sidebar.selectbox("Institute Type (NIT/IIT/IIIT/GFTI)", sorted(df['Institute Type'].dropna().unique()), key="institute_type")

# Filter by Institute Types
filtered_df = df[df['Institute Type'] == Institute_Type]

# Institute Multiselect
institute_options = sorted(filtered_df['Institute'].dropna().unique())
selected_institutes = st.sidebar.multiselect("Institute", institute_options, key="selected_institutes_list")
# Show states of selected institutes
if selected_institutes:
    inst_state_map = filtered_df[['Institute', 'State']].drop_duplicates()
    selected_states_info = inst_state_map[inst_state_map['Institute'].isin(selected_institutes)]
    # Display nicely in sidebar
    st.sidebar.markdown("#### 🏛️ Selected Institute(s) & State(s):")
    for _, row in selected_states_info.iterrows():
        st.sidebar.markdown(f"- **{row['Institute']}** → *{row['State']}*")
select_all = st.sidebar.checkbox("Select All Institutes", key="select_all_Institutes")
if select_all:
    selected_institutes = institute_options

# --- Quota Selection ---
quota = st.sidebar.selectbox("Quota", sorted(filtered_df['Quota'].dropna().unique()), key="quota")

# --- State Filter Only for HS / GO Quota ---
if quota in ["HS", "GO"]:  # Quotas requiring state selection
    state_df = filtered_df[filtered_df['Quota'] == quota]
    available_states = sorted(state_df['State'].dropna().unique())
    selected_states = st.sidebar.multiselect("Home State", available_states, key="selected_states")
    
    select_all_states = st.sidebar.checkbox("Select All States", key="select_all_states")
    if select_all_states:
        selected_states = available_states
else:
    selected_states = filtered_df['State'].dropna().unique()  # All states allowed

# Other dropdowns
category = st.sidebar.selectbox("Seat Type", sorted(filtered_df['Seat Type'].dropna().unique()), key="category")
gender = st.sidebar.selectbox("Gender", sorted(filtered_df['Gender'].dropna().unique()), key="gender")
round_no = st.sidebar.selectbox("Round", sorted(filtered_df['Round'].dropna().unique()), key="round")

# --- Final Filtering ---
filtered = filtered_df[
    ((filtered_df['Closing Rank'] >= rank_input) &
    (filtered_df['Opening Rank'] <= rank_input)) &
    (filtered_df['Institute'].isin(selected_institutes)) &
    (filtered_df['Quota'] == quota) &
    (filtered_df['Seat Type'] == category) &
    (filtered_df['Gender'] == gender) &
    (filtered_df['Round'] == round_no) 
]

# --- Tabs for Results, NIRF, and Seat Matrix ---
tab1, tab2, tab3 = st.tabs(["🎯 Eligible Institutes", "🏆 NIRF 2024 Rankings", "📊 Seat Matrix 2025"])

with tab1:
    st.markdown("### 🎯 Institutes & Branches You May Get")
    if filtered.empty:
        st.warning("🚫 No colleges found based on your input criteria. Please adjust your filters.")
    else:
        st.dataframe(
            filtered[['Institute', 'Academic Program Name', 'Opening Rank', 'Closing Rank']]
            .sort_values(by='Closing Rank')
            .reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )

with tab2:
    st.markdown("### 🏆 NIRF Ranking 2024 (Engineering Only)")
    # Prepare institute options
    institute_options = ["ALL"] + sorted(df_nirf['Name'].dropna().unique())
    selected_institute = st.selectbox("🔍 Search & Select Institute",institute_options)
    if selected_institute != "ALL":
        df_to_display = df_nirf[df_nirf['Name'] == selected_institute]
    else:
        df_to_display = df_nirf
    st.dataframe(df_to_display, use_container_width=True, hide_index=True)

    # Explanation of NIRF Parameters
    st.markdown("### ℹ️ NIRF Parameter Definitions")
    st.markdown("""
    | Code | Full Form                           | Description                                                                 |
    |------|------------------------------------|-----------------------------------------------------------------------------|
    | **TLR** | Teaching, Learning & Resources       | Measures faculty-student ratio, faculty qualifications, infrastructure, etc. |
    | **RPC** | Research and Professional Practice   | Focuses on research output, publications, patents, and PhD graduates.        |
    | **GO**  | Graduation Outcomes                  | Includes placements, higher education stats, median salary, and success rates. |
    | **OI**  | Outreach and Inclusivity             | Diversity of students and faculty by gender, region, and social representation. |
    | **PR**  | Peer Perception                      | Reputation based on academic peers and employers.                            |
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("### 📊 JoSAA Seat Matrix")
    # ❓ Explanation about Supernumerary seats
    st.info(""" 
            ℹ️ **What is Supernumerary?**
            
            - This means some or all of these seats are Supernumerary — i.e., extra seats added on top of the normal sanctioned intake just for female candidates.

            - Their purpose is to increase female participation in technical education (especially in IITs, NITs, IIITs). 
            
            """)
    # Load Seat Matrix Excel file
    @st.cache_data
    def load_seat_matrix():
        df_seat = pd.read_csv("Merged_Seat_Matrix.csv")
        return df_seat
    df_seat_matrix = load_seat_matrix()
    # Optional: Filters (by Institute or Program, if available)
    institute_filter = st.selectbox("🔍 Filter by Institute", ["All"] + sorted(df_seat_matrix['Institute Name'].dropna().unique()))
    if institute_filter != "All":
        df_seat_matrix = df_seat_matrix[df_seat_matrix['Institute Name'] == institute_filter]
    st.dataframe(df_seat_matrix, use_container_width=True, hide_index=True)


# --- Footer ---
st.markdown("""
    <hr style="margin-top: 50px; margin-bottom: 10px;">
    <div style='text-align: center; color: gray; font-size: 14px;'>
        ❤️Created by <b>Vaibhav</b>
    </div>
""", unsafe_allow_html=True)






