# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

import numpy as np
import pandas as pd
import unittest

from shapelets import init_session
from shapelets.dsl import dsl_op
from shapelets.model import Match, Sequence, View
from tests.util.test_util import load_random_series


class FunctionsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._client = init_session("admin", "admin", "https://127.0.0.1", 8443)
        cls._sequences = load_random_series(cls._client)
        cls._sequence = cls.create_sequence()

    @staticmethod
    def create_sequence(data: list = None) -> Sequence:
        if data == None:
            data = [10.30, 10.90, 12.75, 12.95, 15.50, 15.70, 17.65, 17.95,
                    20.20, 25.00, 25.10, 25.20, 25.30, 27.05, 27.25, 27.45]
        np_array = np.array(data, dtype=np.dtype("int32"))
        freq = pd.tseries.offsets.DateOffset(microseconds=1000000)
        index = pd.date_range("2019-01-10 20:08", periods=len(data), freq=freq)
        dataframe = pd.DataFrame(np_array, index=index)
        sequence = FunctionsTest._client.create_sequence(dataframe, name="Test Sequence Indexed")
        return sequence

    def test_functions_uniques_ts(self):
        client = FunctionsTest._client
        data = [1.0, 2.0, 3.14, 3.14285714, 3.14, 3.14285714, 9]
        sequence = self.create_sequence(data)
        nd_array = client.run(dsl_op.uniquesTS(sequence, False))
        nd_array_data = client.get_nd_array_data(nd_array)
        np.testing.assert_array_almost_equal(nd_array_data, np.array([1, 2, 3, 9]))

    def test_auto_correlation(self):
        data = [7, 1, 1, 1]
        sequence = self.create_sequence(data)
        nd_array = FunctionsTest._client.run(dsl_op.autoCorrelation(sequence, 4, True))
        nd_array_data = FunctionsTest._client.get_nd_array_data(nd_array)
        np.testing.assert_array_almost_equal(nd_array_data, np.array([1, -0.11111111, -0.33333333, -1, ]))

    def test_ad_fuller(self):
        # Creates a sequence to fail AdFuller test
        data_1 = [2.1, 4.2, 10.8, 22.2, -5.5, 2.1, 4.2, 13.8, 2.2, -0.5, 2.1, 4.2, 11.8, 22.2, -5.5]
        sequence_1 = self.create_sequence(data_1)
        nd_array_1 = FunctionsTest._client.run(dsl_op.aDFuller(sequence_1))
        nd_array_data_1 = FunctionsTest._client.get_nd_array_data(nd_array_1)
        np.testing.assert_array_almost_equal(nd_array_data_1, np.array([0]))
        # Creates a second sequence to pass AdFuller test
        data_2 = [-0.85228184, 0.96759878, 0.96934673, -1.73297548, -0.15855425,
                  0.23712616, -1.85844138, 0.65276558, 0.92894701, 0.19917203]
        sequence_2 = self.create_sequence(data_2)
        nd_array_2 = FunctionsTest._client.run(dsl_op.aDFuller(sequence_2))
        nd_array_data_2 = FunctionsTest._client.get_nd_array_data(nd_array_2)
        np.testing.assert_array_almost_equal(nd_array_data_2, np.array([1]))

    def test_ergodicity(self):
        # Creates a sequence to fail Ergodicity test
        data_1 = [2.1, 4.2, 10.8, 22.2, -5.5, 2.1, 4.2, 13.8, 2.2, -0.5, 2.1, 4.2, 11.8, 22.2, -5.5]
        sequence_1 = self.create_sequence(data_1)
        nd_array_1 = FunctionsTest._client.run(dsl_op.ergodicityTest(sequence_1))
        nd_array_data_1 = FunctionsTest._client.get_nd_array_data(nd_array_1)
        np.testing.assert_array_almost_equal(nd_array_data_1, np.array([0]))

        # Creates a second sequence to pass Ergodicity test
        sequence_2 = self._sequence
        nd_array_2 = FunctionsTest._client.run(dsl_op.ergodicityTest(sequence_2))
        nd_array_data_2 = FunctionsTest._client.get_nd_array_data(nd_array_2)
        np.testing.assert_array_almost_equal(nd_array_data_2, np.array([1]))

    def test_recommend_metadata_feature_selection(self):
        input_array = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.dtype("float64"))
        nd_array = self._client.create_nd_array(array=input_array, name="test1",
                                                description="Description test")
        nd_array_result = self._client.run(dsl_op.recommendMetadataFeatureSelection(nd_array))
        nd_array_result_data = FunctionsTest._client.get_nd_array_data(nd_array_result)
        np.testing.assert_array_almost_equal(nd_array_result_data, np.array([0, 1]))

    @unittest.skip("Sometimes fails")
    def test_periodicity(self):
        sequence = [sequence for sequence in self._sequences if sequence.name == '73FC001C'][0]
        nd_array = self._client.run(dsl_op.periodicityTest(sequence))
        nd_array_data = FunctionsTest._client.get_nd_array_data(nd_array)
        np.testing.assert_array_almost_equal(nd_array_data, np.array([1]))

    def test_seasonality(self):
        sequence = self._sequences[0]
        nd_array = self._client.run(dsl_op.seasonalityTest(sequence))
        nd_array_data = FunctionsTest._client.get_nd_array_data(nd_array)
        np.testing.assert_array_almost_equal(nd_array_data, np.array([1]))

    def test_trend(self):
        # Creates a sequence to fail Trend test
        data_1 = [-0.18267, 1.27280, -0.74080, 0.64896, 2.34516, -1.25374, -0.53818, 0.43629,
                  -0.45910, 0.79188, -0.59177, -0.37307, -0.96924, 1.14651, 0.32489, 0.86189,
                  0.02995, -0.92409, -0.11956, -1.49242, -0.08233, -0.90231, -1.13066, 0.16642]
        sequence_1 = self.create_sequence(data_1)
        nd_array_1 = FunctionsTest._client.run(dsl_op.trendTest(sequence_1))
        nd_array_data_1 = FunctionsTest._client.get_nd_array_data(nd_array_1)
        np.testing.assert_array_almost_equal(nd_array_data_1, np.array([0]))
        # Creates a second sequence to pass Trend test
        data_2 = [-0.33856, -0.88048, 2.28131, 0.83755, 2.25138, -0.62463, -0.23920, -0.98709,
                  -0.10944, 0.62291, -1.37038, -0.05842, -0.33272, 2.50684, -0.4409, -0.33558,
                  1.55625, 0.32453, -0.4629, -0.97526, 0.36586, -1.19767, -0.61186, 1.67318]
        sequence_2 = self.create_sequence(data_2)
        nd_array_2 = FunctionsTest._client.run(dsl_op.trendTest(sequence_2))
        nd_array_data_2 = FunctionsTest._client.get_nd_array_data(nd_array_2)
        np.testing.assert_array_almost_equal(nd_array_data_2, np.array([1]))

    def test_div(self):
        self.assertEqual(self._client.run(dsl_op.div(10, 2)), 5.0)
        self.assertEqual(self._client.run(dsl_op.div(10.25, 2.5)), 4.1)
        self.assertEqual(self._client.run(dsl_op.div(10, -2)), -5.0)

    def test_fft(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.fft(sequence))
        data = self._client.get_sequence_data(res)
        expected_data = [309, -17.123401, -10, -8.868217, -11, -6.889142, -10, -7.119239,
                         -7, -7.119239, -10, -6.889142, -11, -8.868217, -10, -17.123401]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_max(self):
        self.assertEqual(self._client.run(dsl_op.max(10, 2)), 10.0)
        self.assertEqual(self._client.run(dsl_op.max(10.25, 2.5)), 10.25)
        self.assertEqual(self._client.run(dsl_op.max(-10, 2)), 2.0)
        self.assertEqual(self._client.run(dsl_op.max(-10, -2)), -2.0)

    def test_min(self):
        self.assertEqual(self._client.run(dsl_op.min(10, 2)), 2.0)
        self.assertEqual(self._client.run(dsl_op.min(10.25, 2.5)), 2.5)
        self.assertEqual(self._client.run(dsl_op.min(-10, 2)), -10)
        self.assertEqual(self._client.run(dsl_op.min(-10, -2)), -10)

    def test_paa(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.paa(sequence, 2))
        data = self._client.get_sequence_data(res)
        np.testing.assert_array_almost_equal(data.values, np.array([13.5, 25.125]))

    def test_pow(self):
        self.assertEqual(self._client.run(dsl_op.pow(10, 2)), 100.0)
        self.assertEqual(self._client.run(dsl_op.pow(10.25, 2.5)), 336.36412009764433)
        self.assertEqual(self._client.run(dsl_op.pow(-10, 2)), 100)

    def test_rem(self):
        self.assertEqual(self._client.run(dsl_op.rem(10.0, 10.0)), 0)
        self.assertEqual(self._client.run(dsl_op.rem(10.25, 2.5)), 0.25)
        self.assertEqual(self._client.run(dsl_op.rem(100.50, 50.0)), 0.5)

    def test_divTS(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.divTS(sequence, 2.0))
        data = self._client.get_sequence_data(res)
        expected_data = [5.0, 5.0, 6.0, 6.0, 7.5, 7.5, 8.5, 8.5,
                         10.0, 12.5, 12.5, 12.5, 12.5, 13.5, 13.5, 13.5]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_minus(self):
        self.assertEqual(self._client.run(dsl_op.minus(10, 2)), 8.0)
        self.assertEqual(self._client.run(dsl_op.minus(10.25, 2.5)), 7.75)
        self.assertEqual(self._client.run(dsl_op.minus(-10, 2)), -12)
        self.assertEqual(self._client.run(dsl_op.minus(-10, -2)), -8)

    def test_powTS(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.powTS(sequence, 2.0))
        data = self._client.get_sequence_data(res)
        expected_data = [100, 100, 144, 144, 225, 225, 289, 289,
                         400, 625, 625, 625, 625, 729, 729, 729]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_zNorm(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.zNorm(sequence))
        data = self._client.get_sequence_data(res)
        expected_data = [-1.477712, -1.477712, -1.160351, -1.160351, -0.68431, -0.68431, -0.366949, -0.366949,
                         0.109093, 0.902495, 0.902495, 0.902495, 0.902495, 1.219856, 1.219856, 1.219856]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_equals(self):
        self.assertTrue(self._client.run(dsl_op.equals(10, 10)))
        self.assertTrue(self._client.run(dsl_op.equals(10.52353636345, 10.52353636345)))
        self.assertTrue(self._client.run(dsl_op.equals(-10.5, -10.5)))
        self.assertFalse(self._client.run(dsl_op.equals(10.5, 10)))
        self.assertFalse(self._client.run(dsl_op.equals(-10.5, 10.5)))

    def test_length(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.length(sequence))
        self.assertEqual(res, 16)

    def test_toView(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.toView(sequence.sequence_id, 12, 12))
        data = self._client.get_sequence_data(res.sequence)
        expected_data = [10, 10, 12, 12, 15, 15, 17, 17, 20, 25, 25, 25, 25, 27, 27, 27]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))
        expected_view = View(sequence, 12, 24)
        self.assertEqual(res, expected_view)

    def test_rangeTS(self):
        res = self._client.run(dsl_op.rangeTS(23))
        data = self._client.get_sequence_data(res)
        expected_data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_minusTS(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.minusTS(sequence, 5.0))
        data = self._client.get_sequence_data(res)
        expected_data = [5, 5, 7, 7, 10, 10, 12, 12, 15, 20, 20, 20, 20, 22, 22, 22]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_toMatch(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.toMatch(sequence.sequence_id, 12, 12, 2.0))
        data = self._client.get_sequence_data(res.view.sequence)
        expected_data = [10, 10, 12, 12, 15, 15, 17, 17, 20, 25, 25, 25, 25, 27, 27, 27]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))
        expected_view = View(sequence, 12, 24)
        self.assertEqual(res.view, expected_view)
        expected_match = Match(2.0, expected_view)
        self.assertEqual(res, expected_match)

    def test_lessThan(self):
        self.assertTrue(self._client.run(dsl_op.lessThan(1, 2)))
        self.assertTrue(self._client.run(dsl_op.lessThan(1.124235245, 2.3465)))
        self.assertTrue(self._client.run(dsl_op.lessThan(-9.1, -2.3465)))
        self.assertFalse(self._client.run(dsl_op.lessThan(2, 1)))
        self.assertFalse(self._client.run(dsl_op.lessThan(9.1, -2.3465)))

    def test_meanNorm(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.meanNorm(sequence))
        data = self._client.get_sequence_data(res)
        expected_data = [-0.547794, -0.547794, -0.430147, -0.430147, -0.253676, -0.253676, -0.136029, -0.136029,
                         0.040441, 0.334559, 0.334559, 0.334559, 0.334559, 0.452206, 0.452206, 0.452206]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_concatTS(self):
        sequence_1 = self.create_sequence([1, 2, 3, 4])
        sequence_2 = self.create_sequence([5, 6, 7, 8])
        res = self._client.run(dsl_op.concatTS(sequence_1, sequence_2))
        data = self._client.get_sequence_data(res)
        expected_data = [1, 2, 3, 4, 5, 6, 7, 8]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_reverseTS(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.reverseTS(sequence))
        data = self._client.get_sequence_data(res)
        expected_data = [27, 27, 27, 25, 25, 25, 25, 20, 17, 17, 15, 15, 12, 12, 10, 10]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_notEquals(self):
        self.assertFalse(self._client.run(dsl_op.notEquals(2, 2)))
        self.assertFalse(self._client.run(dsl_op.notEquals(1.124235245, 1.124235245)))
        self.assertFalse(self._client.run(dsl_op.notEquals(-2.3465, -2.3465)))
        self.assertTrue(self._client.run(dsl_op.notEquals(2, 1)))
        self.assertTrue(self._client.run(dsl_op.notEquals(9.1, -2.3465)))

    def test_minusTSTS(self):
        sequence_1 = self._sequence
        sequence_2 = self.create_sequence([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        res = self._client.run(dsl_op.minusTSTS(sequence_1, sequence_2))
        data = self._client.get_sequence_data(res)
        expected_data = [9, 8, 9, 8, 10, 9, 10, 9, 11, 15, 14, 13, 12, 13, 12, 11]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_to_double(self):
        self.assertEqual(self._client.run(dsl_op.to_double(10.0)), 10.0)
        self.assertEqual(self._client.run(dsl_op.to_double(-10.25)), -10.25)
        self.assertEqual(self._client.run(dsl_op.to_double(1)), 1)

    def test_maxMinNorm(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.maxMinNorm(sequence, 10.0, 2.0))
        data = self._client.get_sequence_data(res)
        expected_data = [2, 2, 2.941176, 2.941176, 4.352941, 4.352941, 5.294118, 5.294118,
                         6.705882, 9.058824, 9.058824, 9.058824, 9.058824, 10, 10, 10]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_viavalingam(self):
        # TODO: Returns an irregular sequence, which requires axis in Array format
        sequence = self._sequence
        res = self._client.run(dsl_op.visvalingam(sequence, 4))
        res.axis.every = 1000
        data = self._client.get_sequence_data(res)
        expected_data = [1547150819328, 1547150819328, 1547150950400, 1547150950400]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_greaterThan(self):
        self.assertTrue(self._client.run(dsl_op.greaterThan(11, 10)))
        self.assertTrue(self._client.run(dsl_op.greaterThan(10.52353636345, 10.52353636300)))
        self.assertTrue(self._client.run(dsl_op.greaterThan(-2.5, -10.5)))
        self.assertFalse(self._client.run(dsl_op.greaterThan(10.5, 11)))
        self.assertFalse(self._client.run(dsl_op.greaterThan(-10.5, 10.5)))

    def test_splitEveryN(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.splitEveryN(sequence, 4))
        data_1 = self._client.get_sequence_data(res[0])
        data_2 = self._client.get_sequence_data(res[1])
        data_3 = self._client.get_sequence_data(res[2])
        data_4 = self._client.get_sequence_data(res[3])
        np.testing.assert_array_almost_equal(data_1.values, np.array([10, 10, 12, 12]))
        np.testing.assert_array_almost_equal(data_2.values, np.array([15, 15, 17, 17]))
        np.testing.assert_array_almost_equal(data_3.values, np.array([20, 25, 25, 25]))
        np.testing.assert_array_almost_equal(data_4.values, np.array([25, 27, 27, 27]))

    def test_getRowSingle(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.getRowSingle(sequence, 2))
        self.assertEqual(res, 10)

    def test_decomposeView(self):
        view = View(self._sequence, 2, 10)
        res = self._client.run(dsl_op.decomposeView(view))
        self.assertEqual(res[0], self._sequence.sequence_id)
        self.assertEqual(res[1], 2)
        self.assertEqual(res[2], 10)

    def test_containsValue(self):
        sequence = self._sequence
        self.assertTrue(self._client.run(dsl_op.containsValue(sequence, 10)))
        self.assertTrue(self._client.run(dsl_op.containsValue(sequence, 27.0)))
        self.assertFalse(self._client.run(dsl_op.containsValue(sequence, 28.05)))

    def test_toDenseRegular(self):
        # DENSE_REGULAR
        sequence_1 = self._sequence
        res_1 = self._client.run(dsl_op.toDenseRegular(sequence_1))
        res_data_1 = self._client.get_sequence_data(res_1)
        expected_data_1 = [10, 10, 12, 12, 15, 15, 17, 17, 20, 25, 25, 25, 25, 27, 27, 27]
        np.testing.assert_array_almost_equal(res_data_1.values, np.array(expected_data_1))

    def test_absTSOutputList(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.absTSOutputList(sequence))
        data = self._client.get_sequence_data(res)
        expected_data = [10, 10, 12, 12, 15, 15, 17, 17, 20, 25, 25, 25, 25, 27, 27, 27]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_zNormOutputList(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.zNormOutputList(sequence))
        data = self._client.get_sequence_data(res)
        expected_data = [-1.477712, -1.477712, -1.160351, -1.160351, -0.68431, -0.68431, -0.366949, -0.366949,
                         0.109093, 0.902495, 0.902495, 0.902495, 0.902495, 1.219856, 1.219856, 1.219856]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_lessThanOrEquals(self):
        self.assertTrue(self._client.run(dsl_op.lessThanOrEquals(10, 10)))
        self.assertTrue(self._client.run(dsl_op.lessThanOrEquals(10.5235363600, 10.52353636345)))
        self.assertTrue(self._client.run(dsl_op.lessThanOrEquals(-12.5, -10.5)))
        self.assertFalse(self._client.run(dsl_op.lessThanOrEquals(11.5, 11)))
        self.assertFalse(self._client.run(dsl_op.lessThanOrEquals(10.5, -10.5)))

    def test_decimalScalingNorm(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.decimalScalingNorm(sequence))
        data = self._client.get_sequence_data(res)
        expected_data = [0.1, 0.1, 0.12, 0.12, 0.15, 0.15, 0.17, 0.17, 0.2, 0.25, 0.25, 0.25, 0.25, 0.27, 0.27, 0.27]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_meanNormOutputList(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.meanNormOutputList(sequence))
        data = self._client.get_sequence_data(res)
        expected_data = [-0.547794, -0.547794, -0.430147, -0.430147, -0.253676, -0.253676, -0.136029, -0.136029,
                         0.040441, 0.334559, 0.334559, 0.334559, 0.334559, 0.452206, 0.452206, 0.452206]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_isaxRepresentation(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.isaxRepresentation(sequence, 0))
        data = self._client.get_sequence_data(res)
        expected_data = [19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_greaterThanOrEquals(self):
        self.assertTrue(self._client.run(dsl_op.greaterThanOrEquals(10, 10)))
        self.assertTrue(self._client.run(dsl_op.greaterThanOrEquals(10.52353636345, 10.52353636000)))
        self.assertTrue(self._client.run(dsl_op.greaterThanOrEquals(-9.5, -10.5)))
        self.assertFalse(self._client.run(dsl_op.greaterThanOrEquals(11.5, 21)))
        self.assertFalse(self._client.run(dsl_op.greaterThanOrEquals(-10.5, 10.5)))

    def test_maxMinNormOutputList(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.maxMinNormOutputList(sequence, 20, 9))
        data = self._client.get_sequence_data(res)
        expected_data = [9, 9, 10.294118, 10.294118, 12.235294, 12.235294, 13.529412, 13.529412,
                         15.470588, 18.705882, 18.705882, 18.705882, 18.705882, 20, 20, 20]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_matrixProfileSelfJoin(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.matrixProfileSelfJoin(sequence, 10))
        nd_array_data = self._client.get_nd_array_data(res)
        expected_nd_array_data = np.array([[1.348107, 1.444257, 1.348107, 1.444257, 1.46879, 1.517774, 1.72337],
                                           [2, 3, 0, 1, 2, 3, 4]])
        np.testing.assert_array_almost_equal(nd_array_data, expected_nd_array_data)

    def test_visvalingamOutputList(self):
        # TODO: Returns an irregular sequence, which requires axis in Array format
        sequence = self._sequence
        res = self._client.run(dsl_op.visvalingamOutputList(sequence, 4))
        res.axis.every = 1000
        data = self._client.get_sequence_data(res)
        expected_data = [1547150819328, 1547150819328, 1547150950400, 1547150950400]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_containsValueOutputList(self):
        sequence = self._sequence
        self.assertTrue(self._client.run(dsl_op.containsValueOutputList(sequence, 10.0)))
        self.assertTrue(self._client.run(dsl_op.containsValueOutputList(sequence, 27.0)))
        self.assertFalse(self._client.run(dsl_op.containsValueOutputList(sequence, 28.0)))

    def test_decimalScalingNormOutputList(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.decimalScalingNormOutputList(sequence))
        data = self._client.get_sequence_data(res)
        expected_data = [0.1, 0.1, 0.12, 0.12, 0.15, 0.15, 0.17, 0.17, 0.2, 0.25, 0.25, 0.25, 0.25, 0.27, 0.27, 0.27]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_abs(self):
        self.assertEqual(self._client.run(dsl_op.abs(2)), 2)
        self.assertEqual(self._client.run(dsl_op.abs(-2)), 2)
        self.assertEqual(self._client.run(dsl_op.abs(-2.1234)), 2.1234)

    def test_plus(self):
        self.assertEqual(self._client.run(dsl_op.plus(2, 2)), 4)
        self.assertEqual(self._client.run(dsl_op.plus(-2, 2)), 0)
        self.assertEqual(self._client.run(dsl_op.plus(2.12, 1.30)), 3.42)
        self.assertEqual(self._client.run(dsl_op.plus(-2.12, -1.30)), -3.42)

    def test_times(self):
        self.assertEqual(self._client.run(dsl_op.times(2, 2)), 4)
        self.assertEqual(self._client.run(dsl_op.times(-2, 2)), -4)
        self.assertEqual(self._client.run(dsl_op.times(2.12, 1.30)), 2.7560000000000002)
        self.assertEqual(self._client.run(dsl_op.times(-2.12, -1.30)), 2.7560000000000002)

    def test_plusTS(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.plusTS(sequence, 2))
        data = self._client.get_sequence_data(res)
        expected_data = [12, 12, 14, 14, 17, 17, 19, 19, 22, 27, 27, 27, 27, 29, 29, 29]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_plusTSTS(self):
        sequence_1 = self._sequence
        sequence_2 = self.create_sequence([12, 12, 14, 14, 17, 17, 19, 19, 22, 27, 27, 27, 27, 29, 29, 29])
        res = self._client.run(dsl_op.plusTSTS(sequence_1, sequence_2))
        data = self._client.get_sequence_data(res)
        expected_data = [22, 22, 26, 26, 32, 32, 36, 36, 42, 52, 52, 52, 52, 56, 56, 56]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_timesTS(self):
        sequence = self._sequence
        res = self._client.run(dsl_op.timesTS(sequence, 2))
        data = self._client.get_sequence_data(res)
        expected_data = [20, 20, 24, 24, 30, 30, 34, 34, 40, 50, 50, 50, 50, 54, 54, 54]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))

    def test_timesTSTS(self):
        sequence_1 = self._sequence
        sequence_2 = self.create_sequence([2, 2, 1, 4, 1, 7, 9, 1, 2, 7, 2, 6, 3, 5, 2, 4])
        res = self._client.run(dsl_op.timesTSTS(sequence_1, sequence_2))
        data = self._client.get_sequence_data(res)
        expected_data = [20, 20, 12, 48, 15, 105, 153, 17, 40, 175, 50, 150, 75, 135, 54, 108]
        np.testing.assert_array_almost_equal(data.values, np.array(expected_data))
