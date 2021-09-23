import os
import orgutils
from datetime import datetime as dt

def instantiateSession(args):
    if not os.path.isfile('.nwb.org'):
        print('NWBORG ERROR: not in the uppermost folder of an nwborg project.')
        return
    
    session_skeletons = orgutils.orgToDict(filename='sessionskeletons.org')
    print(args)
    session_archetype = args[0]
    skeleton = session_skeletons[session_archetype]
    for role in skeleton['subject roles'].keys():
        subject_id = input('please enter a subject id to fill the role of ' + str(role) + ' in this session...')
        skeleton[role]['subject id'] = subject_id
                
    if not os.path.isdir('sessions/' + session_archetype):
        print('creating sessions directory...')
        os.mkdir('sessions/' + session_archetype)
        print('complete.')


    session_id = input('please input the session\'s ID, or press enter to autogenerate a new ID')
    if session_id == '':
        session_files = os.listdir('sessions/' + session_archetype)
        largest_id = 0
        for session_file in session_files:
            
            session_num = int(session_file)
            if session_num > largest_id:
                largest_id = session_num
        new_id = session_num + 1
        preceding_zeroes = ''
        if new_id < 1000:
            preceding_zeroes += '0'
        if new_id < 100:
            preceding_zeroes += '0'
        if new_id < 10:
            preceding_zeroes += '0'
        session_id = preceding_zeroes + str(new_id)

    if not os.path.isdir('sessions/' + session_archetype + '/' + session_id):
        print('creating directory for session ' + session_id + '...')
        os.mkdir('sessions/' + session_archetype + '/' + session_id)
        print('complete.')

    print('Proceeding with id ' + session_id + ' for session creation...')
    session_dict = dict()
    session_dict['subject roles'] = skeleton['subject roles']
    session_dict['date'] = input('Please input the date expected for this session to be recorded(ex. 08/11/1998)...')
    session_dict['session supervisor'] = input('Please input the name of the experimenter responsible for this session being recorded...')
    session_dict['date'] = input('Please input the date expected for this session to be recorded(ex. 08/11/1998)...')
    orgutils.dictToOrg(org_data=session_dict,output_filename='sessions/' + session_id + '.org')
    print('session info saved to sessions/' + session_archetype + '/' + session_id + '/' + 'session.org')
    
    
