from enum import Enum


class ScoringFunction(Enum):
    """Enumeration of the scoring functions."""

    MAX = 1
    MIN = 2
    SUM = 3


class ScoringFunctionDirection(Enum):
    """
    Enumeration of the scoring function directions.

    IN_FAVOR: ScoringFunction(R(a,b))
    AGAINST: -ScoringFunction(R(b,a))
    DIFFERENCE: ScoringFunction(R(a,b) - R(b,a))
    """

    IN_FAVOR = 1
    AGAINST = 2
    DIFFERENCE = 3


class CompareProfiles(Enum):
    """Enumeration of the compare profiles types."""

    CENTRAL_PROFILES = 1
    BOUNDARY_PROFILES = 2
    LIMITING_PROFILES = 3


class PreferenceFunction(Enum):
    """Enumeration of the preference functions."""

    USUAL = 1
    U_SHAPE = 2
    V_SHAPE = 3
    LEVEL = 4
    V_SHAPE_INDIFFERENCE = 5
    GAUSSIAN = 6
