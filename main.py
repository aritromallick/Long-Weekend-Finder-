import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
import urllib.parse
from utils import (
    get_countries,
    get_years,
    get_long_weekend_potentials,
    create_whatsapp_share_text,
    get_holidays_for_month
)
from weather_api import weather_api

# Page configuration
st.set_page_config(
    page_title="Long Weekend Finder",
    page_icon="📅",
    layout="wide"
)

# Load custom CSS
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state for favorites
if 'favorites' not in st.session_state:
    st.session_state.favorites = set()

# Title and description
st.title("📅 Long Weekend Finder")
st.markdown("""
Find the perfect long weekend opportunities by planning your leaves strategically!
""")

# Main filters in the content area
col1, col2 = st.columns(2)

with col1:
    selected_country = st.selectbox(
        "Select Country",
        options=get_countries(),
        index=0  # Default to India
    )

with col2:
    selected_year = st.selectbox(
        "Select Year",
        options=get_years(),
        index=1  # Default to 2025
    )

# Main content
content_col1, content_col2 = st.columns([2, 1])

with content_col1:
    st.subheader("Long Weekend Opportunities")
    potentials = get_long_weekend_potentials(selected_country, selected_year)

    for potential in potentials:
        with st.container():
            # Create WhatsApp share link
            share_text = create_whatsapp_share_text(potential)
            whatsapp_link = f"https://wa.me/?text={urllib.parse.quote(share_text)}"

            # Get weather forecast for the start date
            weather = weather_api.get_forecast("Mumbai", potential['start_date'])  # Default to Mumbai for India

            # Check if this plan is in favorites
            plan_id = f"{potential['holiday']}_{potential['holiday_date']}"
            is_favorite = plan_id in st.session_state.favorites

            st.markdown(f"""
            <div class="holiday-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="card-title">{potential['holiday']}</div>
                    <button 
                        class="favorite-btn" 
                        onclick="handleFavorite('{plan_id}')"
                        style="color: {'#FFD700' if is_favorite else '#gray'}">
                        {'★' if is_favorite else '☆'}
                    </button>
                </div>
                <div class="info-text">Holiday: {potential['holiday_date']}</div>
                <div class="info-text">Duration: {potential['total_days']} days</div>
                <div class="info-text">From: {potential['start_date']} To: {potential['end_date']}</div>
                <div class="highlight-text">
                    Leaves needed: {', '.join(potential['leaves_needed']) if potential['leaves_needed'] else 'No leaves needed!'}
                </div>
                {f'''
                <div class="weather-info">
                    <img src="{weather['icon']}" alt="weather" style="width: 32px; height: 32px;"/>
                    <span>{weather['condition']}</span>
                    <span>{weather['max_temp']}°C / {weather['min_temp']}°C</span>
                </div>
                ''' if weather else ''}
                <div style="margin-top: 10px;">
                    <a href="{whatsapp_link}" target="_blank" style="text-decoration: none;">
                        <svg class="whatsapp-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                            <path fill="#25D366" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                        </svg>
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

with content_col2:
    st.subheader("Calendar View")

    # Get current month as default
    current_month = datetime.now().month
    month_names = list(calendar.month_name)[1:]
    selected_month = st.selectbox("Select Month", month_names, index=current_month-1)
    month_num = month_names.index(selected_month) + 1

    # Get calendar and holidays for selected month
    cal = calendar.monthcalendar(selected_year, month_num)
    holidays = get_holidays_for_month(selected_country, selected_year, month_num)

    # Convert calendar to DataFrame for display
    df = pd.DataFrame(cal, columns=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

    # Style the calendar
    def highlight_dates(val):
        if val == 0:
            return ''

        date_str = f"{selected_year}-{month_num:02d}-{val:02d}"
        if date_str in holidays:
            return 'background-color: rgba(37, 211, 102, 0.2)'
        elif pd.to_datetime(date_str).weekday() >= 5:
            return 'background-color: rgba(255, 255, 255, 0.1)'
        return ''

    styled_df = df.style.applymap(highlight_dates)

    # Display calendar
    with st.container():
        st.markdown('<div class="calendar-view">', unsafe_allow_html=True)
        st.table(styled_df)
        st.markdown('</div>', unsafe_allow_html=True)

# Add JavaScript for handling favorites
st.markdown("""
<script>
function handleFavorite(planId) {
    // Toggle favorite status
    const currentState = window.localStorage.getItem(planId) === 'true';
    window.localStorage.setItem(planId, !currentState);

    // Update UI
    const btn = document.querySelector(`button[onclick="handleFavorite('${planId}')"]`);
    btn.innerHTML = !currentState ? '★' : '☆';
    btn.style.color = !currentState ? '#FFD700' : '#gray';
}
</script>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
---
Made with ❤️ by Long Weekend Finder
""")