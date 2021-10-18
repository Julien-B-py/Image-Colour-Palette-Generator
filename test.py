import numpy as np

a1 = np.array([7, 58, 85])
a2 = np.array([7, 34, 61])

print(np.allclose(a1, a2, atol=24))
