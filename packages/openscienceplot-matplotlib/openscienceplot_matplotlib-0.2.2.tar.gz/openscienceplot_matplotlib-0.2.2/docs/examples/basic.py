import numpy as np
import h5py
import matplotlib.pyplot as plt
import openscienceplot_matplotlib as osp

with h5py.File('mydata.hdf5', 'w') as data:

    fig, ax = plt.subplots()

    x = np.linspace(0, 1, 1000)
    y = x ** 2

    handle = ax.plot(x, y, color='r', label='myplot')
    osp.dump(data, 'data', handle)

    data['by'] = osp.info()

    fig.savefig('myplot.pdf')
    plt.close(fig)
