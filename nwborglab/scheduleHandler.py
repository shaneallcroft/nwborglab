import os
from datetime import datetime as dt
from SAPOFTO import SAPOFTO


def schedule(args):
    session_archetype = input('Please input the session type for this session:')
    skeleton = SAPOFTO(key='SKELETON',filename='sessionskeletons.org')
    roles_node = skeleton[session_archetype]['SUBJECT ROLES']
    for role_name in roles_node.key():
        subject_id = input('Please enter a user ID to fill the role of ' + role_name + ' for this session:')
        if subject_id != '':            
            role_nodes[role_name].setValue(subject_id)
        else:
            role_nodes[role_name].setValue('?????')
    schedule_org = None
    if os.path.isfile('session_schedule.org'):
        schedule_org = SAPOFTO('SCHEDULE',filename='session_schedule.org')
    else:
        schedule_org = SAPOFTO('SCHEDULE')
    session_id = input('Please input the session\'s ID, or press enter to autogenerate a new ID...')
    if session_id == '':
        session_files = os.listdir('sessions/' + session_archetype)
        largest_id = 0
        for session_file in session_files:
            if '.' in session_file:
                continue
            session_num = int(session_file)
            if session_num > largest_id:
                largest_id = session_num
        new_id = largest_id + 1
        preceding_zeroes = ''
        if new_id < 1000:
            preceding_zeroes += '0'
        if new_id < 100:
            preceding_zeroes += '0'
        if new_id < 10:
            preceding_zeroes += '0'
        session_id = preceding_zeroes + str(new_id)
    session_key = 'TODO ' + session_archetype + str(session_id)
    schedule_org.addChild(SAPOFTO(key=session_key))
    schedule_org[session_key].addChild(roles_node)
    schedule_org.promote(1)
    

    
    # survey user about subject information
    #dotnwborglab = SAPOFTO(key='dotnwborglab', filename='.nwborglab.org')

    #survey_node = dotnwborglab['SURVEYS']['SUBJECT CREATE']

    #for question_key in survey_node.key():
