from crawler import BFSCrawler
from degree_processor import DegreeProcessor

if __name__ == "__main__":
    c = BFSCrawler("https://catalog.gatech.edu/programs/")
    processor = DegreeProcessor()
    print("retrieving course tables...")
    course_tables = c.get_course_tables()
    print("... course tables retrieved")
    for table in course_tables:
        print(table.program_name, processor.get_gpa(table))