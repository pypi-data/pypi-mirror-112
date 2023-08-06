import numpy as np
from scipy.stats import norm

import pymannkendall

# MK-score (S) is insensitive to removing NaNs, so does S variance. 

# Removing NaNs leads to unevenly-spaced time steps

# Sen's slope tolerate missing data (i.e. NaNs), but not missing time steps
# fed with evenly-spaced time series 


# re-writen from pyMannKendall
# --------------------------------------------------------------------------

def acf(x, nlags):
	n = len(x)
	x2 = x - np.mean(x)
	auto_cov = np.correlate(x2, x2, 'full')[n-1:] / n
	auto_cor = auto_cov / auto_cov[0] # auto_cov[0] = var
	return auto_cor[:nlags+1]

def mk_score(x): 
	n = len(x)

	s = 0
	for k in range(n-1):
		s += np.sum(x[k+1:] > x[k]) - np.sum(x[k+1:] < x[k])
	return s

def variance_s(x):
	n = len(x)
	tp = np.array([np.sum(x==xi) for xi in np.unique(x)])
	var_s = (n*(n-1)*(2*n+5) - np.sum(tp*(tp-1)*(2*tp+5))) / 18
	return var_s

def z_score(s, var_s):

	if s > 0: z = (s-1) / np.sqrt(var_s)
	if s ==0: z = 0
	if s < 0: z = (s+1) / np.sqrt(var_s)

	return z

def p_value(z, alpha):

	p = 2 * (1 - norm.cdf(np.abs(z)))
	h = np.abs(z) > norm.ppf(1 - alpha/2)

	if h:
		if z < 0: trend = 'decreasing'
		if z > 0: trend = 'increasing'
	else: 
		trend = 'no trend'

	return p, h, trend

def get_pair_slope(y):

	n = len(y)
	x = np.arange(n)

	xmat = x[:, np.newaxis] - x[np.newaxis, :] # i - j
	ymat = y[:, np.newaxis] - y[np.newaxis, :] # vi - vj

	tril_idx = np.tril_indices(n, k=-1) # lower triangle index, and exclude diagonal
	xarr = xmat[tril_idx]
	yarr = ymat[tril_idx]

	slps = yarr / xarr
	return slps

def sens_slope(y):

	n = len(y)
	x = np.arange(n)

	slps = get_pair_slope(y)

	slp = np.nanmedian(slps)
	intp = np.median(y - x * slp) # based on wiki

	# intp = np.median(y) - np.median(x) * slp 	# intp eq. in pymannkandall makes less sense

	return slp, intp

# --------------------------------------------------------------------------

# Sen's slope with lower and upper bound

# reference:
# 	https://rdrr.io/cran/trend/src/R/sens.slope.Reference
# 	https://www.real-statistics.com/time-series-analysis/time-series-miscellaneous/sens-slope/

def sens_slope_lub(y, alpha=0.05):

	y2 = y[~np.isnan(y)]

	n = len(y2)
	k = n * (n - 1) / 2 # number of pairs

	var_s = variance_s(y2)

	c = norm.ppf(1 - alpha / 2) * np.sqrt(var_s)
	idx_lo = np.round((k - c) / 2).astype(int)
	idx_up = np.round((k + c) / 2 + 1).astype(int)

	slps = get_pair_slope(y)
	slps = slps[~np.isnan(slps)]

	slp = np.median(slps)
	slp_lo, slp_up = np.sort(slps)[[idx_lo, idx_up]]

	return slp, slp_lo, slp_up
