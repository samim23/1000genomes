import numpy as np
import cPickle
from scipy import sparse
import sys

CHR_NUM = sys.argv[1]
print CHR_NUM
FILE_NAME = 'ALL.chr%s.phase3_shapeit2_mvncall_integrated_v5.20130502.genotypes.vcf' % CHR_NUM
NUM_SAMPLES = 2504

def nnz(s):
    A = s[0]
    B = s[2]
    if A == '0' and B == '0':
        return 0
    elif A == '0' and B != '0':
        return 1
    elif A != '0' and B == '0':
        return 1
    else:
        return 2

idx = 0
X = []
f = open(FILE_NAME)
for line in f:
    if line[0] == '#':
        continue
    if idx % 10000 == 0:
        print idx
    line = line.split('\t')[9:]
    row = [nnz(x) for x in line]
    X.append(row)
    idx += 1
X = sparse.csr_matrix(np.array(X).T)
print X.shape
cPickle.dump(X, open('blobs/X_%s.pkl' % CHR_NUM, 'wb'))
