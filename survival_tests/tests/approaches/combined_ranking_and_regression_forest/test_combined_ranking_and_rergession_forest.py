import os
import unittest

from approaches.combined_ranking_regression_trees.binary_decision_tree import BinaryDecisionTree
from approaches.combined_ranking_regression_trees.borda_score import borda_score_mean_ranking
from approaches.combined_ranking_regression_trees.ranking_loss import squared_hinge_loss
from approaches.combined_ranking_regression_trees.regression_error_loss import mean_square_error
from approaches.combined_ranking_regression_trees.stopping_criteria import loss_under_threshold, max_depth
from approaches.ranking_and_regression_forest.combined_ranking_and_regression_forest import CombinedRankingAndRegressionForest as Forest
from aslib_scenario import ASlibScenario


class TestCombinedRankingAndRegressionForest(unittest.TestCase):
    def test_setup(self):
        self.scenario = ASlibScenario()
        self.fold = 1
        self.amount_of_training_instances = 1
        test_scenario_name = "QBF-2016"
        self.scenario.read_scenario(os.path.join("data", "aslib_data-master", test_scenario_name))

        self.scenario.performance_data = self.scenario.performance_data.iloc[:50]
        self.scenario.feature_data = self.scenario.feature_data.iloc[:50]

        basinc_ranking_loss = squared_hinge_loss
        basic_regression_loss = mean_square_error
        basic_borda_score = borda_score_mean_ranking
        basic_impact_factor = 0.9
        basic_stopping_criterion = max_depth
        self.binary_decision_tree: BinaryDecisionTree = BinaryDecisionTree(
            basinc_ranking_loss, basic_regression_loss, basic_borda_score, basic_impact_factor, basic_stopping_criterion, stopping_threshold=1
        )

        self.forest = Forest(1, self.binary_decision_tree, basic_borda_score)
        self.forest.fit(self.scenario, self.fold, self.amount_of_training_instances)
