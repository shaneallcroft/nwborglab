import os
from orgutils import orgutils
from datetime import datetime as dt

def scheduleSession(args):
    if not os.path.isfile('.nwb.org'):
        print('NWBORG ERROR: not in the uppermost folder of an nwborg project.')
        return
    
    session_skeletons = orgutils.orgToDict(filename='sessionskeletons.org')
    print('args:', args)
    session_archetype = args[0]
    skeleton = session_skeletons[session_archetype]
    for role in skeleton['subject roles'].keys():
        subject_id = input('Please enter a subject id to fill the role of ' + str(role) + ' in this session...')
        print('Proceeding with subject id ' + subject_id + ' filling the roll of ' + role + '...')
        # ACTUAL TODO error handling for input here
        skeleton['subject roles'][role]['subject id'] = subject_id
                
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
    session_skeletons = orgutils.orgToDict(filename='sessionskeletons.org')
    print('args:', args)
    session_archetype = args[0]
    skeleton = session_skeletons[session_archetype]

    session_dict = dict()
    session_dict['subject roles'] = skeleton['subject roles']


    # Read in the hardware configs for the sensors pertaining to the different roles
    hardware_used = dict()
    sensor_files = set()
    for role in session_dict['subject roles'].keys():
        hardware_used[role] = session_dict['subject roles'][role]['sensors']
        sensor_files.add(session_dict['subject roles'][role]['sensors']) # TODO add .split functionality for lists of sensors
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

    
    with open('sessions/' + session_archetype + '/run.py', 'w') as f:
        # autogenerated nwb initializations
        # imports        
        f.write("#!!! This file was automatically generated by nwborg !!!\n")
        f.write("# Code generated primarily from the parsing of: \n")
        f.write("#   - sessionskeletons.org\n")
        for sensor in sensor_files:            
            f.write("#   - sensors/" + str(sensor) + ".org\n")
        f.write("import pynwb\n")
        f.write("import os\n")
        f.write("import argparse\n")
        f.write("from pynwb import NWBHDF5IO\n")
        f.write("from pynwb import NWBFile\n")
        f.write("from datetime import datetime\n")
        f.write("from orgutils import orgutils\n\n")
        # mind the double newline for readability ^^^^
        
        f.write("def main():\n")
        f.write(tab+"nwborg_root_path = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-2])+'/'\n")
        f.write(tab+"overview = orgutils.orgToDict(filename=os.path.join(nwborg_root_path,'overview.org'))\n")
        f.write(tab+"skeleton = orgutils.orgToDict(filename=os.path.join(nwborg_root_path,'sessionskeletons.org'))['" + session_archetype + "']\n")
        f.write(tab+"parser = argparse.ArgumentParser('Default parser generated automatically by nwborg')\n")
        f.write(tab+"parser.add_argument('--session-id',type=str,default=-1,help='id for the session being run')\n")
        f.write(tab+"args,unknown = parser.parse_known_args()\n")
        f.write(tab+"session_id = args.session_id\n")
        f.write(tab+"session_path = nwborg_root_path + 'sessions/" + session_archetype + "/' + session_id + '/'\n")
        f.write(tab+"nwbfile = NWBFile(session_description=skeleton['description'],identifier=session_id,session_start_time=datetime.now(),file_create_date=datetime.today())\n")
        #print(skeleton['nwb unit columns'])
        if 'nwb unit columns' in skeleton.keys():
            for unit_column in skeleton['nwb unit columns'].keys():
                f.write(tab+"nwbfile.add_unit_column('"+str(unit_column)+"','"+str(skeleton['nwb unit columns'][unit_column])+"')\n")
        f.write(tab+"print('nwborg root path: ', nwborg_root_path)\n")
        f.write(tab+"session_dict = orgutils.orgToDict(filename=session_path+'session.org')\n") # pick it up

        
        # ACTUAL TODO add argument for session id for run.py and have...
        # ...it print the session data as a confirmation
        
        # user defined additions to the source code
        # one at a time add the sensors and add prompts to the file ensuring
        for statement in skeleton['programmatic']['initial']:
            f.write(half_tab + statement+'\n')
        
        for role in hardware_used.keys():
            print('initializing sensors for the ' + role + '...')
            sensor = hardware_used[role]
            config = orgutils.orgToDict(filename='sensors/' + sensor + '.org')
            #for sensor in hardware_used[role]:
            
            initialization_code = config['programmatic']['initial']
            for statement in initialization_code:
                statement = statement.replace('ROLE',role)
                f.write(half_tab + statement+'\n')


        # INITIAL STATMENTS END
        # LOOP STATEMENTS BEGIN        
        f.write(tab + 'try:\n')
        f.write((tab * 2) + 'while(True):\n')
        
        for role in hardware_used.keys():
            print('initializing sensors for the ' + role + '...')
            #for sensor in hardware_used[role]:
            sensor = hardware_used[role]
            config = orgutils.orgToDict(filename='sensors/' + sensor + '.org')
            initialization_code = config['programmatic']['loop']
            for statement in initialization_code:
                statement = statement.replace('ROLE',role)
                f.write(tab * 2 + half_tab + statement+'\n')
                    
        for statement in skeleton['programmatic']['loop']:
            f.write(tab * 2 + half_tab + statement+'\n')

        f.write(tab + 'except:\n')
        f.write(tab * 2 + 'print("\\nrecording complete")\n')
        for role in hardware_used.keys():
            print('initializing sensors for the ' + role + '...')
            #for sensor in hardware_used[role]:
            sensor = hardware_used[role]
            config = orgutils.orgToDict(filename='sensors/' + sensor + '.org')
            initialization_code = config['programmatic']['terminal']
            for statement in initialization_code:
                statement = statement.replace('ROLE',role)
                f.write(tab + half_tab + statement+'\n')
                
        for statement in skeleton['programmatic']['terminal']:
            f.write(tab + half_tab + statement+'\n')

        f.write(tab+"with NWBHDF5IO(str(session_id) + '.nwb', 'w') as io:\n")
        f.write(tab*2+"io.write(nwbfile)\n")

        # vvvvvvvv This should be the last step in the code generation process vvvvvvvv
        # Make callable from terminal and add call to main
        f.write("if __name__ == '__main__':\n")
        f.write(tab + "main()\n")





def quickstartSession(args, session_dict=None, subject_id_dict=None, session_id=None, unknown=[]):
    if not os.path.isfile('.nwb.org'):
        print('NWBORG ERROR: not in the uppermost folder of an nwborg project.')
        return
    
    session_skeletons = orgutils.orgToDict(filename='sessionskeletons.org')
    print('args:', args)
    session_archetype = args[0]
    skeleton = session_skeletons[session_archetype]
    for role in skeleton['subject roles'].keys():
        if 'subject id' in skeleton['subject roles'][role].keys():
            subject_id = skeleton['subject roles'][role]['subject id']
            #ACTUAL TODO make sure its valid
        if subject_id_dict != None and role in subject_id_dict.keys():
            # subject id specified via passing in the argument
            subject_id = subject_id_dict[role]['subject id']
        else:
            subject_id = input('Please enter a subject id to fill the role of ' + str(role) + ' in this session...')
        print(subject_id)
        print('Proceeding with subject id ' + subject_id + ' filling the roll of ' + role + '...')
        # ACTUAL TODO error handling for input here
        skeleton['subject roles'][role]['subject id'] = subject_id
                
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
    if session_dict == None: # i.e. if session_dict was not passed as a parameter to this function
        session_dict = dict()
    session_dict['subject roles'] = skeleton['subject roles']
    session_dict['archetype'] = session_archetype
    if not 'date' in session_dict.keys():
        session_dict['date'] = dt.today()

    if not 'session supervisor' in session_dict.keys():
        session_dict['session supervisor'] = input('Please input the name of the experimenter responsible for this session being recorded...')
        
    orgutils.dictToOrg(org_data=session_dict,output_filename='sessions/' + session_archetype + '/' + session_id + '/session.org')
    print('session info saved to sessions/' + session_archetype + '/' + session_id + '/' + 'session.org')

    if not os.path.isfile('sessions/' + session_archetype + '/run.py'):
        generateSessionCode(args)

    # start session
    print('\npython sessions/' + session_archetype + '/run.py --session-id ' + session_id +' '+ ' '.join(unknown) + '\n')
    os.system('python sessions/' + session_archetype + '/run.py --session-id ' + session_id +' '+ ' '.join(unknown))
    return {'args' : args, 'session_dict' : session_dict, 'subject_id_dict' : session_dict['subject roles']}
