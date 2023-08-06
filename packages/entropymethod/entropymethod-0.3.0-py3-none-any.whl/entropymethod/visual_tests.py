import numpy as np
import matplotlib.pyplot as plt
from pw_assoc_probs import pw_assoc_probs
import entropymethod as ent
from ent.find_stable_k import find_stable_k

np.random.seed(2)
data = np.concatenate([np.random.multivariate_normal(mean=np.array([0,1]), cov=np.eye(2)/50, size=30),
					   np.random.multivariate_normal(mean=np.array([1,0]), cov=np.eye(2)/50, size=30),
					   np.random.multivariate_normal(mean=np.array([0,-1]), cov=np.eye(2)/50, size=30),
					   np.random.multivariate_normal(mean=np.array([-1,0]), cov=np.eye(2)/50, size=30)])

fig, axs = plt.subplots(2)

axs[0].scatter(data[:,0], data[:,1])
axs[0].set_aspect('equal')

P = pw_assoc_probs(data,4)
axs[1].imshow(P, cmap='gray', vmin=0, vmax=1)
axs[1].set_xticks(range(data.shape[0]))
axs[1].set_yticks(range(data.shape[0]))
axs[1].axis('off')

# plt.show()

k = find_stable_k(data,k_max=10)
print(k)



