def convert(string_input):
    string_to_use = string_input.replace(" ", "")
    if string_to_use.find('d') != -1:
        days = string_to_use.split('d')[0]
        remains1 = string_to_use.split('d')[1]
    else:
        days = 0
        remains1 = string_to_use

    if string_to_use.find('h') != -1:
        hours = remains1.split('h')[0]
        remains2 = remains1.split('h')[1]
    else:
        hours = 0
        remains2 = remains1

    if string_to_use.find('m') != -1:
        minutes = remains2.split('m')[0]
        remains3 = remains2.split('m')[1]
    else:
        minutes = 0
        remains3 = remains2

    days_in_seconds = days * 24 * 60 * 60
    hours_in_second = hours * 60 * 60
    minutes_in_second = minutes * 60
    seconds = remains3

    return_seconds = days_in_seconds + hours_in_second + minutes_in_second + seconds
    return return_seconds
