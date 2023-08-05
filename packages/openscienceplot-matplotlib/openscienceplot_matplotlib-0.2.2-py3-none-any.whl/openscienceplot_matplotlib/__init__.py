'''
This module provides methods to save data from a matplotlib plot.

:dependencies:

    * numpy
    * matplotlib
    * h5py

:copyright:

    | Tom de Geus
    | tom@geus.me
    | http://www.geus.me
'''

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import h5py
import operator
import functools
from functools import singledispatch

def _interpret(handle):
    r'''
(Private function)
Return to be stored data from a handle.

Essential attributes are outputted as well, as follows:

*   matplotlib.lines.Line2D ('artist'):
    'color', 'linestyle', 'marker', 'label'.

*   matplotlib.container.ErrorbarContainer ('artist'):
    'color', 'linestyle', 'marker', 'label'.
    Warning: for now saved as matplotlib.lines.Line2D, without error-bars.

:param matplotlib_object handle: The object's handle.
:return: (data, attributes)
:rtype: numpy.ndarray, dict
    '''

    import warnings

    if len(handle) == 1:
        handle = handle[0]

    if isinstance(handle, matplotlib.lines.Line2D):
        return (
            handle.get_xydata(),
            {
                "artist" : 'matplotlib.lines.Line2D',
                "color" : handle.get_color(),
                "linestyle" : handle.get_linestyle(),
                "marker" : handle.get_marker(),
                "label" : handle.get_label(),
            })

    if isinstance(handle, matplotlib.container.ErrorbarContainer):

        data = handle[0].get_xydata()
        xerr = None
        yerr = None

        for i in handle[2]:
            seg = np.array(i.get_segments())
            x = seg[:, :, 0]
            y = seg[:, :, 1]
            assert x.shape[0] == y.shape[0] == data.shape[0]
            if np.allclose(x[:, 0], x[:, 1]):
                yerr = np.abs(data[:, 1] - y.T)
            elif np.allclose(y[:, 0], y[:, 1]):
                xerr = np.abs(data[:, 0] - x.T)
            else:
                raise IOError("Unknown data")

        attributes = {
            "artist" : 'matplotlib.lines.Line2D',
            "color" : handle[0].get_color(),
            "linestyle" : handle[0].get_linestyle(),
            "marker" : handle[0].get_marker(),
        }

        if xerr is not None:
            attributes["xerr"] = xerr

        if yerr is not None:
            attributes["yerr"] = yerr

        return (data, attributes)

    raise IOError('Unknown handle. Store manually, or consider filing a bug-report.')


def info():
    r'''
Return basic library information.
    '''

    return [
        'openscienceplot_matplotlib={0:s}'.format(__version__),
        'matplotlib={0:s}'.format(matplotlib.__version__)]


@singledispatch
def dump():
    r'''
Save plot and attributes.

Essential attributes are stored as well, as follows:

*   matplotlib.lines.Line2D ('artist'):
    'color', 'linestyle', 'marker', 'label'.

*   matplotlib.container.ErrorbarContainer ('artist'):
    'color', 'linestyle', 'marker', 'label'.
    Warning: for now saved as matplotlib.lines.Line2D, without error-bars.

:param f: Opened HDF5 file.
:type f: h5py.File, dict.

:param str key:
    Name of the dataset to which to write.
    Path separated by "/", or specified as list.

:param matplotlib_object handle: The handle to write.

:param kwargs: Additional attributes to add (e.g. linestyle).

:return: f
    '''
    pass


@dump.register(h5py.File)
def _(f, key, handle, **kwargs):

    data, attributes = _interpret(handle)

    for key in kwargs:
        assert key not in attributes
        attributes[key] = kwargs[key]

    dset = f.create_dataset(key, data.shape, dtype=data.dtype)
    dset[:] = data

    for key in attributes:
        dset.attrs[key] = attributes[key]


@dump.register(dict)
def _(f, key, handle, **kwargs):

    if type(key) == str:
        key = list(filter(None, key.split("/")))

    data, attributes = _interpret(handle)
    attributes["data"] = data

    for key in kwargs:
        assert key not in attributes
        attributes[key] = kwargs[key]

    functools.reduce(operator.getitem, key[:-1], f)[key[-1]] = attributes


def restore_h5py(data, key, axis=None):
    r'''
Restore plot from HDF5-file.

:param h5py.File data: Opened HDF5 file.
:param str key: Name of the dataset from which to read.
:param matplotlib_object axis: The axis on which to plot (default ``plt.gca()``).
:return: The handle of the created plot.
    '''

    if axis is None:
        plt.gca()

    dset = data[key]

    if dset.attrs['artist'] == 'matplotlib.lines.Line2D':

        xy = dset[...]
        opts = {}

        for key in ['color', 'linestyle', 'marker', 'label']:
            if key in dset.attrs:
                opts[key] = dset.attrs[key]

        e = {}
        for key in ["xerr", "yerr"]:
            if key in dset.attrs:
                e[key] = dset.attrs[key][...]

        if len(e) > 0:
            return axis.errorbar(xy[:, 0], xy[:, 1], **e, **opts)

        return axis.plot(xy, **opts)

    raise IOError('Data-set not interpretable. Please consider filing a bug-report.')
