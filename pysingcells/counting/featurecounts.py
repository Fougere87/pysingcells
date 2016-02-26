
# -*- coding: utf-8 -*-

# std import
import subprocess

# pandas import
from pandas import DataFrame, read_csv

# project import
from ..logger import log
from .abccounting import AbcCounting, tpm

# tested import
try:
    from os import scandir
except ImportError:
    from scandir import scandir

class FeatureCounts(AbcCounting):
    """ Class for run Feature Counts """

    def __init__(self):
        """ Intialize featureCounts runner object """
        super().__init__()
        # command flag
        self.annotation_flag = "-a"
        self.input_flag = ""
        self.output_flag = "-o"

    def _run_counting(self):
        """ Run count effectively """
        
        log.info(self.get_name() + " run raw count")

        raw_output = self.out_path + "raw_counts.tsv"
        list_file = [input_file.path for input_file in scandir(self.in_path) 
                     if input_file.is_file() and
                     input_file.name.endswith(".sam")]

        base_command = [self.bin_path]
        base_command += self.options.split(" ")
        base_command += [self.annotation_flag, self.annotation_path,
                         self.output_flag, raw_output, self.input_flag] 
        base_command += list_file

        process = subprocess.Popen(base_command, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
 
        self._write_process(base_command, self.get_name(),
                            *process.communicate())

        return process.returncode == 0

    def _convert_output(self):
        """ Convert output in useful format """
        
        log.info(self.get_name() + " convert raw count in tpm ")

        # reading
        header = read_csv(self.out_path + "raw_counts.tsv", 
                            header=1, sep='\t', chunksize=1)

        col_type = {index: float if val == int else val 
                    for index, val in header.read().dtypes.iteritems()}

        raw_data = read_csv(self.out_path + "raw_counts.tsv", 
                            header=1, sep='\t', dtype=col_type)

        # cleaning
        delete_col = ["Chr", "Start", "End", "Strand"]
        for colname in delete_col:
            raw_data.drop(colname, inplace=True, axis=1)

        for sample in raw_data.columns[2:]:
            log.info("\t for sample " + sample)

            nb_heat = raw_data[[sample]].sum(numeric_only=True)

            for index, count in raw_data[sample].iteritems():
                if count != 0:
                    new_val = tpm(count, raw_data["Length"][index], nb_heat)
                    raw_data.set_value(index, sample, new_val)


        # more cleaning
        raw_data.drop("Length", inplace=True, axis=1)

        # writing
        raw_data.to_csv(self.out_path + "clean_tpm.csv", index=False)

        return True
