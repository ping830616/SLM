# Author | Eduardo Ortega
import pandas as pd
import numpy as np
import random, sys, math
from decimal import Decimal, getcontext

# Set precision to ensure no floating point errors
getcontext().prec = 50  # High precision for fixed-point arithmetic

# Fixed-point scaling factor for Q20.14
FIXED_SCALE = Decimal(2**14)

# Define constants
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
COSINE = "COSINE"
STD = "STD"
supp_DIST = (STD, COSINE)
MEAN = "MEAN"
JOINT = "JOINT"
supp_AGG = (MEAN, JOINT)

class DISTANCE_CLASS():
    def __init__(self, train_compute=None, train_memory=None, train_sensor=None, DIST=None, AGG=None):
        assert DIST is not None, f"DIST must be declared, supp DIST types : {supp_DIST}"
        assert AGG is not None, f"AGG must be declared, supp AGG types: {supp_AGG}"
        assert train_compute is not None and train_memory is not None and train_sensor is not None, "training data must be passed in"
        self.dim_compute = train_compute.shape[1]
        self.dim_memory = train_memory.shape[1]
        self.dim_sensor = train_sensor.shape[1]
        self.DIST_TYPE = DIST
        self.AGG_TYPE = AGG
    
    def fit(self, train_compute, train_memory, train_sensor):
        self.EX_compute = [np.mean(train_compute[:,d]) for d in range(self.dim_compute)]
        self.EX_memory = [np.mean(train_memory[:,d]) for d in range(self.dim_memory)]
        self.EX_sensor = [np.mean(train_sensor[:,d]) for d in range(self.dim_sensor)]
        if self.DIST_TYPE == STD:
            self.STD_compute = [np.std(train_compute[:,d]) for d in range(self.dim_compute)]
            self.STD_memory = [np.std(train_memory[:,d]) for d in range(self.dim_memory)]
            self.STD_sensor = [np.std(train_sensor[:,d]) for d in range(self.dim_sensor)]
        elif self.DIST_TYPE == COSINE:
            self.EX_NORM_compute = np.linalg.norm(self.EX_compute)**2
            self.EX_NORM_memory = np.linalg.norm(self.EX_memory)**2
            self.EX_NORM_sensor = np.linalg.norm(self.EX_sensor)**2
        else:
            assert False, "fit func: something is wrong"
        return self

    def predict(self, test_compute, test_memory, test_sensor):
        ERR_compute, ERR_memory, ERR_sensor, ERR_agg = [], [], [], []
        # COMPUTE
        for x in test_compute:
            if self.DIST_TYPE == STD:
                ERR_vector_compute = [((1/self.STD_compute[d])*(x[d] - self.EX_compute[d])) for d in range(self.dim_compute)]
                compute_err = sum([a**2 for a in ERR_vector_compute])
            if self.DIST_TYPE == COSINE:
                x_norm = np.linalg.norm(x)**2
                top = np.dot(x, self.EX_compute)**2
                compute_err = x_norm - (top / self.EX_NORM_compute)
            ERR_compute.append(compute_err)
        # MEMORY
        for x in test_memory:
            if self.DIST_TYPE == STD:
                ERR_vector_memory = [((1/self.STD_memory[d])*(x[d] - self.EX_memory[d])) for d in range(self.dim_memory)]
                memory_err = sum([a**2 for a in ERR_vector_memory])
            if self.DIST_TYPE == COSINE:
                x_norm = np.linalg.norm(x)**2
                top = np.dot(x, self.EX_memory)**2
                memory_err = x_norm - (top / self.EX_NORM_memory)
            ERR_memory.append(memory_err)
        # SENSOR
        for x in test_sensor:
            if self.DIST_TYPE == STD:
                ERR_vector_sensor = [((1/self.STD_sensor[d])*(x[d] - self.EX_sensor[d])) for d in range(self.dim_sensor)]
                sensor_err = sum([a**2 for a in ERR_vector_sensor])
            if self.DIST_TYPE == COSINE:
                x_norm = np.linalg.norm(x)**2
                top = np.dot(x, self.EX_sensor)**2
                sensor_err = x_norm - (top / self.EX_NORM_sensor)
            ERR_sensor.append(sensor_err)
        # AGG
        for idx in range(len(ERR_compute)):
            s1, s2, s3 = ERR_compute[idx], ERR_memory[idx], ERR_sensor[idx]
            agg_err = np.mean([s1, s2, s3]) if self.AGG_TYPE == MEAN else s1*s2*s3
            ERR_agg.append(agg_err)
        return ERR_agg, ERR_compute, ERR_memory, ERR_sensor

def to_fixed(x):
    """ Convert a decimal or integer to fixed-point Q20.14 representation. """
    return (Decimal(x) * FIXED_SCALE).quantize(Decimal(1))

def from_fixed(x):
    """ Convert back from fixed-point Q20.14 to a decimal number. """
    return (Decimal(x) / FIXED_SCALE)

class DISTANCE_CLASS_Q2014():
    def __init__(self, train_compute=None, train_memory=None, train_sensor=None, DIST=None, AGG=None):
        assert DIST is not None, f"DIST must be declared, supp DIST types : {supp_DIST}"
        assert AGG is not None, f"AGG must be declared, supp AGG types: {supp_AGG}"
        assert train_compute is not None and train_memory is not None and train_sensor is not None, "training data must be passed in"
        
        self.dim_compute = train_compute.shape[1]
        self.dim_memory = train_memory.shape[1]
        self.dim_sensor = train_sensor.shape[1]
        self.DIST_TYPE = DIST
        self.AGG_TYPE = AGG

    def fit(self, train_compute, train_memory, train_sensor):
        # Convert training data to fixed-point
        train_compute = np.vectorize(to_fixed)(train_compute)
        train_memory = np.vectorize(to_fixed)(train_memory)
        train_sensor = np.vectorize(to_fixed)(train_sensor)

        self.EX_compute = [to_fixed(sum(train_compute[:, d]) // len(train_compute)) for d in range(self.dim_compute)]
        self.EX_memory = [to_fixed(sum(train_memory[:, d]) // len(train_memory)) for d in range(self.dim_memory)]
        self.EX_sensor = [to_fixed(sum(train_sensor[:, d]) // len(train_sensor)) for d in range(self.dim_sensor)]

        if self.DIST_TYPE == STD:
            # Standard deviation calculation in fixed-point
            self.STD_compute = [to_fixed(
                sum(((train_compute[:, d] - self.EX_compute[d]) ** 2) for _ in train_compute) // len(train_compute)
            ) for d in range(self.dim_compute)]

            self.STD_memory = [to_fixed(
                sum(((train_memory[:, d] - self.EX_memory[d]) ** 2) for _ in train_memory) // len(train_memory)
            ) for d in range(self.dim_memory)]

            self.STD_sensor = [to_fixed(
                sum(((train_sensor[:, d] - self.EX_sensor[d]) ** 2) for _ in train_sensor) // len(train_sensor)
            ) for d in range(self.dim_sensor)]

        elif self.DIST_TYPE == COSINE:
            # Compute norms in fixed-point
            self.EX_NORM_compute = to_fixed(sum(x**2 for x in self.EX_compute))
            self.EX_NORM_memory = to_fixed(sum(x**2 for x in self.EX_memory))
            self.EX_NORM_sensor = to_fixed(sum(x**2 for x in self.EX_sensor))
        else:
            assert False, "fit func: something is wrong"
        return self

    def predict(self, test_compute, test_memory, test_sensor):
        # Convert test data to fixed-point
        test_compute = np.vectorize(to_fixed)(test_compute)
        test_memory = np.vectorize(to_fixed)(test_memory)
        test_sensor = np.vectorize(to_fixed)(test_sensor)

        ERR_compute, ERR_memory, ERR_sensor, ERR_agg = [], [], [], []

        # COMPUTE
        for x in test_compute:
            if self.DIST_TYPE == STD:
                ERR_vector_compute = [((x[d] - self.EX_compute[d]) * FIXED_SCALE // self.STD_compute[d]) for d in range(self.dim_compute)]
                compute_err = sum([a**2 for a in ERR_vector_compute])
            if self.DIST_TYPE == COSINE:
                x_norm = sum(a**2 for a in x)
                top = sum(a * b for a, b in zip(x, self.EX_compute)) ** 2
                compute_err = x_norm - (top // self.EX_NORM_compute)
            ERR_compute.append(compute_err)

        # MEMORY
        for x in test_memory:
            if self.DIST_TYPE == STD:
                ERR_vector_memory = [((x[d] - self.EX_memory[d]) * FIXED_SCALE // self.STD_memory[d]) for d in range(self.dim_memory)]
                memory_err = sum([a**2 for a in ERR_vector_memory])
            if self.DIST_TYPE == COSINE:
                x_norm = sum(a**2 for a in x)
                top = sum(a * b for a, b in zip(x, self.EX_memory)) ** 2
                memory_err = x_norm - (top // self.EX_NORM_memory)
            ERR_memory.append(memory_err)

        # SENSOR
        for x in test_sensor:
            if self.DIST_TYPE == STD:
                ERR_vector_sensor = [((x[d] - self.EX_sensor[d]) * FIXED_SCALE // self.STD_sensor[d]) for d in range(self.dim_sensor)]
                sensor_err = sum([a**2 for a in ERR_vector_sensor])
            if self.DIST_TYPE == COSINE:
                x_norm = sum(a**2 for a in x)
                top = sum(a * b for a, b in zip(x, self.EX_sensor)) ** 2
                sensor_err = x_norm - (top // self.EX_NORM_sensor)
            ERR_sensor.append(sensor_err)

        # AGG
        for idx in range(len(ERR_compute)):
            s1, s2, s3 = ERR_compute[idx], ERR_memory[idx], ERR_sensor[idx]
            agg_err = (s1 + s2 + s3) // 3 if self.AGG_TYPE == MEAN else (s1 * s2 * s3) // FIXED_SCALE
            ERR_agg.append(agg_err)

        return ERR_agg, ERR_compute, ERR_memory, ERR_sensor


