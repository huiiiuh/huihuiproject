import re


def validate_phone(phone):
    if re.match('^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\\d{8}$', phone):
        return True
    return False


def validate_email(email):
    if re.match("[\\w!#$%&'*+/=?^_`{|}~-]+(?:\\.[\\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\\w](?:[\\w-]*[\\w])?\\.)+[\\w](?:[\\w-]*[\\w])?", email):
        return True
    return False


if __name__ == '__main__':
    print(validate_email("lx@hd.local"))
