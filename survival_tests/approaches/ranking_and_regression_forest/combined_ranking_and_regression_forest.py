import copy
import logging
import math
import random
from typing import List

import numpy as np
import pandas as pd
from pyexpat import features

from approaches.combined_ranking_regression_trees.binary_decision_tree import BinaryDecisionTree
from aslib_scenario import ASlibScenario

logger = logging.getLogger("run")


class CombinedRankingAndRegressionForest:
    def __init__(self, all_trained_with_one_error, amount_of_trees, tree: BinaryDecisionTree, consensus, feature_percentage=1) -> None:
        if all_trained_with_one_error:
            self.trees: List[BinaryDecisionTree] = [copy.deepcopy(tree) for _ in range(amount_of_trees)]
        else:
            self.trees: List[BinaryDecisionTree] = []
            for _ in range(amount_of_trees):
                self.trees.append(copy.deepcopy(random.choice(tree)))
        self.all_trained_with_one_error = all_trained_with_one_error
        self.consensus = consensus
        self.feature_percentage = feature_percentage
        self.amount_of_features = 0

    def get_name(self):
        if self.all_trained_with_one_error:
            return f"CombinedForest with {len(self.trees)} trees, {self.consensus.__name__} as consensus, {self.feature_percentage} of features"
        else:
            string_of_ranking_errors = set([x.ranking_loss.__name__ for x in self.trees])
            return f"CombinedForest with {len(self.trees)} trees, {self.consensus.__name__} as consensus, {self.feature_percentage} of features, trained with different errors {string_of_ranking_errors}"

    def fit(self, train_scenario: ASlibScenario, fold, amount_of_training_instances, depth=0, do_preprocessing=True):
        self.amount_of_features = math.ceil(len(train_scenario.features) * self.feature_percentage)
        if self.amount_of_features == 0:
            logger.error(f"No features selected for scenario {train_scenario.name}, and fold {fold}, consensus {self.consensus.__name__}, amount of trees {len(self.trees)}")
            raise Exception("No features selected")
        for tree in self.trees:
            selected_instances = copy.deepcopy(train_scenario)

            feature_data = []
            performance_data = []

            # select instances
            for _ in range(len(train_scenario.performance_data)):
                number_of_chosen_instance = np.random.random_integers(0, len(train_scenario.performance_data) - 1)

                feature_data.append(train_scenario.feature_data.iloc[number_of_chosen_instance, :])
                performance_data.append(train_scenario.performance_data.iloc[number_of_chosen_instance, :])

            selected_instances.feature_data = pd.DataFrame(columns=train_scenario.feature_data.columns, data=feature_data)
            selected_instances.performance_data = pd.DataFrame(columns=train_scenario.performance_data.columns, data=performance_data)

            tree.fit(selected_instances, fold, amount_of_training_instances, depth, do_preprocessing, self.amount_of_features)

        return self

    def predict(self, features: np.array, scenario):
        predictions = []
        for tree in self.trees:
            predictions.append(tree.predict(features, scenario))
        return self.consensus(predictions)
