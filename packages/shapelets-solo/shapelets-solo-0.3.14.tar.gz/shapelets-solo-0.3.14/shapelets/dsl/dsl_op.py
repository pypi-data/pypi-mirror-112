# Copyright (c) 2020 Shapelets.io
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# DO NOT COMMIT THIS FILE

from shapelets.dsl.graph import NodeInputParamType, NodeReturnType


def c3(xss: NodeInputParamType, lag: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param lag: LONG
    :return output: ARRAY
    """
    pass


def abs(arg: NodeInputParamType) -> NodeReturnType:
    """
    :param arg: DOUBLE
    :return output: DOUBLE
    """
    pass


def div(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: DOUBLE
    """
    pass


def fft(ts: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def max(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: DOUBLE
    """
    pass


def min(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: DOUBLE
    """
    pass


def paa(ts: NodeInputParamType, bins: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :param bins: INT
    :return output: SEQUENCE
    """
    pass


def pow(arg1: NodeInputParamType, arg2: NodeInputParamType) -> NodeReturnType:
    """
    :param arg1: DOUBLE
    :param arg2: DOUBLE
    :return output: DOUBLE
    """
    pass


def rem(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: DOUBLE
    """
    pass


def sbd(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def plus(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: DOUBLE
    """
    pass


def DTWTS(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def absTS(ts: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def cidCe(xss: NodeInputParamType, zNormalize: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param zNormalize: BOOLEAN
    :return output: ARRAY
    """
    pass


def conjg(ts: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def divTS(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: SEQUENCE
    :param rhs: DOUBLE
    :return output: SEQUENCE
    """
    pass


def mapTS(functor: NodeInputParamType, ts: NodeInputParamType) -> NodeReturnType:
    """
    :param functor: FUNCTION
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def minus(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: DOUBLE
    """
    pass


def powTS(tss: NodeInputParamType, n: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param n: DOUBLE
    :return output: SEQUENCE
    """
    pass


def stdev(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def stomp(subsequenceLength: NodeInputParamType, firstTimeSeries: NodeInputParamType,
          secondTimeSeries: NodeInputParamType) -> NodeReturnType:
    """
    :param subsequenceLength: INT
    :param firstTimeSeries: SEQUENCE
    :param secondTimeSeries: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def sumTS(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def times(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: DOUBLE
    """
    pass


def zNorm(ts: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def equals(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: BOOLEAN
    """
    pass


def kMeans(tss: NodeInputParamType, k: NodeInputParamType, tolerance: NodeInputParamType,
           maxIterations: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param k: INT
    :param tolerance: FLOAT
    :param maxIterations: INT
    :return output: LIST:ARRAY
    """
    pass


def kShape(tss: NodeInputParamType, k: NodeInputParamType, tolerance: NodeInputParamType,
           maxIterations: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param k: INT
    :param tolerance: FLOAT
    :param maxIterations: INT
    :return output: LIST:ARRAY
    """
    pass


def length(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: LONG
    """
    pass


def meanTS(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def moment(tss: NodeInputParamType, k: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param k: INT
    :return output: ARRAY
    """
    pass


def plusTS(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: SEQUENCE
    :param rhs: DOUBLE
    :return output: SEQUENCE
    """
    pass


def toView(sequence_id: NodeInputParamType, index: NodeInputParamType,
           window_size: NodeInputParamType) -> NodeReturnType:
    """
    :param sequence_id: SEQUENCE_ID
    :param index: LONG
    :param window_size: LONG
    :return output: VIEW
    """
    pass


def rangeTS(to: NodeInputParamType) -> NodeReturnType:
    """
    :param to: LONG
    :return output: SEQUENCE
    """
    pass


def minusTS(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: SEQUENCE
    :param rhs: DOUBLE
    :return output: SEQUENCE
    """
    pass


def timesTS(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: SEQUENCE
    :param rhs: DOUBLE
    :return output: SEQUENCE
    """
    pass


def toMatch(sequence: NodeInputParamType, index: NodeInputParamType, window_size: NodeInputParamType,
            correlation: NodeInputParamType) -> NodeReturnType:
    """
    :param sequence: SEQUENCE_ID
    :param index: LONG
    :param window_size: LONG
    :param correlation: DOUBLE
    :return output: MATCH
    """
    pass


def hamming(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def forecast(tss: NodeInputParamType, window: NodeInputParamType, pointsToForecast: NodeInputParamType,
             numberOfCandidates: NodeInputParamType, minCorrelation: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param window: INT
    :param pointsToForecast: INT
    :param numberOfCandidates: INT
    :param minCorrelation: DOUBLE
    :return output: SEQUENCE
    """
    pass


def kurtosis(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def skewness(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def lessThan(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: BOOLEAN
    """
    pass


def plusTSTS(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: SEQUENCE
    :param rhs: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def meanNorm(ts: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def medianTS(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def reduceTS(functor: NodeInputParamType, ts: NodeInputParamType) -> NodeReturnType:
    """
    :param functor: FUNCTION
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def filterTS(functor: NodeInputParamType, ts: NodeInputParamType) -> NodeReturnType:
    """
    :param functor: FUNCTION
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def concatTS(ts1: NodeInputParamType, ts2: NodeInputParamType) -> NodeReturnType:
    """
    :param ts1: SEQUENCE
    :param ts2: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def convolve(xs: NodeInputParamType, ys: NodeInputParamType) -> NodeReturnType:
    """
    :param xs: SEQUENCE
    :param ys: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def aDFuller(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def uniquesTS(ts: NodeInputParamType, isSorted: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :param isSorted: BOOLEAN
    :return output_0: ND_ARRAY
    """
    pass


def manhattan(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def timesTSTS(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: SEQUENCE
    :param rhs: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def trendTest(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def reverseTS(ts: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def absEnergy(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def notEquals(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: BOOLEAN
    """
    pass


def minusTSTS(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: SEQUENCE
    :param rhs: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def to_double(arg: NodeInputParamType) -> NodeReturnType:
    """
    :param arg: DOUBLE
    :return output: DOUBLE
    """
    pass


def maxInterTS(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def minValueTS(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def constantTS(value: NodeInputParamType, phRows: NodeInputParamType) -> NodeReturnType:
    """
    :param value: DOUBLE
    :param phRows: LONG
    :return output: SEQUENCE
    """
    pass


def meanChange(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def minInterTS(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def maxValueTS(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def varianceTS(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def inverseFFT(ts: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def maxMinNorm(ts: NodeInputParamType, high: NodeInputParamType, low: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :param high: DOUBLE
    :param low: DOUBLE
    :return output: SEQUENCE
    """
    pass


def lessThanTS(tss: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param rhs: SEQUENCE
    :return output: ARRAY
    """
    pass


def meanInterTS(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def viavalingam(ts: NodeInputParamType, numPoints: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :param numPoints: INT
    :return output: SEQUENCE
    """
    pass


def euclideanTS(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def sampleStdev(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def greaterThan(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: BOOLEAN
    """
    pass


def splitEveryN(tss: NodeInputParamType, n: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param n: INT
    :return output: SEQUENCE
    """
    pass


def getRowSingle(tss: NodeInputParamType, at: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param at: LONG
    :return output: DOUBLE
    """
    pass


def localMaximals(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def hasDuplicates(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def countEqualsTS(tss: NodeInputParamType, value: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param value: DOUBLE
    :return output: ARRAY
    """
    pass


def greaterThanTS(tss: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param rhs: SEQUENCE
    :return output: ARRAY
    """
    pass


def decomposeView(output: NodeInputParamType) -> NodeReturnType:
    """
    :param output: VIEW
    :return sequence_id: SEQUENCE_ID
    :return index: LONG
    :return end: LONG
    """
    pass


def filterNDArray(functor: NodeInputParamType, nd_array: NodeInputParamType) -> NodeReturnType:
    """
    :param functor: FUNCTION
    :param nd_array: ND_ARRAY
    :return output_0: ND_ARRAY
    """
    pass


def fftAggregated(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def patternInData(tss: NodeInputParamType, queries: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param queries: SEQUENCE
    :return output: ARRAY
    """
    pass


def binnedEntropy(xss: NodeInputParamType, maxBins: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param maxBins: INT
    :return output: ARRAY
    """
    pass


def matrixProfile(tsa: NodeInputParamType, tsb: NodeInputParamType,
                  subsequenceLength: NodeInputParamType) -> NodeReturnType:
    """
    :param tsa: SEQUENCE
    :param tsb: SEQUENCE
    :param subsequenceLength: INT
    :return output: ARRAY
    """
    pass


def containsValue(tss: NodeInputParamType, value: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param value: DOUBLE
    :return output: BOOLEAN
    """
    pass


def toDenseRegular(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def ergodicityTest(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def fftCoefficient(xss: NodeInputParamType, coefficient: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param coefficient: LONG
    :return output: ARRAY
    """
    pass


def countAboveMean(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def countBelowMean(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def generateLevels(tss: NodeInputParamType, sizeInBytes: NodeInputParamType,
                   maxLevels: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param sizeInBytes: LONG
    :param maxLevels: INT
    :return output: LONG
    """
    pass


def adsCreateIndex(adsIndex: NodeInputParamType, numDivisions: NodeInputParamType,
                   sequences: NodeInputParamType) -> NodeReturnType:
    """
    :param adsIndex: ADSINDEX
    :param numDivisions: INT
    :param sequences: SEQUENCE
    :return output: ADSINDEX
    """
    pass


def autoCovariance(xss: NodeInputParamType, r: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param r: FLOAT
    :return output: ARRAY
    """
    pass


def periodicityTest(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def seasonalityTest(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output_0: ND_ARRAY
    """
    pass


def autoCorrelation(xss: NodeInputParamType, maxLag: NodeInputParamType,
                    unbiased: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param maxLag: LONG
    :param unbiased: BOOLEAN
    :return output_0: ND_ARRAY
    """
    pass


def cwtCoefficients(xs: NodeInputParamType, widths: NodeInputParamType, coeff: NodeInputParamType,
                    w: NodeInputParamType) -> NodeReturnType:
    """
    :param xs: SEQUENCE
    :param widths: SEQUENCE
    :param coeff: INT
    :param w: INT
    :return output: SEQUENCE
    """
    pass


def absTSOutputList(ts: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def numberCrossingM(xss: NodeInputParamType, m: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param m: INT
    :return output: ARRAY
    """
    pass


def crossCovariance(xs: NodeInputParamType, ys: NodeInputParamType, unbiased: NodeInputParamType) -> NodeReturnType:
    """
    :param xs: SEQUENCE
    :param ys: SEQUENCE
    :param unbiased: BOOLEAN
    :return output: ARRAY
    """
    pass


def zNormOutputList(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: LIST:SEQUENCE
    """
    pass


def patternSelfMatch(tss: NodeInputParamType, begin: NodeInputParamType, end: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param begin: LONG
    :param end: LONG
    :return index: LONG
    :return window_size: LONG
    :return correlation: DOUBLE
    """
    pass


def lessThanOrEquals(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: BOOLEAN
    """
    pass


def squaredEuclidean(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def hasDuplicatesMax(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def hasDuplicatesMin(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def indexMassQuantile(xss: NodeInputParamType, q: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param q: FLOAT
    :return output: ARRAY
    """
    pass


def symmetryLookingTS(xss: NodeInputParamType, r: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param r: FLOAT
    :return output: ARRAY
    """
    pass


def meanAbsoluteChange(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def adsExactSearchPlus(adsEntry: NodeInputParamType, adsIndex: NodeInputParamType,
                       queryTimeLeafSize: NodeInputParamType) -> NodeReturnType:
    """
    :param adsEntry: ADSENTRY
    :param adsIndex: ADSINDEX
    :param queryTimeLeafSize: INT
    :return output: ADSSEARCHPLUSRESULT
    """
    pass


def crossCorrelationTS(xs: NodeInputParamType, ys: NodeInputParamType, unbiased: NodeInputParamType) -> NodeReturnType:
    """
    :param xs: SEQUENCE
    :param ys: SEQUENCE
    :param unbiased: BOOLEAN
    :return output: ARRAY
    """
    pass


def decimalScalingNorm(ts: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :return output: SEQUENCE
    """
    pass


def meanNormOutputList(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: LIST:SEQUENCE
    """
    pass


def isaxRepresentation(ts: NodeInputParamType, alphabetSize: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :param alphabetSize: INT
    :return output: SEQUENCE
    """
    pass


def feedbackAlgorithms(action: NodeInputParamType, ts: NodeInputParamType, algorithmName: NodeInputParamType,
                       recommendationFeedback: NodeInputParamType) -> NodeReturnType:
    """
    :param action: STRING
    :param ts: ARRAY
    :param algorithmName: STRING
    :param recommendationFeedback: STRING
    :return output: BOOLEAN
    """
    pass


def approximatedEntropy(xss: NodeInputParamType, m: NodeInputParamType, r: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param m: INT
    :param r: FLOAT
    :return output: ARRAY
    """
    pass


def adsApproxSearchPlus(adsEntry: NodeInputParamType, adsIndex: NodeInputParamType,
                        queryTimeLeafSize: NodeInputParamType) -> NodeReturnType:
    """
    :param adsEntry: ADSENTRY
    :param adsIndex: ADSINDEX
    :param queryTimeLeafSize: INT
    :return output: ADSSEARCHPLUSRESULT
    """
    pass


def greaterThanOrEquals(lhs: NodeInputParamType, rhs: NodeInputParamType) -> NodeReturnType:
    """
    :param lhs: DOUBLE
    :param rhs: DOUBLE
    :return output: BOOLEAN
    """
    pass


def energyRatioByChunks(xss: NodeInputParamType, numSegments: NodeInputParamType,
                        segmentFocus: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param numSegments: LONG
    :param segmentFocus: LONG
    :return output: ARRAY
    """
    pass


def maxMinNormOutputList(ts: NodeInputParamType, high: NodeInputParamType, low: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: SEQUENCE
    :param high: DOUBLE
    :param low: DOUBLE
    :return output: SEQUENCE
    """
    pass


def absoluteSumOfChanges(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: ARRAY
    """
    pass


def maxLangevinFixedPoint(xss: NodeInputParamType, m: NodeInputParamType, r: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param m: INT
    :param r: FLOAT
    :return output: LONG
    """
    pass


def matrixProfileSelfJoin(timeSeries: NodeInputParamType, subsequenceLength: NodeInputParamType) -> NodeReturnType:
    """
    :param timeSeries: SEQUENCE
    :param subsequenceLength: INT
    :return output_0: ND_ARRAY
    """
    pass


def getRowSingleNumerical(tss: NodeInputParamType, range: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param range: LONG
    :return output: SEQUENCE
    """
    pass


def visvalingamOutputList(tss: NodeInputParamType, numPoints: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param numPoints: INT
    :return output: LIST:SEQUENCE
    """
    pass


def friedrichCoefficients(xss: NodeInputParamType, m: NodeInputParamType, r: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param m: INT
    :param r: FLOAT
    :return output: ARRAY
    """
    pass


def lastLocationOfMaximum(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def lastLocationOfMinimum(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def splitByPredicateOnAxis(tss: NodeInputParamType, groupingFunction: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param groupingFunction: FUNCTION
    :return output: LIST:SEQUENCE
    """
    pass


def largeStandardDeviation(xss: NodeInputParamType, r: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param r: FLOAT
    :return output: ARRAY
    """
    pass


def firstLocationOfMaximum(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def firstLocationOfMinimum(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def hierarchicalClustering(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: ARRAY
    :return output: STRING
    """
    pass


def longestStrikeAboveMean(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def longestStrikeBelowMean(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def containsValueOutputList(tss: NodeInputParamType, value: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :param value: DOUBLE
    :return output: LIST:BOOLEAN
    """
    pass


def localMaximalsOutputList(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: LIST:ARRAY
    """
    pass


def sumOfReoccurringValuesTS(xss: NodeInputParamType, isSorted: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param isSorted: BOOLEAN
    :return output: ARRAY
    """
    pass


def testFilterGreaterThanValue(maxValue: NodeInputParamType, values: NodeInputParamType) -> NodeReturnType:
    """
    :param maxValue: INT
    :param values: ND_ARRAY
    :return output_0: ND_ARRAY
    """
    pass


def meanSecondDerivativeCentral(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def sumOfReoccurringDataPointsTS(xss: NodeInputParamType, isSorted: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param isSorted: BOOLEAN
    :return output: ARRAY
    """
    pass


def decimalScalingNormOutputList(tss: NodeInputParamType) -> NodeReturnType:
    """
    :param tss: SEQUENCE
    :return output: LIST:SEQUENCE
    """
    pass


def testFilterGreaterThanValueList(maxValue: NodeInputParamType, values: NodeInputParamType) -> NodeReturnType:
    """
    :param maxValue: INT
    :param values: LIST:INT
    :return output_0: LIST:INT
    """
    pass


def timeReversalAsymmetryStatisticTS(xss: NodeInputParamType, lag: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :param lag: INT
    :return output: ARRAY
    """
    pass


def recommendMetadataFeatureSelection(ts: NodeInputParamType) -> NodeReturnType:
    """
    :param ts: ND_ARRAY
    :return output_0: ND_ARRAY
    """
    pass


def ratioValueNumberToTimeSeriesLength(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass


def varianceLargerThanStandardDeviation(xss: NodeInputParamType) -> NodeReturnType:
    """
    :param xss: SEQUENCE
    :return output: ARRAY
    """
    pass
