#!/usr/bin/env python
"""
Created on Mon Jun 23 12:36:21 2014

Author: Oren Freifeld
Email: freifeld@csail.mit.edu
"""

import copy
from of.utils import Bunch

_params_flow_int = Bunch()
_params_flow_int.nTimeSteps=10
_params_flow_int.dt = 0.0001
_params_flow_int.nStepsODEsolver = 10

def get_params_flow_int():
    return copy.deepcopy(_params_flow_int)

if __name__ == "__main__":
    print get_params_flow_int()