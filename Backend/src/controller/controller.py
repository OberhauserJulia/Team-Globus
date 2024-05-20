
from service.homerwork_service import safe_math_homework_service

def safe_homework(classname) : 
    if classname == "math": 
        return safe_math_homework_service() 
