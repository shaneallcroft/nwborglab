import nwborglab
import os
from os.path import expanduser
from datetime import datetime as dt
from SAPOFTO import SAPOFTO

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
