from openautomatumdronedata.dataset import droneDataset
import os
import numpy as np

dataset = droneDataset(os.path.abspath("datasets/highwayautumn-945ee2ff-4e82-407c-a15b-7161876b4248"))

for dynObj in dataset.dynWorld.get_list_of_dynamic_objects():
    vx_vec = np.asarray(dynObj.vx_vec)
    vy_vec = np.asarray(dynObj.vy_vec)
    mean_v = 3.6*np.mean(np.sqrt(vx_vec*vx_vec + vy_vec*vy_vec)) # Calculate the velocity in km/h
    print("%s %s drives with %.2f km/h"%(dynObj.__class__.__name__, dynObj.UUID, mean_v))