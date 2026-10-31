# 🌸 VibeBloom – Social Media Insights & Creator Analytics Dashboard

> **Academic Project Submission**: B.Tech Mini Project  
> **Domain**: Social Media Data Analytics  
> **Tech Stack**: Python, Streamlit, Pandas, Plotly, CSV Datasets  

---

## 📖 Overview

**VibeBloom** is a social media creator analytics dashboard built specifically for content creators, influencers, and digital marketers. Designed with a feminine, modern pastel aesthetic, VibeBloom translates complex social engagement metrics into actionable insights.

The dashboard helps creators optimize publishing schedules, identify high-performing content formats, monitor cross-platform follower velocity, and organize upcoming content pipelines.

---

## 🎨 Visual Design System

VibeBloom closely implements the aesthetic design language inspired by modern creative moodboards:
* **Color Palette**: Pastel Pink (`#E25B88`, `#FFF0F5`), Soft Lavender (`#8B5CF6`, `#DEC6F6`), Light Peach (`#FFE5D9`), and Periwinkle Blue (`#60A5FA`).
* **Cards & Layout**: Rounded cards (`border-radius: 20px`), soft layered drop-shadows, and micro-borders.
* **Typography**: Outfit for clean user interfaces, paired with *Dancing Script* and *Caveat* for artistic cursive accents (*"Create. Analyze. Grow."*).
* **Creative Elements**: Polaroid-style photo frames, inspirational notes (*"Small Content, Big Impact ♡"*), and platform sparklines.

---

## 🚀 Key Dashboard Features

1. **Dashboard Overview**:
   * Hero header banner with dynamic date-range selector and motivational tagline.
   * 4 Platform Stat Cards (Instagram, YouTube, TikTok, Facebook) showing follower counts, period-over-period growth rates, and mini pastel sparklines.
   * Smoothed multi-metric **Engagement Trends** area chart (Likes, Comments, Shares, Saves).
   * Grouped column **Audience Growth** chart.
   * **Top Performing Content** post card gallery.
   * **Platform Comparison** donut chart with center engagement volume.
   * **Best Time to Post** lavender activity heatmap snippet.
   * Quick action **Content Planner** scheduler.
2. **Platform Analysis**:
   * Comparative metrics table across Instagram, YouTube, TikTok, and Facebook.
   * Engagement share donut chart and monthly milestone tracking.
3. **Audience Insights**:
   * Follower growth velocity and unique reach metrics.
   * Like-to-comment ratio and save-to-share intention analysis.
4. **Content Performance**:
   * Reach and engagement rate comparison across formats (Reels, Carousels, Static Posts, Shorts, Videos).
   * Interactive *Reach vs. Engagement Rate* scatter plot.
   * Filterable Top 10 viral posts leaderboard.
5. **Hashtag Analytics**:
   * Frequency distribution and average likes per tag.
   * Interactive hashtag performance simulator and lookup tool.
6. **Best Time to Post**:
   * Full 7 Days × 24 Hours engagement matrix heatmap.
   * Optimal day and peak window recommendation engine.
7. **Content Planner**:
   * Interactive calendar and upcoming content pipeline.
   * Form to schedule posts with status tags (*Scheduled*, *In Progress*, *Idea / Draft*).
   * Local file persistence (`data/content_planner.json`).
8. **Data Explorer**:
   * Search and filter posts by keyword, platform, or date.
   * Live descriptive statistics summary.
   * Download filtered data or template CSV with one click.

---

## 📂 Project Structure

```text
DimpleSocial/
├── .streamlit/
│   └── config.toml             # Custom theme colors (pink/lavender/white font & backgrounds)
├── data/
│   ├── sample_posts.csv        # Realistic 280+ record creator demonstration dataset
│   └── content_planner.json    # Local JSON storage for scheduled posts
├── utils/
│   ├── __init__.py
│   ├── data_loader.py          # Data ingestion, schema validation, CSV cleaning & sample generator
│   ├── analytics.py            # KPI math, engagement rate calculations, growth rates, safe divisions
│   ├── charts.py               # Plotly charts styled with custom pastel palette & tooltips
│   └── styles.py               # Custom CSS injection (fonts, cards, buttons, sidebar styling)
├── app.py                      # Main Streamlit web application
├── test_app.py                 # Automated unit test suite
├── requirements.txt            # Minimal dependencies for Streamlit Community Cloud
└── README.md                   # Project documentation
```

---

## 📊 Dataset Schema

The demonstration dataset includes 280+ realistic creator records with natural trends:

| Column Name | Data Type | Description |
|---|---|---|
| `post_id` | `str` | Unique post identifier (e.g. `VB-1001`) |
| `platform` | `str` | Platform (`Instagram`, `YouTube`, `TikTok`, `Facebook`) |
| `post_date` | `datetime` | Post publishing date and time |
| `post_type` | `str` | Format (`Reel`, `Shorts`, `Carousel`, `Video`, `Static Post`) |
| `caption` | `str` | Caption text and creative concept |
| `hashtags` | `str` | Hashtags used (e.g. `#aesthetic #creativemind`) |
| `likes` | `int` | Number of likes received |
| `comments` | `int` | Number of comments received |
| `shares` | `int` | Number of shares / reposts |
| `saves` | `int` | Number of bookmarks / saves |
| `reach` | `int` | Total unique accounts reached |
| `followers` | `int` | Creator follower count at time of posting |

> **Note**: Sample data is provided for academic demonstration purposes and does not represent live social media API connections. Users can upload their own CSV data using the sidebar at any time.

---

## 🛠️ Local Installation & Running

### Step 1: Clone / Navigate to Project
```bash
cd /Users/apple/Documents/Projects/DimpleSocial
```

### Step 2: Set Up Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Tests
```bash
python test_app.py
```

### Step 5: Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Deployment to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Select your repository, branch (`main`), and set **Main file path** to `app.py`.
4. Click **Deploy!** — Streamlit Cloud will read `requirements.txt` and `.streamlit/config.toml` automatically.
