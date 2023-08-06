import directory


def time_for_calculate(time_string):
    time_split = time_string.split(':')
    hour = int(time_split[0])
    minute = int(time_split[1])
    return hour, minute


def input_for_convert(from_country, from_time, to_country):
    from_country_timezone = directory.country_and_time[from_country.lower()]
    to_country_timezone = directory.country_and_time[to_country.lower()]
    from_time = from_time.replace(" ", "")

    from_country_tzhour = time_for_calculate(from_country_timezone[0])
    from_country_tzminute = time_for_calculate(from_country_timezone[1])
    to_country_tzhour = time_for_calculate(to_country_timezone[0])
    to_country_tzminute = time_for_calculate(to_country_timezone[1])

    from_time_hour = time_for_calculate(from_time[0])
    from_time_minute = time_for_calculate(from_time[1])

    time_difference_hours = from_country_tzhour - to_country_tzhour
    time_difference_minutes = from_country_tzminute - to_country_tzminute
    to_time_hours = from_time_hour - time_difference_hours
    to_time_minutes = from_time_minute - time_difference_minutes

    if to_time_minutes < 0:
        to_time_hours = to_time_hours - 1
        to_time_minutes = to_time_minutes + 60

    elif to_time_minutes > 60:
        to_time_hours = to_time_hours + 1
        to_time_minutes = to_time_minutes - 60

    if to_time_hours < 0:
        to_time_hours = to_time_hours + 24
        additional_info = " in the previous day."

    elif to_time_hours > 23:
        to_time_hours = to_time_hours - 24
        additional_info = " in the next day."

    else:
        additional_info = ""

    to_time = f"{to_time_hours}:{to_time_minutes}{additional_info}"

    return to_time


#and this is the calculation place
