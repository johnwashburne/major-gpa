import requests
import json
import os
from tqdm import tqdm

from course_table import CourseTable, OrGroup

class DegreeProcessor:

    BASE_URL = "https://c4citk6s9k.execute-api.us-east-1.amazonaws.com"
    REQUEST_BASE = "/prod/data/course?courseID="

    def __init__(self, cache_path: str = "cache.json") -> None:
        if os.path.isfile(cache_path):
            with open(cache_path, 'r') as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

        self.cache_path = cache_path

    def get_gpa(self, table: CourseTable) -> float:
        
        requirements = table.get_all_requirements()
        requirement_gpas = []
        for requirement in tqdm(requirements):
            if len(requirement.courses) == 0:
                continue
            try:
                requirement_gpas.append(self.get_requirement_gpa(requirement))
            except Exception as e:
                print(e)

        with open(self.cache_path, 'w') as f:
            json.dump(self.cache, f)

        return sum(requirement_gpas) / len(requirement_gpas)

    def get_requirement_gpa(self, requirement: OrGroup) -> float:

        gpas = []
        for course in requirement.courses:
            try:
                gpas.append(self.get_course_gpa(course.code))
            except Exception as e:
                print(e)
        
        if len(gpas) == 0:
            raise AttributeError(f"None of required courses ({requirement.courses}) could be found")
        return sum(gpas) / len(gpas)
            

    def get_course_gpa(self, course_code: str) -> float:

        if course_code in self.cache.keys():
            return self.cache[course_code]

        if course_code[-1] == "K":
            course_number = course_code[-5:]
            course_abbr = course_code[:-5]
        else:
            course_number = course_code[-4:]
            course_abbr = course_code[:-4]

        course_request= course_abbr + "%20" + course_number
        request_url = self.BASE_URL + self.REQUEST_BASE + course_request
        response = requests.get(request_url).json()

        if len(response['raw']) == 0:
            raise LookupError(f"{course_code} does not exist")

        # rough weighting based on class size estimates 
        total = 0
        students = 0
        for entry in response['raw']:
            size = entry['class_size_group']
            if size == "Very Large (50 students or more)":
                total += entry['GPA'] * 100
                students += 100
            elif size == "Large (31-49 students)":
                total += entry['GPA'] * 40
                students += 40
            elif size == "Mid-Size (21-30 students)" or size == "Mid-size (21-30 students)":
                total += entry['GPA'] * 25
                students += 25
            elif size == "Small (10-20 students)":
                total += entry['GPA'] * 15
                students += 15
            elif size == "Very Small (Fewer than 10 students)" or size == "Very Small (Fewer than 10 Students)":
                total += entry['GPA'] * 5
                students += 5
            else:
                raise ValueError("unknown course size")

        self.cache[course_code] = total / students
        return total / students

if __name__ == "__main__":
    dp = DegreeProcessor()
    print(dp.get_course_gpa("CS3600"))
