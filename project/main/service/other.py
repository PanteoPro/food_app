from datetime import datetime, timedelta


def get_start_today():
    """Возвращаяет datetime начала текущего дня 00:00:00.000000"""
    today = datetime.now()
    today -= timedelta(hours=today.hour, minutes=today.minute, seconds=today.second, microseconds=today.microsecond)
    return today


def get_end_today():
    """Возвращаяет datetime конец текущего дня 23:59:59.999999"""
    today = datetime.now()
    today += timedelta(hours=23-today.hour, minutes=59-today.minute, seconds=59-today.second,
                       microseconds=999999-today.microsecond)
    return today


def get_path_for_avatar(instance, filename) -> str:
    """
        Возвращает строку названия файла
        Функция, которая перехватывает поведение upload_to в модели profile
        Изменяет название файла на шаблон: avatar_profile_id_1.(jpg,png)
    """
    ext = filename.split(".")[1]
    filename = f"avatar_profile_id_{instance.id}.{ext}"
    return f"avatars/{filename}"
