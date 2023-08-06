import matplotlib.pyplot as plt
import numpy as np
import logging, os

class NetworkThresholdFilter():
    n_step = 0.001
    list_bound = np.arange(0, 1, n_step) # define by your data distribution

    def __init__(self, filepath):
        self.filepath = filepath
        self.map_info_path = ".".join(self.filepath.split(".")[:-1]) + "_map_info.txt"

        # map and reduces
        self.list_file_ptr = self.open_writable_map_file_ptr()
        self.n_line, self.list_cnt = self.do_map()
        self.list_file_ptr = self.open_readable_map_file_ptr()

        self.plot_simscore_distribution()

        # self.get_top_k(800000)
        self.get_top_k_by_threshold(0.99995)

    def open_writable_map_file_ptr(self):
        list_file_ptr = []
        n_bound = len(self.list_bound)
        n_exsit = 0
        for bound in self.list_bound:
            output_path = ".".join(self.filepath.split(".")[:-1]) + "_" + str(bound) + ".txt"
            if os.path.exists(output_path):
                n_exsit += 1

        # list_bound do not change
        if n_bound == n_exsit:
            return []

        for bound in self.list_bound:
            output_path = ".".join(self.filepath.split(".")[:-1]) + "_" + str(bound) + ".txt"
            list_file_ptr.append(open(output_path, "w"))
        return list_file_ptr

    def close_file_ptr(self):
        for file_ptr in self.list_file_ptr:
            file_ptr.close()

    def open_readable_map_file_ptr(self):
        list_file_ptr = []
        for bound in self.list_bound:
            output_path = ".".join(self.filepath.split(".")[:-1]) + "_" + str(bound) + ".txt"
            list_file_ptr.append(open(output_path))
        return list_file_ptr

    def do_map(self):
        logging.info("start mapping to several files")
        n_line = 0
        if not self.list_file_ptr:
            n_line, list_cnt = self.load_map_info()
            return n_line, list_cnt
        n_bound = len(self.list_bound)
        list_cnt = [0] * n_bound
        with open(self.filepath) as fp:
            for line in fp:
                tokens = line.split()
                if len(tokens) != 4:
                    continue
                value = float(tokens[3].strip(",()"))
                index =  np.searchsorted(self.list_bound, value, side="left")
                index -= 1
                if value % self.n_step == 0:
                    index += 1
                self.list_file_ptr[index].write("%s\t%s\t%s\n" % (tokens[0].strip(",()"), tokens[2].strip(",()"), tokens[3].strip(",()")))
                n_line += 1
                list_cnt[index] += 1
        self.close_file_ptr()
        self.write_map_info(n_line, list_cnt)
        return n_line, list_cnt

    def load_map_info(self):
        cnt = 0
        with open(self.map_info_path) as fp:
            for line in fp:
                if cnt == 0:
                    n_line = int(line.strip())
                if cnt == 1:
                    list_cnt = line.split()
                    list_cnt = [int(x) for x in list_cnt]
                cnt += 1
        return n_line, list_cnt


    def write_map_info(self, n_line, list_cnt):
        list_cnt = [str(x) for x in list_cnt]
        with open(self.map_info_path, "w") as fp:
            fp.write("%d\n" % n_line)
            fp.write("\t".join(list_cnt)+"\n")


    def get_top_k(self, k = 0.2):
        """
        The graph is not strictly topk , because the map file is not ordered.
        """
        logging.info("start getting top k")
        if k < 1:
            k = self.n_line * k

        output_path = ".".join(self.filepath.split(".")[:-1]) + "_filter.txt"
        cnt_edge = 0

        with open(output_path, "w") as wfp:
            for i in range(len(self.list_file_ptr)):
                fp = self.list_file_ptr[len(self.list_file_ptr)-i-1]
                for line in fp:
                    tokens = line.split()
                    if len(tokens) != 3:
                        continue
                    wfp.write("%s\t%s\n" % (tokens[0], tokens[1]))
                    cnt_edge += 1
                    if (cnt_edge > k):
                        break
                if (cnt_edge > k):
                    break
        self.close_file_ptr()

    def get_top_k_by_threshold(self, threshold = 0.99):
        logging.info("start getting top k by threshold")
        output_path = ".".join(self.filepath.split(".")[:-1]) + "_filter.txt"

        with open(output_path, "w") as wfp:
            for i in range(len(self.list_file_ptr)):
                fp = self.list_file_ptr[len(self.list_file_ptr)-i-1]
                for line in fp:
                    tokens = line.split()
                    if len(tokens) != 3:
                        continue
                    if threshold <= float(tokens[2]):
                        wfp.write("%s\t%s\n" % (tokens[0], tokens[1]))
                if self.list_bound[i] <= threshold:
                    break
        self.close_file_ptr()

    def plot_simscore_distribution(self):
        logging.info("start plotting")

        print(self.list_cnt)
        print(len(self.list_cnt))


        plt.plot(np.arange(0+self.n_step*0.5,1+self.n_step*0.5, self.n_step), self.list_cnt, "ro", markersize=1)
        output_path = ".".join(self.filepath.split(".")[:-1]) + "_distribution.png"
        plt.savefig(output_path)
        # plt.show()
        plt.clf()

        list_sum = []
        n_sum = 0
        for i in range(len(self.list_cnt)):
            n_sum += self.list_cnt[i]
            list_sum.append(n_sum)
        plt.plot(np.arange(0+self.n_step*0.5,1+self.n_step*0.5, self.n_step), list_sum)
        output_path = ".".join(self.filepath.split(".")[:-1]) + "_cumulative_distribution.png"
        plt.savefig(output_path)
        # plt.show()
        plt.clf()

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_yscale('log')
        ax.set_xscale('log')
        plt.plot(np.arange(0+self.n_step, 1+self.n_step, self.n_step),self.list_cnt)
        # plt.xlim(0.01, 10) # Fix the x limits to fit all the points
        output_path = ".".join(self.filepath.split(".")[:-1]) + "_loglog_distribution.png"
        plt.savefig(output_path)
        # plt.show()
        plt.clf()

if __name__ == '__main__':
    NetworkThresholdFilter("./output/matrix_0.txt")







