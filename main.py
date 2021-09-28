import argparse
import initHandler
import subjectHandler
import sessionHandler


def main():
    parser = argparse.ArgumentParser('Takes in parameters for nwborg to run')
    
    # add the parameters for the UltracortexNwbTimeSeries contructor as command line arguments
    parser.add_argument('--command', help='command to be run', default='help', nargs='*')
    
    # parse the args
    # TODO make a .log file all output is appended to then also have a -l or --loud flag for printing output to standard output
    
    args = parser.parse_args()

    # call appropriate command function
    command = args.command[0]
    command_args = args.command[1:]
    
    if command == 'init':
        initHandler.init(command_args)

    if command == 'schedule':
        scheduleHandler(command_args)
        
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
            sessionHandler.quickstartSession(command_args[1:])
        if command_args[0] == 'quickstartmarathon':
            sessionHandler.quickstartSession(command_args[1:], marathon=True)

    print(command)
    print(command_args)
    
if __name__ == '__main__':
    main()
