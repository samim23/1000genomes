#!/usr/bin/env python

from __future__ import division
import numpy as np
import scipy
import sys
from sklearn.base import BaseEstimator, TransformerMixin
from nolearn.dbn import DBN
from sklearn.cross_validation import *
from sklearn.decomposition import *
from sklearn.ensemble import *
from sklearn.externals import joblib
from sklearn.feature_selection import *
from sklearn.linear_model import *
from sklearn.neighbors import *
from sklearn.pipeline import *
from sklearn.preprocessing import *
from sklearn.random_projection import *
from sklearn.svm import *
from sklearn.tree import *
from sklearn import metrics
from utils import *
np.random.seed(42)

if len(sys.argv) == 1:
  print "No chromosomes specified"
  sys.exit(1)

class Transformer(BaseEstimator, TransformerMixin):
    def __init__(self, fn):
        self.fn = fn

    def fit(self, X, y):
        return self

    def transform(self, X):
        return self.fn(X)

def load(L):
  return scipy.sparse.hstack([load_sparse_matrix(x) for x in L])

def classify(X, target):
    Y = joblib.load('blobs/Y%s.pkl' % target)
    print X.shape
    print Y.shape
    sys.stdout.flush()

    le = LabelEncoder()
    Y = le.fit_transform(Y)
    #joblib.dump(le, 'blobs/le%s.pkl' % target)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
    #joblib.dump(Y_train, 'blobs/Y_train%s.pkl' % target)
    #joblib.dump(Y_test, 'blobs/Y_test%s.pkl' % target)

    clf = Pipeline([
      ('s', SparseRandomProjection()),
      ('c', LinearSVC())
    ])
    clf.fit(X_train, Y_train)
    pred = clf.predict(X_test)
    print metrics.f1_score(Y_test, pred)

    joblib.dump(clf.decision_function(X_train), 'blobs/X_train_meta_rand_%s%s.pkl' % (sys.argv[1], target))
    joblib.dump(clf.decision_function(X_test), 'blobs/X_test_meta_rand_%s%s.pkl' % (sys.argv[1], target))

def main():
    chromosomes = [int(x) for x in sys.argv[1].split(',')]
    print "Chromosomes: ", chromosomes
    sys.stdout.flush()

    X = load(["X_%d" % c for c in chromosomes])
    #classify(X, '_superpop')
    classify(X, '')

if __name__ == '__main__':
    main()
