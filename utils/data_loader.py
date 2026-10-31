"""
Data loading, validation, generation, and persistence for VibeBloom.
"""

import os
import json
import random
from datetime import datetime, timedelta
import pandas as pd

REQUIRED_COLUMNS = [
    "post_id", "platform", "post_date", "post_type",
    "caption", "hashtags", "likes", "comments",
    "shares", "saves", "reach", "followers"
]

SAMPLE_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_posts.csv")
PLANNER_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "content_planner.json")


def generate_sample_dataset(num_records: int = 280, filepath: str = SAMPLE_CSV_PATH) -> pd.DataFrame:
    """Generate a realistic dataset for creator analytics."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    random.seed(42)

    platforms = ["Instagram", "YouTube", "TikTok", "Facebook"]
    platform_weights = [0.38, 0.26, 0.20, 0.16]

    types_by_platform = {
        "Instagram": ["Reel", "Carousel", "Static Post"],
        "YouTube": ["Shorts", "Video"],
        "TikTok": ["Video", "Shorts"],
        "Facebook": ["Video", "Static Post", "Carousel"]
    }

    aesthetic_captions = [
        "Soft mornings and pastel skies ♡ Finding peace in everyday quiet routines.",
        "Golden hour magic that feels like pure poetry ✨ Embracing slow living.",
        "Studio reset & creative sprint for the week ahead 🌸 What are you creating today?",
        "Matcha lattes, gentle breeze, and floral journals. Sunday mood board.",
        "Behind the scenes of our latest aesthetic shoot! Lighting was everything today.",
        "Desk makeover with lilac touches and cozy fairy lights 💜 Workspace serenity.",
        "5 creative habits that elevated my photography portfolio this year 🌷",
        "Chasing sunbeams and pastel clouds ☁️ Never underestimate simple joy.",
        "Mini vlog: A day of deep work, book cafes, and thrifted art books.",
        "Curating sweet memories and pastel aesthetics. Little things that matter.",
        "How I organize my digital planner for maximum creative flow ✨",
        "Quiet moments before the world wakes up. Earl grey & fresh ideas.",
        "Palette inspiration: Lavender blush, soft apricot & warm ivory 🎨",
        "Creative burnout is real — here is how I rekindled my artistic spark.",
        "Sunday self-care rituals: Fresh flowers, journaling, and homemade scones.",
        "New creative collection unveiling tomorrow! Sneak peek inside the sketchbook.",
        "Vintage camera test in the botanical garden 🌿 Nature is the best artist.",
        "Cozy evening study session with lo-fi beats and warm peach candlelight.",
        "Weekly reflection: Celebrate small wins. They bloom into big dreams 🌸",
        "Quick tips for editing dreamy pastel photos right from your phone!"
    ]

    hashtag_pool = [
        "#aesthetic", "#creativemind", "#pastelvibes", "#slowliving",
        "#creatorlife", "#dailyvlog", "#floralinspo", "#softaesthetic",
        "#cozyvibes", "#contentcreator", "#studyaesthetic", "#glowup",
        "#mindfulliving", "#artistsoninstagram", "#creativesoul", "#pastelcore",
        "#visualdiary", "#goldenhour", "#cozydesk", "#creativestudio"
    ]

    base_date = datetime(2026, 5, 2, 8, 30)
    end_date = datetime(2026, 10, 28, 22, 0)
    total_seconds = int((end_date - base_date).total_seconds())

    # Baseline platform follower trajectories
    followers_base = {
        "Instagram": 11200,
        "YouTube": 7600,
        "TikTok": 5200,
        "Facebook": 4400
    }

    records = []
    for i in range(1, num_records + 1):
        platform = random.choices(platforms, weights=platform_weights)[0]
        post_type = random.choice(types_by_platform[platform])

        # Random timestamp between May and late October 2026
        rand_sec = random.randint(0, total_seconds)
        post_date = base_date + timedelta(seconds=rand_sec)

        # Realistic time-based follower growth
        progress_ratio = rand_sec / max(total_seconds, 1)
        current_followers = int(followers_base[platform] + (progress_ratio * (followers_base[platform] * random.uniform(0.12, 0.22))))

        # Metric simulations correlated with reach & post type
        if post_type in ["Reel", "Shorts"]:
            reach = int(random.lognormvariate(9.2, 0.7))
            reach = max(2500, min(reach, 120000))
            like_ratio = random.uniform(0.07, 0.16)
            share_ratio = random.uniform(0.015, 0.04)
            save_ratio = random.uniform(0.01, 0.035)
        elif post_type == "Carousel":
            reach = int(random.lognormvariate(8.6, 0.6))
            reach = max(1800, min(reach, 75000))
            like_ratio = random.uniform(0.06, 0.13)
            share_ratio = random.uniform(0.01, 0.025)
            save_ratio = random.uniform(0.025, 0.07)  # carousels get more saves
        elif post_type == "Video":
            reach = int(random.lognormvariate(9.0, 0.65))
            reach = max(2000, min(reach, 90000))
            like_ratio = random.uniform(0.05, 0.12)
            share_ratio = random.uniform(0.015, 0.03)
            save_ratio = random.uniform(0.01, 0.03)
        else:  # Static Post
            reach = int(random.lognormvariate(8.2, 0.5))
            reach = max(1200, min(reach, 45000))
            like_ratio = random.uniform(0.04, 0.10)
            share_ratio = random.uniform(0.005, 0.018)
            save_ratio = random.uniform(0.008, 0.025)

        likes = int(reach * like_ratio)
        comments = int(likes * random.uniform(0.03, 0.08))
        shares = int(reach * share_ratio)
        saves = int(reach * save_ratio)

        # Pick caption & hashtags
        caption = random.choice(aesthetic_captions)
        chosen_tags = random.sample(hashtag_pool, k=random.randint(3, 5))
        hashtags = " ".join(chosen_tags)

        records.append({
            "post_id": f"VB-{1000 + i}",
            "platform": platform,
            "post_date": post_date.strftime("%Y-%m-%d %H:%M:%S"),
            "post_type": post_type,
            "caption": caption,
            "hashtags": hashtags,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "saves": saves,
            "reach": reach,
            "followers": current_followers
        })

    df = pd.DataFrame(records)
    df = df.sort_values(by="post_date", ascending=True).reset_index(drop=True)
    df.to_csv(filepath, index=False)
    return df


def validate_and_clean_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame | None, str]:
    """
    Validates that a dataframe meets the required schema.
    Returns (cleaned_df, error_message).
    """
    if df is None or df.empty:
        return None, "The uploaded file is empty."

    # Normalize column names (strip whitespace and lowercase)
    col_mapping = {col: col.strip().lower() for col in df.columns}
    normalized_df = df.rename(columns=col_mapping)

    missing = [c for c in REQUIRED_COLUMNS if c not in normalized_df.columns]
    if missing:
        return None, f"Missing required columns: {', '.join(missing)}"

    try:
        # Date parsing
        normalized_df["post_date"] = pd.to_datetime(normalized_df["post_date"], errors="coerce")
        if normalized_df["post_date"].isna().all():
            return None, "Column 'post_date' does not contain valid datetime formats."

        # Numeric sanitization
        num_cols = ["likes", "comments", "shares", "saves", "reach", "followers"]
        for col in num_cols:
            normalized_df[col] = pd.to_numeric(normalized_df[col], errors="coerce").fillna(0).astype(int)
            normalized_df[col] = normalized_df[col].clip(lower=0)

        # String sanitization
        str_cols = ["post_id", "platform", "post_type", "caption", "hashtags"]
        for col in str_cols:
            normalized_df[col] = normalized_df[col].fillna("").astype(str).str.strip()

        # Remove rows without valid date
        normalized_df = normalized_df.dropna(subset=["post_date"])
        normalized_df = normalized_df.sort_values(by="post_date", ascending=True).reset_index(drop=True)

        if len(normalized_df) == 0:
            return None, "No valid records remained after cleaning datetime column."

        return normalized_df, ""
    except Exception as e:
        return None, f"Data processing error: {str(e)}"


def load_dataset(uploaded_file=None) -> tuple[pd.DataFrame, bool, str]:
    """
    Loads dataset from uploaded file or loads/generates the default sample data.
    Returns: (df, is_sample, message)
    """
    if uploaded_file is not None:
        try:
            raw_df = pd.read_csv(uploaded_file)
            cleaned_df, err = validate_and_clean_dataset(raw_df)
            if err:
                return load_sample_dataset(), True, f"Upload validation failed ({err}). Showing sample data."
            return cleaned_df, False, "Custom CSV uploaded & validated successfully! 🌸"
        except Exception as e:
            return load_sample_dataset(), True, f"Could not read CSV ({str(e)}). Showing sample data."

    return load_sample_dataset(), True, "Demonstration Dataset (280 Creator Records) loaded."


def load_sample_dataset() -> pd.DataFrame:
    """Loads sample CSV from disk, generating it if needed."""
    if os.path.exists(SAMPLE_CSV_PATH):
        try:
            df = pd.read_csv(SAMPLE_CSV_PATH)
            cleaned_df, err = validate_and_clean_dataset(df)
            if cleaned_df is not None and not err:
                return cleaned_df
        except Exception:
            pass
    return generate_sample_dataset()


def get_sample_csv_template_bytes() -> bytes:
    """Returns sample dataset CSV as downloadable bytes."""
    sample_df = load_sample_dataset()
    return sample_df.to_csv(index=False).encode("utf-8")


# -------------------------------------------------------------
# Content Planner Local Storage Utilities
# -------------------------------------------------------------

DEFAULT_PLANNER_POSTS = [
    {
        "id": "PLAN-101",
        "platform": "Instagram",
        "scheduled_date": "2026-11-05",
        "scheduled_time": "18:00",
        "post_type": "Reel",
        "status": "Scheduled",
        "caption": "Desk setup glow-up with lavender backlights & soft music ♡",
        "hashtags": "#aestheticdesk #workspacegoals #creatorlife"
    },
    {
        "id": "PLAN-102",
        "platform": "YouTube",
        "scheduled_date": "2026-11-07",
        "scheduled_time": "14:30",
        "post_type": "Shorts",
        "status": "In Progress",
        "caption": "3 secrets to color grading dreamy pastel video clips 🌷",
        "hashtags": "#colorgrading #editingtutorial #videocreator"
    },
    {
        "id": "PLAN-103",
        "platform": "TikTok",
        "scheduled_date": "2026-11-09",
        "scheduled_time": "20:00",
        "post_type": "Video",
        "status": "Idea / Draft",
        "caption": "Pack my creative bag for a cafe work sprint with me ☁️",
        "hashtags": "#cafevlog #packwithme #studymood"
    },
    {
        "id": "PLAN-104",
        "platform": "Facebook",
        "scheduled_date": "2026-11-12",
        "scheduled_time": "11:00",
        "post_type": "Carousel",
        "status": "Scheduled",
        "caption": "Full Creative Moodboard & Palette Guide for Autumn 2026 🎨",
        "hashtags": "#moodboard #colorpalette #designideas"
    }
]


def load_planner_posts() -> list[dict]:
    """Loads planner items from local JSON file."""
    if os.path.exists(PLANNER_JSON_PATH):
        try:
            with open(PLANNER_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    return data
        except Exception:
            pass
    save_planner_posts(DEFAULT_PLANNER_POSTS)
    return DEFAULT_PLANNER_POSTS


def save_planner_posts(posts: list[dict]) -> bool:
    """Persists planner items to local JSON file."""
    try:
        os.makedirs(os.path.dirname(PLANNER_JSON_PATH), exist_ok=True)
        with open(PLANNER_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False
