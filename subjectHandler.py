import pynwb
import os
from orgutils import orgutils
from datetime import datetime as dt
import SAPOFTO


def createSubject(args, subject_id=None):
    # survey user about subject information
    #dotnwborglab = SAPOFTO.SAPOFTO(key='dotnwborglab', filename='.nwborglab.org')

    #survey_node = dotnwborglab['SURVEYS']['SUBJECT CREATE']

    #for question_key in survey_node.key():
        

    
    if not os.path.isfile('.nwb.org'):
        print('NWBORG ERROR: not in the uppermost folder of an nwborg project.')
        return


    
    print('Create Subject!')
    if subject_id == None:
        subject_id = input('Please input the subject\'s ID, or press enter to autogenerate a new ID')
    if subject_id == '':
        subject_files = os.listdir('subjects')
        largest_id = 0
        for subject_file in subject_files:
            subject_num = int(subject_file)
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
    os.mkdir('subjects/' + subject_id)
    orgutils.dictToOrg(org_data=subject_dict,output_filename='subjects/' + subject_id + '/' + subject_id + '.org')
    print('subject info saved to subjects/' + subject_id + '.org')
    



def subjectIdToNwbSubjectObject(subject_id):
    subject_node = SAPOFTO.SAPOFTO(os.path.join('Subjects',str(subject_id),str(subject_id),'.org'))

    subject_nwb = pynwb.file.Subject()
    if 'AGE' in subject_node.keys():
        subject_nwb.age = subject_node['AGE'].getValue()
    if 'DESCRIPTION' in subject_node.keys():
        subject_nwb.description = subject_node['DESCRIPTION'].getValue()
    if 'GENOTYPE' in subject_node.keys():
        subject_nwb.genotype = subject_node['GENOTYPE'].getValue()
    if 'SEX' in subject_node.keys():
        subject_nwb.sex = subject_node['SEX'].getValue()
    if 'SPECIES' in subject_node.keys():
        subject_nwb.species = subject_node['SPECIES'].getValue()
    if 'SUBJECT_ID' in subject_node.keys():
        subject_nwb.subject_id = subject_node['SUBJECT_ID'].getValue()
    if 'WEIGHT' in subject_node.keys():
        subject_nwb.weight = subject_node['WEIGHT'].getValue()
    if 'STRAIN' in subject_node.keys():
        subject_nwb.strain = subject_node['STRAIN'].getValue()
    if 'DATE_OF_BIRTH' in subject_node.keys():
        subject_nwb.date_of_birth = subject_node['DATE_OF_BIRTH'].getValue()
    return subject_nwb
