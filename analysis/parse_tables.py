import requests
from bs4 import BeautifulSoup as bs

url = 'https://catalog.gatech.edu/programs/neuroscience-bs/'
digits = set(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])

# copy pasted decode function from stack overflow
def remove_non_ascii(s):
    return "".join(c for c in s if ord(c) < 128)

# determine whether a string represents a course number
def is_course_number(s):
    if len(s) != 4:
        return False

    for c in s:
        if c not in digits:
            return False

    return True


# split a course into subject and number
def course_num_split(s):
    course = ""
    num = ""
    i = 0
    while i < len(s):
        if s[i] in digits:
            break
        course += s[i]
        i += 1
    
    while i < len(s):
        num += s[i]
        i += 1

    return course + " " + num


# scrape the course tables from a given url
def scrape(url):
    all_courses = []

    page = requests.get(url)
    data = bs(page.text, 'lxml')
    tables = data.find_all('table', class_='sc_courselist')

    for table in tables:
        courses = []
        rows = table.find_all('tr')

        for row in rows:
            td = row.find_all('td')
            current = [j.text for j in td]
            if len(current) > 0:
                courses.append(current[0])

        all_courses.append(courses)

    # there could be more course tables then just the requirements
    # in most cases, taking the largest course table works
    largest = all_courses[0]
    for course_list in all_courses:
        if len(course_list) >= len(largest):
            largest = course_list

    return parse(largest)


# parse the raw data from the first column of the course table
def parse(courses):

    # decode unicode strings
    i = 0
    while i < len(courses):
        courses[i] = remove_non_ascii(courses[i])
        i += 1


    i = 0
    res = []
    while i < len(courses):
        current = []
        if courses[i][:6] == "Select" or courses[i][:6] == "Choose":

            # case where table gives many options to fulfill a requirement
            two = False
            if courses[i][:10] == "Select two" or courses[i][:10] == "Choose two":
                two = True

            i += 1

            while is_course_number(courses[i][-4:]):
                if courses[i][:2] == "or":
                    current.append(course_num_split(courses[i][2:]))
                else:
                    current.append(course_num_split(courses[i]))

                i += 1
            i -= 1

            res.append(tuple(current))

            # double weight if two courses are needed
            if two:
                res.append(tuple(current))

        elif i + 1 < len(courses) and courses[i+1][:2] == "or":
            # case where table gives many options to fulfill a requirement using the 'or' syntax
            current.append(course_num_split(courses[i]))
            i += 1
            while courses[i][:2] == "or":
                current.append(course_num_split(courses[i][2:]))
                i += 1
            i -= 1
            res.append(tuple(current))
        elif is_course_number(courses[i][-4:]):
            # regular 1 course case
            current.append(course_num_split(courses[i]))
            res.append(tuple(current))

        i += 1

    return res


if __name__ == "__main__":
    courses = scrape(url)
    for course in courses:
        print(course)