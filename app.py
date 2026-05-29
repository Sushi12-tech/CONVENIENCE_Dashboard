import streamlit as st
import pandas as pd

# Set up page layout to occupy the full width of the screen
st.set_page_config(page_title="AE & DS Performance Dashboard", layout="wide", page_icon="📊")

# Dashboard Header
st.title("📊 AE & DS Performance Dashboard")
st.markdown("---")

# ==================================================================
# ⚠️ ADMIN CONFIGURATION: PASTE YOUR GOOGLE DRIVE FILE SHARING IDs HERE
# ==================================================================
# To get these IDs, share each file in Google Drive as "Anyone with link can view".
# Copy the link and extract the long string of letters/numbers between '/d/' and '/edit'.
DHURANDAR_SHARE_ID = "1N4kEbF621Nhzjg4eJfGz9fkGIXEQ_LA5" 
OUTLET_MASTER_SHARE_ID = "1kxGk5IvkPLGLE0Dg6vCxQ1NeT8V8xPQu" 
RADAR_ROUTE_SHARE_ID = "1AKW089LhV37onfSEmk4H6l86f4MsQTCr"

# Formulating direct-download CSV export endpoints for Google Drive
URL_BREEZE = f"https://docs.google.com/uc?export=download&id={DHURANDAR_SHARE_ID}"
URL_MASTER = f"https://docs.google.com/uc?export=download&id={OUTLET_MASTER_SHARE_ID}"
URL_ROUTE = f"https://docs.google.com/uc?export=download&id={RADAR_ROUTE_SHARE_ID}"
# ------------------------------------------------------------------
# 1. LIVE CLOUD DATA LOADING (WITH AUTOMATIC 1-HOUR CACHE REFRESH)
# ------------------------------------------------------------------
@st.cache_data(ttl=3600)  # Caches data for 1 hour for high performance, then auto-refreshes
def load_live_cloud_data():
    # If the default placeholder strings haven't been swapped yet, halt cleanly
    if "YOUR_GOOGLE_DRIVE_ID" in DHURANDAR_SHARE_ID:
        return None, None, None, "setup_needed"
        
    try:
        # Pulling files directly from your central Google Drive cloud
        # Skiprows=2 accommodates the dual-header structure inside the Breeze Summary Sheet
        df_breeze = pd.read_csv(URL_BREEZE, skiprows=2, encoding="latin-1")
        df_master = pd.read_csv(URL_MASTER, encoding="latin-1")
        df_route = pd.read_csv(URL_ROUTE, encoding="latin-1")
        return df_breeze, df_master, df_route, "success"
    except Exception as e:
        return None, None, None, str(e)

# Run the live network cloud fetch sequence
df_breeze, df_master, df_route, status_msg = load_live_cloud_data()

# Failsafe error window if IDs are missing or link sharing permissions are restricted
if status_msg == "setup_needed":
    st.info("👋 Welcome to your Shared Field Performance Dashboard!")
    st.warning("⚠️ **Admin Setup Required:** Please open `app.py` and replace the placeholder Google Drive File IDs (lines 14-16) with your live spreadsheet sharing keys.")
    st.stop()
elif status_msg != "success":
    st.error("💥 Critical Connection Error while fetching files from Google Drive cloud server.")
    st.markdown(f"**Technical Details:** {status_msg}")
    st.info("💡 **Troubleshooting Checklist:** Ensure your Google Drive files are set to *'Anyone with the link can view'*. If access is restricted, the cloud server will block the connection request.")
    st.stop()

# ------------------------------------------------------------------
# 2. DATA SANITIZATION & CROSS-SHEET FIELD MAPPING
# ------------------------------------------------------------------
if df_breeze is not None and df_master is not None and df_route is not None:
    st.sidebar.success("🟢 Connected to Live Google Drive Storage")
    
    # Standardize spaces and text formats across common linkage keys
    df_breeze['AE ID'] = df_breeze['AE ID'].astype(str).str.strip()
    df_breeze['DS ID_str'] = df_breeze['DS ID'].astype(str).str.strip()
    df_breeze['DS Type'] = df_breeze['DS Type'].astype(str).str.strip()
    df_breeze['Rank'] = pd.to_numeric(df_breeze['Rank'], errors='coerce')
    
    df_master['AE ID'] = df_master['AE ID'].astype(str).str.strip()
    df_master['DS/TL ID_str'] = df_master['DS/TL ID'].astype(str).str.strip()
    
    df_route['DS Id_str'] = df_route['DS Id'].astype(str).str.strip()
    
    # Generate indexed lookup tables (Acts as lightning-fast backend VLOOKUP arrays)
    ds_to_wd_dict = df_master.groupby('DS/TL ID_str')['WD ID'].first().to_dict()
    van_ds_to_wd_dict = df_route.groupby('DS Id_str')['WD Code'].first().to_dict()
    
    # Routing function to link active WD Codes based on structural segment parameters
    def assign_linked_wd_code(row):
        is_van = "van" in str(row['DS Type']).lower()
        ds_id = row['DS ID_str']
        
        if is_van and ds_id in van_ds_to_wd_dict:
            return van_ds_to_wd_dict[ds_id]
        else:
            return ds_to_wd_dict.get(ds_id, None)
            
    df_breeze['WD Code (Linked)'] = df_breeze.apply(assign_linked_wd_code, axis=1)
    
    # Extract alpha-sorted unique values list to populate the autocomplete dropdown window
    unique_ae_ids = sorted(df_breeze['AE ID'].dropna().unique())
    
    # User Lookup Dropdown Widget
    st.subheader("🔍 Select or Search AE ID")
    selected_ae = st.selectbox(
        "Type or select an Executive AE ID to view live operational metrics:",
        options=unique_ae_ids,
        index=0
    )
    
    # ------------------------------------------------------------------
    # 3. GLOBAL TOP 3 LEAGUE LEADERBOARD
    # ------------------------------------------------------------------
    st.markdown("### 🏆 Global Dhurandar League: Top 3 Ranks (All Over Data)")
    
    # Filter global records matching overall Rank positions 1, 2, or 3
    df_global_top3 = df_breeze[df_breeze['Rank'].isin([1, 2, 3])].sort_values(by='Rank', ascending=True).copy()
    
    if not df_global_top3.empty:
        # Create clear formatting columns for presentation layout
        display_global = df_global_top3[['Rank', 'DS Name', 'DS Type', 'AE ID', 'WD Code (Linked)']].copy()
        display_global.columns = ['Rank 🏅', 'DS Name', 'DS Type', 'Mapped AE ID', 'Linked WD Code']
        display_global = display_global.reset_index(drop=True)
        
        # Enclose within an expandable wrapper segment to maximize narrow device screen layout usability
        with st.expander("👁️ Click to View / Hide Global Rank 1, 2 & 3 Performers Table", expanded=True):
            st.dataframe(
                display_global,
                use_container_width=True,
                column_config={
                    "Rank 🏅": st.column_config.NumberColumn("Rank 🏅", format="%d")
                }
            )
    else:
        st.warning("No global data found matching Rank 1, 2, or 3 parameters.")
        
    st.markdown("---")
    
    # ------------------------------------------------------------------
    # 4. INDIVIDUAL REGIONAL FILTERS & HIGH-LEVEL KPI CARDS
    # ------------------------------------------------------------------
    df_ae_filtered = df_breeze[df_breeze['AE ID'] == selected_ae].copy()
    
    if not df_ae_filtered.empty:
        st.subheader(f"📊 Live Dashboard: Executive Summary for {selected_ae}")
        
        # Address multi-header duplicate name assignments injected automatically by pandas engine
        # index 2 (.2) references target metrics under the strict Radar tracking matrix for Van DS
        qual_cols = [c for c in df_breeze.columns if 'till date qual' in c.lower()]
        van_visit_col = qual_cols[2] if len(qual_cols) >= 3 else qual_cols[0]
        
        # Formulate conditional cross-segment field parsers
        def get_resolved_metrics(row):
            is_van = "van" in str(row['DS Type']).lower()
            if is_van:
                mapped = pd.to_numeric(row['Outlet Mapped'], errors='coerce')
                visits = pd.to_numeric(row[van_visit_col], errors='coerce')
            else:
                mapped = pd.to_numeric(row['Outlets Mapped'], errors='coerce')
                visits = pd.to_numeric(row['Till date Visit'], errors='coerce')
            return pd.Series([mapped, visits])

        # Execute data mappings across filtered sub-rows
        df_ae_filtered[['Resolved_Mapped', 'Resolved_Visits']] = df_ae_filtered.apply(get_resolved_metrics, axis=1)
        
        # Enforce numeric fallback parameters to bypass NaN breaks
        df_ae_filtered['Resolved_Mapped'] = df_ae_filtered['Resolved_Mapped'].fillna(0).astype(int)
        df_ae_filtered['Resolved_Visits'] = df_ae_filtered['Resolved_Visits'].fillna(0).astype(int)
        
        # Calculate scorecard summation fields
        total_ds_count = len(df_ae_filtered)
        total_outlets_mapped = df_ae_filtered['Resolved_Mapped'].sum()
        total_effective_visits = df_ae_filtered['Resolved_Visits'].sum()
        
        # % UOV Calculation logic
        if total_outlets_mapped > 0:
            pct_uov = (total_effective_visits / total_outlets_mapped) * 100
        else:
            pct_uov = 0.0
            
        # Display horizontal dashboard UI KPI elements block
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="👥 Total DS Count", value=f"{total_ds_count}")
        with m_col2:
            st.metric(label="📍 Total Outlets Mapped", value=f"{total_outlets_mapped:,}")
        with m_col3:
            st.metric(label="📈 Percentage UOV", value=f"{pct_uov:.2f}%")
            
        # ------------------------------------------------------------------
        # 5. FILTERED LOCAL LEADERBOARD MATRIX
        # ------------------------------------------------------------------
        st.markdown("### 🏆 Top 3 DS Performance Leaderboard (Selected AE Only)")
        
        # Extract targeted regional winners ranking positions
        top_3_ds = df_ae_filtered.sort_values(by='Rank', ascending=True).head(3)
        
        # Format layout data tracking elements
        display_leaderboard = top_3_ds[['Rank', 'DS Name', 'DS Type', 'WD Code (Linked)', 'Resolved_Mapped', 'Resolved_Visits']].copy()
        display_leaderboard.columns = ['Rank Position', 'Digital Sales Representative (DS)', 'DS Type', 'Linked WD Code', 'Outlets Mapped', 'Till Date Visits']
        display_leaderboard = display_leaderboard.reset_index(drop=True)
        
        # Construct main presentation interactive grid
        st.dataframe(
            display_leaderboard, 
            use_container_width=True,
            column_config={
                "Rank Position": st.column_config.NumberColumn("Rank 🏅", format="%d"),
                "Outlets Mapped": st.column_config.NumberColumn("Outlets Mapped", format="%d"),
                "Till Date Visits": st.column_config.NumberColumn("Till Date Visits", format="%d")
            }
        )
        
    else:
        st.error(f"No active records indexed under the entered AE ID: {selected_ae}")