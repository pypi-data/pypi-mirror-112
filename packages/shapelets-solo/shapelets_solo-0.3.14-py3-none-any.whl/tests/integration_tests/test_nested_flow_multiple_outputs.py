# Copyright (c) 2021 Grumpy Cat Software S.L.
#
# This Source Code is licensed under the MIT 2.0 license.
# the terms can be found in LICENSE.md at the root of
# this project, or at http://mozilla.org/MPL/2.0/.

import unittest

import numpy as np
import pandas as pd

from shapelets import init_session
from shapelets.dsl import dsl_op, InputParameter

from tests.util.test_util import (
    load_small_sequence1,
    load_small_sequence2,
    create_small_df
)


def my_flow(seq_a, seq_b):
    a = dsl_op.plusTSTS(seq_a, seq_b)
    b = dsl_op.timesTSTS(a, seq_b)
    c = dsl_op.plusTSTS(a, b)
    d = dsl_op.plusTS(b, 2)
    return c, d


def my_flow2(tss_a, tss_b, const):
    a = dsl_op.timesTS(tss_a, const)
    b = dsl_op.my_flow(a, tss_b)
    c = dsl_op.autoCorrelation(b[1], 4, False)  # requires CPP
    return b[0], c


def no_flow(tss_a, tss_b, const):
    a = dsl_op.timesTS(tss_a, const)
    a_1 = dsl_op.plusTSTS(a, tss_b)
    b_1 = dsl_op.timesTSTS(a_1, tss_b)
    c_1 = dsl_op.plusTSTS(a_1, b_1)
    c_2 = dsl_op.plusTS(b_1, 2)
    auto_corr = dsl_op.autoCorrelation(c_2, 4, False)
    return c_1, auto_corr


class NestedFlowMultipleOutputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._client = init_session("admin", "admin", "https://127.0.0.1", 8443)
        cls._sequence1 = load_small_sequence1(cls._client)
        cls._sequence2 = load_small_sequence2(cls._client)

    @unittest.skip("Re-enable when you have a CPP worker available")
    def test_end_to_end(self):
        seq1 = NestedFlowMultipleOutputs._sequence1
        seq2 = NestedFlowMultipleOutputs._sequence2
        client = NestedFlowMultipleOutputs._client
        client.register_flow(
            "my_flow",
            my_flow(
                InputParameter(0, "seq_a"),
                InputParameter(1, "seq_b")),
            ["out1", "out2"])
        client.register_flow(
            "my_flow2",
            my_flow2(
                InputParameter(0, "seq_a"),
                InputParameter(1, "seq_b"),
                InputParameter(2, "constant")))
        result_flow = client.run(dsl_op.my_flow2(seq1, seq2, -1))
        result_no_flow = client.run(no_flow(seq1, seq2, -1))
        result_flow_seq = client.get_sequence_data(result_flow[0])
        result_no_flow_seq = client.get_sequence_data(result_no_flow[0])
        result_expected = create_small_df([3.1, 10.4, 23.6, 464.0, 49.5]).iloc[:, 0]
        pd.testing.assert_series_equal(result_flow_seq, result_expected, check_names=False)
        pd.testing.assert_series_equal(result_flow_seq, result_no_flow_seq, check_names=False)
        np.testing.assert_array_equal(result_flow[1], result_no_flow[1])
