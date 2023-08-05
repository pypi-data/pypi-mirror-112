import unittest
import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import openscienceplot_matplotlib as osp


class Test_plot(unittest.TestCase):

    def test_basic(self):

        x = np.random.random(10)
        y = np.random.random(10)

        filename = 'myfile.h5'

        for f in [filename]:
            if os.path.isfile(f):
                os.remove(f)

        with h5py.File(filename, 'w') as plot_data:

            fig, ax = plt.subplots()
            h = ax.plot(x, y)
            osp.dump(plot_data, 'mycurve', h)
            plt.close(fig)

            xy = plot_data['mycurve'][...]
            self.assertTrue(np.allclose(x, xy[:, 0]))
            self.assertTrue(np.allclose(y, xy[:, 1]))

            # todo: add assertions
            fig, ax = plt.subplots()
            h = osp.restore_h5py(plot_data, "mycurve", axis=ax)
            plt.close(fig)

        for f in [filename]:
            os.remove(f)


class Test_errorbar(unittest.TestCase):

    def test_basic(self):

        x = np.random.random(10)
        y = np.random.random(10)
        xerr = np.random.random(10)
        yerr = np.random.random(10)

        filename = 'myfile.h5'

        if os.path.isfile(filename):
            os.remove(filename)

        with h5py.File(filename, 'w') as plot_data:

            fig, ax = plt.subplots()
            h = ax.errorbar(x, y, xerr=xerr, yerr=yerr)
            osp.dump(plot_data, 'mycurve', h)
            plt.close(fig)

            xy = plot_data['mycurve'][...]
            self.assertTrue(np.allclose(x, xy[:, 0]))
            self.assertTrue(np.allclose(y, xy[:, 1]))

            e = plot_data['mycurve'].attrs["xerr"][...]
            self.assertTrue(np.allclose(xerr, e[0, :]))
            self.assertTrue(np.allclose(xerr, e[1, :]))

            e = plot_data['mycurve'].attrs["yerr"][...]
            self.assertTrue(np.allclose(yerr, e[0, :]))
            self.assertTrue(np.allclose(yerr, e[1, :]))

            # todo: add assertions
            fig, ax = plt.subplots()
            h = osp.restore_h5py(plot_data, "mycurve", axis=ax)
            plt.close(fig)

        os.remove(filename)

    def test_only_xerr(self):

        x = np.random.random(10)
        y = np.random.random(10)
        xerr = np.random.random(10)

        filename = 'myfile.h5'

        if os.path.isfile(filename):
            os.remove(filename)

        with h5py.File(filename, 'w') as plot_data:

            fig, ax = plt.subplots()
            h = ax.errorbar(x, y, xerr=xerr)
            osp.dump(plot_data, 'mycurve', h)
            plt.close(fig)

            xy = plot_data['mycurve'][...]
            self.assertTrue(np.allclose(x, xy[:, 0]))
            self.assertTrue(np.allclose(y, xy[:, 1]))

            e = plot_data['mycurve'].attrs["xerr"][...]
            self.assertTrue(np.allclose(xerr, e[0, :]))
            self.assertTrue(np.allclose(xerr, e[1, :]))

            self.assertTrue("yerr" not in plot_data['mycurve'].attrs)

            # todo: add assertions
            fig, ax = plt.subplots()
            h = osp.restore_h5py(plot_data, "mycurve", axis=ax)
            plt.close(fig)

        os.remove(filename)

    def test_only_yerr(self):

        x = np.random.random(10)
        y = np.random.random(10)
        yerr = np.random.random(10)

        filename = 'myfile.h5'

        if os.path.isfile(filename):
            os.remove(filename)

        with h5py.File(filename, 'w') as plot_data:

            fig, ax = plt.subplots()
            h = ax.errorbar(x, y, yerr=yerr)
            osp.dump(plot_data, 'mycurve', h)
            plt.close(fig)

            xy = plot_data['mycurve'][...]
            self.assertTrue(np.allclose(x, xy[:, 0]))
            self.assertTrue(np.allclose(y, xy[:, 1]))

            e = plot_data['mycurve'].attrs["yerr"][...]
            self.assertTrue(np.allclose(yerr, e[0, :]))
            self.assertTrue(np.allclose(yerr, e[1, :]))

            self.assertTrue("xerr" not in plot_data['mycurve'].attrs)

            # todo: add assertions
            fig, ax = plt.subplots()
            h = osp.restore_h5py(plot_data, "mycurve", axis=ax)
            plt.close(fig)

        os.remove(filename)

    def test_asymmetric(self):

        x = np.random.random(10)
        y = np.random.random(10)
        xerr = np.random.random(20).reshape(2, -1)
        yerr = np.random.random(20).reshape(2, -1)

        filename = 'myfile.h5'

        if os.path.isfile(filename):
            os.remove(filename)

        with h5py.File(filename, 'w') as plot_data:

            fig, ax = plt.subplots()
            h = ax.errorbar(x, y, xerr=xerr, yerr=yerr)
            osp.dump(plot_data, 'mycurve', h)
            plt.close(fig)

            xy = plot_data['mycurve'][...]
            self.assertTrue(np.allclose(x, xy[:, 0]))
            self.assertTrue(np.allclose(y, xy[:, 1]))

            e = plot_data['mycurve'].attrs["xerr"][...]
            self.assertTrue(np.allclose(xerr, e))

            e = plot_data['mycurve'].attrs["yerr"][...]
            self.assertTrue(np.allclose(yerr, e))

            # todo: add assertions
            fig, ax = plt.subplots()
            h = osp.restore_h5py(plot_data, "mycurve", axis=ax)
            plt.close(fig)

        os.remove(filename)


if __name__ == '__main__':

    unittest.main()
