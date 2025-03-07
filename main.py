import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
import urllib.parse
from utils import (
    get_countries,
    get_years,
    get_long_weekend_potentials,
    create_whatsapp_share_text
)

# Page configuration
st.set_page_config(
    page_title="Long Weekend Finder",
    page_icon="📅",
    layout="wide"
)

# Load custom CSS
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title and description
st.title("📅 Long Weekend Finder")
st.markdown("""
Find the perfect long weekend opportunities by planning your leaves strategically!
Choose your country and year to get started.
""")

# Sidebar filters
with st.sidebar:
    st.header("Settings")
    selected_country = st.selectbox(
        "Select Country",
        options=get_countries(),
        index=0  # Default to India
    )

    selected_year = st.selectbox(
        "Select Year",
        options=get_years(),
        index=1  # Default to 2025
    )

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Long Weekend Opportunities")

    potentials = get_long_weekend_potentials(selected_country, selected_year)

    for potential in potentials:
        with st.container():
            # Create WhatsApp share link
            share_text = create_whatsapp_share_text(potential)
            whatsapp_link = f"https://wa.me/?text={urllib.parse.quote(share_text)}"

            st.markdown(f"""
            <div class="holiday-card">
                <div class="card-title">{potential['holiday']}</div>
                <div class="info-text">Holiday: {potential['holiday_date']}</div>
                <div class="info-text">Duration: {potential['total_days']} days</div>
                <div class="info-text">From: {potential['start_date']} To: {potential['end_date']}</div>
                <div class="highlight-text">
                    Leaves needed: {', '.join(potential['leaves_needed']) if potential['leaves_needed'] else 'No leaves needed!'}
                </div>
                <div style="margin-top: 10px;">
                    <a href="{whatsapp_link}" target="_blank" style="text-decoration: none;">
                        <button style="background-color: #25D366; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">
                            Share on WhatsApp 💬
                        </button>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

with col2:
    st.subheader("Calendar View")

    # Create calendar view
    month_names = list(calendar.month_name)[1:]
    selected_month = st.selectbox("Select Month", month_names)
    month_num = month_names.index(selected_month) + 1

    # Get calendar for selected month
    cal = calendar.monthcalendar(selected_year, month_num)

    # Convert calendar to DataFrame for display
    df = pd.DataFrame(cal, columns=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

    # Style the calendar
    def highlight_weekends(val):
        color = '#f0f2f6' if val != 0 else ''
        return f'background-color: {color}'

    styled_df = df.style.map(highlight_weekends)

    # Display calendar
    with st.container():
        st.markdown('<div class="calendar-view">', unsafe_allow_html=True)
        st.table(styled_df)
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
---
Made with ❤️ by Long Weekend Finder
""")