# GT Major GPAs
I was discussing with a friend whether which degree program is the most difficult at Georgia Tech and thought it would be cool to add an element of data to the discussion. While it is impossible to come to a conclusive answer to that question due to many different factors such as students having different talents and learning specific subjects easier than others, the main "concrete" metric that is seen by many students to represent difficulty is average GPA. At the very minimum, it would be a interesting topic to explore._
Georgia Tech publishes the average GPA of all of the courses offered here, with an option to sort by subject. What this doesn't take into account, though, is (1) a student will not take every single course offered with their respective subject code and (2) all students have to take courses that fall outside of their major subject. The only way to get an average GPA that is truly representative of a student's experience within their major is to take the average GPA of all of the requirements within their degree program. __
So, in order to produce an average that meets this criteria, I would have to find a way to determine all of the requirements of a given degree program, what courses can be used to fill that requirement, and the credit hours of each requirement. The GT catalog website does have a table of requirements for each major, but the formatting varies widely and there's many different syntax options to be considered. I created a file (parse_tables.py) to take in a major url, look for tables that could hold the degree requirements, and parse those tables into a list of tuples where each tuple in the list represents one requirement and each element in the tuple is a course that can be used to fill the requirement.__
Next, the average GPA for each of those requirements must be found. GT stores all of there course averages in a website, Course Critique. Course Critique does not have a public API, though, and the data that can be pulled through their private API is not nearly as structured as it appears on the website. So, I had to pull their data and then recalculate average GPA. I could have also used a scraping tool to pull directly from their front-end, but that would not have been nearly as efficient. Once the average GPA for each course is found, the average for that particular major program can be calculated pretty easily.__
Now that average GPA can be found if you feed in the correct url, the question becomes: How do you get the correct URL for each major program? The Georgia Tech catalog has a page with links to every major program, but the requirements table that we're looking for is usual buried under a few more layers of links. To get around this, I designed a BFS web crawler that starts by scraping all of the links off of the major lists page and using that as the starting point for the queue. Once the queue is initialized, BFS runs by taking in all of the links on the page, determining if a course list exists on the current page, and never navigatig off of the catalog website. By taking these steps, the list of urls found in urls.json was produced.
The list of major GPAs calculated by the above method is below: 