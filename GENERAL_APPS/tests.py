def manage_checklist(text, user):
    res_message = {
        "status": False,
        "message": ""
    }

    text = text.strip()
    match = re.match(r'^\S+', text)
    template = {
        "Name": "",
        "Items": [],
        "message": '',
        "status": False
    }
    if match:
        if match.group().lower() == 'create':
            checklist_pattern = r'(?<=list)(.*?)(?=\n)'
            match = re.search(checklist_pattern, text)
            if match and len(match.group(1).strip()) > 1:
                template['Name'] = match.group(1).strip()
                checklist_item = r'(?<=\n)(.*?)(?=\n)'
                matches = re.findall(checklist_item, text)
                try:
                    for i, line in enumerate(matches, 1):
                        template['Items'].append(line.strip())
                    last_line_pattern = r'(?<=\n)[^\n]*$'
                    last_line_match = re.search(last_line_pattern, text)
                    if last_line_match:
                        template['Items'].append(last_line_match.group())
                    return save_check_list(template, user)

                except Exception as e:
                    res_message['status'] = True
                    res_message['message'] = f'Exception {e}'
            else:
                res_message['status'] = False
                res_message['message'] = "Opps template Name couldn't find in the prompt"
        elif match.group().lower() == 'delete':
            match = re.search(r'delete\s+(.+)', text, re.IGNORECASE)
            if match:
                print(match.group(1))

            res_message['status'] = False
            res_message['message'] = f"delete  {match.group(1)} {record}"
        elif match.group().lower() == 'rename':
            res_message['status'] = False
            res_message['message'] = "rename check"
        else:
            res_message['status'] = False
            res_message['message'] = "Opps I am not sure about this prompt !"

        return res_message

    else:
        template['status'] = False
        template['message'] = "E-Opps I am not sure about this prompt !"