"""
UI Components: Premium styling, custom CSS injection, and layout components.
"""

import streamlit as st


def inject_custom_css():
    """Injects premium styling and glassmorphism elements."""
    st.markdown(
        """
        <style>
        /* Glassmorphic Cards */
        .glass-card {
            background: rgba(31, 38, 53, 0.6);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 24px;
            margin-bottom: 20px;
            color: #fafafa;
        }
        
        /* Metric KPI Cards */
        .kpi-container {
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }
        
        .kpi-card {
            flex: 1;
            min-width: 200px;
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.15) 0%, rgba(31, 38, 53, 0.8) 100%);
            border: 1px solid rgba(138, 43, 226, 0.3);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        }
        
        .kpi-val {
            font-size: 2rem;
            font-weight: 700;
            color: #b388ff;
            margin-bottom: 4px;
        }
        
        .kpi-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #a5b4fc;
        }
        
        /* Streamlit Adjustments */
        .stButton>button {
            background: linear-gradient(135deg, #8a2be2 0%, #4a0e4e 100%);
            color: white;
            border: none;
            padding: 8px 24px;
            font-weight: 600;
            border-radius: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(138, 43, 226, 0.6);
            background: linear-gradient(135deg, #a044ff 0%, #6a11cb 100%);
            color: white;
        }
        
        /* Table enhancements */
        .dataframe {
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            background-color: #1f2635 !important;
            color: #fafafa !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, icon: str = "🎯"):
    """Renders a single KPI card."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">{icon}</div>
            <div class="kpi-val">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_header(title: str, subtitle: str):
    """Renders a standard premium header."""
    st.markdown(
        f"""
        <div style="margin-bottom: 30px;">
            <h1 style="color: #fafafa; font-size: 2.5rem; margin-bottom: 8px; font-weight: 800; background: linear-gradient(to right, #ffffff, #b388ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{title}</h1>
            <p style="color: #a5b4fc; font-size: 1.1rem; margin-top: 0;">{subtitle}</p>
            <hr style="border-color: rgba(138, 43, 226, 0.2); margin-top: 20px;">
        </div>
        """,
        unsafe_allow_html=True
    )
