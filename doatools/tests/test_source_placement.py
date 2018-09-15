import unittest
import numpy as np
import numpy.testing as npt
from doatools.model.sources import FarField1DSourcePlacement, FarField2DSourcePlacement

class TestSourcePlacement(unittest.TestCase):

    def setUp(self):
        self.wavelength = 1

    # def test_far_field_stochastic_creation(self):
    #     sources = FarField1DSourcePlacement.generate(-np.pi/3, np.pi/3, 6)
    #     self.assertEqual(sources.n_sources, 6)
    #     npt.assert_array_almost_equal(
    #         sources.locations,
    #         np.linspace(-np.pi/3, np.pi/3, 6).reshape((-1, 1))
    #     )
    
    # def test_far_field_stochastic_creation_2d(self):
    #     sources = FarField2DSourcePlacement.generate((0, -1), (1.5, 1), (4, 3))
    #     self.assertEqual(sources.n_sources, 12)
    #     locations_expected = np.array([
    #         [0., -1.],
    #         [0., 0.],
    #         [0., 1.],
    #         [0.5, -1.],
    #         [0.5, 0.],
    #         [0.5, 1.],
    #         [1., -1.],
    #         [1., 0.],
    #         [1., 1.],
    #         [1.5, -1.],
    #         [1.5, 0.],
    #         [1.5, 1.],
    #     ])
    #     npt.assert_array_almost_equal(
    #         sources.locations,
    #         locations_expected
    #     )

    def test_far_field_1d(self):
        n_sources = 10
        locations = np.linspace(-60, 60, n_sources)
        sources = FarField1DSourcePlacement(locations, 'deg')
        self.assertEqual(sources.n_sources, n_sources)
        self.assertEqual(sources.unit, 'deg')
        npt.assert_array_equal(sources.locations, locations)
        # Test indexing
        for i in range(sources.n_sources):
            self.assertEqual(sources[i], locations[i])
        # Test slicing
        sources_subset = sources[:5]
        self.assertEqual(sources_subset.n_sources, 5)
        self.assertEqual(sources_subset.unit, 'deg')
        npt.assert_array_equal(sources_subset.locations, locations[:5])

    def test_far_field_1d_delay(self):
        sources = FarField1DSourcePlacement(np.linspace(-np.pi/3, np.pi/4, 5))
        # 1D array
        sensor_locations_1 = np.array([0, 1, 2]).reshape((-1, 1))
        D1, DD1 = sources.phase_delay_matrix(sensor_locations_1, self.wavelength, True)
        D1_expected = np.array([
            [  0.000000,  0.000000,  0.000000, 0.000000, 0.000000],
            [ -5.441398, -3.490751, -0.820120, 2.019664, 4.442883],
            [-10.882796, -6.981501, -1.640241, 4.039327, 8.885766]
        ])
        DD1_expected = np.array([
            [0.000000,  0.000000,  0.000000,  0.000000, 0.000000],
            [3.141593,  5.224278,  6.229432,  5.949737, 4.442883],
            [6.283185, 10.448555, 12.458864, 11.899475, 8.885766]
        ])
        npt.assert_array_almost_equal(D1, D1_expected)
        npt.assert_array_almost_equal(DD1, DD1_expected)

    def test_far_field_2d(self):
        locations = np.array([
            [0, 30], [0, 50], [135, 35], [150, 70], [240, 60]
        ])
        sources = FarField2DSourcePlacement(locations, 'deg')
        self.assertEqual(sources.n_sources, len(locations))
        self.assertEqual(sources.unit, 'deg')
        npt.assert_array_equal(sources.locations, locations)
        # Test indexing
        for i in range(sources.n_sources):
            npt.assert_array_equal(sources[i], locations[i])
        # Test slicing
        sources_subset = sources[-2:]
        self.assertEqual(sources_subset.n_sources, 2)
        self.assertEqual(sources_subset.unit, 'deg')
        npt.assert_array_equal(sources_subset.locations, locations[-2:])

if __name__ == '__main__':
    unittest.main()

