from datetime import datetime
from dateutil.tz import tzlocal
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

import pynwb
from pynwb import TimeSeries
import brainflow as bf
import argparse
import time
import orgutils
import os



CYTON_BOARD = 0


def main():
    # ---------------------------------------------------
    # user facing calibration program
    # --------------------------------------------------
    # arg parse stuff
    parser = argparse.ArgumentParser('Takes in parameters of the input')
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection'
                        , default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False, default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='/dev/ttyUSB0')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    parser.add_argument('--sample_frequency', type=float, help='float value designating the time between reads in seconds',
                        default=1.0)
    parser.add_argument('--subject-name', type=str, help='arbitrary identifier for player / subject')
    parser.add_argument('--video-path', type=str, help='path to the folder with the calibration videos')   
    args = parser.parse_args()

    # Read into params from args
    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file

    # read other args variables 
    pipe_path = args.pipe_path # for the controller
    sleep_time = 1.0 / float(args.sample_frequency)
    video_path = args.video_path

    # initialize dataflow objects
    board = BoardShim(CYTON_BOARD, params)
    data_filter = DataFilter()
    board.prepare_session()
    
    
    
    # board.start_stream() # use this for default option
    # start stream
    board.start_stream(45000,args.streamer_params)
    print('Waiting 5 to ensure connection starting now...')
    time.sleep(5)
    print('Waiting over! Calibration process begin:')
    subject_id = input('Please input the name/id of the subject:')
    
    # data = board.get_current_board_data(256)
    for video_file in os.listdir(video_path):
        if not video_file.endswith('.mkv') or video_file.endswith('.mp4') or video_file.endswith('.mov'):
            continue
        input('Please prepare subject' + str(subject_id) ' to watch ' + str(video_file) + ' when you are ready, please press enter, wait 3 seconds and then press "play" on the video player. If you haven\'t done so already, turn on your EEG recording device now. Press Ctrl+c a single time once the video ends ')
        try:
            # vvvvv NWB stuff vvvvv
            start_time = datetime.now()
            rate_ts = TimeSeries(name=str(subject_id) + str(video_file[0:-4]))
            
            first_write_to_file = True
            while(True):
                eeg_data = board.get_board_data()
                if first_write_to_file:                    
                    datafilter.write_file(data=eeg_data,file_mode='w')
                else:
                    datafilter.write_file(data=eeg_data,file_mode='a')
                    first_write_to_file = False
                time.sleep(sleep_time)
        except:
            print('EEG Data recording for video complete, prompt the subject to answer these questions:')
            input('On a scale from 1 to 9, how engaged/excited were you during the watching of that video?')
            input('On a scale from 1 to 9, how much pleasure/enjoyment did you experience while watching that video?')
            # TODO write metadata into file to mesh with raw data in an NWB acceptable way
    board.stop_stream()
    board.release_session()


if __name__ == '__main__':
    main()
