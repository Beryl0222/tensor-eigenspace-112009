"""提供工位合成矩阵的只读分块输入。"""

import numpy as np


class SymmetricBlocks:
    """按协议提供有尺寸上限的半开矩形读取。"""

    def __init__(self, profile):
        self.size = profile["n"]
        self.block_size = profile["block_size"]
        prefix = profile["diag_top"]
        self._diag = np.empty(self.size, dtype=np.float64)
        self._diag[:len(prefix)] = prefix
        self._diag[len(prefix):] = np.resize(profile["diag_rest"], self.size - len(prefix))
        self._u = np.zeros(self.size)
        self._v = np.zeros(self.size)
        self._u[:len(profile["u_first"])] = profile["u_first"]
        self._v[:len(profile["v_first"])] = profile["v_first"]

    def read(self, row_start, row_stop, col_start, col_stop):
        """返回请求的矩形，拒绝越界或过大的读取。"""
        if not (0 <= row_start < row_stop <= self.size and
                0 <= col_start < col_stop <= self.size and
                row_stop - row_start <= self.block_size and
                col_stop - col_start <= self.block_size):
            raise ValueError("读取矩形超出资料范围或分块尺寸")
        rows = slice(row_start, row_stop)
        cols = slice(col_start, col_stop)
        tile = np.outer(self._u[rows], self._v[cols])
        tile += np.outer(self._v[rows], self._u[cols])
        diagonal = np.arange(max(row_start, col_start), min(row_stop, col_stop))
        tile[diagonal - row_start, diagonal - col_start] += self._diag[diagonal]
        return tile
