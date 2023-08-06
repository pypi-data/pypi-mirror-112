import numpy as np
import entropymethod as ent
from ent.pw_assoc_probs import pw_assoc_probs
from ent.entropy_score import entropy_score

def find_stable_k(X, k_range, B=100, f=0.5, out='argmin',verbose=False):
	"""
	Estimate the number of clusters with the Entropy Method.

	Parameters
    ----------
    X : ndarray 
    	The data matrix in standard format (rows are samples).
	k_max : int
		The maximum value of k to search over.
	k_min : int
		The minimum value of k to search over. Must be at least 2.
	B : int, optional
		The number of resamplings used when computing pairwise assocation 
		probabilities.
	f : float between 0 and 1, optional
		Specifies the relative number of samples drawn when subsampling 
		the data. If f=0.5, each subsampled data set has half as many
		samples as X. This setting is the default because the subsampling
		procedure then resembles the bootstrap.
	out : {'argmin', 'full'}, optional
		Specifies the desired form ofthe output. If out='argmin', the most stable
		value for k is returned. If out='full', a tuple (k_vals, scores)
		is returned, where scores is the full array of entropy scores for
		the whole range of k values considered. The array k_vals stores
		the associated values of k at each index of scores.

	Returns
    -------
    k : int
    	The number of clusters k that minimizes the relative average binary 
    	entropy. Other output formats are possible. Please see the description
    	of the parameter out above.
	"""

	k_vals = k_range
	scores = np.zeros(len(k_vals))

	if verbose:
		print('\nAssessing stability for different numbers of clusters...')
	for i in range(len(k_vals)):
		k = k_vals[i]
		P = pw_assoc_probs(X, k, B, f)
		scores[i] = entropy_score(P,k)
		if verbose:
			print('\tk = ' + str(k_vals[i]) + ': entropy = ' + 
				str(np.format_float_scientific(scores[i], precision=3)))


	stable_k = k_vals[np.argmin(scores)]
	if verbose:
		print('Stability analysis completed.')
		print('Most stable number of clusters: k = ' + str(stable_k))

	if (out == 'argmin'):
		return stable_k
	elif (out == 'full'):
		return (k_vals, scores)




