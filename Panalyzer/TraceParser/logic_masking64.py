import numpy as np
import re
from Panalyzer.utils.BinaryMethods import BinaryMethods


class Arm64MaskingCalculator:
    def __init__(self, length, ops, src1, src2, reg_num, reg_val_table):
        self.lnum = length
        self.op = ops
        self.num_reg = reg_num
        self.src1_list = src1
        self.src2_list = src2
        self.reg_val_matrix = reg_val_table

    def lmasking_calculator(self, avg_mask=0.12):
        masking_table = np.full([self.num_reg, self.lnum], 0, dtype=float)
        for i in range(self.lnum):
            current_src1 = self.src1_list[i]
            current_src2 = self.src2_list[i]
            if len(current_src1) > 0:
                if current_src1[0] is 'x' or current_src1[0] is 'w':
                    regid = int(re.search(r'\d+', current_src1).group())
                    if current_src1[0] is 'x':
                        masking_table[regid, i] = 0.5
                    else:
                        masking_table[regid, i] = avg_mask

            if len(current_src2) > 0:
                if current_src2[0] is 'x' or current_src2[0] is 'w':
                    regid = int(re.search(r'\d+', current_src2).group())
                    if current_src2[0] is 'x':
                        masking_table[regid, i] = 0.5
                    else:
                        masking_table[regid, i] = avg_mask
        return masking_table


if __name__ == "__main__":
    ops = ['mov.w', 'mov.w', 'mov', 'ldr.w', 'ldr', 'ldr', 'bl.w', 'mov.w', 'and', 'movt.w']
    src1h = ['0', '0', 'w1', 'w1', 'w1', 'x1', '', '0', 'w1', 'x1']
    src2h = ['', '', 'x0', '', '', '', '', '', 'x2', '0']
    regtable = np.array([[0, 0, 0, 0, 66437, 66437, 66437, 66437, 66437, 66437],
                         [0, 0, 0, 0, 15, 6637, 37, 66, 664, 7]])
    # res = regval_fetcher(8, src1h, src2h, regtable)
    # m_table = arm32masking_calculator(10, ops, src1h, src2h, 2,
    #                                   regtable).lmasking_calculator()
    m_table = Arm64MaskingCalculator(10, ops, src1h, src2h, 3, regtable).lmasking_calculator()

    print(m_table)