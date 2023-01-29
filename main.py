from crawler import BFSCrawler
from degree_processor import DegreeProcessor
import csv

if __name__ == "__main__":
    c = BFSCrawler("https://catalog.gatech.edu/programs/")
    processor = DegreeProcessor()
    course_tables = c.get_course_tables()

    with open("results.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for table in course_tables:
            gpa = processor.get_gpa(table)
            writer.writerow([table.program_name, gpa])
            print(table.program_name, processor.get_gpa(table))