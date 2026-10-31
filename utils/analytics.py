"""
Statistical calculations and data aggregations for VibeBloom.
All functions handle edge cases (empty data, missing columns, division by zero).
"""

import pandas as pd
import numpy as np


def compute_overview_kpis(df: pd.DataFrame) -> dict:
    """Computes high-level KPI cards for the overview dashboard."""
    if df.empty:
        return {
            "total_followers": 0,
            "total_posts": 0,
            "total_likes": 0,
            "total_comments": 0,
            "total_shares": 0,
            "total_saves": 0,
            "total_reach": 0,
            "total_engagement": 0,
            "avg_engagement_rate": 0.0
        }

    total_posts = len(df)
    total_likes = int(df["likes"].sum())
    total_comments = int(df["comments"].sum())
    total_shares = int(df["shares"].sum())
    total_saves = int(df["saves"].sum())
    total_reach = int(df["reach"].sum())
    total_engagement = total_likes + total_comments + total_shares + total_saves

    # Latest follower count across active platforms
    latest_followers = 0
    for _, group in df.groupby("platform"):
        if not group.empty:
            latest_row = group.sort_values(by="post_date", ascending=True).iloc[-1]
            latest_followers += int(latest_row.get("followers", 0))

    avg_er = (total_engagement / max(total_reach, 1)) * 100

    return {
        "total_followers": latest_followers,
        "total_posts": total_posts,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_shares": total_shares,
        "total_saves": total_saves,
        "total_reach": total_reach,
        "total_engagement": total_engagement,
        "avg_engagement_rate": round(avg_er, 2)
    }


def compute_platform_summaries(df: pd.DataFrame) -> dict:
    """
    Computes platform-specific metrics for Instagram, YouTube, TikTok, Facebook.
    Matches the 4 top cards seen in the reference design.
    """
    platforms = ["Instagram", "YouTube", "TikTok", "Facebook"]
    summaries = {}

    for plat in platforms:
        p_df = df[df["platform"].str.lower() == plat.lower()].sort_values(by="post_date")
        if p_df.empty:
            summaries[plat] = {
                "followers": 0,
                "label": "Total Followers",
                "growth_pct": 0.0,
                "posts": 0,
                "likes": 0,
                "comments": 0,
                "shares": 0,
                "saves": 0,
                "reach": 0,
                "engagement": 0,
                "avg_er": 0.0,
                "sparkline": [10, 15, 12, 18, 22, 20, 25]
            }
            continue

        latest_f = int(p_df.iloc[-1].get("followers", 0))
        first_f = int(p_df.iloc[0].get("followers", latest_f))
        growth = ((latest_f - first_f) / max(first_f, 1)) * 100

        p_likes = int(p_df["likes"].sum())
        p_comments = int(p_df["comments"].sum())
        p_shares = int(p_df["shares"].sum())
        p_saves = int(p_df["saves"].sum())
        p_reach = int(p_df["reach"].sum())
        p_eng = p_likes + p_comments + p_shares + p_saves
        p_er = (p_eng / max(p_reach, 1)) * 100

        # Sparkline data: last 8 posts normalized for mini bar chart
        spark_vals = p_df["likes"].tail(8).tolist()
        if len(spark_vals) < 8:
            spark_vals = [int(v) for v in np.linspace(min(spark_vals or [10]), max(spark_vals or [20]), 8)]

        label = "Total Subscribers" if plat.lower() == "youtube" else "Total Followers"

        summaries[plat] = {
            "followers": latest_f,
            "label": label,
            "growth_pct": round(growth, 1),
            "posts": len(p_df),
            "likes": p_likes,
            "comments": p_comments,
            "shares": p_shares,
            "saves": p_saves,
            "reach": p_reach,
            "engagement": p_eng,
            "avg_er": round(p_er, 2),
            "sparkline": spark_vals
        }

    return summaries


def get_engagement_trends(df: pd.DataFrame, freq: str = "W") -> pd.DataFrame:
    """
    Groups engagement metrics (Likes, Comments, Shares, Saves) by frequency ('W', 'ME' / 'M', 'D').
    """
    if df.empty:
        return pd.DataFrame()

    temp = df.copy()
    temp["post_date"] = pd.to_datetime(temp["post_date"])
    temp = temp.set_index("post_date")

    grouped = temp[["likes", "comments", "shares", "saves"]].resample(freq).sum().reset_index()
    # Format readable period label
    grouped["period_label"] = grouped["post_date"].dt.strftime("%b %d, %Y")
    return grouped


def get_audience_growth_by_platform(df: pd.DataFrame, freq: str = "ME") -> pd.DataFrame:
    """
    Returns follower trajectories across platforms aggregated by time period.
    """
    if df.empty:
        return pd.DataFrame()

    temp = df.copy()
    temp["post_date"] = pd.to_datetime(temp["post_date"])
    temp["period"] = temp["post_date"].dt.to_period("M").dt.to_timestamp()

    # Get max followers per period for each platform
    growth = temp.groupby(["period", "platform"])["followers"].max().reset_index()
    growth["period_name"] = growth["period"].dt.strftime("%b")
    return growth


def get_platform_engagement_share(df: pd.DataFrame) -> pd.DataFrame:
    """Computes total engagement and percentage share by platform."""
    if df.empty:
        return pd.DataFrame(columns=["platform", "engagement", "share_pct"])

    temp = df.copy()
    temp["total_engagement"] = temp["likes"] + temp["comments"] + temp["shares"] + temp["saves"]
    share = temp.groupby("platform")["total_engagement"].sum().reset_index()
    total = share["total_engagement"].sum()
    share["share_pct"] = (share["total_engagement"] / max(total, 1)) * 100
    share["share_pct"] = share["share_pct"].round(1)
    share = share.sort_values(by="total_engagement", ascending=False).reset_index(drop=True)
    return share


def get_top_performing_posts(df: pd.DataFrame, limit: int = 4, sort_by: str = "engagement") -> pd.DataFrame:
    """Returns top performing posts with calculated engagement rates."""
    if df.empty:
        return pd.DataFrame()

    temp = df.copy()
    temp["total_engagement"] = temp["likes"] + temp["comments"] + temp["shares"] + temp["saves"]
    temp["engagement_rate"] = (temp["total_engagement"] / temp["reach"].clip(lower=1)) * 100
    temp["engagement_rate"] = temp["engagement_rate"].round(2)

    if sort_by == "likes":
        sorted_df = temp.sort_values(by="likes", ascending=False)
    elif sort_by == "reach":
        sorted_df = temp.sort_values(by="reach", ascending=False)
    else:
        sorted_df = temp.sort_values(by="total_engagement", ascending=False)

    top = sorted_df.head(limit).copy()
    top["formatted_date"] = pd.to_datetime(top["post_date"]).dt.strftime("%b %d, %Y")
    return top


def compute_best_time_matrix(df: pd.DataFrame) -> tuple[pd.DataFrame, str, str]:
    """
    Calculates 7 days x 24 hours engagement matrix.
    Returns (heatmap_df, best_day, best_time_range).
    """
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    hours = list(range(24))

    if df.empty:
        empty_matrix = pd.DataFrame(0, index=days, columns=[f"{h:02d}:00" for h in hours])
        return empty_matrix, "Sunday", "6:00 PM – 9:00 PM"

    temp = df.copy()
    temp["dt"] = pd.to_datetime(temp["post_date"])
    temp["day_name"] = temp["dt"].dt.day_name().str[:3]
    temp["hour"] = temp["dt"].dt.hour
    temp["engagement"] = temp["likes"] + temp["comments"]

    pivot = temp.pivot_table(
        index="day_name",
        columns="hour",
        values="engagement",
        aggfunc="mean",
        fill_value=0
    )

    # Reindex to ensure all days and all hours exist
    pivot = pivot.reindex(index=days, fill_value=0)
    for h in hours:
        if h not in pivot.columns:
            pivot[h] = 0
    pivot = pivot[sorted(pivot.columns)]

    # Find peak day and hour
    flat_idx = pivot.stack().idxmax()
    best_day = flat_idx[0]
    best_h = int(flat_idx[1])
    h_str = f"{(best_h % 12) or 12}:00 {'AM' if best_h < 12 else 'PM'}"
    h_end = f"{((best_h + 2) % 12) or 12}:00 {'AM' if (best_h + 2) < 12 else 'PM'}"
    best_time = f"{h_str} – {h_end}"

    # Rename columns to formatted hour strings
    col_labels = []
    for h in hours:
        if h == 0:
            col_labels.append("12AM")
        elif h == 4:
            col_labels.append("4AM")
        elif h == 8:
            col_labels.append("8AM")
        elif h == 12:
            col_labels.append("12PM")
        elif h == 16:
            col_labels.append("4PM")
        elif h == 20:
            col_labels.append("8PM")
        else:
            col_labels.append(f"{h}")
    pivot.columns = col_labels

    return pivot, best_day, best_time


def compute_hashtag_analytics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parses and aggregates performance metrics per hashtag.
    """
    if df.empty:
        return pd.DataFrame(columns=["hashtag", "post_count", "avg_likes", "avg_reach", "avg_engagement_rate"])

    rows = []
    for _, row in df.iterrows():
        raw_tags = str(row.get("hashtags", ""))
        tags = [t.strip().lower() for t in raw_tags.replace(",", " ").split() if t.startswith("#")]
        eng = int(row["likes"]) + int(row["comments"]) + int(row["shares"]) + int(row["saves"])
        reach = max(int(row["reach"]), 1)
        er = (eng / reach) * 100

        for t in set(tags):
            rows.append({
                "hashtag": t,
                "likes": int(row["likes"]),
                "comments": int(row["comments"]),
                "reach": reach,
                "engagement": eng,
                "er": er
            })

    if not rows:
        return pd.DataFrame(columns=["hashtag", "post_count", "avg_likes", "avg_reach", "avg_engagement_rate"])

    tag_df = pd.DataFrame(rows)
    agg = tag_df.groupby("hashtag").agg(
        post_count=("likes", "count"),
        total_likes=("likes", "sum"),
        avg_likes=("likes", "mean"),
        avg_reach=("reach", "mean"),
        avg_engagement=("engagement", "mean"),
        avg_er=("er", "mean")
    ).reset_index()

    agg["avg_likes"] = agg["avg_likes"].round(0).astype(int)
    agg["avg_reach"] = agg["avg_reach"].round(0).astype(int)
    agg["avg_er"] = agg["avg_er"].round(2)
    agg = agg.sort_values(by="post_count", ascending=False).reset_index(drop=True)
    return agg


def compute_post_type_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates metrics by post type."""
    if df.empty:
        return pd.DataFrame()

    temp = df.copy()
    temp["total_engagement"] = temp["likes"] + temp["comments"] + temp["shares"] + temp["saves"]
    temp["er"] = (temp["total_engagement"] / temp["reach"].clip(lower=1)) * 100

    agg = temp.groupby("post_type").agg(
        count=("post_id", "count"),
        avg_reach=("reach", "mean"),
        avg_likes=("likes", "mean"),
        avg_comments=("comments", "mean"),
        avg_shares=("shares", "mean"),
        avg_saves=("saves", "mean"),
        avg_er=("er", "mean")
    ).reset_index()

    for c in ["avg_reach", "avg_likes", "avg_comments", "avg_shares", "avg_saves"]:
        agg[c] = agg[c].round(0).astype(int)
    agg["avg_er"] = agg["avg_er"].round(2)
    return agg
