import re

text = '''checklist teste
adasfsaf       
afsfsf         
sdfsds         
ok nok'''


def create_or_add_checklist(text):
    checklist = {
        "Name": "",
        "Items": []
    }
    checklist_pattern = r'(?<=checklist)(.*?)(?=\n)'
    match = re.search(checklist_pattern, text)
    if match:
        checklist['Name'] = match.group(1).strip()
        checklist_item = r'(?<=\n)(.*?)(?=\n)'
        matches = re.findall(checklist_item, text)
        for i, line in enumerate(matches, 1):
            checklist['Items'].append(line.strip())
        last_line_pattern = r'(?<=\n)[^\n]*$'
        last_line_match = re.search(last_line_pattern, text)
        if last_line_match:
            checklist['Items'].append(last_line_match.group())
    print(checklist)
    return checklist


create_checklist(text)
