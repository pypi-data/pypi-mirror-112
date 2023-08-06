import numpy as np
from sklearn.cluster import KMeans

def compute_prob_mat(X, k, B=100, f=0.5):
    """
    Compute the matrix of pairwise association probabilities for a 
    specified number of clusters. Each entry i,j stores the empirical
    probability that data points i and j are put into the same cluster,
    over many subsamplings of the data.

    More precisely, the entry i,j is the *conditional* probability that 
    data points i, j are put into the same cluster *given* that they
    both appear in the same subsample.

    Parameters
    ----------
    X : ndarray 
        The data matrix in standard format (rows are samples).
    k : int
    	The desired number of clusters.
    B : int, optional
        The number of resamplings used when computing pairwise assocation 
        probabilities.
    f : float between 0 and 1, optional
        Specifies the relative number of samples drawn when subsampling 
        the data. If f=0.5, each subsampled data set has half as many
        samples as X. This setting is the default because the subsampling
        procedure then resembles the bootstrap.


    Returns
    -------
    P : ndarray
        The matrix of pairwise association probabilities for k clusters.

    """
    n = X.shape[0]
    
    # set clustering algorithm
    cluster = KMeans(n_clusters=k)
    # association matrix tracks which data points are put in same cluster
    assoc_mat = np.zeros(shape=(n,n))
    # occurrence matrix tracks how often data points appear in same subsample
    occ_mat = np.zeros(shape=assoc_mat.shape)
    
    for b in range(B):
        # resample the data
        subsample = np.random.choice(n, size=int(np.floor(n*f)), replace=False)
        data_sub = X[subsample, :]

        # remember which data points appeared in the subsample together
        occ_mat[subsample[:, np.newaxis], subsample[np.newaxis,:]] += 1
    
        # obtain cluster memberships for subsampled data
        cluster_sub = cluster.fit_predict(X=data_sub)
        # remember which pairs of datapoints cluster together
        for group in np.unique(cluster_sub):
            this_cluster = subsample[cluster_sub == group]
            assoc_mat[this_cluster[:, np.newaxis], this_cluster[np.newaxis,:]] += 1

    return assoc_mat/occ_mat



def entropy_score(P, k):
	"""
	Compute entropy score from probability matrix,

    Parameters
    ----------
    P : ndarray 
        The probability matrix (see entropymethod.core.compute_prob_mat)
    k : int
    	The number of clusters for which P was computed

    Returns
    -------
    S : float
    	Entropy score, a low number indicates a good choice of k

    """

	np.seterr(all="ignore")
	entropy_w_nan = -(P*np.log2(P) + (1-P)*np.log2(1-P))
	pw_entropy_mat = np.nan_to_num(entropy_w_nan, nan=0.0)
	average_entropy = np.mean(pw_entropy_mat)
	ref_entropy = (1/k)*np.log2(k) + (1 - (1/k))*np.log2(1/(1-(1/k)))
	
	return average_entropy/ref_entropy




def find_k(X, k_range, B=100, f=0.5, out='argmin',verbose=False):
    """
    Estimate the number of clusters with the Entropy Method.

    Parameters
    ----------
    X : ndarray 
        The data matrix in standard format (rows are samples).
    k_range : iterable
        Contains numbers of clusters k to search over
    B : int, optional
        The number of resamplings used when computing pairwise assocation 
        probabilities.
    f : float between 0 and 1, optional
        Specifies the relative number of samples drawn when subsampling 
        the data. If f=0.5, each subsampled data set has half as many
        samples as X. This setting is the default because the subsampling
        procedure then resembles the bootstrap.
    out : {'argmin', 'full'}, optional
        Specifies the desired form of the output. If out='argmin', the most 
        stable value of k is returned. If out='full', a tuple (k_range, scores)
        is returned, where scores is the full array of entropy scores for
        the whole range of k values considered. The array k_range stores
        the associated values of k at each index of scores.
    verbose : bool, optional
        Decide whether the algorithm should print its progress and final result

    Returns
    -------
    k : int
        The number of clusters k that minimizes the entropy score.
        Other output formats are possible (see description of input parameter
        <out> above).
    """

    scores = np.zeros(len(k_range))

    if verbose:
        print('\nAssessing stability for different numbers of clusters...')
    for i, k in enumerate(k_range):
        P = compute_prob_mat(X, k, B, f)
        scores[i] = entropy_score(P,k)
        if verbose:
            print('\tk = ' + str(k_range[i]) + ': entropy = ' + 
                str(np.format_float_scientific(scores[i], precision=3)))


    stable_k = k_range[np.argmin(scores)]
    if verbose:
        print('Stability analysis completed.')
        print('Most stable number of clusters: k = ' + str(stable_k))

    if (out == 'argmin'):
        return stable_k
    elif (out == 'full'):
        return (k_range, scores)