import numpy as np
import concurrent.futures
import time
from pathlib import Path

from Panalyzer.VfAnalyzer.ace_calculator_packed import ace_calculators
from Panalyzer.parallel.parallel_window_slicer import window_slicer


class parallel_ace:
    def __init__(self, info, reg_count, n_sample, f_length):
        self.csvin = info
        self.reg_count = reg_count
        self.num_sample = n_sample
        self.length = f_length

    def multiprocessing_ace(self, threads, start, n_window, lineoffset, mode, avg_masking=0):
        time_history = []
        slice_info = window_slicer(self.length, threads, n_window, self.num_sample)
        window_size = slice_info['window_size']
        n_groups = slice_info['n_groups']
        sample_ratio = slice_info['sample_ratio']
        analyzing_length = slice_info['analyzing_length']
        threads_group_counter = 0

        print(slice_info)
        sampled_window_length = int(sample_ratio * window_size)
        ace_matrix_whole = np.zeros([self.reg_count + 1, 0], dtype=np.int64)

        while start < analyzing_length + 1:
            # print(start)
            t_start = time.perf_counter()
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results_this_thread = [executor.submit(ace_calculators(self.csvin, self.reg_count).
                                                       ace_calculator_detailed, start + i * window_size, window_size,
                                                       sample_ratio, lineoffset, mode, avg_masking) for i in range(threads)]
                for f in concurrent.futures.as_completed(results_this_thread):
                    if threads_group_counter < n_groups:
                        ace_temp = f.result()
                        ace_matrix_whole = np.hstack((ace_matrix_whole, ace_temp))
            start = start + threads * window_size
            threads_group_counter += 1
            t_passed = time.perf_counter() - t_start
            print(t_passed)
            time_history.append(t_passed)
        ace_matrix_whole = ace_matrix_whole[:, ace_matrix_whole[-1, :].argsort()]
        matrix_size = np.shape(ace_matrix_whole)[1]
        # print(time_history)
        # print(matrix_size)
        for i in range(sampled_window_length - 1, matrix_size, sampled_window_length):
            last_singlewindow = np.reshape(ace_matrix_whole[:-1, i], (self.reg_count, 1))
            ace_matrix_whole[:-1, i + 1: i + sampled_window_length + 1] += last_singlewindow

        return ace_matrix_whole

    def multiprocessing_ace_q(self, threads, start, n_window, lineoffset, mode):
        time_history = []
        slice_info = window_slicer(self.length, threads, n_window)
        window_size = slice_info['window_size']
        n_groups = slice_info['n_groups']
        analyzing_length = slice_info['analyzing_length']
        threads_group_counter = 0

        print(slice_info)
        sampled_window_length = int(1)
        ace_matrix_whole = np.zeros([self.reg_count + 1, 0], dtype=np.int64)

        while start < analyzing_length + 1:
            # print(start)
            t_start = time.perf_counter()
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results_this_thread = [executor.submit(ace_calculators(self.csvin, self.reg_count).
                                                       ace_calculator_quanta, start + i * window_size, window_size,
                                                       lineoffset, mode) for i in range(threads)]
                for f in concurrent.futures.as_completed(results_this_thread):
                    if threads_group_counter < n_groups:
                        ace_temp = f.result()
                        ace_matrix_whole = np.hstack((ace_matrix_whole, ace_temp))
            start = start + threads * window_size
            threads_group_counter += 1
            t_passed = time.perf_counter() - t_start
            print(t_passed)
            time_history.append(t_passed)
        ace_matrix_whole = ace_matrix_whole[:, ace_matrix_whole[-1, :].argsort()]
        matrix_size = np.shape(ace_matrix_whole)[1]
        # print(time_history)
        # for i in range(sampled_window_length - 1, matrix_size, sampled_window_length):
        #     last_singlewindow = np.reshape(ace_matrix_whole[:-1, i], (self.reg_count, 1))
        #     ace_matrix_whole[:-1, i + 1: i + sampled_window_length + 1] += last_singlewindow
        ace_shifted = np.roll(ace_matrix_whole[-1, :], 1)
        ace_shifted[0] = 0
        ace_matrix_whole[-1, :] = ace_matrix_whole[-1, :] - ace_shifted

        return ace_matrix_whole


if __name__ == "__main__":
    reg_num = 16
    project_dir = Path(__file__).resolve().parent.parent
    csv_dir = project_dir.joinpath('tempcsv')
    fname = "prime.csv"
    filein = csv_dir / fname

    n_datapoint = 100
    flength = 10000
    thread = 6
    startp = 0
    n_of_groups = 12

    ace_test = parallel_ace(filein, reg_num, n_datapoint, flength).multiprocessing_ace_q(thread, startp, n_of_groups, [])
    print(ace_test)
    print(np.shape(ace_test))
