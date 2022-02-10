import nwborglab
import os
from os.path import expanduser
from datetime import datetime as dt
from SAPOFTO import SAPOFTO
from pynwb import NWBHDF5IO



def init(args):
    # print ascii art
    # looks messed up in .py src cause you have to escape the escapes
    # aka M-x replace-string \ --> \\ -->
    print("""
      ___           ___           ___     
     /\\__\\         /\\__\\         /\\  \\    
    /::|  |       /:/ _/_       /::\\  \\   
   /:|:|  |      /:/ /\\__\\     /:/\\:\\  \\  
  /:/|:|  |__   /:/ /:/ _/_   /::\\~\\:\\__\\ 
 /:/ |:| /\\__\\ /:/_/:/ /\\__\\ /:/\\:\\ \\:|__|
 \\/__|:|/:/  / \\:\\/:/ /:/  / \\:\\~\\:\\/:/  /
     |:/:/  /   \\::/_/:/  /   \\:\\ \\::/  / 
     |::/  /     \\:\\/:/  /     \\:\\/:/  /  
     /:/  /       \\::/  /       \\::/__/   
     \\/__/         \\/__/         ~~       
      ___           ___           ___     
     /\\  \\         /\\  \\         /\\  \\    
    /::\\  \\       /::\\  \\       /::\\  \\   
   /:/\\:\\  \\     /:/\\:\\  \\     /:/\\:\\  \\  
  /:/  \\:\\  \\   /::\\~\\:\\  \\   /:/  \\:\\  \\ 
 /:/__/ \\:\\__\\ /:/\\:\\ \\:\\__\\ /:/__/_\\:\\__\\
 \\:\\  \\ /:/  / \\/_|::\\/:/  / \\:\\  /\\ \\/__/
  \\:\\  /:/  /     |:|::/  /   \\:\\ \\:\\__\\  
   \\:\\/:/  /      |:|\\/__/     \\:\\/:/  /  
    \\::/  /       |:|  |        \\::/  /   
     \\/__/         \\|__|         \\/__/
      ___        ___            ___     
     /\\__\\      /\\  \\          /\\  \\    
    /:/  /     /::\\  \\        /::\\  \\   
   /:/  /     /:/\\:\\  \\      /:/\\:\\  \\  
  /:/  /     /::\\~\\:\\  \\    /::\\~\\:\\__\\ 
 /:/__/     /:/\\:\\ \\:\\__\\  /:/\\:\\ \\:|__|
 \\:\\  \\     \\/__\\:\\/:/   / \\:\\~\\:\\/:/  /
  \\:\\  \\         \\::/  /    \\:\\ \\::/  / 
   \\:\\  \\        /:/  /      \\:\\/:/  /  
    \\:\\__\\      /:/  /        \\::/__/   
     \\/__/      \\/__/          ~~       


       		   		   v0.0.1""")
    
    if len(args) > 0:
        print('INIT ERROR: attempting nwborglab initialization from file')
        if not os.path.isfile(args[0]):
            print(args[0] + ' no such file :(')
        if not args[0].endswith('.nwb'):
            print('INIT ERROR: specified file is not an nwb file')
            return
        io = NWBHDF5IO(args[0], 'r')
        nwbfile_in = io.read()

        print(nwbfile_in.get_scratch('nwborglab_sensors'))
        sensors_sapofto = SAPOFTO.SAPOFTO('sensors',nwbfile_in.get_scratch('nwborglab_sensors'), case_sensitive=True)
        overview_sapofto = SAPOFTO.SAPOFTO('OVERVIEW',nwbfile_in.get_scratch('nwborglab_overview'))
        session_skeleton_sapofto = SAPOFTO.SAPOFTO('SKELETONS',nwbfile_in.get_scratch('nwborglab_session_skeleton'))
        #session_skeleton_sapofto = nwbfile_in.get_scratch('nwborglab_session_source_code')
        
        SAPOFTO.recursiveFolderWrite(os.getcwd(), safe_mode=True)
        return
    
    tab = '    '
    half_tab = '  '

    home = expanduser("~")
    if not os.path.isfile(os.path.join(home,'.nwborglabsrc.org')):
        print('First nwborglab initialization! Setting up... ')
        with open('/'.join(nwborglab.__file__.split('/')[:-1]) + '/' + '.nwborglabsrc.org', 'r') as f: # TODO replace this with where the package will be
            content = f.read()

        with open(os.path.join(home,'.nwborglabsrc.org'), 'w') as f: # TODO replace this with where the package will be
            f.write(content)

    if os.path.isfile('.nwborglab.org'):
        print('ERROR: This directory is already the root of an nwborg project.')
        return

    # TODO fill out the .nwborg
    init_org = SAPOFTO.SAPOFTO('.nwborglab')
    nwborglabsrc_sapofto = SAPOFTO.SAPOFTO(key='NWBORGLABSRC',filename=os.path.join(home,'.nwborglabsrc.org'))

    with open('overview.org', 'w') as f:
        f.write(str(nwborglabsrc_sapofto['OVERVIEW SRC'].getValue()))
        nwborglabsrc_sapofto.pop('OVERVIEW SRC')
    with open('session_skeletons.org', 'w') as f:
        f.write(str(nwborglabsrc_sapofto['SESSION_SKELETONS SRC'].getValue()))
        nwborglabsrc_sapofto.pop('SESSION_SKELETONS SRC')
    with open('.nwborglab.org', 'w') as f:
        f.write(str(nwborglabsrc_sapofto.castOrgLiteral()))
    # TODO make .nwb.org in each subdirectory
    # and make root path a variable accessible in the project no matter where you are at
    # make directories if necessary
    if not os.path.isdir('subjects'):
        print('creating subjects directory...')
        os.mkdir('subjects')
        print('complete.')
    else:
        print('subjects directory found')

    if not os.path.isdir('sensors'):
        print('creating sensors directory...')
        os.mkdir('sensors')
        print('complete.')
    else:        
        print('sensors directory found')
        
    if not os.path.isdir('stimuli'):
        print('creating stimuli directory...')
        os.mkdir('stimuli')
        print('complete.')
    else:
        print('stimuli directory found')
        
    if not os.path.isdir('sessions'):
        print('creating sessions directory...')
        os.mkdir('sessions')
        print('complete.')
    else:
        print('sessions directory found')

    if not os.path.isdir('src'):
        print('creating src directory...')
        os.mkdir('src')
        print('complete.')
    else:
        print('src directory found')
