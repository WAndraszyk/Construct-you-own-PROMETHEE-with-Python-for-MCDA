"""
This module computes weights of criteria. It requires the user to specify the
criteria ranking. In this ranking each criterion is associated with a rank
which represents its importance.
The lowest and rank is 1, and it represents the highest importance.
"""
from pandas import Series
from core.aliases import NumericValue
from core.enums import SurrogateMethod
from typing import List
from core.preference_commons import criteria_series
from core.input_validation import surrogate_weights_validation
import pandas as pd

__all__ = ["surrogate_weights"]


def surrogate_weights(ranked_criteria: pd.Series, method: SurrogateMethod,
                      decimal_place: int = 3) -> pd.Series:
    """
    Calculates weights with chosen surrogate weights method.

    :param ranked_criteria: criteria with according ranks
    :param method: chosen method of calculating weights
    :param decimal_place: with this you can choose the decimal_place of the
     output numbers
    :return: Criteria with weights
    """

    def _weight_order(rc: pd.Series, weights: List[NumericValue]) -> Series:
        """
        This method assigns weights to according criteria.

        :return: Criteria with weights
        """
        rank_summed = rc.replace([i + 1 for i in range(len(weights))],
                                 weights)
        return criteria_series(rank_summed.index, rank_summed.values)

    def equal_weights(rc: pd.Series, dp: NumericValue = 3) -> pd.Series:
        """
        In this method all weights are computed with the same value and sum
        up to 1.

        :return: Criteria with weights
        """
        n = rc.size
        weights = []
        wi = round(1 / n, dp)
        for i in range(1, n + 1):
            weights.append(wi)
        return criteria_series(rc.index, weights)

    def rank_sum(rc: pd.Series, dp: NumericValue = 3) -> Series:
        """
        In this method the more important the criterion is, the greater
         its weight.

        :return: Criteria with weights
        """
        n = rc.size
        weights = []
        for i in range(1, n + 1):
            weights.append(round(2 * (n + 1 - i) / (n * (n + 1)), dp))
        return _weight_order(rc, weights)

    def reciprocal_of_ranks(rc: pd.Series, dp: NumericValue = 3) -> Series:
        """
        This method computes weights by dividing each reciprocal of rank by
        the sum of these
        reciprocals for all criteria.

        :return: Criteria with weights
        """
        n = rc.size
        weights = []
        sigma = 0
        for j in range(1, n + 1):
            sigma += 1 / j
        for i in range(1, n + 1):
            weights.append(round((1 / i) / sigma, dp))
        return _weight_order(rc, weights)

    def rank_order_centroid(rc: pd.Series, dp: NumericValue = 3) -> Series:
        """
        The weights in this method reflect the centroid of the simplex
        defined by ranking of
        the criteria.

        :return: Criteria with weights
        """
        n = rc.size
        weights = []
        for j in range(1, n + 1):
            sigma = 0
            for i in range(j, n + 1):
                sigma += 1 / i
            wi = round((1 / n) * sigma, dp)
            weights.append(wi)
        return _weight_order(rc, weights)

    surrogate_weights_validation(ranked_criteria, decimal_place)
    if method is SurrogateMethod.EW:
        return equal_weights(ranked_criteria, decimal_place)
    if method is SurrogateMethod.RS:
        return rank_sum(ranked_criteria, decimal_place)
    if method is SurrogateMethod.RR:
        return reciprocal_of_ranks(ranked_criteria, decimal_place)
    if method is SurrogateMethod.ROC:
        return rank_order_centroid(ranked_criteria, decimal_place)
    else:
        raise TypeError("Method should be a SurrogateMethod Enum.")
