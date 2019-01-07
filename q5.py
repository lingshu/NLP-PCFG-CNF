import os
import collections
from math import log
import json

class CKY(object):
    def __init__(self, parse_train_file, parse_dev_file, output_file):
        self.parse_train_file = parse_train_file
        self.parse_dev_file = parse_dev_file
        self.output_file = output_file
        self.nonterminal = collections.defaultdict(int)
        self.terminal = set()
        self.q_unary = collections.defaultdict(lambda: float("-inf"))
        self.unary = collections.defaultdict(int)
        self.binary = collections.defaultdict(int)
        self.q_binary = collections.defaultdict(lambda: collections.defaultdict(lambda: float("-inf")))
        self.cache = []

    def get_parameters(self):
        os.system("python count_cfg_freq.py " + self.parse_train_file + " > cfg.rare.counts")
        for l in open("cfg.rare.counts"):
            line = l.split()
            if line[1] == "NONTERMINAL":
                self.nonterminal[line[2]] += int(line[0])
            elif line[1] == "UNARYRULE":
                self.terminal.add(line[3])
                self.unary[(line[2], line[3])] += int(line[0])
            elif line[1] == "BINARYRULE":
                self.binary[(line[2], line[3], line[4])] += int(line[0])
        # print self.binary
        # print self.unary
        # print self.nonterminal
        # print self.terminal

        for key, value in self.unary.items():
            self.q_unary[key] = log(float(value)) - log(float(self.nonterminal[key[0]]))
        for key, value in self.binary.items():
            self.q_binary[key[0]][(key[1], key[2])] = log(float(value)) - log(float(self.nonterminal[key[0]]))
        # print self.q_unary
        # print self.q_binary

    def run_cky(self):
        def build_tree(left, right, bp, X, line):
            if left == right:
                return [X, line[left]]
            else:
                bp_xys = bp[(left, right, X)]
                # print bp_xys
                return [X, build_tree(left, bp_xys[1], bp, bp_xys[0][0], line),
                        build_tree(bp_xys[1] + 1, right, bp, bp_xys[0][1], line)]

        # get new line with _RARE_ signals
        for lines in open(self.parse_dev_file):
            x = []
            line = lines.strip().split(" ")
            for word in line:
                if word not in self.terminal:
                    x.append("_RARE_")
                else:
                    x.append(word)

            pi = collections.defaultdict(lambda: float("-inf"))
            bp = collections.defaultdict(tuple)

            # initialization
            for i in xrange(len(x)):
                for X in self.nonterminal:
                    if (X, x[i]) in self.q_unary:
                        pi[(i, i, X)] = self.q_unary[(X, x[i])]

            # do algorithm
            for l in xrange(1, len(x)):
                for i in xrange(len(x) - l):
                    j = i + l
                    for X in self.nonterminal:
                        max_pi = float("-inf")
                        max_bp = ()
                        for YZ in self.q_binary[X]:
                            Y = YZ[0]
                            Z = YZ[1]
                            for s in xrange(i, j):
                                cur_pi = self.q_binary[X][YZ] + pi[(i, s, Y)] + pi[(s + 1, j, Z)]
                                if cur_pi > max_pi:
                                    max_pi = cur_pi
                                    max_bp = (YZ, s)
                            pi[(i, j, X)] = max_pi
                            bp[(i, j, X)] = max_bp

            if pi[(0, len(x) - 1, "S")] != float("-inf"):
                tree = build_tree(0, len(x) - 1, bp, "S", line)
                t = json.dumps(tree)
                self.cache.append(t)
            else:
                max_pi = float("-inf")
                new_S = ""
                for X in self.nonterminal:
                    cur_pi = pi[(0, len(x) - 1, X)]
                    if cur_pi > max_pi:
                        max_pi = cur_pi
                        new_S = X
                tree = build_tree(0, len(x) - 1, bp, new_S, line)
                t = json.dumps(tree)
                self.cache.append(t)

    def write(self):
        with open(self.output_file, "w") as f:
            f.write("\n".join(self.cache))




