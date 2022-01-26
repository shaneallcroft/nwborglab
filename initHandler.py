import os
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

    print('args')
    if os.path.isfile('.nwborglab.org'):
        print('ERROR: This directory is already the root of an nwborg project.')
        return

    # TODO fill out the .nwborg
    init_org = SAPOFTO('.nwborglab')
    content = ''
    with open('.nwborglabsrc.org', 'r') as f: # TODO replace this with where the package will be
        content = f.read()
    with open('.nwborglab.org', 'w') as f:
        f.write(content)
    with open('overviewsrc.org', 'r') as f: # TODO replace this with where the package will be
        content = f.read()
    with open('overview.org', 'w') as f:
        f.write(content)

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
