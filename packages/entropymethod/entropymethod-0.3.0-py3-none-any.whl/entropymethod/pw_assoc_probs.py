import numpy as np
from sklearn.cluster import KMeans

def pw_assoc_probs(data, k, B=100, f=0.5):
    """
    Compute the pairwise association probabilities for a specified number of clusters.
    """
    n = data.shape[0]
    
    # set clustering algorithm
    cluster = KMeans(n_clusters=k)
    # association matrix remembers which data points are clustered together
    assoc_mat = np.zeros(shape=(n,n))
    # occurrence matrix remembers how often data points appear in a subsample together
    occ_mat = np.zeros(shape=assoc_mat.shape)
    
    for b in range(B):
        # resample the data
        subsample = np.random.choice(n, size=int(np.floor(n*f)), replace=False)
        data_sub = data[subsample, :]

        # remember which data points appeared in the subsample together
        occ_mat[subsample[:, np.newaxis], subsample[np.newaxis,:]] += 1
    
        # obtain cluster memberships for subsampled data
        cluster_sub = cluster.fit_predict(X=data_sub)
        # remember which pairs of datapoints cluster together
        for group in np.unique(cluster_sub):
            this_cluster = subsample[cluster_sub == group]
            assoc_mat[this_cluster[:, np.newaxis], this_cluster[np.newaxis,:]] += 1

    return assoc_mat/occ_mat
