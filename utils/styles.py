"""
Custom CSS styling and design system for VibeBloom.
Recreates the aesthetic, color palette, typography, and layout of the reference UI.
"""

def get_custom_css() -> str:
    return """
<style>
/* Import Google Fonts: Outfit for UI, Dancing Script & Caveat for creative cursive accents */
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Dancing+Script:wght@600;700&family=Outfit:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

:root {
    --bg-main: #FFF8FA;
    --card-bg: #FFFFFF;
    --text-primary: #2C2235;
    --text-muted: #877795;
    --accent-pink: #E25B88;
    --accent-light-pink: #FFE8F0;
    --accent-lavender: #C4B5FD;
    --accent-peach: #FFD6C9;
    --accent-cyan: #70D6FF;
    --accent-purple: #9D84B7;
    --card-border: rgba(235, 215, 228, 0.6);
    --card-shadow: 0 8px 24px rgba(214, 180, 205, 0.12);
    --card-radius: 20px;
}

/* Global App Container */
.stApp {
    background: linear-gradient(145deg, #FFF9FB 0%, #FDF4F8 40%, #F6ECF7 100%);
    font-family: 'Outfit', sans-serif;
    color: var(--text-primary);
}

/* Hide Streamlit default hamburger menu & footer padding */
#MainMenu, header, footer {
    visibility: hidden;
}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 96% !important;
}

/* Typography styles */
h1, h2, h3, h4, p, span, div {
    font-family: 'Outfit', sans-serif;
}

.script-accent {
    font-family: 'Dancing Script', cursive;
    color: #E25B88;
    font-weight: 700;
}

.handwritten-note {
    font-family: 'Caveat', cursive;
    font-size: 1.25rem;
    color: #4A3E56;
}

/* ---------------- HERO HEADER ---------------- */
.hero-card {
    background: linear-gradient(120deg, #FFFFFF 0%, #FFF3F7 60%, #F8EAF5 100%);
    border-radius: var(--card-radius);
    padding: 24px 32px;
    border: 1px solid var(--card-border);
    box-shadow: var(--card-shadow);
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}

.hero-pill-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #FFF0F5;
    color: #D84A78;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    border: 1px solid rgba(226, 91, 136, 0.2);
    margin-bottom: 10px;
}

.hero-title {
    font-size: 2.35rem;
    font-weight: 700;
    color: #2D2237;
    margin: 0;
    line-height: 1.2;
}

.hero-title .grow-word {
    font-family: 'Dancing Script', cursive;
    font-size: 2.9rem;
    color: #E25B88;
    font-weight: 700;
    margin-left: 6px;
}

.hero-subtitle {
    color: var(--text-muted);
    font-size: 1rem;
    margin-top: 8px;
    margin-bottom: 0;
}

.sticky-note {
    background: #FFFDF0;
    border: 1px dashed #E2D9B3;
    padding: 10px 16px;
    border-radius: 8px;
    box-shadow: 2px 4px 10px rgba(0,0,0,0.04);
    transform: rotate(-3deg);
    display: inline-block;
    text-align: center;
}

.date-pill-card {
    background: #FFFFFF;
    border: 1px solid rgba(226, 91, 136, 0.25);
    border-radius: 24px;
    padding: 8px 18px;
    font-size: 0.88rem;
    font-weight: 600;
    color: #4A3E56;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 3px 10px rgba(226, 91, 136, 0.08);
}

/* ---------------- PLATFORM METRIC CARDS ---------------- */
.stat-card {
    background: var(--card-bg);
    border-radius: var(--card-radius);
    padding: 20px 22px;
    border: 1px solid var(--card-border);
    box-shadow: var(--card-shadow);
    position: relative;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.stat-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(214, 180, 205, 0.2);
}

.stat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}

.stat-platform-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    color: #3B2E47;
}

.stat-icon {
    width: 28px;
    height: 28px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
}

.stat-watermark {
    font-size: 1.6rem;
    opacity: 0.15;
    color: #79668D;
}

.stat-value {
    font-size: 1.95rem;
    font-weight: 700;
    color: #261B30;
    line-height: 1.1;
    margin-bottom: 2px;
}

.stat-label {
    font-size: 0.82rem;
    color: var(--text-muted);
    margin-bottom: 10px;
}

.stat-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 6px;
}

.growth-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #10B981;
    background: #ECFDF5;
    padding: 3px 8px;
    border-radius: 12px;
}

.growth-badge.down {
    color: #EF4444;
    background: #FEF2F2;
}

.mini-sparkline {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 28px;
}

.spark-bar {
    width: 5px;
    border-radius: 3px 3px 0 0;
    transition: height 0.3s ease;
}

/* ---------------- CONTENT / CHART CARDS ---------------- */
.content-card {
    background: var(--card-bg);
    border-radius: var(--card-radius);
    padding: 22px 24px;
    border: 1px solid var(--card-border);
    box-shadow: var(--card-shadow);
    margin-bottom: 20px;
    height: 100%;
}

.content-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.content-card-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #2D2237;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 0;
}

.content-card-subtitle {
    font-size: 0.82rem;
    color: var(--text-muted);
    margin: 2px 0 0 0;
}

/* ---------------- TOP POST GALLERY CARDS ---------------- */
.post-preview-card {
    background: #FFFFFF;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(230, 210, 225, 0.8);
    box-shadow: 0 4px 14px rgba(220, 190, 210, 0.12);
    transition: transform 0.2s ease;
}

.post-preview-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(220, 190, 210, 0.22);
}

.post-thumb-container {
    height: 130px;
    position: relative;
    overflow: hidden;
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    padding: 8px;
}

.post-platform-overlay {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(4px);
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.post-preview-body {
    padding: 10px 12px;
}

.post-preview-metrics {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #4A3E56;
    margin-bottom: 4px;
}

.post-preview-date {
    font-size: 0.74rem;
    color: var(--text-muted);
}

/* ---------------- BOTTOM PLANNER QUICK BANNER ---------------- */
.planner-banner {
    background: linear-gradient(90deg, #FFE8F1 0%, #FFF0F5 50%, #F5ECF8 100%);
    border-radius: var(--card-radius);
    padding: 16px 24px;
    border: 1px solid rgba(226, 91, 136, 0.25);
    box-shadow: var(--card-shadow);
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 10px;
}

/* ---------------- SIDEBAR AESTHETICS ---------------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #FFF7FA 50%, #F8EEF6 100%);
    border-right: 1px solid rgba(230, 210, 225, 0.6);
}

.sidebar-logo {
    text-align: center;
    padding: 12px 0 16px 0;
    border-bottom: 1px dashed rgba(226, 91, 136, 0.2);
    margin-bottom: 16px;
}

.sidebar-brand-name {
    font-size: 1.85rem;
    font-weight: 700;
    color: #2D2237;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
}

.sidebar-brand-name .brand-script {
    font-family: 'Dancing Script', cursive;
    color: #E25B88;
    font-size: 2.2rem;
}

.sidebar-tagline {
    font-size: 0.78rem;
    color: #8C7B99;
    margin-top: 2px;
}

.sidebar-card-box {
    background: #FFFFFF;
    border: 1px solid rgba(230, 210, 225, 0.7);
    border-radius: 14px;
    padding: 12px 14px;
    box-shadow: 0 2px 8px rgba(220, 190, 210, 0.08);
    margin-top: 14px;
    margin-bottom: 14px;
}

/* Polaroid footer inside sidebar */
.polaroid-card {
    background: #FFFFFF;
    border: 1px solid #EADFE7;
    border-radius: 10px;
    padding: 8px 8px 12px 8px;
    box-shadow: 0 4px 12px rgba(200, 170, 190, 0.15);
    text-align: center;
    margin-top: 18px;
}

.polaroid-img-box {
    height: 90px;
    border-radius: 6px;
    background: linear-gradient(135deg, #FFB7C5 0%, #C4B5FD 100%);
    background-size: cover;
    background-position: center;
    margin-bottom: 8px;
}

.polaroid-text {
    font-family: 'Caveat', cursive;
    font-size: 1.05rem;
    color: #4A3E56;
    margin: 0;
}

/* Custom interactive buttons */
.stButton > button {
    background: linear-gradient(135deg, #E25B88 0%, #D84A78 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 20px !important;
    padding: 8px 20px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    box-shadow: 0 4px 12px rgba(226, 91, 136, 0.25) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(226, 91, 136, 0.35) !important;
    color: #FFFFFF !important;
}

/* Secondary outline buttons (like Download Sample CSV) */
.stDownloadButton > button {
    background: #FFFFFF !important;
    color: #D84A78 !important;
    border: 1.5px solid rgba(226, 91, 136, 0.4) !important;
    border-radius: 16px !important;
    padding: 7px 16px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    box-shadow: 0 2px 8px rgba(226, 91, 136, 0.08) !important;
    width: 100% !important;
}

.stDownloadButton > button:hover {
    background: #FFF0F5 !important;
    border-color: #D84A78 !important;
    color: #C23A66 !important;
}

/* Badge tags for hashtags and post types */
.tag-badge {
    display: inline-block;
    background: #FFF0F5;
    color: #C23A66;
    border: 1px solid rgba(226, 91, 136, 0.25);
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 2px 4px 2px 0;
}

/* Custom table & dataframe rounded look */
div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid var(--card-border);
}

/* Streamlit alerts / info callouts styling */
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border: 1px solid rgba(226, 91, 136, 0.2) !important;
    background-color: #FFF5F8 !important;
}
</style>
"""


def render_stat_card_html(platform: str, followers_str: str, label: str, growth_pct: float, sparkline_vals: list[int]) -> str:
    """Generates pure HTML/CSS representation for a platform KPI card matching reference."""
    colors = {
        "Instagram": {"primary": "#E25B88", "bg": "#FFF0F5", "spark": "#F472B6", "icon": "📸", "watermark": "📷"},
        "YouTube": {"primary": "#EF4444", "bg": "#FEF2F2", "spark": "#FB7185", "icon": "▶️", "watermark": "🎬"},
        "TikTok": {"primary": "#06B6D4", "bg": "#ECFEFF", "spark": "#67E8F9", "icon": "🎵", "watermark": "🎶"},
        "Facebook": {"primary": "#3B82F6", "bg": "#EFF6FF", "spark": "#93C5FD", "icon": "👥", "watermark": "🌐"}
    }
    cfg = colors.get(platform, {"primary": "#E25B88", "bg": "#FFF0F5", "spark": "#F472B6", "icon": "🌸", "watermark": "✨"})

    # Build mini sparkline bars
    max_val = max(sparkline_vals or [1])
    bars_html = ""
    for v in sparkline_vals:
        h = max(6, int((v / max_val) * 26))
        bars_html += f'<div class="spark-bar" style="height:{h}px; background-color:{cfg["spark"]};"></div>'

    growth_class = "growth-badge" if growth_pct >= 0 else "growth-badge down"
    growth_arrow = "↑" if growth_pct >= 0 else "↓"

    return f"""
<div class="stat-card">
    <div>
        <div class="stat-header">
            <div class="stat-platform-badge">
                <span class="stat-icon" style="background-color:{cfg['bg']}; color:{cfg['primary']};">{cfg['icon']}</span>
                <span>{platform}</span>
            </div>
            <div class="stat-watermark">{cfg['watermark']}</div>
        </div>
        <div class="stat-value">{followers_str}</div>
        <div class="stat-label">{label}</div>
    </div>
    <div class="stat-footer">
        <span class="{growth_class}">{growth_arrow} {abs(growth_pct)}%</span>
        <div class="mini-sparkline">
            {bars_html}
        </div>
    </div>
</div>
"""
