import json
import requests
from parse_tables import scrape
import bs4 as bs
import csv

# GT Course Critique private api base
base_url = "https://c4citk6s9k.execute-api.us-east-1.amazonaws.com/prod/data/course?courseID="

# O(1) string digit lookup
digits = set(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])

# valid course catalog urls found by crawler.py
with open("../crawler/urls.json", "r") as read_file:
    program_urls = json.load(read_file)

# course GPA caching and failed course GPA caching
with open("cache.json", "r") as read_file:
    cache = json.load(read_file)


with open("error_cache.json", "r") as read_file:
    error_set = set(json.load(read_file))


# probably should be replaced with regex matching
def is_course(s):
    return not (s[-1] not in digits or s[-2] not in digits
                or s[-3] not in digits or s[-4] not in digits
                or s[:2] == 'or')


def get_course_gpa(course):

    # O(1) cache lookup
    if course in cache.keys():
        return cache[course]['gpa'], cache[course]['credits']
    elif course in error_set:
        raise LookupError

    # call Course Critique private api
    url = base_url + course
    response = requests.get(url).json()
    total = 0
    students = 0
    if 'raw' not in response.keys() or response['raw'] is None:
        error_set.add(course)
        raise LookupError

    # rough weighting based on class size estimates 
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
            print(size)

    # return and cache
    if students != 0:
        cache[course] = {}
        cache[course]['gpa'] = total / students
        cache[course]['credits'] = response['header'][0]['credits']
        return total / students, response['header'][0]['credits']
    else:
        error_set.add(course)
        raise LookupError(str(course) + " not found")


def get_major_gpa(catalog_url):

    # retreive course requirements
    requirements = scrape(catalog_url)
    major_gpa = 0
    major_credits = 0

    # some courses are very free elective heavy - no need to consider these
    if len(requirements) < 20:
        raise LookupError

    # iterate through each requirement
    # find average gpa of all courses that fulfill that requirement
    for requirement in requirements:
        requirement_gpa = 0
        requirement_credits = 0
        count = 0
        for course in requirement:
            try:
                gpa, credits = get_course_gpa(course)
                requirement_gpa += gpa * credits
                requirement_credits += credits
                count += 1
            except LookupError:
                continue
            except TypeError:
                requirement_credits = 0

        if requirement_credits != 0:
            requirement_gpa /= requirement_credits
            major_gpa += requirement_gpa * (requirement_credits / count)
            major_credits += (requirement_credits / count)

    # rewrite cache after every major completion
    with open("cache.json", "w") as write_file:
        json.dump(cache, write_file)

    with open("error_cache.json", "w") as write_file:
        json.dump(list(error_set), write_file)

    return major_gpa / major_credits


# additional request to catalog url to retreive name
# could probably be bundled with the other request but this is easier
def get_major_name(url):
    response = requests.get(url)
    source = bs.BeautifulSoup(response.text, 'lxml').find(id="col-content")
    name = source.find(class_="page-title").text
    return name


if __name__ == "__main__":

    # iterate through all degree programs, find gpa, and write to csv
    rows = []
    for program in program_urls:
        try:
            gpa = get_major_gpa(program)
            name = get_major_name(program)
            rows.append([name, gpa])
            print(name, round(gpa, 2))
        except LookupError:
            continue

    with open('results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile,  delimiter=',')
        for row in rows:
            csvwriter.writerow(row) 
