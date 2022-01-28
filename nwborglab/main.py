import argparse
from nwborglab import initHandler
from nwborglab import subjectHandler
from nwborglab import sessionHandler
from nwborglab import scheduleHandler

def main():
    parser = argparse.ArgumentParser('nwborglab','Takes in parameters for nwborg to run')
    
    # add the parameters for the UltracortexNwbTimeSeries contructor as command line arguments
    parser.add_argument('--command', help='command to be run', default='help', nargs='*')
    
    #parser.add_argument('args', nargs=argparse.REMAINDER)
    # parse the args
    # TODO make a .log file all output is appended to then also have a -l or --loud flag for printing output to standard output
    
    args, unknown = parser.parse_known_args()
    #Namespace(args)
    print(unknown)
    # call appropriate command function
    command = args.command[0]
    command_args = args.command[1:]
    
    if command == 'init':
        initHandler.init(command_args)

    if command == 'schedule':
        scheduleHandler.schedule(command_args)
        
    if command == 'assign':
        assignHandler(command_args)

    if command == 'subject':
        subjectHandler.createSubject(command_args)

    if command == 'session':
        if command_args[0] == 'build':
            sessionHandler.generateSessionCode(command_args[1:])
        if command_args[0] == 'schedule':
            sessionHandler.scheduleSession(command_args[1:])
        if command_args[0] == 'start':
            sessionHandler.quickstartSession(command_args[1:])
        if command_args[0] == 'quickstart':
            sessionHandler.quickstartSession(command_args[1:], unknown=unknown)
        if command_args[0] == 'quickstartmarathon':
            session_resultant_metadata = sessionHandler.quickstartSession(command_args[1:])
            while True:
                print('Session complete!\n')
                answer =input("Press 'enter' when you are ready to continue to the next session, or q to quit...")
                if answer == 'q':
                    quit()
                else:                    
                    session_resultant_metadata = sessionHandler.quickstartSession(args=session_resultant_metadata['args'],
                                                                                  session_dict=session_resultant_metadata['session_dict'],
                                                                                  subject_id_dict=session_resultant_metadata['subject_id_dict'])
                    

    print(command)
    print(command_args)
    
if __name__ == '__main__':
    main()
