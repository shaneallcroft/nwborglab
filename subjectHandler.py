import os
from orgutils import orgutils
from datetime import datetime as dt

def createSubject(args):
    # survey user about subject information
    if not os.path.isfile('.nwb.org'):
        print('NWBORG ERROR: not in the uppermost folder of an nwborg project.')
        return
    
    print('Create Subject!')
    subject_id = input('Please input the subject\'s ID, or press enter to autogenerate a new ID')
    if subject_id == '':
        subject_files = os.listdir('subjects')
        largest_id = 0
        for subject_file in subject_files:
            subject_num = int(subject_file[:-4])
            if subject_num > largest_id:
                largest_id = subject_num
        new_id = largest_id + 1
        preceding_zeroes = ''
        if new_id < 1000:
            preceding_zeroes += '0'
        if new_id < 100:
            preceding_zeroes += '0'
        if new_id < 10:
            preceding_zeroes += '0'
        subject_id = preceding_zeroes + str(new_id)
    
    print('Proceeding with id ' + subject_id + ' for subject creation...')
    
    subject_dict = dict()
    subject_dict['Subject ID'] = subject_id
    subject_dict['Species'] = input('Please enter subject species...')
    subject_dict['Age'] = input('Please enter subject age in any desired units (ex. "23 years")...')
    subject_dict['Sex'] = input('Please enter subject sex M for male F for female O for other...')
    subject_dict['Date of Birth'] = input('Please input the subject\'s date of birth (ex. 08/11/1998)...')
    subject_dict['Description'] = input('Please provide additional description for the subject...')
    orgutils.dictToOrg(org_data=subject_dict,output_filename='subjects/' + subject_id + '.org')
    print('subject info saved to subjects/' + subject_id + '.org')
    
