import os
from datetime import datetime as dt
from SAPOFTO import SAPOFTO


def schedule(args):
    session_archetype = input('Please input the session type for this session:')
    print(session_archetype)
    skeleton = SAPOFTO.SAPOFTO(key='SKELETON',filename='session_skeletons.org')
    print(skeleton.keys())
    roles_node = skeleton[session_archetype]['SUBJECT ROLES']
    for role_name in roles_node.keys():
        roles_node[role_name].removeAllChildren()
        print(roles_node[role_name].keys())
        subject_id = input('Please enter a user ID to fill the role of ' + role_name + ' for this session:')
        if subject_id != '':            
            roles_node[role_name].setValue(subject_id)
        else:
            roles_node[role_name].setValue('?????')
        roles_node[role_name].removeAllChildren()
    schedule_org = None
    if os.path.isfile('session_schedule.org'):
        schedule_org = SAPOFTO.SAPOFTO('SCHEDULE',filename='session_schedule.org')
        if not  str(session_archetype) + ' SCHEDULE' in schedule_org.keys():
            schedule_org.addChild(SAPOFTO.SAPOFTO(str(session_archetype) + ' SCHEDULE'))
    else:
        schedule_org = SAPOFTO.SAPOFTO('SCHEDULE')
        schedule_org.addChild(SAPOFTO.SAPOFTO(str(session_archetype) + ' SCHEDULE'))
    session_id = input('Please input the session\'s ID, or press enter to autogenerate a new ID...')
    if session_id == '':
        if os.path.isdir(os.path.join('sessions',session_archetype)):
            session_files = os.listdir(os.path.join('sessions',session_archetype))
        else:
            session_files = []            
            os.mkdir(os.path.join('sessions',session_archetype))
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
    schedule_org[str(session_archetype) + ' SCHEDULE'].addChild(SAPOFTO.SAPOFTO(key=session_key))
    schedule_org[str(session_archetype) + ' SCHEDULE'][session_key].addChild(roles_node)
    with open('session_schedule.org', 'w') as f:
        
        f.write(str(schedule_org.castOrgLiteral()))

    

    
    # survey user about subject information
    #dotnwborglab = SAPOFTO(key='dotnwborglab', filename='.nwborglab.org')

    #survey_node = dotnwborglab['SURVEYS']['SUBJECT CREATE']

    #for question_key in survey_node.key():
