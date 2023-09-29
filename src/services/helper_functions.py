from datetime import datetime

def string_to_time_foramt(date_time: str):

    dt_object = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%f")
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")

def time_format_to_string(date_time: datetime):

    return date_time.strftime('%Y-%m-%d %H:%M:%S')
