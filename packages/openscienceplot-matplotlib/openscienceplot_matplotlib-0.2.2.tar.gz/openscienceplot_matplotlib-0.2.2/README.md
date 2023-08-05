# openscienceplot_matplotlib

The goal of this library is to allow you to share the raw-data from a (scientific) plot 
in an open way. 
In particular:

*   You choose the data that matters to you, and you choose how you organise the 
    data-file that you share.
*   Only open (and free!) data file-types are used.
*   Where possible, the amount of code you need to create the data-file is minimal.

>   A long-term gaol is to have similar libraries for different languages 
>   (e.g. Python/matplotlib, Matlab, ...)
>   and different file-type
>   (e.g. HDF5, yaml, JSON, ...)
>   to allow sharing data is a custom but still somewhat unified way.

# Usage

Please consider this minimal example

## Store to HDF5

```python
import numpy as np
import h5py
import matplotlib.pyplot as plt
import openscienceplot_matplotlib as osp

with h5py.File('mydata.hdf5', 'w') as data:

    fig, ax = plt.subplots()

    x = np.linspace(0, 1, 1000)
    y = x ** 2

    handle = ax.plot(x, y, color='r', label='myplot')
    osp.write_h5py(data, 'data', handle)
    
    data['by'] = osp.info()

    fig.savefig('myplot.pdf')
    plt.close(fig)
```
