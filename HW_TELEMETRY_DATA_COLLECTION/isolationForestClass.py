# Author | Eduardo Ortega
import math, time, numbers, statistics, random, sys
import pandas as pd
import numpy as np
from sklearn.utils import (
        check_random_state, 
        check_array, 
        gen_batches, 
        get_chunk_n_rows,)
from sklearn.tree._tree import DTYPE as tree_dtype
from sklearn.utils.validation import check_is_fitted, _num_samples
from sklearn.ensemble._bagging import BaseBagging
from scipy.sparse import issparse
from scipy.stats import entropy
from numbers import Integral, Real
import random
import matplotlib.pyplot as plt

''' SUPPORTED SPLITS '''
RANDOM = "RANDOM"
QUANT = "QUANTIZED"
STURGE = "STURGE"
FREEDMAN = "FREEDMAN DIACONIS"
PROP = "PROPOSED"
GEN = "GENERAL"
SUPP_SPLITS = (RANDOM, QUANT, STURGE, FREEDMAN, PROP, GEN)
SUPP_QUANT = (QUANT, STURGE, FREEDMAN, PROP, GEN)

''' TYPES OF NODES '''
LEAF = "LEAF"
NODE = "NODE"

''' QUANTIZATION VARIABLES (EXPERIMENTAL) '''
MEDIAN = 0
STD = 1

def c_n(x):
    return 2.0*(np.log(x-1.0)+0.5772156649) - (2.0*(x-1.0)/x)

def auto_opt_bin(data, res_array, mul_factor=1):
    cost, bin_width_compare = [], []
    range = max(data) - min(data)
    upper_stdev_bound = statistics.mean(data) + (mul_factor * statistics.stdev(data))
    lower_stdev_bound = statistics.mean(data) - (mul_factor * statistics.stdev(data))
    upper_bound_data = data[data <= upper_stdev_bound]
    lower_bound_data = data[data >= lower_stdev_bound]
    data_within_one_stdev = np.intersect1d(upper_bound_data, lower_bound_data)
    try: 
        for resolution in res_array:
            bin_width, bin_width_count, diff_sub_count, diff_of_subseq_counts = [], [], [], []
            bin_step = (max(data_within_one_stdev) - min(data_within_one_stdev)) * resolution
            range_bin_width = np.arange(min(data), max(data), bin_step)
            num_of_bin = math.floor(range / bin_step)
        
            counts, centers = np.histogram(data, bins=range_bin_width)
            bin_width.append(centers[1] - centers[0])
            bin_width_compare.append(bin_step)
        
            diff_of_subseq_counts = [(abs(counts[c] - counts[c-1])) for c in np.arange(1, len(counts), 1)]
            cost.append((max(diff_of_subseq_counts)) / bin_step)
    except ValueError:
        for resolution in res_array:
            bin_width, bin_width_count, diff_sub_count, diff_of_subseq_counts = [], [], [], []
            bin_step = 0.001 * resolution
            range_bin_width = np.arange(min(data), max(data), bin_step)
            num_of_bin = math.floor(range / bin_step)
        
            counts, centers = np.histogram(data, bins=range_bin_width)
            bin_width.append(centers[1] - centers[0])
            bin_width_compare.append(bin_step)
        
            diff_of_subseq_counts = [(abs(counts[c] - counts[c-1])) for c in np.arange(1, len(counts), 1)]
            cost.append((max(diff_of_subseq_counts)) / bin_step)
    assert isinstance(cost, object)
    idx = cost.index(min(cost))
    optimal_bin_width = bin_width_compare[idx]
    assert isinstance(optimal_bin_width, object)
    bin_array_optimal = np.arange(min(data), max(data), optimal_bin_width)
    bin_counts_optimal, bin_centers_optimal = np.histogram(data, bin_array_optimal)
    num_bins_optimal = len(bin_centers_optimal)
    
    return (num_bins_optimal, optimal_bin_width, bin_array_optimal, bin_counts_optimal)

def auto_opt_bin_per_dim(X, start=0.01, end=0.1, step=0.005, quant_bin_per=1.0):
    assert quant_bin_per > 0.0 and quant_bin_per <= 1.0, "ERR | quant bin sel not valid"
    res_array = np.arange(start, end, step)
    bin_opt_num_of_bin_list = []
    bin_arrays_list = []
    bin_counts_avg_list = []
    for dimension in range(X.shape[1]):
        data = X[:, dimension]
        optimal_bin_info = auto_opt_bin(data, res_array)
        optimal_num_of_bin = optimal_bin_info[0]
        optimal_bin_width = optimal_bin_info[1]
        bin_array_optimal = optimal_bin_info[2]
        bin_counts_optimal = optimal_bin_info[3]
        
        bin_counts_avg = np.zeros(len(bin_counts_optimal)+1)
        for i in range(len(bin_counts_optimal)+1):
            if i == 0:
                bin_counts_avg[i] = bin_counts_optimal[i]/2
            elif i == len(bin_counts_optimal):
                bin_counts_avg[i] = bin_counts_optimal[i-1]/2
            else:
                bin_counts_avg[i] = (bin_counts_optimal[i-1] + bin_counts_optimal[i]) / 2
        bin_opt_num_of_bin_list.append(optimal_num_of_bin)
        bin_counts_avg_list.append(bin_counts_avg)
        
        inverse_bin_counts_avg = np.negative(bin_counts_avg)
        bin_dimension = -math.ceil(len(inverse_bin_counts_avg) * quant_bin_per)
        select_idx = np.argpartition(inverse_bin_counts_avg, bin_dimension)[bin_dimension:]
        bin_array_optimal = bin_array_optimal[np.sort(select_idx)]
        
        bin_arrays_list.append(bin_array_optimal)
    return [bin_opt_num_of_bin_list, bin_arrays_list, bin_counts_avg_list]

def sturge_function(data, number_of_data_points):
    num_bins = int(1+np.log2(number_of_data_points))
    bin_select_points = []
    bins, bin_edges = np.histogram(data, bins=num_bins)
    for idx in range(1, len(bin_edges)):
        bin_edge_prev, bin_edge_curr = bin_edges[idx-1], bin_edges[idx]
        bin_edge_select = (bin_edge_prev + bin_edge_curr) / 2
        bin_select_points.append(bin_edge_select)
    return num_bins, np.array(bin_select_points), np.array(bins)

def sturge_per_dim(X):
    num_bins, bin_selections, bin_count_data = [], [], []
    for dim in range(X.shape[1]):
        data_x = X[:,dim]
        bin_num, bin_select_points, bin_counts = sturge_function(data_x, len(data_x))
        num_bins.append(bin_num)
        bin_selections.append(bin_select_points)
        bin_count_data.append(bin_counts)
    return num_bins, bin_selections, bin_count_data

def transform_hist_bins_to_pk(bins):
    sum_hist = sum(bins)
    return np.array([(count/sum_hist) for count in bins])

def proposed_func(data):
    num_bins_fdr = 10 ** 6
    bin_fdr, bin_edges_fdr = np.histogram(data, bins=num_bins_fdr)
    pk = transform_hist_bins_to_pk(bin_fdr)
    H = entropy(pk, base=2)
    bin_num_proposed = math.ceil(H) + 1
    bins, bin_edges = np.histogram(data, bins=bin_num_proposed)
    bin_select_points = []
    for idx in range(1, len(bin_edges)):
        bin_edge_prev, bin_edge_curr = bin_edges[idx-1], bin_edges[idx]
        bin_edge_select = (bin_edge_prev + bin_edge_curr) / 2
        bin_select_points.append(bin_edge_select)
    return bin_num_proposed, np.array([bin_select_points]), np.array(bins)

def proposed_per_dim(X):
    num_bins, bin_selections, bin_count_data = [], [], []
    for dim in range(X.shape[1]):
        data_x = X[:,dim]
        bin_num, bin_select_points, bin_counts = proposed_func(data_x)
        num_bins.append(bin_num)
        bin_selections.append(bin_select_points)
        bin_count_data.append(bin_counts)
    return num_bins, bin_selections, bin_count_data

def freedman_diaconis_function(data, num_points):
    q_75, q_25 = np.percentile(data, [75, 25])
    IQR = q_75 - q_25
    bin_width = 2*IQR*np.power(len(data), -1/3)
    bin_select_points = []
    try:
        num_bins = abs(int((max(data) - min(data)) / bin_width))
    except OverflowError:
        bin_width = 2*0.001*np.power(len(data), -1/3)
        num_bins = abs(int((max(data) - min(data)) / bin_width))
    print(num_bins)
    bins, bin_edges = np.histogram(data, bins=num_bins)
    for idx in range(1, len(bin_edges)):
        edge_prev, edge_curr = bin_edges[idx-1], bin_edges[idx]
        bin_select = (edge_prev + edge_curr) / 2
        bin_select_points.append(bin_select)
    return num_bins, np.array(bin_select_points), np.array(bins)

def freedman_diaconis_per_dim(X):
    num_bins, bin_selections, bin_count_data = [], [], []
    for dim in range(X.shape[1]):
        data_x = X[:,dim]
        bin_num, bin_select_points, bin_counts = freedman_diaconis_function(data_x, len(data_x))
        num_bins.append(bin_num)
        bin_selections.append(bin_select_points)
        bin_count_data.append(bin_counts)
    return num_bins, bin_selections, bin_count_data

def general_dic(data, ndp):
    bins, bin_edges = np.histogram(data, bins=ndp)
    bin_select_points = []
    for idx in range(1, len(bin_edges)):
        bin_edge_prev, bin_edge_curr = bin_edges[idx-1], bin_edges[idx]
        bin_edge_sel = (bin_edge_prev + bin_edge_curr) / 2
        bin_select_points.append(bin_edge_sel)
    return np.array([bin_select_points]), np.array(bins)

def general_disc_per_dim(X, ndp):
    num_bins, bin_selections, bin_count_data = [], [], []
    for dim in range(X.shape[1]):
        data_x = X[:,dim]
        bin_select_points, bin_counts = general_dic(data_x, ndp)
        num_bins.append(ndp)
        bin_selections.append(bin_select_points)
        bin_count_data.append(bin_counts)
    return num_bins, bin_selections, bin_count_data

class tree_node(object):
    def __init__(self, 
                curr_depth=None, feature_val=None, feature_decision=None, 
                id=LEAF, left=None, right=None, node_size=None):
        self.curr_depth = curr_depth
        self.SIZE = node_size
        self.feature_val = feature_val
        self.feature_decision = feature_decision
        self.right = right
        self.left = left
        self.id = id
            
    def _children_factor(self):
        children = []
        if self.right is not None: 
            children.append(self.right)
        if self.left is not None:
            children.append(self.left)
        return children
        
class base_regression_tree():
    def __init__(self, 
                max_features=None, splitter=None, random_state=None,
                max_depth=None, min_samples_for_split=2,
                dimension_training=None, dimension_info=None,
                bin_num_list=None, bin_arrays=None, bin_counts=None):
        self.splitter = splitter if splitter in SUPP_SPLITS else None
        assert self.splitter is not None, f"Split value ({splitter}), not supported \
                                            Supported split types | {SUPP_SPLITS}"
        self.max_depth = max_depth
        self.max_features = max_features
        self.min_samples_for_split = min_samples_for_split
        self.dim = dimension_training
        self.bin_number_list = bin_num_list
        self.bin_array = bin_arrays
        self.bin_count = bin_counts
        self.tree = None
        self.median_std, self.std_factor = None, None
        
    def traverse_and_print_the_tree(self, root):
        tab_spacer = root.curr_depth * ' '
        print(f"{tab_spacer}CURR DEPTH | {root.curr_depth}")
        print(f"{tab_spacer}Decide Feat | {root.feature_decision}")
        print(f"{tab_spacer}Decide Val | {root.feature_val}")
        print(f"{tab_spacer}Node ID | {root.id}")
        root = root._children_factor()
        assert len(root.children) < 3, "Children, too many!!!"
        if len(root.children) > 0:
            for root_i in root.children:
                    self.traverse_and_print_the_tree(root_i)
        
    def get_depths_of_tree(self, root, depth_list):
        root_childs = root._children_factor()
        assert len(root_childs) < 3, f"Children, Too Many!! | {root.children}"
        if len(root_childs) > 0:
            for root_i in root_childs:
                self.get_depths_of_tree(root_i, depth_list)
        else:
            depth_list.append(root.curr_depth)
        return depth_list
        
    def get_total_nodes(self, root, node_count, leaf_count, memory_bytes, ratio):
        root_childs = root._children_factor()
        assert len(root_childs) < 3, f"Children, Too Many!! | {root.children}"
        if ratio < 0.5:
            #root ID
            memory_bytes += 2
            # SIZE factor
            memory_bytes += 2
            # feature
            memory_bytes += 2
        else:
            # root ID is boolean - 2 bytes
            memory_bytes += 2
            # SIZE factor at node, int, 4 bytes
            memory_bytes += 4
            # feature which can be referred to as int - 4 bytes
            memory_bytes += 4
        # split point - float - 8 bytes
        memory_bytes += (8*ratio)
        # pointer to node, 8 bytes
        memory_bytes += (8*ratio)
        if len(root_childs) > 0:
            node_count += 1
            for root_i in root_childs:
                node_count, leaf_count, memory_bytes = self.get_total_nodes(root_i, node_count, leaf_count, memory_bytes, ratio)
        else:
            leaf_count += 1
        return node_count, leaf_count, memory_bytes
        
    def compute_spatial_metrics(self, ratio):
        list_of_leaf_depths = self.get_depths_of_tree(self.tree, [])
        node_count, leaf_count, memory_bytes = self.get_total_nodes(self.tree, 0, 0, 0, ratio)
        total_nodes = leaf_count + node_count
        avg_depth = np.average(list_of_leaf_depths)
        return avg_depth, leaf_count, total_nodes, node_count, memory_bytes
        
    def compute_std_depth(self):
        list_of_leaf_depths = self.get_depths_of_tree(self.tree, [])
        std_depth = np.std(list_of_leaf_depths)
        return std_depth
        
    def get_depth(self, sample, node, depth):
        if node.id is LEAF:
            if node.SIZE <= 1:
                return depth
            else:
                return depth + c_n(node.SIZE)
        else:
            sample_val = sample[node.feature_decision]
            if sample_val < node.feature_val:
                return self.get_depth(sample, node.left, depth+1)
            else:
                return self.get_depth(sample, node.right, depth+1)

    def predict(self, sample):
        return self.get_depth(sample, self.tree, 0) 

    def grow_the_tree(self, cd, depth, X, bin_array, grow=None):
        feat_idx = random.choice(np.arange(X.shape[1]))
        random.seed(None)
        if grow is RANDOM:
            if (cd >= depth) or (len(X) <= 1):
                return tree_node(curr_depth=cd, node_size=X.shape[0])
            else:
                first = X.min(axis=0)
                prob = random.uniform(0, 1)
                second = X.max(axis=0) * prob
                third = -1 * X.min(axis=0)
                third = third * prob
                split_val = first + second + third
                split_val = split_val[feat_idx]
                f_dec, f_val = feat_idx, split_val
                left_X, right_X = X[X[:, feat_idx] < split_val], X[X[:, feat_idx] >= split_val]

                return tree_node(curr_depth=cd+1,
                        feature_val=f_val,
                        feature_decision=f_dec,
                        id=NODE,
                        left=self.grow_the_tree(cd+1, depth, left_X, bin_array, grow),
                        right=self.grow_the_tree(cd+1, depth, right_X, bin_array, grow))

        elif grow in SUPP_QUANT:
            if (cd >= depth) or (len(X) <= 1):
                return tree_node(curr_depth=cd, node_size=X.shape[0])
            trunc_bin_arr = bin_array[feat_idx][(bin_array[feat_idx]<=X.max(axis=0)[feat_idx]) & (bin_array[feat_idx]>=X.min(axis=0)[feat_idx])]
            if (trunc_bin_arr.size <= 0):
                return tree_node(curr_depth=cd, node_size=X.shape[0])
            else:
                split_val = trunc_bin_arr[random.randint(0, len(trunc_bin_arr)-1)]
                f_dec, f_val = feat_idx, split_val
                left_X, right_X = X[X[:, feat_idx] < split_val], X[X[:, feat_idx] >= split_val]
                return tree_node(curr_depth=cd+1,
                        feature_val=f_val,
                        feature_decision=f_dec,
                        id=NODE,
                        left=self.grow_the_tree(cd+1, depth, left_X, bin_array, grow),
                        right=self.grow_the_tree(cd+1, depth, right_X, bin_array, grow))
        else:
            assert False
    
    def preprocess_leaf_factor(self):
        list_of_leaf_depths = self.get_depths_of_tree(self.tree, [])
        self._middle_perc = np.percentile(list_of_leaf_depths, 50.0)
        self._std = np.std(list_of_leaf_depths)
        self._linear_est_std_slope = -1.0 / self._std
        self._linear_est_offset = self._middle_perc / self._std
        return self
    
    def fit(self, X, y, sample, idx):
        X_idx = random.sample(range(len(X)), sample)
        X_sample = X[X_idx]
        self.tree = self.grow_the_tree(0, self.max_depth, X_sample, self.bin_array, grow=self.splitter)
        return self
        
class i_forest(BaseBagging):
    def __init__(self, 
                n_estimators=100,   max_samples="auto",     max_features=1.0,
                random_state=None,  type_itree=False,   training_set=None,
                sub_samp_size=256,  grow_full_tree=False, 
                quant_bin_sel=0.8, ndp=0):
        assert sub_samp_size is not None, "Sampling size is not declared"
        assert type_itree in SUPP_SPLITS, "iTree Type not supported"
        assert training_set is not None, "Training data must be passed @ initialization"
        if type_itree is GEN:
            assert ndp>1, "{ndp} must be greater than 1 for GEN DiTree"
        # ARGS FOR Estimation Tree Regressor LIST
        self.split = type_itree
        self.max_features = max_features
        self.max_samples = max_samples
        self.random_state = random_state
        self.n_estimators = n_estimators
        self.max_depth=None
        self.sub_sample_size = sub_samp_size
        self.full_grow=grow_full_tree
        
        # For prediction/Modeling
        self.anomaly_th = None
        self.estimators = []
        self.estimator_features = []
        
        if self.split in SUPP_QUANT:
            assert training_set is not None, "Quantized IF needs training set passed in @ init."
            self.dimension, dim_info = training_set.shape[1], dict()
            for dim in range(self.dimension):
                median = np.median(training_set[:, dim])
                std = np.std(training_set[:, dim])
                dim_info[dim] = [median, std]
            self.dimension_info = dim_info
            if self.split is QUANT:
                bin_info = auto_opt_bin_per_dim(training_set, quant_bin_per=quant_bin_sel)
            elif self.split is STURGE:
                bin_info = sturge_per_dim(training_set)
            elif self.split is FREEDMAN:
                bin_info = freedman_diaconis_per_dim(training_set)
            elif self.split is PROP:
                bin_info = proposed_per_dim(training_set)
            elif self.split is GEN:
                bin_info = general_disc_per_dim(training_set, ndp)
            self.bin_num_list = bin_info[0]
            self.bin_arrays = bin_info[1]
            self.bin_counts = bin_info[2]
            
        else:
            self.dimension = training_set.shape[1]
            self.dimension_info = None
            self.bin_num_list = None
            self.bin_counts = None
            self.bin_arrays = None
            
    def _set_oob_score(self):
        raise NotImplementedError("Not implemented yet")

    def validate_data(self, X):
        return self._validate_data(X, accept_sparse=["csr"], dtype=tree_dtype)

    def get_max_depth_and_out_shape(self, X):
        if issparse(X):
            X.sort_indices()
        y = check_random_state(self.random_state).uniform(size=X.shape[0])
        max_depth = int(np.ceil(np.log2(max(self.sub_sample_size, 2))))
        max_depth = max_depth if self.full_grow is False else self.sub_sample_size - 1
        self.max_depth = max_depth
        return max_depth, y
        
    def apply_params_to_est(self, X):
        X = self.validate_data(X)
        md, y = self.get_max_depth_and_out_shape(X)
        estimators = self.get_tree_regr(X, 
                                    self.max_features, 
                                    self.random_state, 
                                    self.n_estimators,
                                    max_depth=md)
        return estimators, y
    
    def get_tree_regr(self, X, m_s, random_state, n_estimators, max_depth=None):
        etr_list = [base_regression_tree(max_features=m_s, 
                        splitter=self.split,
                        max_depth=max_depth,
                        dimension_training=self.dimension,
                        dimension_info=self.dimension_info,
                        bin_num_list=self.bin_num_list,
                        bin_arrays=self.bin_arrays,
                        bin_counts=self.bin_counts) 
        for tree in range(n_estimators)]
        return etr_list

    def fit(self, X):
        self.num_of_samples = len(X)
        self.estimators, y = self.apply_params_to_est(X)
        self.estimator_features = [np.array([feature for feature in range(X.shape[1])]) for est in range(self.n_estimators)]
        self.estimators = [tree_est.fit(X, y, self.sub_sample_size, idx) for idx, tree_est in enumerate(self.estimators)]
        return self
    
    def get_quant_bin_size(self):
        if self.split is QUANT:
            quant_lengths = [len(dim) for dim in self.bin_arrays]
            avg = np.average(quant_lengths)
            std = np.std(quant_lengths)
            var = std / avg
            return avg, var
        else:
            return 0, 0
        
    def set_anomaly_threshold(self, anomaly):
        '''
        Note the following and that s is the anomaly threshold:
            if s is close to 1  -> definite anomaly
            if s is @ 0.5       -> entire sample does not have any distinct anomaly
            if s is close to 0  -> safe, normal instance
        '''
        assert (anomaly > 0) and (anomaly < 1), f"anomaly threshold {anomaly} not in valid range, e.g. 0 <= s <= 1"
        self.anomaly_th = anomaly
        return self
    
    def set_leaf_factor(self):
        self.estimators = [tree_est.preprocess_leaf_factor() for tree_est in self.estimators]
        self._std_factor = np.average([tree_est._std for tree_est in self.estimators])
        return self
        
    def compute_score(self, X):
        tree_depth_scores = [tree.predict(X) for tree in self.estimators]
        tree_depth_ave = np.average(tree_depth_scores)
        score = 2 ** (-1.0 * (tree_depth_ave / c_n(self.sub_sample_size)))
        return score

    def gen_score_matrix(self, X):
        score = [self.compute_score(entry) for entry in X]
        return np.array(score)

    def get_spatial_metrics(self, bits):
        ratio = bits / 64
        depth_ave, leaf_ave, split_node_ave, total_node_ave, memory_bytes_total = [], [], [], [], 0
        for tree in self.estimators:
            ave_depth, num_leaves, total_nodes, num_split_node, memory_bytes = tree.compute_spatial_metrics(ratio)
            depth_ave.append(ave_depth)
            leaf_ave.append(num_leaves)
            split_node_ave.append(num_split_node)
            total_node_ave.append(total_nodes)
            memory_bytes_total += memory_bytes
        ave_depth_tree = np.average(depth_ave)
        ave_leaf_tree = np.average(leaf_ave)
        ave_split_node = np.average(split_node_ave)
        ave_tree_size = np.average(total_node_ave)
        return ave_depth_tree, ave_leaf_tree, ave_split_node, ave_tree_size, memory_bytes_total
    
    def predict(self, X, raw=False):
        check_is_fitted(self)
        assert self.anomaly_th is not None, "Anomaly threshold was never set"
        score_matrix = self.gen_score_matrix(X)
        is_nom = np.ones_like(score_matrix, dtype=int)
        is_nom[score_matrix > self.anomaly_th] = -1
        return is_nom, score_matrix
