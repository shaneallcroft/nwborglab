from SAPOFTO import SAPOFTO

def applySurvey(survey_sapofto):
    for question_key in survey_sapofto.keys():
        if not survey_sapofto[question_key].hasTag('survey'):
            continue
        question_prompt = survey_sapofto[question_key].getValue()
        survey_sapofto[question_key].setValue(input(question_prompt))
        survey_sapofto.addTag('answered')
        survey_sapofto.removeTag('survey')
    return survey_sapofto
            
        
