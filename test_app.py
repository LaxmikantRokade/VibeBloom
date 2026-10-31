"""
Automated verification and unit test suite for VibeBloom.
Validates data generation, schema conformance, analytical math, and chart rendering.
"""

import os
import unittest
import pandas as pd
import plotly.graph_objects as go

from utils.data_loader import (
    generate_sample_dataset,
    validate_and_clean_dataset,
    load_sample_dataset,
    load_planner_posts,
    save_planner_posts,
    REQUIRED_COLUMNS
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


class TestVibeBloom(unittest.TestCase):

    def setUp(self):
        self.df = load_sample_dataset()

    def test_sample_dataset_generation(self):
        """Verify sample dataset generates >= 250 records and has all required columns."""
        self.assertGreaterEqual(len(self.df), 250, "Dataset should have at least 250 records")
        for col in REQUIRED_COLUMNS:
            self.assertIn(col, self.df.columns, f"Column {col} must exist in dataset")

    def test_data_validation_and_cleaning(self):
        """Test dataset validation with valid and corrupted inputs."""
        cleaned, err = validate_and_clean_dataset(self.df)
        self.assertEqual(err, "", "Valid dataset should have empty error message")
        self.assertIsNotNone(cleaned)

        # Empty dataframe test
        empty_df = pd.DataFrame()
        _, err_empty = validate_and_clean_dataset(empty_df)
        self.assertIn("empty", err_empty.lower())

        # Missing columns test
        bad_df = pd.DataFrame({"post_id": ["1"], "caption": ["hello"]})
        _, err_missing = validate_and_clean_dataset(bad_df)
        self.assertIn("missing required columns", err_missing.lower())

    def test_division_by_zero_safety(self):
        """Ensure analytics functions do not raise ZeroDivisionError even with zero reach/followers."""
        zero_df = pd.DataFrame([{
            "post_id": "VB-000",
            "platform": "Instagram",
            "post_date": "2026-06-01 10:00:00",
            "post_type": "Reel",
            "caption": "test",
            "hashtags": "#test",
            "likes": 0,
            "comments": 0,
            "shares": 0,
            "saves": 0,
            "reach": 0,
            "followers": 0
        }])
        zero_df["post_date"] = pd.to_datetime(zero_df["post_date"])

        kpis = compute_overview_kpis(zero_df)
        self.assertEqual(kpis["avg_engagement_rate"], 0.0)

        summaries = compute_platform_summaries(zero_df)
        self.assertIn("Instagram", summaries)
        self.assertEqual(summaries["Instagram"]["avg_er"], 0.0)

    def test_overview_kpis(self):
        """Verify overview KPI calculations."""
        kpis = compute_overview_kpis(self.df)
        self.assertGreater(kpis["total_posts"], 0)
        self.assertGreater(kpis["total_followers"], 0)
        self.assertGreater(kpis["total_engagement"], 0)
        self.assertGreater(kpis["avg_engagement_rate"], 0.0)

    def test_platform_summaries(self):
        """Verify all 4 platforms are analyzed."""
        summaries = compute_platform_summaries(self.df)
        for plat in ["Instagram", "YouTube", "TikTok", "Facebook"]:
            self.assertIn(plat, summaries)
            self.assertGreater(summaries[plat]["followers"], 0)
            self.assertEqual(len(summaries[plat]["sparkline"]), 8)

    def test_best_time_matrix(self):
        """Verify 7x24 heatmap computation."""
        matrix, best_d, best_t = compute_best_time_matrix(self.df)
        self.assertEqual(matrix.shape[0], 7, "Matrix must have 7 days")
        self.assertEqual(matrix.shape[1], 24, "Matrix must have 24 hours")
        self.assertIsInstance(best_d, str)
        self.assertIsInstance(best_t, str)

    def test_hashtag_analytics(self):
        """Verify hashtag parsing and calculations."""
        tags = compute_hashtag_analytics(self.df)
        self.assertFalse(tags.empty)
        self.assertIn("hashtag", tags.columns)
        self.assertIn("avg_likes", tags.columns)

    def test_plotly_chart_generation(self):
        """Ensure all Plotly chart rendering functions return valid Figures."""
        trends_df = get_engagement_trends(self.df, freq="W")
        fig_trend = plot_engagement_trends(trends_df)
        self.assertIsInstance(fig_trend, go.Figure)

        growth_df = get_audience_growth_by_platform(self.df, freq="ME")
        fig_growth = plot_audience_growth(growth_df)
        self.assertIsInstance(fig_growth, go.Figure)

        share_df = get_platform_engagement_share(self.df)
        fig_donut = plot_platform_comparison_donut(share_df)
        self.assertIsInstance(fig_donut, go.Figure)

        matrix, _, _ = compute_best_time_matrix(self.df)
        fig_heat = plot_best_time_heatmap(matrix)
        self.assertIsInstance(fig_heat, go.Figure)

        type_df = compute_post_type_breakdown(self.df)
        fig_types = plot_post_type_comparison(type_df)
        self.assertIsInstance(fig_types, go.Figure)

        tags = compute_hashtag_analytics(self.df)
        fig_tags = plot_hashtag_ranking(tags)
        self.assertIsInstance(fig_tags, go.Figure)

        fig_scatter = plot_reach_vs_engagement_scatter(self.df)
        self.assertIsInstance(fig_scatter, go.Figure)

    def test_planner_persistence(self):
        """Verify content planner loading and saving."""
        posts = load_planner_posts()
        self.assertIsInstance(posts, list)
        self.assertGreater(len(posts), 0)

        test_item = {
            "id": "PLAN-TEST",
            "platform": "Instagram",
            "scheduled_date": "2026-11-20",
            "scheduled_time": "12:00",
            "post_type": "Reel",
            "status": "Scheduled",
            "caption": "Test caption",
            "hashtags": "#test"
        }
        posts.append(test_item)
        saved = save_planner_posts(posts)
        self.assertTrue(saved)

        reloaded = load_planner_posts()
        ids = [p["id"] for p in reloaded]
        self.assertIn("PLAN-TEST", ids)

        # Cleanup test item
        cleaned_posts = [p for p in reloaded if p["id"] != "PLAN-TEST"]
        save_planner_posts(cleaned_posts)


if __name__ == "__main__":
    unittest.main()
