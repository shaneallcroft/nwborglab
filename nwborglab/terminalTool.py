import argparse
import orgutils
#from src.orgutils.orgutils import orgutils



def main():
    
    parser = argparse.ArgumentParser('Takes in parameters for skelorg to run')
    parser.add_argument('command',default='translate')
    parser.add_argument('--translator')
    parser.add_argument('--translatee')
    with open(args.translatee) as f:
        org_str_content = str(f.read())
    with open(args.translator) as f:
        org_str_translator = str(f.read())
    #print(dictToHtml(orgutils.orgToDict(filename='test.org'), full_document=True))
    translator = OrgNode(key='html_translate', content=org_str_translator)
    translatee = OrgNode(key=args.org_file, content=org_str_content)
    print(translator.translate(org_to_translate=translatee))

    
    
    
        

    
    
    

if __name__ == '__main__':
    main()
