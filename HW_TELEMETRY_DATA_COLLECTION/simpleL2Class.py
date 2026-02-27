# Author | Eduardo Ortega
import pandas as pd
import numpy as np
import random, sys, math
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
AE="AE"
STD="STD"
supp_l2 = (AE, STD)

class L2_CLASS():
    def __init__(self, x_train=None, l2=None):
        assert l2 is not None, f"l2 must be declared, supp L2 types : {supp_l2}"
        assert x_train is not None, "training data must be passed in"
        self.train = x_train
        self.dim = x_train.shape[1]
        self.num_sample = x_train.shape[0]
        self.L2_TYPE = l2
        self.EX, self.STD = None, None
    
    def fit(self):
        self.EX = [np.mean(self.train[:,d]) for d in range(self.dim)]
        if self.L2_TYPE == STD:
            self.STD = [np.std(self.train[:,d]) for d in range(self.dim)]
        return self

    def adjust_ex(self):
        ex = [np.float16(e) for e in self.EX]
        self.EX = ex
        return self

    def adjust_std(self):
        std = [np.float16(s) for s in self.STD]
        self.STD = std
        return self
   
    def adjust_for_16_precision(self): 
        ex = [np.float16(e) for e in self.EX]
        self.EX = ex
        if self.L2_TYPE == STD:
            std = [np.float16(s) for s in self.STD]
            self.STD = std
        return self

    def build_ERR_vector(self, x):
        if self.L2_TYPE == AE:
            ERR_vector = [(x[d] - self.EX[d]) for d in range(self.dim)]
        else:
            ERR_vector = [((1/self.STD[d])*(x[d] - self.EX[d])) for d in range(self.dim)]
        return ERR_vector

    def helper_print_std(self):
        print(self.STD)

    def L2_norm(self, err_vector):
        L2_ERR = sum([x**2 for x in err_vector])
        return L2_ERR

    def predict(self, test_data):
        L2_ERROR_SCORES = []
        for x in test_data:
            ERR_vector = self.build_ERR_vector(x)
            L2 = self.L2_norm(ERR_vector)
            L2_ERROR_SCORES.append(L2)
        return L2_ERROR_SCORES

