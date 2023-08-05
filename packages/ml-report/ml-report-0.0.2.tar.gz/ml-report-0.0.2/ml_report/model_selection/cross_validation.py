import numpy as np
from collections import deque
from typing import Iterable, Union
from sklearn.model_selection import BaseCrossValidator

class BaseSplitter(object):


class FeatureStratifiedSplitter(BaseSplitter):
    def __init__(self, features:Union[str, Iterable[str]], df, dv, feature, n_splits, sorted=True, seed=0):
        self.features = features
        self.n_splits = n_splits
        self.seed = seed

    def get_n_splits(self, X=None, y=None, groups=None):

    def split(self, X, y=None, groups=None):
        np.random.seed(self.seed)
        splits = deque([] for _ in range(n_splits))
        for _, gb in df.groupby(feature):
            if sorted:
                gb = gb.sort_values(dv)
            else:
                gb = gb.sample(frac=1)
            indices = list(pd.Series(gb.index))
            while indices:
                index = indices.pop()
                # Add index to leftmost split.
                splits[0].append(index)
                # Rotate splits in split list.
                splits.append(splits.popleft())
        return [([index for s in splits for index in s if s != split], split) for split in splits]


