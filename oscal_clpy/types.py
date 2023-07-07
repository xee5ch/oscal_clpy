#!/usr/bin/env python3

from enum import Enum
from os import PathLike
from typing import Union

class Model(Enum):
    AssessmentPlan = 'assessment-plan'
    AssessmentResults = 'assessment-results'
    Catalog = 'catalog'
    POAM = 'poam'
    Profile = 'profile'
    SSP = 'system-security-plan'

_PathOrStr = Union[str, PathLike]

