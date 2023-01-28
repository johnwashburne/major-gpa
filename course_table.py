import bs4 as bs
from typing import List


class Course:

    name: str
    code: str
    hours: int

    def __init__(self, name: str, code: str, hours: int) -> None:
        self.name = name
        self.code = "".join(code.split())
        self.hours = hours

    def __repr__(self) -> str:
        return self.code


class OrGroup:

    courses: List[Course]
    
    def __init__(self, or_group: List[bs.element.Tag]) -> None:
        self.courses = []

        for tr in or_group:
            tds = tr.find_all('td')
            if len(tds) == 3:
                code = tds[0].text
                name = tds[1].text
                hours = tds[2].text
                self.courses.append(Course(name, code, hours))
            elif len(tds) == 2 and "orclass" in tr.get("class"):
                code = tds[0].text.replace("or", "")
                name = tds[1].text
                self.courses.append(Course(name, code, hours))

            # TODO: handle Any HUM, Any SS, options

class CoreArea:

    name: str
    requirements: List[OrGroup]

    def __init__(self, name: str, core_area: List[List[bs.element.Tag]]) -> None:
        self.name = name
        self.requirements = []
        for or_group in core_area:
            self.requirements.append(OrGroup(or_group))


class CourseTable:
    """
    A class to hold contain course table information for a degree program
    """
    program_name: str
    core_areas: List[CoreArea]

    def __init__(self, program_name: str, table_html: bs.element.Tag) -> None:
        self.program_name = program_name
        self.core_areas = []
        self._process_table(table_html)
        
    def _process_table(self, table_html: bs.element.Tag):

        curr_core_area = []
        curr_core_area_name = ""

        table_body = table_html.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            if 'areaheader' in row.get('class'):
                if len(curr_core_area) != 0:
                    self.core_areas.append(CoreArea(curr_core_area_name, curr_core_area))

                curr_core_area = []
                curr_core_area_name = row.find('td').text
                continue
            elif 'orclass' in row.get('class'):
                curr_core_area[-1].append(row)
            elif 'listsum' in row.get('class'):
                pass
            else:
                curr_core_area.append([row])

    def get_all_requirements(self) -> List[OrGroup]:

        res = []
        for core_area in self.core_areas:
            res.extend(core_area.requirements)

        return res

    def is_valid(self) -> bool:
        return len(self.get_all_requirements()) != 0