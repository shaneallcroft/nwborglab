# pynwb imports
import pynwb
from pynwb import TimeSeries
from pynwb import NWBHDF5IO
from pynwb import NWBFile
from pynwb.ecephys import ElectricalSeries
from orgutils import orgutils

from datetime import datetime
from dateutil.tz import tzlocal
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

import brainflow as bf
import pandas as pd
import argparse
import time
import os

import numpy as np

CYTON_BOARD = 0


class NwborgExperiment (object):
    def __init__ (self, experiment_path): # actual argument should be a path to the nwborg experiment folder and that's it
        # read in stuff necessary to make self.nwb_file
        # then (maybe recursively) iterate over the rest of the thing paying attention to tags
        self.overviewOrg = None
        self.hwConfigDict = None
        self.sessionSkeletons = None
        
        # first read in the baseline NWB function
        for filename in os.listdir(experiment_path):
            if filename.endswith('overview.org'):
                # bingo, read in the org as a dictionary
                self.overviewOrg = orgutils.orgToDict(filename=os.path.join(experiment_path, filename))
            else
        self.sessionSkeletons = self.overviewOrg['Session Skeletons']
        

    def createSessionOrgs(self):
        print('TODO implement createsessionorgs')

    def buildNwbFiles():

    def recordSession
        
    


def main():
    argparse


if __name__ == '__main__':
    main()
