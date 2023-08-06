
![](https://www.automatum-data.com/-_-/res/364f0a3b-b8c0-4436-b97c-efad6e87a10b/images/files/364f0a3b-b8c0-4436-b97c-efad6e87a10b/83a25a57-6446-4c1e-9106-005ac5fd2d72/640-135/828451cade2c8f19c5be794314a323bbac5f0b82)

# Motivation
The AUTOMATUM DATA dataset is a new dataset for statistically meaningful, logical and practical solutions for researchers and industry in the development and realisation of automated driving. 

The presented dataset is freely available for future research and development-based endeavors under Creative Commons license model CC BY-ND.

# open.automatum.dronedata

This package provides an object-oriented structure for loading and analyzing data sets. It is intended to allow rapid use of the Automatum-Data drone dataset in research and development. In addition, a web server based visualization is provided, which allows to get an immediate overview of the datasets.

You can find additionally information about about automatum-data on [https://www.automatum-data.com](https://www.automatum-data.com).

Source code documentation: [https://openautomatumdronedata.rtfd.io](https://openautomatumdronedata.rtfd.io)



## Installation
Since we are currently in the pre-alpha phase, we are only available threw test.pypi
```
pip install openautomatumdronedata
```
or depending on your machine
```
pip3 install openautomatumdronedata
```

In addition, the package can also be installed manually, e.g. by placing the sources in your project folder.

## Exmaples 

```python
from openautomatumdronedata.dataset import droneDataset
import os
import numpy as np

dataset = droneDataset(os.path.abspath("datasets/highwayautumn-945ee2ff-4e82-407c-a15b-7161876b4248"))

for dynObj in dataset.dynWorld.get_list_of_dynamic_objects():
    vx_vec = np.asarray(dynObj.vx_vec)
    vy_vec = np.asarray(dynObj.vy_vec)
    mean_v = 3.6*np.mean(np.sqrt(vx_vec*vx_vec + vy_vec*vy_vec)) # Calculate the velocity in km/h
    print("%s %s drives with %.2f km/h"%(dynObj.__class__.__name__, dynObj.UUID, mean_v))

```


## Datasets

An example dataset is included in the Git repository. However, due to the large size, it is not included in the pip package. You can use the included dataset to get a brief idea of automatum-data dronedata. 

Every dataset consists of **dynamicWorld.json** including the objects and their movement, as well as the **staticWorld.xodr describing** the road geometry. 


To get full access to the dataset, please contact us via our website: [https://www.automatum-data.com](https://www.automatum-data.com).

A video with annotated objects can be found [here.](https://www.youtube.com/watch?v=FTHRNN-XNdY)

![](https://www.automatum-data.com/-_-/res/364f0a3b-b8c0-4436-b97c-efad6e87a10b/images/files/364f0a3b-b8c0-4436-b97c-efad6e87a10b/9fbc7c7c-1347-45ea-93f2-9b826b1c3e89/384-464/2cdf0d1b33e51842927cdc507a9f491c0e136db9?o=width:384/height:464/
)



## Visualization

This package also provides a basic visualization of the dataset via a web server realized by bokeh.


In addition, the package can also be installed manually, e.g. by placing the source in the appropriate project folder.


If you installed the package via pip simply starte the visualization by typing:
```
automatum_vis
```
To start the visualization manually execute the ```automatumBokehSever.py``` script. 

To open a dataset simple copy the path of the dataset folder into the text filed on the top of the webpage. 
By clicking load the dataset will be loaded and visualized. 

![](https://www.automatum-data.com/-_-/res/364f0a3b-b8c0-4436-b97c-efad6e87a10b/images/files/364f0a3b-b8c0-4436-b97c-efad6e87a10b/650b86fa-0811-48f9-be39-edc07e552107/240-43/568f0d4c3c716632137e10b91718c8316df39e66)


After loading a dataset you should get a comparable view:

![](https://www.automatum-data.com/-_-/res/364f0a3b-b8c0-4436-b97c-efad6e87a10b/images/files/364f0a3b-b8c0-4436-b97c-efad6e87a10b/80ddc0e3-f350-42e6-af88-721688ab8fdd/240-401/c48ba2dae76049521920e458e0dedfb171c59e0a)


## Note
We are currently in an early alpha phase of our development. 

The implemantation of XODR in over Bukeh server is currently only supporting streight or single curve streets. Other road items will not or wrongly displayd. The XODR itself is generated with CarMaker and remains fully compatible. 

## Requeired python packages: 
- bokeh 


