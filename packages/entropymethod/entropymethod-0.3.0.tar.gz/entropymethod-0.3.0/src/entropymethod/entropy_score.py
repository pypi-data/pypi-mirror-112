import numpy as np
import entropymethod as ent
from ent.safe_entropy import safe_entropy

def entropy_score(P, k):
	"""
	Compute relative average binary entropy from pairwise association probabilities
	"""
	pw_entropy_mat = safe_entropy(P)
	average_entropy = np.mean(pw_entropy_mat)
	ref_entropy = (1/k)*np.log2(k) + (1 - (1/k))*np.log2(1/(1-(1/k)))
	
	return average_entropy/ref_entropy