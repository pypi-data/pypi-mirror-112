def to_12(time_string):
    time_string_to_use = time_string.replace(" ", "")
    hour = time_string_to_use.split(":")[0]
    minute = time_string_to_use.split(":")[1]
    if 0 < hour < 13:
        addition = " AM"
    elif 13 <= hour < 25:
        hour = str(hour - 12)
        addition = " PM"
    elif hour == 0:
        addition = " AM"
        hour = str(12)

    return hour + minute + addition


def to_24(time_string):
    time_string_to_use = time_string.replace(" ", "")
    hour = int(time_string_to_use.split(":")[0])
    temp = time_string_to_use.split(":")[1]
    minute = temp[:-2]
    addition = temp[2:].lower()
    if addition == "am":
        if hour == 12:
            hour = str(0)
        elif 0 < hour < 12:
            hour = str(hour)
    elif addition == "pm":
        if hour == 12:
            hour = str(hour)
        elif 0 < hour < 12:
            hour = str(hour + 12)

    return hour + minute
