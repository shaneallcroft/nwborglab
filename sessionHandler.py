import subjectHandler
import os
import SAPOFTO
import orgutils
from datetime import datetime as dt


def scheduleSession(args):
    if not os.path.isfile('.nwborglab.org'):
        print('NWBORG ERROR: not in the uppermost folder of an nwborg project.')
        return
    
    session_skeletons = SAPOFTO.SAPOFTO(key='sessionskeletons',filename='sessionskeletons.org')
    print('args:', args)
    session_archetype = args[0]
    skeleton = session_skeletons[session_archetype]
    for role in skeleton['subject roles'].keys():
        subject_id = input('Please enter a subject id to fill the role of ' + str(role) + ' in this session...')
        if not os.path.isdir(os.path.join('subjects', str(subject_id))):
            print('Subject ' + subject_id + ' not found, proceeding to subject registration...')
            subjectHandler.createSubject(args,subject_id=subject_id)                    
        print('Proceeding with subject id ' + subject_id + ' filling the roll of ' + role + '...')
        # ACTUAL TODO error handling for input here
        skeleton['SUBJECT ROLES'][role.upper()].addChild(SAPOFTO.SAPOFTO('SUBJECT ID',content=str(subject_id) ))
        
        
    if not os.path.isdir('sessions/' + session_archetype):
        print('creating sessions directory...')
        os.mkdir('sessions/' + session_archetype)
        print('complete.')
    
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

    if not os.path.isdir('sessions/' + session_archetype + '/' + session_id):
        print('creating directory for session ' + session_id + '...')
        os.mkdir('sessions/' + session_archetype + '/' + session_id)
        print('complete.')

    print('Proceeding with id ' + session_id + ' for session creation...')
    session_dict = dict()
    session_dict['subject roles'] = skeleton['subject roles']
    session_dict['date'] = input('Please input the date expected for this session to be recorded(ex. 08/11/1998)...')
    session_dict['session supervisor'] = input('Please input the name of the experimenter responsible for this session being recorded...')
    orgutils.dictToOrg(org_data=session_dict,output_filename='sessions/' + session_archetype + '/' + session_id + '/session.org')
    print('session info saved to sessions/' + session_archetype + '/' + session_id + '/' + 'session.org')
    # Read in the hardware configs for the sensors pertaining to the different roles
    hardware_used = dict()
    sensor_files = set()
    for role in session_dict['subject roles'].keys():
        hardware_used[role] = session_dict['subject roles'][role]['sensors']
        sensor_files.add(session_dict['subject roles'][role]['sensors']) # TODO add .split functionality for lists of sensors
        # ^^^^ Also you can probably just keep track of this better by seeing where orgutils is opening org files.
        # ^^^^ Better yet maybe orgutils feature incoming?
        




def generateSessionCode(args):
    session_skeletons = SAPOFTO.SAPOFTO(key='sessionskeletons',filename='sessionskeletons.org')
    print('args:', args)
    session_archetype = args[0]
    skeleton = session_skeletons[session_archetype]

    session_sapofto = SAPOFTO.SAPOFTO('SESSION SAPOFTO')
    print(session_sapofto.keys())

    session_sapofto.addChild(skeleton['SUBJECT ROLES'])

    # Read in the hardware configs for the sensors pertaining to the different roles
    hardware_used = SAPOFTO.SAPOFTO('HARDWARE')
    sensor_files = set()
    for role in session_sapofto['SUBJECT ROLES'].keys():
        hardware_used.addChild(SAPOFTO.SAPOFTO(role, ''))
        hardware_used[role].append(session_sapofto['SUBJECT ROLES'][role.upper()]['SENSORS'].getValue())
        sensor_files.add(session_sapofto['SUBJECT ROLES'][role.upper()]['SENSORS'].getValue()) # TODO add .split functionality for lists of sensors
        
        # ^^^^ Also you can probably just keep track of this better by seeing where orgutils is opening org files.
        # ^^^^ Better yet maybe orgutils feature incoming?


    # source code generation 
    print(session_archetype + '/run.py not found... generating now....')
    tab = '    '
    half_tab = '  '

    # should be ubiquitous to all sessions, probably should be an alternate command acutally
    # that happens to run if run.py doesn't exist
    if not os.path.isdir('sessions/' + session_archetype):
        print('creating sessions directory...')
        os.mkdir('sessions/' + session_archetype)
        print('complete.')

    session_code = SAPOFTO.SAPOFTO('SESSION CODE')
    # autogenerated nwb initializations
    # imports
    dotnwborglab = SAPOFTO.SAPOFTO(key='dotnwborglab', filename='.nwborglab.org')

    # contstruct prototype parameters
    prototype_parameters = SAPOFTO.SAPOFTO(key='prototype_parameters')
    prototype_parameters.addChild(SAPOFTO.SAPOFTO('SESSION_ARCHETYPE', content=session_archetype))

    dotnwborglab.populatePrototype(prototype_parameters)
    session_code.appendLine("#!!! This file was automatically generated by nwborg !!!")
    session_code.appendLine("# Code generated primarily from the parsing of: ")
    session_code.appendLine("#   - sessionskeletons.org")
    for sensor in sensor_files:
        session_code.appendLine("#   - sensors/" + str(sensor) + ".org")

    session_code.append(('\n').join(dotnwborglab['SESSION IMPORTS'].lineList(with_tab=True, tab_displacement=-1)))
    session_code.appendLine('')
    #header_proto = SAPOFTO.SAPOFTO('SESSION_ARCHETYPE', content=session_archetype)
    dotnwborglab['SESSION HEADER'].populatePrototype(prototype_parameters)
    session_code.append(dotnwborglab['SESSION HEADER'].getValue())
    #print(skeleton['nwb unit columns'])
    if 'NWB UNIT COLUMNS' in skeleton.keys():
        for unit_column in skeleton['NWB UNIT COLUMNS'].keys():
            session_code.appendLine('\n'+tab+"nwbfile.add_unit_column('"+str(unit_column)+"','"+skeleton['nwb unit columns'][unit_column].getValue().replace('\n', ' ')+"')")

    # ACTUAL TODO add argument for session id for run.py and have...
    # ...it print the session data as a confirmation

    # user defined additions to the source code
    # one at a time add the sensors and add prompts to the file ensuring

    # SURVEY 
    for role in skeleton['SUBJECT ROLES'].keys():
        if 'SURVEY' in skeleton['SUBJECT ROLES'][role].keys():
            session_code.appendLine('\n'+tab+'print("Survey for ' + role + ':")')
             session_code.appendLine('\n'+tab+'skeleton["SUBJECT ROLES"]["'+role+'"]["SURVEY"]["INITIAL"].applySurvey()')
        
    
            
    session_code.append('\n'+tab + ('\n'+tab).join(skeleton['code']['initial'].lineList(with_tab=True, tab_displacement=-1)))

    for role in hardware_used.keys():
        print('initializing sensors for the ' + role + '...')
        sensor = hardware_used[role].getValue()
        config = SAPOFTO.SAPOFTO(key=sensor + '_config', filename='sensors/' + sensor + '.org')
        #for sensor in hardware_used[role]:

        initialization_code = config['code']['initial'].lineList(with_tab=True, tab_displacement=-1)
        session_code.append('\n' + tab + ('\n'+tab).join(initialization_code))

    session_code.appendLine('\n' + tab + 'try:')
    session_code.appendLine((tab * 2) + 'while(True):')

    for role in hardware_used.keys():
        print('initializing sensors for the ' + role + '...')
        #for sensor in hardware_used[role]:
        sensor = hardware_used[role].getValue()
        config = SAPOFTO.SAPOFTO(key=sensor + '_config',filename='sensors/' + sensor + '.org')
        initialization_code = config['code']['loop'].lineList(with_tab=True, tab_displacement=-1)
        session_code.append(('\n'+(tab*3)) + ('\n'+(tab*3)).join(initialization_code))

    session_code.append('\n'+tab + ('\n'+(tab*3)).join(skeleton['code']['loop'].lineList(with_tab=True, tab_displacement=-1)))
    session_code.appendLine('\n' + tab + 'except:')
    
    session_code.appendLine('\n' + tab * 2 + 'print("recording complete")')#, e)')
    # Apply survey questions
    #
    for role in skeleton['SUBJECT ROLES'].keys():
        if 'SURVEY' in skeleton['SUBJECT ROLES'][role].keys():
            session_code.appendLine('\n'+tab*2+'print("Survey for ' + role + ':")')
            session_code.appendLine('\n'+tab*2+'skeleton["SUBJECT ROLES"]["'+role+'"]["SURVEY"]["TERMINAL"].applySurvey()')

    
    # ACTUAL TODO FIX THE DEBUG ^^^^^^
    # ACTUAL TODO FIX THE OUTPUT vvvvv

    for role in hardware_used.keys():
        print('initializing sensors for the "' + role + '" role...')
        #for sensor in hardware_used[role]:
        sensor = hardware_used[role].getValue()
        config = SAPOFTO.SAPOFTO(key=sensor + '_config',filename='sensors/' + sensor + '.org')
        initialization_code = config['code']['terminal'].lineList(with_tab=True, tab_displacement=-1)
        session_code.append(('\n'+(tab*2)) + ('\n'+(tab*2)).join(initialization_code))




    session_code.append('\n'+tab*2 + ('\n'+(tab*2)).join(skeleton['code']['terminal'].lineList(with_tab=True, tab_displacement=-1)))
    dotnwborglab['SESSION FOOTER'].populatePrototype(prototype_parameters)
    session_code.append('\n'+tab+dotnwborglab['SESSION FOOTER'].getValue())
    session_code.appendLine('\n'+tab+"with NWBHDF5IO(str(session_id) + '.nwb', 'w') as io:")
    session_code.appendLine(tab*2+"io.write(nwbfile)")

    # vvvvvvvv This should be the last step in the code generation process vvvvvvvv
    # Make callable from terminal and add call to main
    session_code.appendLine("\nif __name__ == '__main__':")
    session_code.appendLine(tab + "main()")
    session_code.writeToFile(os.path.join('sessions', session_archetype + '/'), 'run.py' )





def quickstartSession(args, session_dict=None, subject_id_dict=None, session_id=None, unknown=[], session_sapofto=None):
    # PICK IT UP 998
    if not os.path.isfile('.nwborglab.org'):
        print('NWBORG ERROR: not in the uppermost folder of an nwborg project.')
        return
    
    session_skeletons = SAPOFTO.SAPOFTO(key='SKELETON',filename='sessionskeletons.org')
    print('args:', args)
    session_archetype = args[0]
    skeleton = session_skeletons[session_archetype]
    for role in skeleton['subject roles'].keys():
        if 'SUBJECT ID' in skeleton['SUBJECT ROLES'][role.upper()].keys():            
            subject_id = skeleton['SUBJECT ROLES'][role.upper()]['SUBJECT ID'].getValue()            
            #ACTUAL TODO make sure its valid
        if subject_id_dict != None and role in subject_id_dict.keys():
            # subject id specified via passing in the argument
            subject_id = subject_id_dict[role]['SUBJECT ID'].getValue()
        else:
            subject_id = input('Please enter a subject id to fill the role of ' + str(role) + ' in this session...')
        print(subject_id)
        print('Proceeding with subject id ' + subject_id + ' filling the roll of ' + role + '...')
        # ACTUAL TODO error handling for input here
        #skeleton['SUBJECT ROLES'][role]['SUBJECT ID'] = subject_id
        skeleton['SUBJECT ROLES'][role.upper()].addChild(SAPOFTO.SAPOFTO('SUBJECT ID',content=str(subject_id) ))
                
    if not os.path.isdir('sessions/' + session_archetype):
        print('creating sessions directory...')
        os.mkdir('sessions/' + session_archetype)
        print('complete.')
    if session_id == None:  # i.e. if session_id was not passed as a parameter to this function
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

    if not os.path.isdir('sessions/' + session_archetype + '/' + session_id):
        print('creating directory for session ' + session_id + '...')
        os.mkdir('sessions/' + session_archetype + '/' + session_id)
        print('complete.')

    print('Proceeding with id ' + session_id + ' for session creation...')
    if session_sapofto == None: # i.e. if session_sapofto was not passed as a parameter to this function
        session_sapofto = SAPOFTO.SAPOFTO('SESSION METADATA')
    session_sapofto.addChild(skeleton['SUBJECT ROLES'])
    session_sapofto.addChild(SAPOFTO.SAPOFTO('ARCHETYPE', content=session_archetype))
    if not 'DATE' in session_sapofto.keys():
        session_sapofto.addChild(SAPOFTO.SAPOFTO('DATE', content=str(dt.today())))
    
    if not 'SESSION SUPERVISOR' in session_sapofto.keys():
        session_sapofto.addChild(SAPOFTO.SAPOFTO('SESSION SUPERVISOR', input('Please input the name of the experimenter responsible for this session being recorded...')))
    print(session_sapofto)
    session_sapofto.writeToFile('sessions/' + session_archetype + '/' + session_id + '/', 'session.org')

    print('session info saved to sessions/' + session_archetype + '/' + session_id + '/' + 'session.org')

    if not os.path.isfile('sessions/' + session_archetype + '/run.py'):
        generateSessionCode(args)

    # start session
    print('\npython sessions/' + session_archetype + '/run.py --session-id ' + session_id +' '+ ' '.join(unknown) + '\n')
    os.system('python sessions/' + session_archetype + '/run.py --session-id ' + session_id +' '+ ' '.join(unknown))
    return {'args' : args, 'session_sapofto' : session_sapofto, 'subject_id_dict' : session_sapofto['subject roles']}
