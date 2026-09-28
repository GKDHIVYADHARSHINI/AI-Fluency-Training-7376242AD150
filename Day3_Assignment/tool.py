def get_course_fee(course):
    fees = {
        "cse": 100000,
        "ece": 90000,
        "mech": 80000
    }
    return str(fees.get(course.lower(), "Course not found"))


def calculator(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid calculation"