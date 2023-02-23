
import os
import json

_pylint_output_file_path = 'tmp/pylint_output.txt'
score_line_file_path = 'tmp/pylint_score_line.txt'

score_data_file_path = 'docs/pylint_scores.json'

if os.path.exists(score_line_file_path):
    score_line_file = open(score_line_file_path,'r')
    score_line_string = score_line_file.read()

    line_elements = score_line_string.split(' ')

    def extract_score():
        _current_score = line_elements[6]
        _diff = line_elements[10][0:-2]
        return (_current_score,_diff)

    extraction_result = extract_score()

    writable = open(score_data_file_path,'w')

    score_data = json.dumps({"score": extraction_result[0],"diff": extraction_result[1]},indent=4)
    writable.write(score_data)
    writable.close()
    score_line_file.close()

    os.remove(score_line_file_path)
    os.remove(_pylint_output_file_path)
