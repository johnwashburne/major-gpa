import aiohttp
import asyncio
import json
import os

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
        # ensure async operations run without warning on Windows
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        gpa = asyncio.run(self._get_gpa(table))
        with open(self.cache_path, 'w') as f:
            json.dump(self.cache, f)

        return gpa

    async def _get_gpa(self, table: CourseTable) -> float:
        
        async with aiohttp.ClientSession(self.BASE_URL) as session:
            requirements = table.get_all_requirements()
            if len(requirements) == 0:
                return None
            
            coros = []
            for requirement in requirements:
                if len(requirement.courses) == 0:
                    continue
                coros.append(self.get_requirement_gpa(requirement, session))

            requirement_gpas = await asyncio.gather(*coros, return_exceptions=True)

        results = []
        for requirement_gpa in requirement_gpas:
            if isinstance(requirement_gpa, Exception):
                print(requirement_gpa)
            else:
                results.append(requirement_gpa)
        return sum(results) / len(results)

    async def get_requirement_gpa(self, requirement: OrGroup, session: aiohttp.ClientSession) -> float:

        gpas = []
        for course in requirement.courses:
            gpas.append(await self.get_course_gpa(course.code, session))
        
        sm = 0
        count = 0
        for gpa in gpas:
            if isinstance(gpa, Exception):
                print(gpa)
            else:
                sm += gpa
                count += 1
        
        if count == 0:
            raise AttributeError(f"no gpa could be found for requirement fulfilled by {requirement.courses}")
        return sm / count
            

    async def get_course_gpa(self, course_code: str, session: aiohttp.ClientSession) -> float:

        if course_code in self.cache.keys():
            return self.cache[course_code]

        if course_code[-1] == "K":
            course_number = course_code[-5:]
            course_abbr = course_code[:-5]
        else:
            course_number = course_code[-4:]
            course_abbr = course_code[:-4]

        course_request= course_abbr + "%20" + course_number
        request_url = self.REQUEST_BASE + course_request
        async with session.get(request_url) as resp:
            response = await resp.json()

        while 'raw' not in response.keys():
            time = 1
            async with session.get(request_url) as resp:
                await asyncio.sleep(time)
                time *= 2
                print("retrying", course_code)
                response = await resp.json()

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
