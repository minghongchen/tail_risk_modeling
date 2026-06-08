""" Functions used for copula construction and sampling """

import numpy as np
import pandas as pd
import openturns as ot

def build_copula_sample(resid_cdf, copula, sample_size=10000):
    ''' Build copula with transformed residuals and sample from it '''
    # Build copula with transformed residuals
    if copula == 'studentT':
        cmodel = ot.StudentCopulaFactory().build(ot.Sample(resid_cdf.values))
    elif copula == 'gaussian':
        cmodel = ot.NormalCopulaFactory().build(ot.Sample(resid_cdf.values))
    
    # Get sample from copula
    samples = cmodel.getSample(sample_size).asDataFrame()
    return samples