# GT Major GPAs
Georgia Tech publishes the average GPA of all of the courses offered here, with an option to sort by subject. What this doesn't take into account, though, is (1) a student will not take every single course offered with their respective subject code and (2) all students have to take courses that fall outside of their major subject. The only way to get an average GPA that is truly representative of a student's experience within their major is to take the average GPA of all of the requirements within their degree program.<br/><br/>
In order to produce an average that meets this criteria, I would have to determine all of the requirements of a given degree program and which courses can be used to fill that requirement. The GT catalog website does have a table of requirements for each major, but the formatting varies widely and there's many different syntax options to be considered. I created a file (parse_tables.py) to take in a major's catalog URL, find the table containing the major requirement, and parse the table into a program understandable format.<br/><br/>
Next, the average GPA for each of those requirements must be found. GT stores all of there course averages in a website, Course Critique. Course Critique does not have a public API, though, so the GPA data for each course was pulled from their private API (gpa.py) <br/><br/>
Now that average GPA can be found if you feed in a major's catalog URL, the question becomes: How do you get the correct URL for each major program? The Georgia Tech catalog has a page with links to every major program, but the requirements table that we're looking for is usually buried under a few more layers of links. To get around this, I designed a BFS web crawler that starts by scraping all of the links off of the major lists page and using that as the starting point for the queue. Once the queue is initialized, BFS runs by taking in all of the links on the page, determining if a valid requirements table exists on the current page, and continuing onto the next page. The resulting list of major catalog URLs can be found in urls.json.<br/><br/>
Note: this method is certainly not perfect, as it does not account for every single possibility when parsing the requirements table. For example, it does not account for free elective credit hours. However, I felt as though the process provided an adequete approximation for the purposes of this project.<br/><br/>
The histogram below shows the approximately normal distribution of the calculated GPAs:
![histogram](http://url/to/img.png)

The list of calculates major GPAs is below: 
Major Program | Average GPA
---- | ----
Computational Media - People-Interaction Design | 3.502
Industrial Design | 3.501
Architecture | 3.493
Computational Media - People-Games | 3.492
Computational Media - Music Technology-People | 3.485
Computational Media - Intelligence-Interaction Design | 3.474
Computational Media - Media-Interaction Design | 3.474
 Business Administration - Strategy and Innovation | 3.467
Computational Media - Media-Games | 3.461
History, Technology, and Society | 3.459
Computational Media - Intelligence - Games | 3.456
Computational Media - People-Film & Media Studies | 3.454
Computational Media- Music Technology-Media  | 3.44
Business Administration - Marketing | 3.437
Computational Media- Music Technology-Intelligence | 3.434
Computational Media - Intelligence-Film & Media Studies | 3.422
Computational Media - Media-Film & Media Studies | 3.415
Business Administration - Finance | 3.409
Music Technology - General | 3.409
Business Administration - Leadership and Organizational Change | 3.406
Neuroscience | 3.4
Business Administration - Operations and Supply Chain Management | 3.394
Business Administration - Information Technology Management | 3.381
Music Technology - Electrical and Computer Engineering: Signal Processing | 3.379
Building Construction | 3.376
Business Administration - General Management | 3.375
Biology - General | 3.37
Biology - Business Option | 3.367
Business Administration - Accounting | 3.353
Music Technology - Mechanical Engineering: Controls and Robotics | 3.343
Chemistry - Pre-Health Option | 3.322
Economics and International Affairs | 3.315
Computer Science - Thread: People & Systems and Architecture | 3.313
Music Technology - Mechanical Engineering: Acoustics and Vibrations | 3.308
Computer Science - Thread: Devices & People | 3.305
Computer Science - Thread: Devices & Information Internetworks | 3.303
Computer Science - Thread: Modeling-Simulation & People | 3.302
Computer Science - Thread: Theory & People | 3.301
Computer Science - Thread: Devices & Intelligence | 3.299
Computer Science - Thread: Intelligence & People | 3.299
Civil Engineering - Construction and Infrastructure Systems Engineering | 3.299
Computer Science - Thread: Devices & Systems and Architecture | 3.293
Computer Science - Thread: Information Internetworks & People | 3.288
Computer Engineering - Distributed System & Software Design and Devices | 3.286
Computer Engineering - Cybersecurity and Devices | 3.284
Computer Science - Thread: Modeling-Simulation & Devices | 3.282
Computer Science - Thread: Intelligence & Systems and Architecture | 3.282
Biochemistry - Business Option | 3.281
Computer Engineering - Distributed System & Software Design and Information Internetworks | 3.28
Computer Science - Thread: Media & People | 3.279
Computer Science - Thread: Information Internetworks & Systems and Architecture | 3.279
Computer Science - Thread: Information Internetworks & Intelligence | 3.279
Computer Engineering - Distributed System & Software Design and Systems & Architecture | 3.279
Computer Engineering - Cybersecurity and Information Internetworks | 3.278
Computer Science - Thread: Devices & Media | 3.278
Computer Engineering - Cybersecurity and Distributed System & Software Design | 3.277
Computer Engineering - Cybersecurity and Systems & Architecture | 3.277
Applied Physics - Physics of Living Systems | 3.277
Computer Science - Thread: Intelligence & Media | 3.276
Computer Science - Thread: Theory & Intelligence | 3.274
Computer Science - Thread: Modeling - Simulation & Systems and Architecture | 3.273
Computer Science - Thread: Devices & Theory | 3.272
Biochemistry - Pre-Health Option | 3.271
Biochemistry - General | 3.27
Computer Science - Thread: Modeling-Simulation & Intelligence | 3.269
Computer Science - Thread: Theory & Systems and Architecture | 3.268
Computer Science - Thread: Media & Systems and Architecture | 3.266
Materials Science and Engineering - Polymer and Fiber Materials | 3.265
Computer Science - Thread: Modeling-Simulation & Information Internetworks | 3.265
Computer Engineering - Computing Hardware & Emerging Architectures and Devices | 3.264
Computer Science - Thread: Information Internetworks & Media | 3.262
Computer Science - Thread: Theory & Media | 3.261
Computer Science - Thread: Theory & Information Internetworks | 3.259
Computer Engineering - Computing Hardware & Emerging Architectures and Information Internetworks | 3.258
Computer Engineering - Computing Hardware & Emerging Architectures and Systems & Architecture | 3.258
Computer Science - Distributed System & Software Design and Computing Hardware & Emerging Architectures | 3.257
Computer Engineering- Cybersecurity and Computing Hardware & Emerging Architectures | 3.255
Industrial Engineering - Supply Chain Engineering | 3.254
Earth and Atmospheric Sciences - Business Option | 3.253
Biomedical Engineering | 3.253
Computer Science - Thread: Modeling-Simulation & Theory | 3.252
Computer Science - Thread: Modeling and Simulation & Media | 3.25
Industrial Engineering -  Quality and Statistics | 3.244
Mechanical Engineering - Automotive | 3.243
Computer Engineering - Distributed System & Software Design and Signal & Information Processing | 3.24
Mathematics - Probability and Statistics | 3.239
Computer Engineering - Cybersecurity and Signal & Information Processing | 3.238
Earth and Atmospheric Sciences - General | 3.234
Physics - Physics of Living Systems  | 3.234
Industrial Engineering - Analytics and Data Science | 3.234
Mathematics - Business Option | 3.233
Nuclear and Radiological Engineering - Radiological Science and Engineering concentration | 3.232
Industrial Engineering - General | 3.23
Computer Engineering - Distributed System & Software Design and Robotics & Autonomous Systems | 3.228
Chemistry - Polymers and Materials Option | 3.227
Computer Engineering - Distributed System & Software Design and Telecommunications | 3.226
Mathematics - Applied Mathematics  | 3.226
Computer Engineering - Cybersecurity and Robotics & Autonomous Systems | 3.226
Computer Engineering - Cybersecurity and Telecommunications | 3.225
Mathematics - General | 3.222
Materials Science and Engineering - Structural and Functional Materials | 3.222
Computer Engineering - Computing Hardware & Emerging Architectures and Signal & Information Processing | 3.219
Applied Physics - Business Option | 3.219
Industrial Engineering - Economic and Financial Systems | 3.218
Chemistry - Biochemistry Option | 3.217
Mechanical Engineering - Manufacturing | 3.216
Electrical Engineering - Bioengineering and Sensing & Exploration | 3.21
Computer Engineering - Computing Hardware & Emerging Architectures and Robotics & Autonomous Systems  | 3.207
Applied Physics - General | 3.207
Mechanical Engineering - Micro- and Nanoengineering | 3.206
Computer Engineering - Computing Hardware & Emerging Architectures and Telecommunications | 3.206
Electrical Engineering - Signal & Information Processing and Sensing & Exploration  | 3.204
Materials Science and Engineering - Biomaterials | 3.203
Nuclear and Radiological Engineering - Nuclear Engineering Concentration | 3.202
Chemistry - Business Option | 3.194
Electrical Engineering - Signal & Information Processing and Bioengineering | 3.193
Electrical Engineering - Robotics & Autonomous Systems and Sensing & Exploration | 3.191
Mathematics - Discrete Mathematics | 3.19
Electrical Engineering - Circuit Technology and Sensing & Exploration | 3.19
Electrical Engineeering - Electronic Devices and Sensing & Exploration | 3.189
Electrical Engineering - Sensing & Exploration and Telecommunications | 3.189
Aerospace Engineering | 3.185
Electrical Engineering - Electric Energy Systems and Sensing & Exploration | 3.181
Electrical Engineering - Robotics & Autonomous Systems and Bioengineering  | 3.18
Environmental Engineering | 3.179
Electrical Engineering - Circuit Technology and Bioengineering | 3.178
Electrical Engineering - Electronic Devices and Bioengineering | 3.178
Electrical Engineering - Bioengineering and Telecommunications | 3.178
Mathematics - Pure Mathematics | 3.176
Physics - Business Option | 3.174
Electrical Engineering - Signal & Information Processing and Robotics & Autonomous Systems  | 3.174
Electrical Engineering - Signal & Information Processing and Circuit Technology | 3.172
Mechanical Engineering - Nuclear and Radiological Engineering | 3.172
Electrical Engineering - Signal & Information Processing and Electronic Devices  | 3.172
Electrical Engineering - Signal & Information Processing and Telecommunications  | 3.172
Electrical Engineering - Electric Energy Systems and Bioengineering | 3.17
Mechanical Engineering - Thermal, Fluid, & Energy Systems | 3.17
Mechanical Engineering - Automation and Robotic Systems | 3.167
Civil Engineering (Standard) | 3.166
Mechanical Engineering - Design | 3.166
Chemistry - General  | 3.164
Electrical Engineering - Electric Energy Systems and Signal & Information Processing | 3.164
Electrical Engineering - Robotics & Autonomous Systems and Circuit Technology | 3.16
Electrical Engineering - Robotics & Autonomous Systems and Electronic Devices  | 3.16
Mechanical Engineering - Mechanics of Materials | 3.16
Electrical Engineering - Robotics & Autonomous Systems and Telecommunications | 3.16
Electrical Engineering - Electronic Devices and Circuit Technology  | 3.158
Electrical Engineering - Circuit Technology and Telecommunications | 3.158
Electrical Engineering - Electronic Devices and Telecommunications | 3.158
Mechanical Engineering - General | 3.158
Physics - General | 3.156
Electrical Engineering - Robotics & Autonomous Systems and Electric Energy Systems | 3.152
Electrical Engineering - Electric Energy Systems and Circuit Technology | 3.15
Electrical Engineering - Electric Energy Systems and Electronic Devices  | 3.15
Electrical Engineering - Electric Energy Systems and Telecommunications | 3.15
Physics - Astrophysics | 3.146
Chemical and Biomolecular Engineering - Biotechnology Option | 3.071
Chemical and Biomolecular Engineering - Standard Option | 3.071
