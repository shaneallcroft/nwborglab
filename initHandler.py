import os
from datetime import datetime as dt

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
       		   		   v0.0.1""")
    

    
    print('hello')
    if os.path.isfile('.nwb.org'):
        print('ERROR: This directory is already the root of an nwborg project.')
        return

    # TODO fill out the .nwborg
    if not os.path.isfile('.nwb.org'):
        with open('.nwb.org', 'w') as f:
            f.write('nwborg experiment first initialized ' + str(dt.now()) + '\n')
        

    # overview.org
    if not os.path.isfile('overview.org'):
        print('generating overview.org...')
        with open('overview.org', 'w') as overview:
            overview.write('* Experiment Abstract\n')
            overview.write('* Experimenter\n')
            overview.write('* Lab\n')
            overview.write('* Institution\n')
        print('complete.')
    else:
        print('found overview.org...')

    # sessionSkeletons.org
    if not os.path.isfile('sessionskeletons.org'):
        print('generating sessionskeletons.org...')
        with open('sessionskeletons.org', 'w') as sessionSkeletons:
            sessionSkeletons.write('* example skeleton\n')
            sessionSkeletons.write('* subject sensor map\n')
            sessionSkeletons.write('* Lab\n')
            sessionSkeletons.write('* Institution\n')
        print('complete.')
    else:
        print('found sessionSkeletons.org...')

    
    # make directories if necessary
    if not os.path.isfile('subjects'):
        print('creating subjects directory...')
        os.mkdir('subjects')
        print('complete.')
    else:
        print('subjects directory found')

    if not os.path.isfile('sensors'):
        print('creating sensors directory...')
        os.mkdir('sensors')
        print('complete.')
    else:        
        print('sensors directory found')
        
    if not os.path.isfile('stimuli'):
        print('creating stimuli directory...')
        os.mkdir('stimuli')
        print('complete.')
    else:
        print('stimuli directory found')
        
    if not os.path.isfile('sessions'):
        print('creating sessions directory...')
        os.mkdir('sessions')
        print('complete.')
    else:
        print('sessions directory found')

    
    
