import streamlit as st
import pandas as pd
import os

# Set up page layout to occupy full width with a custom page title
st.set_page_config(
    page_title="Dhurandar League", 
    layout="wide", 
    page_icon="⚡"
)

# ------------------------------------------------------------------
# SYNC URL PARAMETERS WITH POPUP MODE (REMOVES GHOST BUTTONS)
# ------------------------------------------------------------------
if "show_cat" in st.query_params:
    st.session_state['show_popup_category'] = st.query_params["show_cat"]
else:
    st.session_state['show_popup_category'] = None

# ------------------------------------------------------------------
# PREMIUM CUSTOM DARK MODE CSS INJECTION
# ------------------------------------------------------------------
st.markdown("""
    <style>
        /* Global App Background and Text colors */
        .stApp {
            background-color: #0d1117;
            color: #c9d1d9;
        }
        
        /* Modern Glassmorphic Container Cards with Fixed Height for Uniformity */
        .metric-card {
            background: linear-gradient(135deg, rgba(22, 27, 34, 0.8), rgba(13, 17, 23, 0.8));
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            min-height: 160px; 
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        
        /* Interactive text link items styled inside the card boundary */
        .category-link {
            color: #58a6ff !important;
            font-weight: 700 !important;
            text-decoration: underline !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
        }
        .category-link:hover {
            color: #ffffff !important;
            text-shadow: 0 0 10px rgba(88, 166, 255, 0.8);
        }
        
        /* Premium Badges for Leaderboard ranks */
        .rank-badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 13px;
            display: inline-block;
            text-align: center;
            min-width: 80px;
        }
        .rank-1 { background-color: rgba(212, 175, 55, 0.2); color: #ffd700; border: 1px solid #ffd700; }
        .rank-2 { background-color: rgba(192, 192, 192, 0.2); color: #c0c0c0; border: 1px solid #c0c0c0; }
        .rank-3 { background-color: rgba(205, 127, 50, 0.2); color: #cd7f32; border: 1px solid #cd7f32; }
        .rank-other { background-color: rgba(48, 54, 61, 0.4); color: #c9d1d9; border: 1px solid #30363d; }

        /* Clean typography styles */
        .metric-label {
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #8b949e;
            font-weight: 600;
            margin-bottom: 4px;
        }
        .metric-value {
            font-size: 36px;
            font-weight: 700;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin-bottom: 4px;
        }
        .metric-glow {
            text-shadow: 0 0 12px rgba(88, 166, 255, 0.6);
            color: #58a6ff;
        }

        /* Bold, High Impact, Mechanical Subheading Design */
        .subtitle-league-container {
            margin-top: 5px;
            margin-bottom: 25px;
            padding: 2px 0px;
        }
        .subtitle-league {
            font-family: 'Segoe UI', apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            font-weight: 900 !important;
            font-size: 28px !important;
            letter-spacing: 5px !important;
            color: #ffffff !important;
            text-transform: uppercase !important;
            text-shadow: 0 0 15px rgba(88, 166, 255, 0.75) !important;
            display: block !important;
        }
        
        /* Leaderboard Row List Styling */
        .leaderboard-row {
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            background: linear-gradient(90deg, #161b22, #0d1117);
            padding: 16px 24px; 
            margin-bottom: 10px; 
            border-radius: 12px; 
            border: 1px solid #30363d;
            transition: border-color 0.2s ease, background-color 0.2s ease;
        }
        .leaderboard-row:hover {
            border-color: #444c56;
            background: #1c2128;
        }
    </style>
""", unsafe_allow_html=True)

# App Logo Header Banner
st.markdown('<div class="subtitle-league-container"><span class="subtitle-league">DHURANDAR LEAGUE</span></div>', unsafe_allow_html=True)
st.markdown("   ")

#                                                                   
# CONFIGURATION: GOOGLE DRIVE FILE SHARING IDs
#                                                                   
DHURANDAR_SHARE_ID = "1ofdBAMowgrFcf-NyjOW4QMFVh8Wk7OKi" 
OUTLET_MASTER_SHARE_ID = "1kxGk5IvkPLGLE0Dg6vCxQ1NeT8V8xPQu" 
RADAR_ROUTE_SHARE_ID = "1AKW089LhV37onfSEmk4H6l86f4MsQTCr"

# Formulating direct download links
URL_BREEZE = f"https://docs.google.com/uc?export=download&id={DHURANDAR_SHARE_ID}"
URL_MASTER = f"https://docs.google.com/uc?export=download&id={OUTLET_MASTER_SHARE_ID}"
URL_ROUTE = f"https://docs.google.com/uc?export=download&id={RADAR_ROUTE_SHARE_ID}"

@st.cache_data(ttl=3600)
def load_live_cloud_data():
    if "YOUR_GOOGLE_DRIVE_ID" in DHURANDAR_SHARE_ID:
        return None, None, None, "setup_needed"
    try:
        df_breeze = pd.read_csv(URL_BREEZE, skiprows=2, encoding="latin-1")
        df_master = pd.read_csv(URL_MASTER, encoding="latin-1")
        df_route = pd.read_csv(URL_ROUTE, encoding="latin-1")
        return df_breeze, df_master, df_route, "success"
    except Exception as e:
        return None, None, None, str(e)

df_breeze, df_master, df_route, status_msg = load_live_cloud_data()

if status_msg == "setup_needed":
    st.info("👋 Welcome to Breeze!")
    st.warning("⚠️ **Configuration Key Missing:** Please open your `app.py` script file and input your active Google Drive sharing hashes to enable cloud streaming.")
    st.stop()
elif status_msg != "success":
    st.error("💥 Cloud Connection Aborted.")
    st.markdown(f"**Error Details:** `{status_msg}`")
    st.stop()

#                                                                   
# DATA PIPELINE & CALCULATIONS ENGINE
#                                                                   
if df_breeze is not None and df_master is not None and df_route is not None:
    
    # Text sanitization pipeline
    df_breeze['AE ID'] = df_breeze['AE ID'].astype(str).str.strip()
    df_breeze['DS ID_str'] = df_breeze['DS ID'].astype(str).str.strip()
    df_breeze['DS Type'] = df_breeze['DS Type'].astype(str).str.strip()
    df_breeze['Rank'] = pd.to_numeric(df_breeze['Rank'], errors='coerce')
    
    df_master['DS/TL ID_str'] = df_master['DS/TL ID'].astype(str).str.strip()
    df_route['DS Id_str'] = df_route['DS Id'].astype(str).str.strip()
    
    # Map out cross sheet relationships
    ds_to_wd_dict = df_master.groupby('DS/TL ID_str')['WD ID'].first().to_dict()
    van_ds_to_wd_dict = df_route.groupby('DS Id_str')['WD Code'].first().to_dict()
    
    def assign_linked_wd_code(row):
        is_van = "van" in str(row['DS Type']).lower()
        ds_id = row['DS ID_str']
        if is_van and ds_id in van_ds_to_wd_dict:
            return van_ds_to_wd_dict[ds_id]
        return ds_to_wd_dict.get(ds_id, None)
            
    df_breeze['WD Code (Linked)'] = df_breeze.apply(assign_linked_wd_code, axis=1)
    unique_ae_ids = sorted(df_breeze['AE ID'].dropna().unique())
    
    # Styled Input Selector Widget Block
    col_sb, _ = st.columns([2, 2])
    with col_sb:
        selected_ae = st.selectbox("Choose AE id", options=unique_ae_ids, index=0)
    
    # ------------------------------------------------------------------
    # DATA ASSIGNMENT PARSERS & PRE-CALCULATIONS FOR FILTERED AE
    # ------------------------------------------------------------------
    df_ae_filtered = df_breeze[df_breeze['AE ID'] == selected_ae].copy()
    
    if not df_ae_filtered.empty:
        qual_cols = [c for c in df_breeze.columns if 'till date qual' in c.lower()]
        van_visit_col = qual_cols[2] if len(qual_cols) >= 3 else qual_cols[0]
        
        def get_resolved_metrics(row):
            is_van = "van" in str(row['DS Type']).lower()
            if is_van:
                return pd.Series([pd.to_numeric(row['Outlet Mapped'], errors='coerce'), pd.to_numeric(row[van_visit_col], errors='coerce')])
            return pd.Series([pd.to_numeric(row['Outlets Mapped'], errors='coerce'), pd.to_numeric(row['Till date Visit'], errors='coerce')])

        df_ae_filtered[['Resolved_Mapped', 'Resolved_Visits']] = df_ae_filtered.apply(get_resolved_metrics, axis=1)
        df_ae_filtered['Resolved_Mapped'] = df_ae_filtered['Resolved_Mapped'].fillna(0).astype(int)
        df_ae_filtered['Resolved_Visits'] = df_ae_filtered['Resolved_Visits'].fillna(0).astype(int)
        
        # Summary variables computation
        total_ds_count = len(df_ae_filtered)
        total_outlets_mapped = df_ae_filtered['Resolved_Mapped'].sum()
        total_effective_visits = df_ae_filtered['Resolved_Visits'].sum()
        pct_uov = (total_effective_visits / total_outlets_mapped * 100) if total_outlets_mapped > 0 else 0.0

        # Calculate counts
        ds_types_lower = df_ae_filtered['DS Type'].astype(str).str.lower()
        conv_count = (ds_types_lower.str.contains('conv')).sum()
        rmd_count = (ds_types_lower.str.contains('rmd')).sum()
        van_count = (ds_types_lower.str.contains('van')).sum()

    # ------------------------------------------------------------------
    # DYNAMIC INTERACTIVE DETAIL POPUP WINDOW MODAL (URL DRIVEN)
    # ------------------------------------------------------------------
    if st.session_state['show_popup_category'] is not None:
        cat_selected = st.session_state['show_popup_category']
        
        if cat_selected == 'conv':
            df_popup_base = df_ae_filtered[df_ae_filtered['DS Type'].astype(str).str.lower().str.contains('conv')].copy()
            popup_label = "Conventional DS Segment"
        elif cat_selected == 'rmd':
            df_popup_base = df_ae_filtered[df_ae_filtered['DS Type'].astype(str).str.lower().str.contains('rmd')].copy()
            popup_label = "RMD DS Segment"
        else:
            df_popup_base = df_ae_filtered[df_ae_filtered['DS Type'].astype(str).str.lower().str.contains('van')].copy()
            popup_label = "Van DS Segment"

        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1c2128, #0d1117); border: 2px solid #58a6ff; border-radius: 16px; padding: 20px; margin-bottom: 25px; box-shadow: 0 0 20px rgba(88, 166, 255, 0.25);">
                <h4 style="color: #ffffff; margin: 0 0 10px 0;">Detailed Summary: {popup_label} ({selected_ae})</h4>
            </div>
        """, unsafe_allow_html=True)
        
        pop_ctrl_1, pop_ctrl_2 = st.columns([3, 1])
        
        with pop_ctrl_1:
            unique_popup_wds = sorted(df_popup_base['WD Code (Linked)'].dropna().astype(str).unique())
            chosen_popup_wd = st.selectbox(
                "Choose WD Code",
                options=[""] + unique_popup_wds,
                index=0,
                format_func=lambda x: "Select WD Code (Showing All)..." if x == "" else f"WD Code: {x}",
                key="wd_popup_search_filter"
            )
        
        with pop_ctrl_2:
            st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
            if st.button("❌ Close Details", key="btn_close_popup_panel", use_container_width=True):
                st.query_params.clear()
                st.session_state['show_popup_category'] = None
                st.rerun()

        if chosen_popup_wd != "":
            df_popup_filtered = df_popup_base[df_popup_base['WD Code (Linked)'].astype(str) == chosen_popup_wd].copy()
        else:
            df_popup_filtered = df_popup_base.copy()

        popup_records = []
        for _, prow in df_popup_filtered.iterrows():
            p_name = prow['DS Name']
            p_wd = prow['WD Code (Linked)'] if pd.notna(prow['WD Code (Linked)']) else 'N/A'
            
            if cat_selected == 'van':
                p_qual = prow['Till Date Qualifed.1'] if 'Till Date Qualifed.1' in prow and pd.notna(prow['Till Date Qualifed.1']) else 0
                p_visit = prow['Till Date Qualifed.2'] if 'Till Date Qualifed.2' in prow and pd.notna(prow['Till Date Qualifed.2']) else 0
            else:
                p_qual = prow['Till Date Qualifed'] if 'Till Date Qualifed' in prow and pd.notna(prow['Till Date Qualifed']) else 0
                p_visit = prow['Till date Visit'] if 'Till date Visit' in prow and pd.notna(prow['Till date Visit']) else 0
                
            popup_records.append({
                "DS Name": p_name,
                "Linked WD Code": p_wd,
                "Till Date Qualified": int(pd.to_numeric(p_qual, errors='coerce') if pd.notna(p_qual) else 0),
                "Total Visit": int(pd.to_numeric(p_visit, errors='coerce') if pd.notna(p_visit) else 0)
            })

        df_popup_final_grid = pd.DataFrame(popup_records)
        
        if not df_popup_final_grid.empty:
            st.dataframe(df_popup_final_grid.reset_index(drop=True), use_container_width=True)
        else:
            st.info("No active sales records mapped under the chosen filtration settings.")
            
        st.markdown("---")

    # ------------------------------------------------------------------
    # UI COMPONENT: 🏆 GLOBAL DHURANDAR LEAGUE EXPANDER
    # ------------------------------------------------------------------
    df_global_top3 = df_breeze[df_breeze['Rank'].isin([1, 2, 3])].sort_values(by='Rank', ascending=True).copy()
    
    if not df_global_top3.empty:
        with st.expander("Global League Leaderboard (Rank 1-3)", expanded=False):
            for idx, row in df_global_top3.iterrows():
                r = int(row['Rank'])
                badge_class = f"rank-{r}"
                
                st.markdown(f"""
                    <div class="leaderboard-row" style="border-left: 4px solid #1f6feb;">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <span class="rank-badge {badge_class}">RANK {r}</span>
                            <strong style="color: #ffffff; font-size: 16px;">{row['DS Name']}</strong>
                            <span style="color: #8b949e; font-size: 13px;">({row['DS Type']})</span>
                        </div>
                        <div>
                            <span style="color: #8b949e; font-size: 13px;">AE ID:</span> <strong style="color: #58a6ff;">{row['AE ID']}</strong>
                            <span style="margin-left: 15px; color: #8b949e; font-size: 13px;">WD Code:</span> <strong style="color: #58a6ff;">{row['WD Code (Linked)'] if pd.notna(row['WD Code (Linked)']) else 'N/A'}</strong>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ------------------------------------------------------------------
    # UI COMPONENT: 📊 LIVE METRIC GLASS CARDS (CLEAN INLINE TEXT LINKS)
    # ------------------------------------------------------------------
    if not df_ae_filtered.empty:
        c1, c2, c3 = st.columns(3)
        
        with c1:
            # Clickable text link objects targeting _self parameters completely locks the action within bounds
            st.markdown(f"""
                <div class="metric-card">
                    <div>
                        <div class="metric-label">👥 Total DS Workforce</div>
                        <div class="metric-value">{total_ds_count} <span style="font-size:18px; color:#58a6ff;">Hawkers</span></div>
                    </div>
                    <div style="border-top: 1px solid #30363d; padding-top: 10px; font-size: 13px; color: #8b949e; display: flex; justify-content: space-between; gap: 4px; width: 100%;">
                        <span>Conv: <a href="?show_cat=conv" target="_self" class="category-link">({conv_count})</a></span>
                        <span>RMD: <a href="?show_cat=rmd" target="_self" class="category-link">({rmd_count})</a></span>
                        <span>Van: <a href="?show_cat=van" target="_self" class="category-link">({van_count})</a></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
                    
        with c2:
            st.markdown(f"""
                <div class="metric-card">
                    <div>
                        <div class="metric-label">📍 Total Outlets Mapped</div>
                        <div class="metric-value">{total_outlets_mapped:,} <span style="font-size:18px; color:#34d399;">Stores</span></div>
                    </div>
                    <div style="margin-top: auto; border-top: 1px solid transparent; padding-top: 10px; font-size: 12px; color: #8b949e; text-align: left;">
                        Database Records Active
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
                <div class="metric-card">
                    <div>
                        <div class="metric-label">📈 Overall Efficiency</div>
                        <div class="metric-value metric-glow">{pct_uov:.2f}%</div>
                    </div>
                    <div style="margin-top: auto; border-top: 1px solid transparent; padding-top: 10px; font-size: 12px; color: #8b949e; text-align: left;">
                        Unique Visit Coverage (% UOV)
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # ------------------------------------------------------------------
        # UI COMPONENT: CUSTOM STYLED PERFORMANCE STANDINGS HEADING WITH ID
        # ------------------------------------------------------------------
        st.markdown(f"### Performance Standings <span style='color: #58a6ff; font-weight: 400; font-size: 22px; margin-left: 8px;'>({selected_ae})</span>", unsafe_allow_html=True)
        
        # Extract top 3 local area representatives
        top_3_ds = df_ae_filtered.sort_values(by='Rank', ascending=True).head(3)
        
        for idx, row in top_3_ds.iterrows():
            r = int(row['Rank']) if pd.notna(row['Rank']) else "N/A"
            
            if r == 1:
                badge_class = "rank-1"
                row_border = "border-left: 5px solid #ffd700;"
            elif r == 2:
                badge_class = "rank-2"
                row_border = "border-left: 5px solid #c0c0c0;"
            elif r == 3:
                badge_class = "rank-3"
                row_border = "border-left: 5px solid #cd7f32;"
            else:
                badge_class = "rank-other"
                row_border = "border-left: 5px solid #30363d;"
                
            wd_code_display = row['WD Code (Linked)'] if pd.notna(row['WD Code (Linked)']) else 'N/A'
            
            st.markdown(f"""
                <div class="leaderboard-row" style="{row_border}">
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <span class="rank-badge {badge_class}">RANK {r}</span>
                        <div>
                            <div style="color: #ffffff; font-size: 18px; font-weight: 700;">{row['DS Name']}</div>
                            <div style="color: #8b949e; font-size: 13px; margin-top: 2px;">
                                Type: <span style="color: #c9d1d9;">{row['DS Type']}</span> | 
                                WD Code: <span style="color: #58a6ff; font-weight: 600;">{wd_code_display}</span>
                            </div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 30px; text-align: right;">
                        <div>
                            <div style="color: #8b949e; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Outlets Mapped</div>
                            <div style="color: #ffffff; font-size: 20px; font-weight: bold; margin-top: 4px;">{int(row['Resolved_Mapped'])}</div>
                        </div>
                        <div>
                            <div style="color: #8b949e; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Till Date Visits</div>
                            <div style="color: #34d399; font-size: 20px; font-weight: bold; margin-top: 4px;">{int(row['Resolved_Visits'])}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    else:
        st.error(f"No records indexed under area segment parameter: {selected_ae}")
