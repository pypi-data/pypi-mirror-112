import numpy as np

def safe_entropy(P):
	"""
	Computes the elementwise binary entropies of a probability
	matrix, correctly accounting for zero or unit probabilities.
	"""
	# Binary entropy becomes nan when probability is close
	# to 0 or 1. The appearance of nan leads to a warning
	# about invalid multiplication, which we ignore below.
	np.seterr(all="ignore")
	entropy_w_nan = -(P*np.log2(P) + (1-P)*np.log2(1-P))
	return(np.nan_to_num(entropy_w_nan, nan=0.0))