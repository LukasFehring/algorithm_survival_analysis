import os
import unittest

import numpy as np

from approaches.combined_ranking_regression_trees.borda_score import borda_score_mean_performance, borda_score_mean_ranking, borda_score_median_ranking
from approaches.combined_ranking_regression_trees.ranking_transformer import calculate_ranking_from_performance_data
from aslib_scenario import ASlibScenario


class TestRankingTransformer(unittest.TestCase):
    def setUp(self) -> None:
        test_scenario_name = "MAXSAT15-PMS-INDU"
        scenario = ASlibScenario()
        scenario.read_scenario(os.path.join("data", "aslib_data-master", test_scenario_name))
        self.performance_data = scenario.performance_data.iloc[0:1000]
        self.ranking_data = calculate_ranking_from_performance_data(self.performance_data.values)

    def test_borda_score_mean_ranking(self):
        borda_ranking = borda_score_mean_ranking(self.ranking_data, self.performance_data)
        self.assertTrue(
            np.array_equal(
                borda_ranking, [22.0, 23.0, 17.0, 4.0, 3.0, 2.0, 5.0, 12.0, 6.0, 14.0, 10.0, 28.0, 28.0, 7.0, 19.0, 18.0, 21.0, 20.0, 1.0, 0.0, 16.0, 13.0, 8.5, 8.5, 11.0, 15.0, 28.0, 28.0, 28.0]
            )
        )

    def test_borda_score_median_ranking(self):
        borda_ranking = borda_score_median_ranking(self.ranking_data, self.performance_data)  # check again because of bad input
        self.assertTrue(
            np.array_equal(
                borda_ranking, [28.0, 28.0, 28.0, 13.5, 12.0, 11.0, 3.0, 9.0, 6.5, 9.0, 9.0, 28.0, 28.0, 3.0, 28.0, 28.0, 28.0, 28.0, 3.0, 0.5, 28.0, 28.0, 0.5, 5.0, 6.5, 13.5, 28.0, 28.0, 28.0]
            )
        )

    def test_borda_score_mean_performance(self):
        borda_ranking = borda_score_mean_performance(self.ranking_data, self.performance_data)
        self.assertTrue(
            np.array_equal(
                borda_ranking, [26.0, 28.0, 15.0, 13.0, 12.0, 8.0, 6.0, 9.0, 1.0, 10.0, 11.0, 22.0, 21.0, 0.0, 25.0, 24.0, 27.0, 23.0, 2.0, 3.0, 16.0, 17.0, 5.0, 4.0, 7.0, 14.0, 20.0, 18.0, 19.0]
            )
        )
