"""
VibeBloom – Social Media Insights & Creator Analytics Dashboard
A feminine, creative, and lightweight creator analytics web app built with Streamlit, Pandas, and Plotly.
"""

from datetime import datetime, date
import streamlit as st
import pandas as pd

from utils.styles import get_custom_css, render_stat_card_html
from utils.data_loader import (
    load_dataset,
    load_sample_dataset,
    get_sample_csv_template_bytes,
    load_planner_posts,
    save_planner_posts
)
from utils.analytics import (
    compute_overview_kpis,
    compute_platform_summaries,
    get_engagement_trends,
    get_audience_growth_by_platform,
    get_platform_engagement_share,
    get_top_performing_posts,
    compute_best_time_matrix,
    compute_hashtag_analytics,
    compute_post_type_breakdown
)
from utils.charts import (
    plot_engagement_trends,
    plot_audience_growth,
    plot_platform_comparison_donut,
    plot_best_time_heatmap,
    plot_post_type_comparison,
    plot_hashtag_ranking,
    plot_reach_vs_engagement_scatter
)

# -------------------------------------------------------------
# App Configuration & Styling
# -------------------------------------------------------------
st.set_page_config(
    page_title="VibeBloom – Social Media Insights",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(get_custom_css(), unsafe_allow_html=True)

# -------------------------------------------------------------
# Sidebar Navigation & Data Controls
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-brand-name">
            <span class="brand-script">VibeBloom</span> 🌸
        </div>
        <div class="sidebar-tagline">Social Media Insights for Creative Minds ♡</div>
    </div>
    """, unsafe_allow_html=True)

    nav_selection = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📊 Platform Analysis",
            "👥 Audience Insights",
            "▶️ Content Performance",
            "＃ Hashtag Analytics",
            "🕒 Best Time to Post",
            "📅 Content Planner",
            "🗄️ Data Explorer"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("#### 🗂️ Data Source")
    data_source_mode = st.radio(
        "Select Data Mode",
        ["Sample Dataset (Demo)", "Upload Custom CSV"],
        label_visibility="collapsed"
    )

    uploaded_file = None
    if data_source_mode == "Upload Custom CSV":
        uploaded_file = st.file_uploader("Upload CSV File", type=["csv"], help="Upload CSV containing required social media columns.")

    # Download Template Button
    sample_bytes = get_sample_csv_template_bytes()
    st.download_button(
        label="📥 Download Sample CSV",
        data=sample_bytes,
        file_name="vibebloom_sample_data.csv",
        mime="text/csv"
    )

    # Decorative Polaroid Card (Matches reference design)
    st.markdown("""
    <div class="polaroid-card">
        <div class="polaroid-img-box" style="background: linear-gradient(135deg, #F8BBD0 0%, #D1C4E9 50%, #FFE0B2 100%);"></div>
        <p class="polaroid-text">Good Content, Brighter People ♡</p>
    </div>
    <div style="text-align: center; margin-top: 14px; font-size: 0.8rem; color: #8A7999;">
        Made with 💜 for Creative Souls
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# Data Loading & Ingestion
# -------------------------------------------------------------
df_raw, is_sample, status_msg = load_dataset(uploaded_file if data_source_mode == "Upload Custom CSV" else None)

# If upload had an error or sample loaded, show notification
if not is_sample:
    st.success(status_msg)
elif data_source_mode == "Upload Custom CSV" and uploaded_file is None:
    st.info("💡 Awaiting custom CSV upload. Showing demonstration sample dataset in the meantime.")

# -------------------------------------------------------------
# Global Date & Platform Filtering
# -------------------------------------------------------------
min_date = df_raw["post_date"].min().date() if not df_raw.empty else date(2026, 5, 2)
max_date = df_raw["post_date"].max().date() if not df_raw.empty else date(2026, 10, 28)

# Format human-friendly default date range string
date_range_str = f"{min_date.strftime('%b %d, %Y')} – {max_date.strftime('%b %d, %Y')}"

# -------------------------------------------------------------
# Hero Banner (Matches Reference UI)
# -------------------------------------------------------------
st.markdown(f"""
<div class="hero-card">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
        <div>
            <div class="hero-pill-tag">✦ Turn Your Ideas Into Impact ✦</div>
            <h1 class="hero-title">Create. Analyze. <span class="grow-word">Grow.</span></h1>
            <p class="hero-subtitle">Your complete social media analytics dashboard</p>
        </div>
        <div style="display: flex; align-items: center; gap: 14px; flex-wrap: wrap;">
            <div class="sticky-note">
                <span class="handwritten-note">Small Content, Big Impact ♡</span>
            </div>
            <div class="date-pill-card">
                <span>📅</span>
                <span>{date_range_str}</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Interactive Filter Bar
with st.expander("✨ Filter Dashboard Content (Date Range & Platforms)", expanded=False):
    f_col1, f_col2 = st.columns([1, 1])
    with f_col1:
        date_selection = st.date_input(
            "Select Date Filter Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    with f_col2:
        available_platforms = sorted(df_raw["platform"].unique().tolist())
        selected_platforms = st.multiselect(
            "Filter Platforms",
            options=available_platforms,
            default=available_platforms
        )

# Apply Filters safely
df = df_raw.copy()
if isinstance(date_selection, (tuple, list)) and len(date_selection) == 2:
    start_d, end_d = date_selection
    df = df[(df["post_date"].dt.date >= start_d) & (df["post_date"].dt.date <= end_d)]

if selected_platforms:
    df = df[df["platform"].isin(selected_platforms)]

if df.empty:
    st.warning("⚠️ No records match your selected filters. Please expand your date range or platforms.")
    st.stop()


# =============================================================
# TAB 1: DASHBOARD OVERVIEW (Direct Replica of Reference Image)
# =============================================================
if nav_selection == "🏠 Dashboard":
    # 1. Top 4 Platform KPI Cards
    platform_data = compute_platform_summaries(df)
    c1, c2, c3, c4 = st.columns(4)

    def format_k(num: int) -> str:
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        if num >= 1_000:
            return f"{num / 1_000:.1f}K"
        return str(num)

    with c1:
        ig = platform_data.get("Instagram", {})
        st.markdown(render_stat_card_html("Instagram", format_k(ig.get("followers", 0)), ig.get("label", "Total Followers"), ig.get("growth_pct", 0.0), ig.get("sparkline", [])), unsafe_allow_html=True)

    with c2:
        yt = platform_data.get("YouTube", {})
        st.markdown(render_stat_card_html("YouTube", format_k(yt.get("followers", 0)), yt.get("label", "Total Subscribers"), yt.get("growth_pct", 0.0), yt.get("sparkline", [])), unsafe_allow_html=True)

    with c3:
        tt = platform_data.get("TikTok", {})
        st.markdown(render_stat_card_html("TikTok", format_k(tt.get("followers", 0)), tt.get("label", "Total Followers"), tt.get("growth_pct", 0.0), tt.get("sparkline", [])), unsafe_allow_html=True)

    with c4:
        fb = platform_data.get("Facebook", {})
        st.markdown(render_stat_card_html("Facebook", format_k(fb.get("followers", 0)), fb.get("label", "Total Followers"), fb.get("growth_pct", 0.0), fb.get("sparkline", [])), unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # 2. Middle Row: Engagement Trends + Audience Growth
    trend_col, growth_col = st.columns([1.1, 0.9])

    with trend_col:
        st.markdown("""
        <div class="content-card">
            <div class="content-card-header">
                <div>
                    <h3 class="content-card-title">📈 Engagement Trends</h3>
                    <p class="content-card-subtitle">Likes • Comments • Shares • Saves</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        grain_choice = st.selectbox("Aggregation", ["Weekly", "Monthly", "Daily"], index=0, key="trend_grain", label_visibility="collapsed")
        freq_map = {"Weekly": "W", "Monthly": "ME", "Daily": "D"}
        trends_df = get_engagement_trends(df, freq=freq_map[grain_choice])
        st.plotly_chart(plot_engagement_trends(trends_df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with growth_col:
        st.markdown("""
        <div class="content-card">
            <div class="content-card-header">
                <div>
                    <h3 class="content-card-title">👥 Audience Growth</h3>
                    <p class="content-card-subtitle">Follower growth across platforms</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        growth_choice = st.selectbox("Interval", ["Monthly", "Weekly"], index=0, key="growth_grain", label_visibility="collapsed")
        growth_freq = "ME" if growth_choice == "Monthly" else "W"
        growth_df = get_audience_growth_by_platform(df, freq=growth_freq)
        st.plotly_chart(plot_audience_growth(growth_df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # 3. Third Row: Top Performing Content + Platform Comparison + Best Time
    b_col1, b_col2, b_col3 = st.columns([1.2, 0.9, 0.9])

    with b_col1:
        st.markdown("""
        <div class="content-card">
            <div class="content-card-header">
                <div>
                    <h3 class="content-card-title">⭐ Top Performing Content</h3>
                    <p class="content-card-subtitle">Your best performing posts across all platforms</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        top_posts = get_top_performing_posts(df, limit=4, sort_by="likes")
        thumb_cols = st.columns(len(top_posts))

        thumb_styles = [
            "linear-gradient(135deg, #FAD0C4 0%, #FFD1FF 100%)",
            "linear-gradient(135deg, #C1DFC4 0%, #DEECDD 100%)",
            "linear-gradient(135deg, #D4FC79 0%, #96E6A1 100%)",
            "linear-gradient(135deg, #E0C3FC 0%, #8EC5FC 100%)"
        ]

        platform_icons = {
            "Instagram": "📸",
            "YouTube": "▶️",
            "TikTok": "🎵",
            "Facebook": "👥"
        }

        for idx, (_, post) in enumerate(top_posts.iterrows()):
            with thumb_cols[idx]:
                bg_grad = thumb_styles[idx % len(thumb_styles)]
                plat_icon = platform_icons.get(post["platform"], "🌸")
                st.markdown(f"""
                <div class="post-preview-card">
                    <div class="post-thumb-container" style="background:{bg_grad};">
                        <div class="post-platform-overlay">{plat_icon}</div>
                    </div>
                    <div class="post-preview-body">
                        <div class="post-preview-metrics">
                            <span>❤️ {format_k(int(post['likes']))}</span>
                            <span>💬 {format_k(int(post['comments']))}</span>
                        </div>
                        <div class="post-preview-date">{post['formatted_date']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with b_col2:
        st.markdown("""
        <div class="content-card">
            <div class="content-card-header">
                <div>
                    <h3 class="content-card-title">🍩 Platform Comparison</h3>
                    <p class="content-card-subtitle">Share of total engagement</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        share_df = get_platform_engagement_share(df)
        st.plotly_chart(plot_platform_comparison_donut(share_df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with b_col3:
        matrix_df, best_d, best_t = compute_best_time_matrix(df)
        st.markdown(f"""
        <div class="content-card">
            <div class="content-card-header">
                <div>
                    <h3 class="content-card-title">🕒 Best Time to Post</h3>
                    <p class="content-card-subtitle">When your audience is most active</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(plot_best_time_heatmap(matrix_df), use_container_width=True, config={"displayModeBar": False})
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; color: #8A7999; margin-top: -6px;">
            <span>Less Active</span>
            <span style="letter-spacing: 2px;">🟪🟪🟪</span>
            <span>More Active</span>
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # 4. Bottom Quick Planner Bar (Matches Reference Image)
    st.markdown("""
    <div class="planner-banner">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="font-size: 1.8rem;">📅</div>
            <div>
                <h4 style="margin: 0; font-weight: 700; color: #2D2237;">Content Planner</h4>
                <p style="margin: 0; font-size: 0.85rem; color: #8A7999;">Plan and organize your upcoming content</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("➕ Open Quick Post Scheduler", expanded=False):
        with st.form("quick_schedule_form"):
            q_col1, q_col2, q_col3 = st.columns(3)
            with q_col1:
                qp_platform = st.selectbox("Target Platform", ["Instagram", "YouTube", "TikTok", "Facebook"], key="qp_plat")
                qp_type = st.selectbox("Content Format", ["Reel", "Shorts", "Carousel", "Video", "Static Post"], key="qp_type")
            with q_col2:
                qp_date = st.date_input("Scheduled Date", value=date.today(), key="qp_d")
                qp_time = st.time_input("Scheduled Time", key="qp_t")
            with q_col3:
                qp_caption = st.text_input("Post Caption / Idea", placeholder="e.g. Cozy studio tour & desk setup reveal ♡", key="qp_cap")
                qp_tags = st.text_input("Hashtags", placeholder="#aesthetic #workspace #creatorlife", key="qp_tags")

            quick_submit = st.form_submit_button("🌸 Schedule New Post")
            if quick_submit:
                if not qp_caption.strip():
                    st.error("Please provide a caption or idea for your scheduled post.")
                else:
                    new_item = {
                        "id": f"PLAN-{datetime.now().strftime('%M%S')}",
                        "platform": qp_platform,
                        "scheduled_date": str(qp_date),
                        "scheduled_time": qp_time.strftime("%H:%M"),
                        "post_type": qp_type,
                        "status": "Scheduled",
                        "caption": qp_caption.strip(),
                        "hashtags": qp_tags.strip() or "#aesthetic #creativemind"
                    }
                    posts = load_planner_posts()
                    posts.append(new_item)
                    save_planner_posts(posts)
                    st.success(f"Post successfully scheduled for {qp_platform} on {qp_date}! 🎉")


# =============================================================
# TAB 2: PLATFORM ANALYSIS
# =============================================================
elif nav_selection == "📊 Platform Analysis":
    st.markdown("""
    <div class="content-card">
        <h2 style="font-weight: 700; color: #2D2237; margin: 0;">📊 Cross-Platform Performance Comparison</h2>
        <p style="color: #8A7999; margin-top: 4px;">Compare engagement rates, reach efficiency, and audience growth across Instagram, YouTube, TikTok, and Facebook.</p>
    </div>
    """, unsafe_allow_html=True)

    # Aggregated platform table
    plat_summary_dict = compute_platform_summaries(df)
    summary_rows = []
    for plat_name, stats in plat_summary_dict.items():
        summary_rows.append({
            "Platform": plat_name,
            "Followers / Subs": f"{stats['followers']:,}",
            "Growth Rate": f"{stats['growth_pct']:+0.1f}%",
            "Total Posts": stats["posts"],
            "Total Reach": f"{stats['reach']:,}",
            "Total Likes": f"{stats['likes']:,}",
            "Total Comments": f"{stats['comments']:,}",
            "Total Shares": f"{stats['shares']:,}",
            "Total Saves": f"{stats['saves']:,}",
            "Avg Engagement Rate": f"{stats['avg_er']:.2f}%"
        })

    summary_df = pd.DataFrame(summary_rows)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown("### 🍩 Engagement Share Breakdown")
        share_df = get_platform_engagement_share(df)
        st.plotly_chart(plot_platform_comparison_donut(share_df), use_container_width=True)

    with p_col2:
        st.markdown("### 📈 Follower Milestones by Platform")
        growth_df = get_audience_growth_by_platform(df, freq="ME")
        st.plotly_chart(plot_audience_growth(growth_df), use_container_width=True)


# =============================================================
# TAB 3: AUDIENCE INSIGHTS
# =============================================================
elif nav_selection == "👥 Audience Insights":
    st.markdown("""
    <div class="content-card">
        <h2 style="font-weight: 700; color: #2D2237; margin: 0;">👥 Audience Demographics & Growth Dynamics</h2>
        <p style="color: #8A7999; margin-top: 4px;">Understand follower velocity, reach scalability, and community loyalty interactions.</p>
    </div>
    """, unsafe_allow_html=True)

    kpi = compute_overview_kpis(df)
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        st.metric("Total Follower Base", f"{kpi['total_followers']:,}")
    with a2:
        st.metric("Total Unique Reach", f"{kpi['total_reach']:,}")
    with a3:
        st.metric("Overall Engagement Rate", f"{kpi['avg_engagement_rate']}%")
    with a4:
        like_comment_ratio = round(kpi['total_likes'] / max(kpi['total_comments'], 1), 1)
        st.metric("Like-to-Comment Ratio", f"{like_comment_ratio} : 1")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    st.markdown("### 📈 Monthly Growth Velocity")
    growth_df = get_audience_growth_by_platform(df, freq="ME")
    st.plotly_chart(plot_audience_growth(growth_df), use_container_width=True)

    # Save to share community bookmark ratio
    save_share_ratio = round(kpi['total_saves'] / max(kpi['total_shares'], 1), 2)
    st.markdown(f"""
    <div class="hero-card" style="margin-top: 16px;">
        <h4 style="margin: 0; color: #2D2237;">💡 Audience Intent Insight</h4>
        <p style="margin: 6px 0 0 0; color: #645572; font-size: 0.95rem;">
            Your content achieves a <b>Save-to-Share ratio of {save_share_ratio}</b>. High save ratios indicate that viewers treat your posts as 
            inspirational references, tutorials, and aesthetic moodboards to revisit later!
        </p>
    </div>
    """, unsafe_allow_html=True)


# =============================================================
# TAB 4: CONTENT PERFORMANCE
# =============================================================
elif nav_selection == "▶️ Content Performance":
    st.markdown("""
    <div class="content-card">
        <h2 style="font-weight: 700; color: #2D2237; margin: 0;">▶️ Content Performance & Formats</h2>
        <p style="color: #8A7999; margin-top: 4px;">Analyze which post formats (Reels, Carousels, Static, Videos) yield the highest viral reach and interaction depth.</p>
    </div>
    """, unsafe_allow_html=True)

    cp_col1, cp_col2 = st.columns([1, 1])

    with cp_col1:
        st.markdown("### 📊 Average Reach & Likes by Post Type")
        type_df = compute_post_type_breakdown(df)
        st.plotly_chart(plot_post_type_comparison(type_df), use_container_width=True)

    with cp_col2:
        st.markdown("### 🎯 Reach vs. Engagement Rate Scatter")
        st.plotly_chart(plot_reach_vs_engagement_scatter(df), use_container_width=True)

    st.markdown("### 🏆 Top 10 Best Performing Posts")
    sort_choice = st.selectbox("Rank By", ["Total Engagement", "Likes", "Reach"], index=0)
    sort_key = "engagement" if sort_choice == "Total Engagement" else sort_choice.lower()
    top_10 = get_top_performing_posts(df, limit=10, sort_by=sort_key)

    display_cols = ["post_id", "platform", "post_type", "formatted_date", "caption", "likes", "comments", "shares", "saves", "reach", "engagement_rate"]
    st.dataframe(top_10[display_cols].rename(columns={"formatted_date": "Date", "engagement_rate": "ER (%)"}), use_container_width=True, hide_index=True)


# =============================================================
# TAB 5: HASHTAG ANALYTICS
# =============================================================
elif nav_selection == "＃ Hashtag Analytics":
    st.markdown("""
    <div class="content-card">
        <h2 style="font-weight: 700; color: #2D2237; margin: 0;">＃ Hashtag Discovery & Engagement Volume</h2>
        <p style="color: #8A7999; margin-top: 4px;">Uncover the aesthetic hashtags driving community discovery, algorithm suggestions, and viral spread.</p>
    </div>
    """, unsafe_allow_html=True)

    tag_df = compute_hashtag_analytics(df)

    h_col1, h_col2 = st.columns([1.1, 0.9])
    with h_col1:
        st.markdown("### 🌸 Top Hashtags by Average Likes")
        st.plotly_chart(plot_hashtag_ranking(tag_df, limit=12), use_container_width=True)

    with h_col2:
        st.markdown("### 🏷️ Top Hashtag Summary Table")
        st.dataframe(
            tag_df.head(12)[["hashtag", "post_count", "avg_likes", "avg_reach", "avg_er"]]
            .rename(columns={"hashtag": "Tag", "post_count": "Posts", "avg_likes": "Avg Likes", "avg_reach": "Avg Reach", "avg_er": "Avg ER (%)"}),
            use_container_width=True,
            hide_index=True
        )

    # Hashtag simulator
    st.markdown("---")
    st.markdown("### 🔍 Hashtag Performance Lookup")
    user_tag = st.text_input("Enter a hashtag to inspect (e.g. #aesthetic, #pastelvibes, #creativemind)", value="#aesthetic")
    clean_search = user_tag.strip().lower()
    if not clean_search.startswith("#") and clean_search:
        clean_search = "#" + clean_search

    matched_tag = tag_df[tag_df["hashtag"] == clean_search]
    if not matched_tag.empty:
        r = matched_tag.iloc[0]
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Posts Tagged", f"{int(r['post_count'])}")
        s2.metric("Avg Likes / Post", f"{int(r['avg_likes']):,}")
        s3.metric("Avg Reach", f"{int(r['avg_reach']):,}")
        s4.metric("Avg Engagement Rate", f"{r['avg_er']}%")
    else:
        st.info(f"Hashtag '{clean_search}' is not currently in the filtered dataset.")


# =============================================================
# TAB 6: BEST TIME TO POST
# =============================================================
elif nav_selection == "🕒 Best Time to Post":
    matrix_df, best_day, best_time_window = compute_best_time_matrix(df)

    st.markdown(f"""
    <div class="content-card">
        <h2 style="font-weight: 700; color: #2D2237; margin: 0;">🕒 Optimal Posting Schedules</h2>
        <p style="color: #8A7999; margin-top: 4px;">Determine when your creator audience is active and receptive to newly published posts.</p>
        <div style="margin-top: 14px; display: flex; gap: 18px; flex-wrap: wrap;">
            <div style="background: #FFF0F5; border: 1px solid rgba(226, 91, 136, 0.3); border-radius: 12px; padding: 10px 18px;">
                <span style="font-size: 0.82rem; color: #8A7999;">Optimal Day:</span>
                <div style="font-size: 1.25rem; font-weight: 700; color: #E25B88;">{best_day}</div>
            </div>
            <div style="background: #F5EEFD; border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 10px 18px;">
                <span style="font-size: 0.82rem; color: #8A7999;">Peak Engagement Hours:</span>
                <div style="font-size: 1.25rem; font-weight: 700; color: #8B5CF6;">{best_time_window}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🟪 Day × Hour Activity Heatmap")
    st.plotly_chart(plot_best_time_heatmap(matrix_df), use_container_width=True)

    st.markdown("""
    <div class="hero-card" style="margin-top: 20px;">
        <h4 style="margin: 0; color: #2D2237;">🌸 Best Practices for Creators</h4>
        <ul style="color: #645572; margin: 8px 0 0 0; padding-left: 20px; font-size: 0.95rem; line-height: 1.6;">
            <li>Publish <b>30 to 45 minutes prior</b> to the peak window so your post gets indexed and begins accumulating early velocity.</li>
            <li>Schedule visually rich content (Reels & Carousels) on <b>Thursday through Sunday evenings</b> when relaxation browsing is highest.</li>
            <li>Maintain consistent weekly cadences to foster algorithm loyalty across Instagram and YouTube.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# =============================================================
# TAB 7: CONTENT PLANNER
# =============================================================
elif nav_selection == "📅 Content Planner":
    st.markdown("""
    <div class="content-card">
        <h2 style="font-weight: 700; color: #2D2237; margin: 0;">📅 Creative Content Calendar & Planner</h2>
        <p style="color: #8A7999; margin-top: 4px;">Organize upcoming posts, plan visual aesthetics, and maintain posting consistency across platforms.</p>
    </div>
    """, unsafe_allow_html=True)

    planner_posts = load_planner_posts()

    with st.expander("➕ Schedule a New Post", expanded=False):
        with st.form("full_planner_form"):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                f_plat = st.selectbox("Platform", ["Instagram", "YouTube", "TikTok", "Facebook"])
                f_type = st.selectbox("Content Type", ["Reel", "Shorts", "Carousel", "Video", "Static Post"])
                f_status = st.selectbox("Status", ["Scheduled", "In Progress", "Idea / Draft"])
            with col_b:
                f_date = st.date_input("Scheduled Date", value=date.today())
                f_time = st.time_input("Scheduled Time")
            with col_c:
                f_caption = st.text_area("Caption / Concept", height=90, placeholder="Write your post draft or concept here...")
                f_tags = st.text_input("Planned Hashtags", placeholder="#aesthetic #creativemind #slowliving")

            submitted = st.form_submit_button("🌸 Add to Schedule")
            if submitted:
                if not f_caption.strip():
                    st.error("Please enter a caption or concept.")
                else:
                    new_entry = {
                        "id": f"PLAN-{datetime.now().strftime('%M%S')}",
                        "platform": f_plat,
                        "scheduled_date": str(f_date),
                        "scheduled_time": f_time.strftime("%H:%M"),
                        "post_type": f_type,
                        "status": f_status,
                        "caption": f_caption.strip(),
                        "hashtags": f_tags.strip() or "#aesthetic"
                    }
                    planner_posts.append(new_entry)
                    save_planner_posts(planner_posts)
                    st.success("Post successfully added to your creative planner! 🌷")
                    st.rerun()

    # Display scheduled posts
    st.markdown("### 📋 Scheduled Creator Pipeline")
    if not planner_posts:
        st.info("No content currently scheduled. Click 'Schedule a New Post' above to create one!")
    else:
        status_badges = {
            "Scheduled": "background:#ECFDF5; color:#10B981; border: 1px solid #A7F3D0;",
            "In Progress": "background:#EFF6FF; color:#3B82F6; border: 1px solid #BFDBFE;",
            "Idea / Draft": "background:#FFFBEB; color:#F59E0B; border: 1px solid #FDE68A;"
        }

        for idx, item in enumerate(planner_posts):
            badge_style = status_badges.get(item.get("status", "Scheduled"), "background:#FFF0F5; color:#E25B88;")
            st.markdown(f"""
            <div class="content-card" style="margin-bottom: 12px; padding: 16px 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-weight: 700; color: #2D2237; font-size: 1.05rem;">{item.get('platform', 'Instagram')}</span>
                        <span class="tag-badge">{item.get('post_type', 'Reel')}</span>
                        <span style="padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; {badge_style}">{item.get('status', 'Scheduled')}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #8A7999; font-weight: 500;">
                        📅 {item.get('scheduled_date', '')} at {item.get('scheduled_time', '')}
                    </div>
                </div>
                <p style="margin: 10px 0 6px 0; color: #3B2E47; font-size: 0.95rem;">{item.get('caption', '')}</p>
                <div style="font-size: 0.82rem; color: #E25B88;">{item.get('hashtags', '')}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ Clear All Scheduled Items", key="clear_planner"):
            save_planner_posts([])
            st.rerun()


# =============================================================
# TAB 8: DATA EXPLORER
# =============================================================
elif nav_selection == "🗄️ Data Explorer":
    st.markdown("""
    <div class="content-card">
        <h2 style="font-weight: 700; color: #2D2237; margin: 0;">🗄️ Creator Data Explorer & Query Hub</h2>
        <p style="color: #8A7999; margin-top: 4px;">Inspect raw post records, apply granular column filters, and export customized subsets.</p>
    </div>
    """, unsafe_allow_html=True)

    # Search keyword
    search_term = st.text_input("🔍 Search captions or hashtags", placeholder="e.g. cozy, studio, #aesthetic")
    filtered_df = df.copy()
    if search_term.strip():
        term = search_term.strip().lower()
        filtered_df = filtered_df[
            filtered_df["caption"].str.lower().str.contains(term, na=False) |
            filtered_df["hashtags"].str.lower().str.contains(term, na=False)
        ]

    st.markdown(f"**Showing {len(filtered_df)} of {len(df_raw)} records**")

    # Column display options
    all_cols = filtered_df.columns.tolist()
    chosen_cols = st.multiselect("Visible Columns", options=all_cols, default=all_cols)
    st.dataframe(filtered_df[chosen_cols], use_container_width=True)

    # Export filtered data
    csv_bytes = filtered_df[chosen_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Dataset as CSV",
        data=csv_bytes,
        file_name="vibebloom_filtered_records.csv",
        mime="text/csv"
    )

    st.markdown("### 📊 Dataset Statistical Summary")
    st.dataframe(filtered_df[["likes", "comments", "shares", "saves", "reach", "followers"]].describe(), use_container_width=True)
