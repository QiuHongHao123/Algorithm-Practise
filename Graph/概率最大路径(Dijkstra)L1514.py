from typing import List
from collections import defaultdict
import heapq
import copy


class Solution:
    """
    给你一个由 n 个节点（下标从 0 开始）组成的无向加权图，该图由一个描述边的列表组成，
    其中 edges[i] = [a, b] 表示连接节点 a 和 b 的一条无向边，且该边遍历成功的概率为 succProb[i] 。
    指定两个节点分别作为起点 start 和终点 end ，请你找出从起点到终点成功概率最大的路径，并返回其成功概率。
    """

    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start: int, end: int) -> float:
        """
        我用的方法就是直接dfs用邻接矩阵储存连接信息
        但是会超时在有1000个节点的时候
        :param n:
        :param edges:
        :param succProb:
        :param start:
        :param end:
        :return:
        """
        matrix = [[0] * n for _ in range(n)]
        for i, e in enumerate(edges):
            matrix[e[0]][e[1]] = succProb[i]
            matrix[e[1]][e[0]] = succProb[i]
        res = 0

        def dfs(cur, matrix, end, cursp, havedone):
            if cur == end:
                nonlocal res
                res = max(res, cursp)

            for i, sp in enumerate(matrix[cur]):
                if sp != 0 and i not in havedone:
                    newmatrix = copy.deepcopy(matrix)
                    newmatrix[i][cur] = 0
                    newmatrix[cur][i] = 0
                    nhavedone = havedone[:]
                    nhavedone.append(cur)
                    ncursp = cursp * sp

                    dfs(i, newmatrix, end, ncursp, nhavedone)

        dfs(start, matrix, end, 1, [start])
        return res

    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start: int, end: int) -> float:
        """
        官网使用的迪杰斯特拉算法
        并用优先队列进行了优化

        这道题可以用迪杰斯特拉的原因是这道题是为了获取最“大”概率路径
        而由于乘法性质路径延申概率是单调递减的。

        :param n:
        :param edges:
        :param succProb:
        :param start:
        :param end:
        :return:
        """
        graph = defaultdict(list)
        for i, (x, y) in enumerate(edges):
            graph[x].append((succProb[i], y))
            graph[y].append((succProb[i], x))

        # 这里-1应该是方便优先队列优化
        # 优先队列默认是出最小元素值出来(即最小元素在堆顶)，但是这里是要获取最大的概率值
        que = [(-1.0, start)]
        prob = [0.0] * n
        prob[start] = 1.0

        while que:
            pr, node = heapq.heappop(que)
            pr = -pr
            if pr < prob[node]:
                # 这样相当于避免了重复遍历
                continue
            for prNext, nodeNext in graph[node]:
                if prob[nodeNext] < prob[node] * prNext:
                    prob[nodeNext] = prob[node] * prNext

                    heapq.heappush(que, (-prob[nodeNext], nodeNext))

        return prob[end]
