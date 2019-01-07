#!/usr/local/bin/python2.7
import collections
import os
import json


class Processor(object):

    RARE_COUNTS = 5

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.counter = collections.defaultdict(int)
        self.cache = []

    def run_freq(self):
        os.system("python count_cfg_freq.py " + self.input_file + " > cfg.counts")

    # Get the counter of Processor. The counter is the number of each word
    def count(self):
        for l in open("cfg.counts"):
            line = l.strip().split(" ")
            if line[1] == "UNARYRULE":
                self.counter[line[3]] += int(line[0])
        # print self.counter

    # repalce the words whose frequency is lower than RARE_COUNTS
    def replace_rare(self, t):
        if len(t) == 2:
            if self.counter[t[1]] < Processor.RARE_COUNTS:
                t[1] = "_RARE_"
        elif len(t) == 3:
            self.replace_rare(t[1])
            self.replace_rare(t[2])

    def make_rare(self):
        for l in open(self.input_file):
            t = json.loads(l)
            self.replace_rare(t)
            self.cache.append(json.dumps(t))

    # write cache into output file
    def write(self):
        with open(self.output_file, "w") as f:
            f.write("\n".join(self.cache))




