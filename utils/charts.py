"""
Plotly chart generators for VibeBloom.
Recreates the exact visual language, pastel colors, and layout seen in the reference UI.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# Pastel Theme Palette matching the reference image
PALETTE = {
    "likes": "#E25B88",       # Rose Pink
    "comments": "#8B5CF6",    # Lavender Purple
    "shares": "#38BDF8",      # Sky Blue
    "saves": "#FB923C",       # Peach / Apricot
    "instagram": "#F472B6",   # Pastel Pink
    "youtube": "#FB7185",     # Pastel Coral
    "tiktok": "#38BDF8",      # Soft Cyan
    "facebook": "#60A5FA",    # Periwinkle Blue
    "text": "#2C2235",
    "muted": "#8A7999",
    "grid": "rgba(235, 215, 230, 0.45)"
}


def _apply_common_layout(fig: go.Figure, height: int = 320) -> go.Figure:
    """Applies common pastel styling, transparent backgrounds, and typography."""
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit, sans-serif", color=PALETTE["text"], size=12),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="rgba(226, 91, 136, 0.4)",
            font=dict(family="Outfit, sans-serif", size=12, color=PALETTE["text"])
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color=PALETTE["muted"])
        )
    )
    return fig


def plot_engagement_trends(df: pd.DataFrame) -> go.Figure:
    """
    Renders multi-line smoothed area chart for Likes, Comments, Shares, Saves.
    Direct replica of the 'Engagement Trends' chart in reference image.
    """
    fig = go.Figure()

    if df.empty or "post_date" not in df.columns:
        fig.add_annotation(text="No trend data available", showarrow=False, font=dict(size=14, color=PALETTE["muted"]))
        return _apply_common_layout(fig, height=320)

    x_vals = df["post_date"]

    # 1. Likes trace
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=df["likes"],
        name="Likes",
        mode="lines+markers",
        line=dict(color=PALETTE["likes"], width=2.5, shape="spline"),
        marker=dict(size=5, color=PALETTE["likes"]),
        fill="tozeroy",
        fillcolor="rgba(226, 91, 136, 0.08)",
        hovertemplate="<b>Likes:</b> %{y:,.0f}<extra></extra>"
    ))

    # 2. Comments trace
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=df["comments"],
        name="Comments",
        mode="lines+markers",
        line=dict(color=PALETTE["comments"], width=2.5, shape="spline"),
        marker=dict(size=5, color=PALETTE["comments"]),
        fill="tozeroy",
        fillcolor="rgba(139, 92, 246, 0.06)",
        hovertemplate="<b>Comments:</b> %{y:,.0f}<extra></extra>"
    ))

    # 3. Shares trace
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=df["shares"],
        name="Shares",
        mode="lines+markers",
        line=dict(color=PALETTE["shares"], width=2.5, shape="spline"),
        marker=dict(size=5, color=PALETTE["shares"]),
        fill="tozeroy",
        fillcolor="rgba(56, 189, 248, 0.06)",
        hovertemplate="<b>Shares:</b> %{y:,.0f}<extra></extra>"
    ))

    # 4. Saves trace
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=df["saves"],
        name="Saves",
        mode="lines+markers",
        line=dict(color=PALETTE["saves"], width=2.5, shape="spline"),
        marker=dict(size=5, color=PALETTE["saves"]),
        fill="tozeroy",
        fillcolor="rgba(251, 146, 60, 0.06)",
        hovertemplate="<b>Saves:</b> %{y:,.0f}<extra></extra>"
    ))

    fig.update_xaxes(
        showgrid=False,
        linecolor=PALETTE["grid"],
        tickfont=dict(color=PALETTE["muted"], size=11),
        tickformat="%b"
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=PALETTE["grid"],
        tickfont=dict(color=PALETTE["muted"], size=11),
        zeroline=False
    )

    return _apply_common_layout(fig, height=310)


def plot_audience_growth(df: pd.DataFrame) -> go.Figure:
    """
    Grouped bar chart for follower growth across platforms.
    Matches the 'Audience Growth' chart in reference image.
    """
    fig = go.Figure()

    if df.empty or "period_name" not in df.columns:
        fig.add_annotation(text="No audience data available", showarrow=False, font=dict(size=14, color=PALETTE["muted"]))
        return _apply_common_layout(fig, height=310)

    platform_colors = {
        "Instagram": PALETTE["instagram"],
        "YouTube": PALETTE["youtube"],
        "TikTok": PALETTE["tiktok"],
        "Facebook": PALETTE["facebook"]
    }

    platforms = ["Instagram", "YouTube", "TikTok", "Facebook"]

    for plat in platforms:
        plat_data = df[df["platform"] == plat]
        if not plat_data.empty:
            fig.add_trace(go.Bar(
                x=plat_data["period_name"],
                y=plat_data["followers"],
                name=plat,
                marker=dict(
                    color=platform_colors.get(plat, PALETTE["instagram"]),
                    line=dict(width=0)
                ),
                hovertemplate=f"<b>{plat}:</b> %{{y:,.0f}} followers<extra></extra>"
            ))

    fig.update_layout(barmode="group", bargap=0.25, bargroupgap=0.1)
    fig.update_xaxes(showgrid=False, linecolor=PALETTE["grid"], tickfont=dict(color=PALETTE["muted"], size=11))
    fig.update_yaxes(showgrid=True, gridcolor=PALETTE["grid"], tickfont=dict(color=PALETTE["muted"], size=11), zeroline=False)

    return _apply_common_layout(fig, height=310)


def plot_platform_comparison_donut(df: pd.DataFrame) -> go.Figure:
    """
    Donut chart showing share of total engagement with center total metric.
    Matches the 'Platform Comparison' donut in reference image.
    """
    fig = go.Figure()

    if df.empty or "total_engagement" not in df.columns:
        fig.add_annotation(text="No platform data", showarrow=False, font=dict(size=14, color=PALETTE["muted"]))
        return _apply_common_layout(fig, height=270)

    color_map = {
        "Instagram": PALETTE["instagram"],
        "YouTube": PALETTE["youtube"],
        "TikTok": PALETTE["tiktok"],
        "Facebook": PALETTE["facebook"]
    }
    colors = [color_map.get(p, PALETTE["likes"]) for p in df["platform"]]

    total_eng = df["total_engagement"].sum()
    if total_eng >= 1_000_000:
        center_text = f"<b>{total_eng/1_000_000:.1f}M</b><br><span style='font-size:11px; color:#8A7999; font-weight:normal;'>Total Eng.</span>"
    elif total_eng >= 1_000:
        center_text = f"<b>{total_eng/1_000:.0f}K</b><br><span style='font-size:11px; color:#8A7999; font-weight:normal;'>Total Eng.</span>"
    else:
        center_text = f"<b>{total_eng}</b><br><span style='font-size:11px; color:#8A7999; font-weight:normal;'>Total Eng.</span>"

    fig.add_trace(go.Pie(
        labels=df["platform"],
        values=df["total_engagement"],
        hole=0.68,
        marker=dict(colors=colors, line=dict(color="#FFFFFF", width=3)),
        textinfo="percent",
        textposition="inside",
        insidetextorientation="radial",
        hoverinfo="label+value+percent",
        hovertemplate="<b>%{label}</b><br>Engagement: %{value:,.0f} (%{percent})<extra></extra>"
    ))

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=11, color=PALETTE["muted"])
        ),
        annotations=[dict(
            text=center_text,
            showarrow=False,
            font=dict(size=18, family="Outfit, sans-serif", color=PALETTE["text"])
        )],
        margin=dict(l=10, r=90, t=10, b=10),
        height=260,
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def plot_best_time_heatmap(matrix_df: pd.DataFrame) -> go.Figure:
    """
    7 days x hours engagement matrix heatmap.
    Matches the 'Best Time to Post' matrix in reference image with lavender/purple shading.
    """
    fig = go.Figure()

    if matrix_df.empty:
        fig.add_annotation(text="No timing data", showarrow=False, font=dict(size=14, color=PALETTE["muted"]))
        return _apply_common_layout(fig, height=270)

    # Lavender-purple gradient colorscale
    colorscale = [
        [0.0, "#FBF7FD"],
        [0.2, "#EFE4FA"],
        [0.4, "#DEC6F6"],
        [0.6, "#C59EF2"],
        [0.8, "#A775E7"],
        [1.0, "#7E43D6"]
    ]

    fig.add_trace(go.Heatmap(
        z=matrix_df.values,
        x=matrix_df.columns,
        y=matrix_df.index,
        colorscale=colorscale,
        showscale=False,
        xgap=3,
        ygap=3,
        hovertemplate="<b>Day:</b> %{y}<br><b>Hour:</b> %{x}<br><b>Avg Engagement:</b> %{z:,.0f}<extra></extra>"
    ))

    fig.update_xaxes(
        side="bottom",
        showgrid=False,
        tickfont=dict(color=PALETTE["muted"], size=10),
        linecolor="rgba(0,0,0,0)"
    )
    fig.update_yaxes(
        autorange="reversed",
        showgrid=False,
        tickfont=dict(color=PALETTE["muted"], size=10),
        linecolor="rgba(0,0,0,0)"
    )

    fig.update_layout(
        height=260,
        margin=dict(l=40, r=10, t=10, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def plot_post_type_comparison(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart comparing Reach and Likes across content types."""
    fig = go.Figure()

    if df.empty:
        return _apply_common_layout(fig, height=320)

    fig.add_trace(go.Bar(
        x=df["post_type"],
        y=df["avg_reach"],
        name="Avg Reach",
        marker=dict(color="#C4B5FD")
    ))
    fig.add_trace(go.Bar(
        x=df["post_type"],
        y=df["avg_likes"],
        name="Avg Likes",
        marker=dict(color="#F472B6")
    ))

    fig.update_layout(barmode="group", bargap=0.3)
    fig.update_xaxes(showgrid=False, tickfont=dict(color=PALETTE["muted"]))
    fig.update_yaxes(showgrid=True, gridcolor=PALETTE["grid"], tickfont=dict(color=PALETTE["muted"]))
    return _apply_common_layout(fig, height=320)


def plot_hashtag_ranking(tag_df: pd.DataFrame, limit: int = 10) -> go.Figure:
    """Horizontal bar chart for top hashtags by average engagement."""
    fig = go.Figure()

    if tag_df.empty:
        return _apply_common_layout(fig, height=350)

    top = tag_df.head(limit).iloc[::-1]

    fig.add_trace(go.Bar(
        y=top["hashtag"],
        x=top["avg_likes"],
        orientation="h",
        marker=dict(
            color=top["avg_likes"],
            colorscale=[[0, "#FFD6E8"], [1, "#E25B88"]],
            line=dict(width=0)
        ),
        hovertemplate="<b>%{y}</b><br>Avg Likes: %{x:,.0f}<extra></extra>"
    ))

    fig.update_xaxes(showgrid=True, gridcolor=PALETTE["grid"], tickfont=dict(color=PALETTE["muted"]))
    fig.update_yaxes(showgrid=False, tickfont=dict(color=PALETTE["text"], size=11))
    return _apply_common_layout(fig, height=350)


def plot_reach_vs_engagement_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter plot mapping Reach vs Engagement Rate for content performance analysis."""
    if df.empty:
        fig = go.Figure()
        return _apply_common_layout(fig, height=340)

    temp = df.copy()
    temp["total_engagement"] = temp["likes"] + temp["comments"] + temp["shares"] + temp["saves"]
    temp["er"] = (temp["total_engagement"] / temp["reach"].clip(lower=1)) * 100

    color_map = {
        "Instagram": PALETTE["instagram"],
        "YouTube": PALETTE["youtube"],
        "TikTok": PALETTE["tiktok"],
        "Facebook": PALETTE["facebook"]
    }

    fig = px.scatter(
        temp,
        x="reach",
        y="er",
        color="platform",
        size="likes",
        color_discrete_map=color_map,
        hover_data=["post_id", "post_type", "caption"],
        labels={"reach": "Unique Reach", "er": "Engagement Rate (%)"}
    )

    fig.update_xaxes(showgrid=True, gridcolor=PALETTE["grid"], tickfont=dict(color=PALETTE["muted"]))
    fig.update_yaxes(showgrid=True, gridcolor=PALETTE["grid"], tickfont=dict(color=PALETTE["muted"]))
    return _apply_common_layout(fig, height=340)
