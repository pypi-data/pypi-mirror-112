# contains functions that run the greedy detector for dense regions in a sparse matrix.
# use aveDegree or sqrtWeightedAveDegree or logWeightedAveDegree on a sparse matrix,
# which returns ((rowSet, colSet), score) for the most suspicious block.


import time
import math
import numpy as np
import random
from scipy import sparse
import sys, copy, os

from ..global_context import *
from ..utils.collection import MinTree
from ..utils.utils import get_abspath

class FraudarAnalyzer():
    '''
    Usage:
        from easygraphs.graph_analyzer.fraudar_analyzer import FraudarAnalyzer
        fa = FraudarAnalyzer(gl)
        bestRowSet, bestColSet, bestAveScore = fa.run()
        gc.collect()
    '''
    def __init__(self, graphloader):
        self.graphloader = graphloader

        self.dir_output = self.graphloader.dir_output + "FraudarAnalyzer/"
        if not os.path.exists(self.dir_output):
            os.makedirs(self.dir_output)

    def run(self, *args, **kwargs):
        return self.run_algorithm(self.graphloader.data(), self.graphloader.netname, self.dir_output, *args, **kwargs)

    @classmethod
    def get_rowset_savepath(cls, netname, dir_output, t=1):
        return "%s%s_%s.rows" % (dir_output, netname, t)

    @classmethod
    def get_colset_savepath(cls, netname, dir_output, t=1):
        return "%s%s_%s.cols" % (dir_output, netname, t)

    @classmethod
    def run_algorithm(cls, edges, netname, dir_output, algorithm_args=None, inject_args=None, k=1):
        start_time = time.time()
        src, dst, val = edges.data()
        if inject_args is not None:
            src, dst = cls.inject_block(src, dst, inject_args)

        M = cls.to_csr(src, dst)
    
        print(("finished reading data: shape = %d, %d @ %d" % (M.shape[0], M.shape[1], time.time() - start_time)))

        # if len(sys.argv) > 3: # node suspiciousness present
        # 	print("using node suspiciousness")
        # 	rowSusp = np.loadtxt("%s.rows" % (sys.argv[3], ))
        # 	colSusp = np.loadtxt("%s.cols" % (sys.argv[3], ))
        # 	lwRes = logWeightedAveDegree(M, (rowSusp, colSusp))
        # else:

        
        Mcur = M.copy().tolil()
        res = []
        weightFunc = cls.logDegree
        detectFunc = cls.fastGreedyDecreasingHomo
        while (t < k):
            W, colWeights = weightFunc(Mcur)
            list_row, list_col, score = detectFunc(W, colWeights)
            print("Fraudar iter %s finished." % t)
            res.append((list_row, list_col, score))
            
            t +=1

            if (t >= k):
                break

            ## only delete inner connections
            (rs, cs) = Mcur.nonzero() # (u, v)
            rowSet = set(list_row)
            colSet = set(list_col)
            for i in range(len(rs)):
                if rs[i] in rowSet and cs[i] in colSet:
                    Mcur[rs[i], cs[i]] = 0

            ## delete nodes
            # diag = scipy.sparse.eye(Mcur.shape[0]).tolil()
            # for r in list_row:
            #     diag[r, r] = 0
            # diag = diag.tocsr()
            # Mcur = diag.dot(Mcur)

            # diag = scipy.sparse.eye(Mcur.shape[1]).tolil()
            # for c in list_col:
            #     diag[c, c] = 0
            # diag = diag.tocsr()
            # Mcur = Mcur.dot(diag)

            np.savetxt(cls.get_rowset_savepath(netname, dir_output, t), np.array(list(list_row)), fmt='%d')
            np.savetxt(cls.get_colset_savepath(netname, dir_output, t), np.array(list(list_col)), fmt='%d')
            print("In cluster%s, score obtained is %f" % (t, score))
        print("done @ %f" % (time.time() - start_time))
        return res


    # reads matrix from file and returns sparse matrix. first 2 columns should be row and column indices of ones.
    # @profile
    @classmethod
    def inject_block(cls, src, dst, inject_args = None):
        from ..utils.graph_generator import inject_block, generate_dense_graph, generate_bipartite_graph
        n_nodes = max(src) + 1
        n_inject, p = inject_args
        given_node_ids = list(range(n_nodes, n_nodes+n_inject))
        list_src, list_dst = generate_dense_graph(n_inject, p, given_node_ids)

        # target_ids = list(range(n_nodes+n_inject, n_nodes+n_inject+5))
        # list_src, list_dst = generate_bipartite_graph(given_node_ids, target_ids, p)
        src.extend(list_src)
        dst.extend(list_dst)

        return src, dst

    @classmethod
    def to_csr(cls, src, dst):
        m = max(src) + 1
        n = max(dst) + 1
        M = sparse.coo_matrix(([1]*len(src), (src, dst)), shape=(m, n))
        M1 = M > 0
        return M1.astype('int')


    # inject a clique of size m0 by n0, with density pp. the last parameter testIdx determines the camouflage type.
    # testIdx = 1: random camouflage, with camouflage density set so each fraudster outputs approximately equal number of fraudulent and camouflage edges
    # testIdx = 2: random camouflage, with double the density as in the previous setting
    # testIdx = 3: biased camouflage, more likely to add camouflage to high degree columns
    @classmethod
    def injectCliqueCamo(cls, M, m0, n0, p, testIdx):
        (m,n) = M.shape
        M2 = M.copy().tolil()

        colSum = np.squeeze(M2.sum(axis = 0).A)
        colSumPart = colSum[n0:n]
        colSumPartPro = np.int_(colSumPart)
        colIdx = np.arange(n0, n, 1)
        population = np.repeat(colIdx, colSumPartPro, axis = 0)

        for i in range(m0):
            # inject clique
            for j in range(n0):
                if random.random() < p:
                    M2[i,j] = 1
            # inject camo
            if testIdx == 1:
                thres = p * n0 / (n - n0)
                for j in range(n0, n):
                    if random.random() < thres:
                        M2[i,j] = 1
            if testIdx == 2:
                thres = 2 * p * n0 / (n - n0)
                for j in range(n0, n):
                    if random.random() < thres:
                        M2[i,j] = 1
            # biased camo
            if testIdx == 3:
                colRplmt = random.sample(population, int(n0 * p))
                M2[i,colRplmt] = 1

        return M2.tocsc()

    # sum of weighted edges in rowSet and colSet, plus node suspiciousness values, in matrix M
    @classmethod
    def c2Score(cls, M, rowSet, colSet, nodeSusp = None):
        suspTotal = 0
        if nodeSusp:
            suspTotal = nodeSusp[0][list(rowSet)].sum() + nodeSusp[1][list(colSet)].sum()
        return M[list(rowSet),:][:,list(colSet)].sum(axis=None) + suspTotal


    # run greedy algorithm using square root column weights
    @classmethod
    def sqrtDegree(cls, M):
        (m, n) = M.shape
        colSums = M.sum(axis=0)
        colWeights = 1.0 / np.sqrt(np.squeeze(colSums) + 5)
        colDiag = sparse.lil_matrix((n, n))
        colDiag.setdiag(colWeights)
        W = M * colDiag
        return W, colWeights

    # run greedy algorithm using logarithmic weights
    @classmethod
    def logDegree(cls, M):
        (m, n) = M.shape
        colSums = M.sum(axis=0)
        colWeights = np.squeeze(np.array(1.0 / np.log(np.squeeze(colSums) + 5)))
        colDiag = sparse.lil_matrix((n, n))
        colDiag.setdiag(colWeights)
        W = M * colDiag
        print("finished computing weight matrix")
        return W, colWeights

    @classmethod
    def Degree(cls, M):
        # For each edge u-v, weight is 1/d(v)
        (m, n) = M.shape
        colSums = M.sum(axis=0)
        colWeights = np.squeeze(np.array(1.0 / (np.squeeze(colSums) + 1e-9)))
        colDiag = sparse.lil_matrix((n, n))
        colDiag.setdiag(colWeights)
        W = M * colDiag
        return W, colWeights

    @classmethod
    def One(self, M):
        # For each edge u-v, weight is 1/d(v)
        (m, n) = M.shape
        colSums = M.sum(axis=0)
        colWeights = np.ones(n)
        colDiag = sparse.lil_matrix((n, n))
        colDiag.setdiag(colWeights)
        W = M * colDiag
        return W, colWeights

    @classmethod
    def subsetAboveDegree(self, M, col_thres, row_thres):
        M = M.tocsc()
        (m, n) = M.shape
        colSums = np.squeeze(np.array(M.sum(axis=0)))
        rowSums = np.squeeze(np.array(M.sum(axis=1)))
        colValid = colSums > col_thres
        rowValid = rowSums > row_thres
        M1 = M[:, colValid].tocsr()
        M2 = M1[rowValid, :]
        rowFilter = [i for i in range(m) if rowValid[i]]
        colFilter = [i for i in range(n) if colValid[i]]
        return M2, rowFilter, colFilter

    @classmethod
    def fastGreedyDecreasing(cls, M, colWeights):
        (m, n) = M.shape
        Md = M.todok()
        Ml = M.tolil()
        Mlt = M.transpose().tolil()
        rowSet = set(range(0, m))
        colSet = set(range(0, n))
        curScore = c2Score(M, rowSet, colSet)
        print("cur_total", curScore)

        bestAveScore = curScore / (len(rowSet) + len(colSet))
        
        print("finished setting up greedy")
        rowDeltas = np.squeeze(M.sum(axis=1).A) # *decrease* in total weight when *removing* this row
        colDeltas = np.squeeze(M.sum(axis=0).A)
        print("delta row", rowDeltas)
        print("delta col", colDeltas)
        print("finished setting deltas")
        rowTree = MinTree(rowDeltas)
        colTree = MinTree(colDeltas)
        print("finished building min trees")

        numDeleted = 0
        deleted = []
        bestNumDeleted = 0

        while rowSet and colSet:
            if (len(colSet) + len(rowSet)) % 100000 == 0:
                print("current set size = ", len(colSet) + len(rowSet))
            (nextRow, rowDelt) = rowTree.getMin()
            (nextCol, colDelt) = colTree.getMin()
            if rowDelt <= colDelt:
                print("delete row", nextRow)
                curScore -= rowDelt
                for j in Ml.rows[nextRow]:
                    delt = colWeights[j]
                    colTree.changeVal(j, -colWeights[j])
                rowSet -= {nextRow}
                rowTree.changeVal(nextRow, float('inf'))
                deleted.append((0, nextRow))
            else:
                print("delete col", nextCol)
                curScore -= colDelt
                for i in Mlt.rows[nextCol]:
                    delt = colWeights[nextCol]
                    rowTree.changeVal(i, -colWeights[nextCol])
                colSet -= {nextCol}
                colTree.changeVal(nextCol, float('inf'))
                deleted.append((1, nextCol))

            numDeleted += 1
            curAveScore = curScore / (len(colSet) + len(rowSet))

            print("cur_total", curScore)
            # print("set", rowSet)
            print("size", len(colSet), len(rowSet))
            print("cur", curAveScore)
            print("best", bestAveScore)

            if curAveScore > bestAveScore:
                bestAveScore = curAveScore
                bestNumDeleted = numDeleted

        # reconstruct the best row and column sets
        finalRowSet = set(range(m))
        finalColSet = set(range(n))
        for i in range(bestNumDeleted):
            if deleted[i][0] == 0:
                finalRowSet.remove(deleted[i][1])
            else:
                finalColSet.remove(deleted[i][1])
        return finalRowSet, finalColSet, bestAveScore

    @classmethod
    def fastGreedyDecreasingHomo(cls, M, colWeights, nodeSusp=None):
        '''
        Args: 
		
        Returns: 
            bestRowSet: The rank of nodes are meaningful. The latest node is most suspisious in some extent.
            bestColSet, bestAveScore
        '''
        # print("m", M)
        # print("weight", colWeights)

        (m, n) = M.shape
        if nodeSusp is None:
            nodeSusp = (np.zeros(m), np.zeros(n))
        Md = M.todok()
        Ml = M.tolil()
        Mlt = M.transpose().tolil()
        
        rowSet = set(range(0, m))
        colSet = set(range(0, n))

        curScore = cls.c2Score(M, rowSet, colSet, nodeSusp)
        bestAveScore = curScore / len(rowSet)

        print("finished initialization")
        rowDeltas = np.squeeze(M.sum(axis=1).A) + nodeSusp[0] # contribution of this row to total weight, i.e. *decrease* in total weight when *removing* this row
        colDeltas = np.squeeze(M.sum(axis=0).A) + nodeSusp[1]
        print("delta row", rowDeltas)
        print("delta col", colDeltas)

        print("finished setting deltas")
        rowTree = MinTree(rowDeltas)
        colTree = MinTree(colDeltas)
        print("finished building min trees")

        numDeleted = 0
        deleted = set()
        list_deleted = []
        bestNumDeleted = 0
        print("cur_total", curScore)
        print("cur_avg", bestAveScore)

        while rowSet and colSet:
            if len(colSet) % 100000 == 0:
                print("current set size = %d" % len(rowSet))
            (nextRow, rowDelt) = rowTree.getMin()
            (nextCol, colDelt) = colTree.getMin()
            # print("row", nextRow, rowDelt)
            # print("col", nextCol, colDelt)

            if rowDelt <= colDelt:
                # print("delete row", nextRow)
                curScore -= rowTree.getVal(nextRow)
                # print("rowDeltas", rowTree.getVal(nextRow))
                curScore -= colTree.getVal(nextRow)
                # print("colDeltas", colTree.getVal(nextRow))

                for j in Ml.rows[nextRow]:
                    if j in deleted:
                        continue
                    colTree.changeVal(j, -colWeights[j])
                    # print("change value:", j, -colWeights[j])
                rowSet -= {nextRow}
                rowTree.changeVal(nextRow, float('inf'))

                
                for i in Mlt.rows[nextRow]:
                    if i in deleted:
                        continue
                    rowTree.changeVal(i, -colWeights[nextRow])
                    # print("change value:", i, -colWeights[nextRow])
                colSet -= {nextRow}
                colTree.changeVal(nextRow, float('inf'))

                list_deleted.append(nextRow)
                deleted.add(nextRow)
            else:
                # print("delete col", nextCol)
                curScore -= rowTree.getVal(nextCol)
                # print("rowDeltas", rowTree.getVal(nextCol))
                curScore -= colTree.getVal(nextCol)
                # print("colDeltas", colTree.getVal(nextCol))


                for j in Ml.rows[nextCol]:
                    if j in deleted:
                        continue
                    colTree.changeVal(j, -colWeights[j])
                    # print("change value:", j, -colWeights[j])
                rowSet -= {nextCol}
                rowTree.changeVal(nextCol, float('inf'))
                
                for i in Mlt.rows[nextCol]:
                    if i in deleted:
                        continue
                    rowTree.changeVal(i, -colWeights[nextCol])
                    # print("change value:", i, -colWeights[nextCol])
                colSet -= {nextCol}
                colTree.changeVal(nextCol, float('inf'))

                list_deleted.append(nextCol)
                deleted.add(nextCol)
    
                    
            numDeleted += 1
            if len(rowSet) <= 0:
                break

            curAveScore = curScore / len(rowSet)
            
            # print("cur_total", curScore)
            # # print("set", rowSet)
            # print("size", len(colSet), len(rowSet))
            # print("cur", curAveScore)
            # print("best", bestAveScore)

            if curAveScore > bestAveScore + 0.00001:
                bestAveScore = curAveScore
                bestNumDeleted = numDeleted
                # print("update", curAveScore, bestAveScore, bestNumDeleted)

            # print()

        bestRowSet = list_deleted[-(m - bestNumDeleted):]
        bestColSet = bestRowSet
        return bestRowSet, bestColSet, bestAveScore

    @classmethod
    def fast_greedy_decreasing_monosym(mat):
        # return the subgraph with optimal (weighted) degree density using Charikai's greedy algorithm
        (m, n) = mat.shape
        #uprint((m, n))
        assert m == n
        ml = mat.tolil()
        node_set = set(range(0, m))
        # print(len(node_set))
        final_ = copy.copy(node_set)
        
        cur_score = c2score(mat, node_set, node_set)
        best_avgscore = cur_score * 1.0 / len(node_set)
        # best_sets = node_set
        #print("finished setting up greedy, init score: {}".format(best_avgscore / 2.0))

        # *decrease* in total weight when *removing* this row / column
        delta = np.squeeze(1.0*mat.sum(axis=1).A)
        tree = PriorQueMin(delta)
        #print("finished building min trees")

        n_dels = 0
        deleted = list()
        best_n_dels = 0

        while len(node_set) > 1:
            if len(node_set) % 500000 == 0:
                print("   PROC: current set size = {}".format(len(node_set)))
            (delidx_, delt_) = tree.getMin()
            cur_score -= delt_ * 2
            for j in ml.rows[delidx_]:   # remove this row / column
                tree.changeVal(j, -1.0 * ml[delidx_, j])

            tree.changeVal(delidx_, float('inf'))
            node_set -= {delidx_}
            deleted.append(delidx_)

            n_dels += 1
            if n_dels < n:
                cur_avgscore = cur_score * 1.0 / len(node_set)
                if cur_avgscore > best_avgscore:
                    best_avgscore = cur_avgscore
                    best_n_dels = n_dels

        # reconstruct the best row and column sets
        for i in range(best_n_dels):
            nd_id = deleted[i]
            final_.remove(nd_id)

        return list(final_), list(final_), best_avgscore

    def evaluate_result(self, res):
        from sklearn.metrics import classification_report, roc_auc_score
        from ..utils.math import scale
        from ..utils.evaluate_utils import plot_roc_curve

        for list_row, list_col, _ in res:
            ## get score
            sus_score = np.zeros(self.graphloader.data().number_of_nodes()) + EPS
            for i in range(1, len(list_row)+1):
                sus_score[list_row[i-1]] = i

            ## compute score metrics
            sus_score = np.log2(sus_score)
            sus_score = scale(sus_score)
            print("score", sus_score)
            AUC = roc_auc_score(self.graphloader.labels, sus_score)
            print("AUC", AUC)
            plot_roc_curve(self.graphloader.labels, sus_score, self.dir_output, identifier=self.graphloader.netname+"_"+str(AUC))

            ## get labels
            fraudar_labels = np.zeros(self.graphloader.data().number_of_nodes())
            fraudar_labels[list_row] = 1
            print(sum(fraudar_labels))

            ## compute label metrics
            print(classification_report(self.graphloader.labels, fraudar_labels))   
            

            if list_row != list_col:
                fraudar_labels = np.zeros(8405)
                fraudar_labels[list_col] = 1
                print(sum(fraudar_labels))
                print("fraudar col", classification_report(self.graphloader.labels, fraudar_labels))   