#!/usr/local/bin/python2.7
import sys
import q4
import q5

if __name__ == "__main__":
    if sys.argv[1] == "q4":
        rare_processor = q4.Processor(sys.argv[2], sys.argv[3])
        # get cfg.counts
        rare_processor.run_freq()
        # Get the counter of Processor. The counter is the number of each word
        rare_processor.count()
        # repalce the words whose frequency is lower than RARE_COUNTS
        rare_processor.make_rare()
        # write cache into output file
        rare_processor.write()
    elif sys.argv[1] == "q5" or sys.argv[1] == "q6":
        cky = q5.CKY(sys.argv[2], sys.argv[3], sys.argv[4])
        # get parameters the CKY need
        cky.get_parameters()
        # run cky algorithm
        cky.run_cky()
        # write cache into output file
        cky.write()
