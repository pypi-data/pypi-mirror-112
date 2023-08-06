import numpy as np
import surpyval
from surpyval import nonparametric as nonp
from surpyval.nonparametric.nonparametric_fitter import NonParametricFitter

def fleming_harrington(x, c=None, n=None, **kwargs):
	r"""
	Fleming-Harrington estimation of survival distribution.

	Attributes
	----------
	
	x : array like
        The values of the random variables.
	c : array like, default is None
        The array, of same length as x, that flags whether a value in x is left censored (-1), right censored (1), observed (0), or interval censored (2)
    n : int
        The number of trials (copied from `b3inomtest` input).

	Ref:
	Fleming, T. R., and Harrington, D. P. (1984). “Nonparametric Estimation of the Survival Distribution in Censored Data.” Communications in Statistics—Theory and Methods 13:2469–2486.

	The Fleming-Harrington method estimates, like the Nelson-Aalen estimator the instantaneous hazard rate. With the instantaneous rate, the cumulative hazard is then computed, then the reliability function.

	Hazard Rate:
	at each x, for each d:

	.. math:: h = 1/r + 1/(r-1) + ... + 1/(r-d)
	
	Cumulative Hazard Function:

	.. math:: H = cumsum(h)

	Survival Function:

	.. math:: R = e^{-H}

    Methods
    -------
    proportion_ci :
        Compute the confidence interval for the estimate of the proportion.

    """
	x, r, d = surpyval.xcnt_to_xrd(x, c, n, **kwargs)

	h = [np.sum([1./(r[i]-j) for j in range(d[i])]) for i in range(len(x))]
	H = np.cumsum(h)
	R = np.exp(-H)
	return x, r, d, R

class FlemingHarrington_(NonParametricFitter):
	def __init__(self):
		self.how = 'Fleming-Harrington'

FlemingHarrington = FlemingHarrington_()