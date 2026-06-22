import streamlit as st
import anthropic
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="PRD Generator — AI-Powered Product Requirements",
    page_icon="📋",
    layout="wide"
)
# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #0F1117;
    }
    
    .stApp {
        background-color: #0F1117;
        color: #E8EAF0;
    }

    h1, h2, h3 {
        color: #E8EAF0 !important;
        font-weight: 700 !important;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        color: #E8EAF0;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #8B92A5;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    .accent {
        color: #4F8EF7;
    }

    .card {
        background: #1A1D27;
        border: 1px solid #2A2D3A;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .section-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #4F8EF7;
        margin-bottom: 0.5rem;
    }

    .prd-output {
        background: #1A1D27;
        border: 1px solid #2A2D3A;
        border-radius: 12px;
        padding: 2rem;
        font-family: 'Inter', sans-serif;
        color: #E8EAF0;
        line-height: 1.8;
    }

    .prd-section-title {
        color: #4F8EF7;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #2A2D3A;
    }

    .tag {
        display: inline-block;
        background: #1E2A45;
        color: #4F8EF7;
        border: 1px solid #2A4080;
        border-radius: 20px;
        padding: 0.2rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 500;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }

    .stTextArea textarea {
        background-color: #1A1D27 !important;
        color: #E8EAF0 !important;
        border: 1px solid #2A2D3A !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.92rem !important;
    }

    .stTextArea textarea:focus {
        border-color: #4F8EF7 !important;
        box-shadow: 0 0 0 2px rgba(79, 142, 247, 0.15) !important;
    }

    .stSelectbox > div > div {
        background-color: #1A1D27 !important;
        color: #E8EAF0 !important;
        border: 1px solid #2A2D3A !important;
        border-radius: 8px !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #4F8EF7, #3B6FD4) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #6BA3FF, #4F8EF7) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 15px rgba(79, 142, 247, 0.3) !important;
    }

    .stDownloadButton > button {
        background: #1A1D27 !important;
        color: #4F8EF7 !important;
        border: 1px solid #4F8EF7 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }

    .metric-box {
        background: #1A1D27;
        border: 1px solid #2A2D3A;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
    }

    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #4F8EF7;
    }

    .metric-label {
        font-size: 0.75rem;
        color: #8B92A5;
        margin-top: 0.2rem;
    }

    div[data-testid="stMarkdownContainer"] p {
        color: #C8CDD8;
    }

    .stSpinner > div {
        border-top-color: #4F8EF7 !important;
    }

    hr {
        border-color: #2A2D3A !important;
    }

    .footer {
        text-align: center;
        color: #4A5060;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #2A2D3A;
    }
</style>
""", unsafe_allow_html=True)


def generate_prd(feature_request: str, product_context: str, target_users: str, 
                  priority: str, platform: str) -> str:
    """Generate a structured PRD using Claude API."""
    
    client = anthropic.Anthropic()
    
    system_prompt = """You are a senior Technical Product Manager at a top-tier tech company. 
Your job is to turn raw feature requests into clear, structured Product Requirements Documents (PRDs).

Output a PRD with exactly these sections, using this format:

## Overview
[2-3 sentence summary of what this feature is and why it matters]

## Problem Statement
[The specific user pain point or business gap this solves. Be precise.]

## Goals & Success Metrics
[3-5 measurable outcomes. Use KPIs, not vague statements.]

## User Stories
[3-5 user stories in format: As a [user type], I want to [action] so that [benefit]]

## Functional Requirements
[Numbered list of specific, testable requirements — what the system must do]

## Non-Functional Requirements
[Performance, security, scalability, accessibility constraints]

## Acceptance Criteria
[Numbered list of conditions that must be true for this feature to be considered complete]

## Edge Cases & Risks
[3-5 scenarios that could break the feature or create problems]

## Out of Scope
[What this feature explicitly does NOT include — prevents scope creep]

## Open Questions
[2-4 unresolved decisions that need stakeholder input]

Be specific, direct, and concise. No filler. Write like a PM who respects engineers' time."""

    user_message = f"""Generate a PRD for the following:

Feature Request: {feature_request}

Product Context: {product_context if product_context else "Not provided"}

Target Users: {target_users if target_users else "Not specified"}

Priority Level: {priority}

Platform/Surface: {platform}

Output only the PRD. No preamble."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": user_message}
        ],
        system=system_prompt
    )
    
    return message.content[0].text


def count_sections(prd_text: str) -> int:
    return prd_text.count("##")


# ── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 2rem 0 1rem 0;">
    <div class="hero-title">AI <span class="accent">PRD</span> Generator</div>
    <div class="hero-subtitle">Turn a rough feature idea into a structured Product Requirements Document in seconds.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── LAYOUT ──────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1.4], gap="large")

with left_col:
    st.markdown('<div class="section-label">Feature Request</div>', unsafe_allow_html=True)
    feature_request = st.text_area(
        label="feature_request",
        placeholder="e.g. Add Apple Pay to the checkout flow so users can complete purchases without entering card details manually",
        height=120,
        label_visibility="collapsed"
    )

    st.markdown('<div class="section-label" style="margin-top:1rem;">Product Context</div>', unsafe_allow_html=True)
    product_context = st.text_area(
        label="product_context",
        placeholder="e.g. B2C e-commerce platform, 2M monthly active users, mobile-first, existing payment methods: Stripe credit/debit",
        height=90,
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-label" style="margin-top:1rem;">Target Users</div>', unsafe_allow_html=True)
        target_users = st.text_area(
            label="target_users",
            placeholder="e.g. Mobile shoppers aged 18-35 who prefer fast checkout",
            height=80,
            label_visibility="collapsed"
        )

    with col2:
        st.markdown('<div class="section-label" style="margin-top:1rem;">Priority</div>', unsafe_allow_html=True)
        priority = st.selectbox(
            label="priority",
            options=["P0 — Critical", "P1 — High", "P2 — Medium", "P3 — Low"],
            label_visibility="collapsed"
        )

        st.markdown('<div class="section-label" style="margin-top:0.8rem;">Platform</div>', unsafe_allow_html=True)
        platform = st.selectbox(
            label="platform",
            options=["Mobile (iOS & Android)", "Web", "Mobile + Web", "API / Backend", "Desktop", "Other"],
            label_visibility="collapsed"
        )

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    generate_btn = st.button("Generate PRD →", type="primary")

    # Example tags
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Try an example</div>', unsafe_allow_html=True)
    st.markdown("""
    <div>
        <span class="tag">Apple Pay checkout</span>
        <span class="tag">In-app notifications</span>
        <span class="tag">Dark mode</span>
        <span class="tag">User onboarding flow</span>
        <span class="tag">Search filters</span>
        <span class="tag">Subscription billing</span>
    </div>
    """, unsafe_allow_html=True)


with right_col:
    if generate_btn:
        if not feature_request.strip():
            st.error("Please enter a feature request before generating.")
        else:
            with st.spinner("Generating your PRD..."):
                try:
                    prd_output = generate_prd(
                        feature_request=feature_request,
                        product_context=product_context,
                        target_users=target_users,
                        priority=priority,
                        platform=platform
                    )
                    
                    st.session_state["prd_output"] = prd_output
                    st.session_state["prd_generated"] = True
                    st.session_state["feature_name"] = feature_request[:50]

                except Exception as e:
                    st.error(f"Error generating PRD: {str(e)}")
                    st.info("Make sure your ANTHROPIC_API_KEY is set correctly.")

    if st.session_state.get("prd_generated"):
        prd_text = st.session_state["prd_output"]
        section_count = count_sections(prd_text)
        word_count = len(prd_text.split())

        # Metrics row
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{section_count}</div>
                <div class="metric-label">Sections</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">{word_count}</div>
                <div class="metric-label">Words</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-value">~{max(1, word_count // 200)}m</div>
                <div class="metric-label">Read time</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

        # PRD Output
        st.markdown('<div class="prd-output">', unsafe_allow_html=True)
        st.markdown(prd_text)
        st.markdown('</div>', unsafe_allow_html=True)

        # Download
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"PRD_{timestamp}.md"
        st.download_button(
            label="⬇ Download PRD as Markdown",
            data=prd_text,
            file_name=filename,
            mime="text/markdown"
        )

    else:
        # Placeholder state
        st.markdown("""
        <div class="card" style="margin-top: 0; min-height: 400px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📋</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #E8EAF0; margin-bottom: 0.5rem;">Your PRD will appear here</div>
            <div style="color: #8B92A5; font-size: 0.9rem; max-width: 300px;">Fill in the feature request on the left and click Generate to create a structured PRD instantly.</div>
        </div>
        """, unsafe_allow_html=True)

# ── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built with Claude API + Streamlit · 
    <a href="https://github.com/capsaarang" style="color: #4F8EF7; text-decoration: none;">github.com/capsaarang</a>
</div>
""", unsafe_allow_html=True)
