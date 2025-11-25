insert into department(dept_name, building, budget) values ('Psychology', 'Denise hall', 90000);
insert into department(dept_name, building, budget) values ('Engineering', 'Paris hall', 89000);
insert into department (dept_name, building, budget) values
('Computer Science', 'Mathematical Sciences Building', 99000000),
('Architecture', 'Center for Architecture and Environmental Design', 750000),
('Biology', 'Cunningham Hall', 800000),
('Chemistry', 'Integrated Sciences Building', 950000),
('Business', 'Business Administration Building', 700000),
('Sociology', 'Merrill Hall', 650000),
('Nursing', 'Henderson Hall', 980000);


insert into student (first_name, last_name, dept_name, tot_credits) values ('Will', 'Smith', 'Biology', 29);
insert into student (first_name, last_name, dept_name, tot_credits) values ('Ryan', 'Reynolds', 'Engineering', 48);
insert into student (first_name, last_name, dept_name, tot_credits) values ('Kevin', 'Hart', 'Nursing', 70);
insert into student (first_name, last_name, dept_name, tot_credits) values ('Jennifer', 'Lawrence', 'Computer Science', 14);
insert into student (first_name, last_name, dept_name, tot_credits) values ('Robert', 'Irwin', 'Psychology', 87);
insert into student (first_name, last_name, dept_name, tot_credits) values
('Danielle', 'Clason', 'Computer Science', 94),
('Tessa', 'Wood', 'Computer Science', 103),
('Ashlee', 'Cunningham', 'Computer Science', 99),
('Leah', 'Brechtelsbauer', 'Architecture', 45),
('Mikayla', 'Zagar', 'Architecture', 60),
('Anthony', 'Maricocchi', 'Architecture', 65),
('Madelyn', 'Lawrence', 'Biology', 94),
('Sarah', 'Becker', 'Biology', 87),
('Marley', 'Nash', 'Biology', 93),
('Sofia', 'DeCola', 'Chemistry', 105),
('Riley', 'Kuwatch', 'Chemistry', 104),
('Giana', 'Nakoul', 'Chemistry', 95),
('Payton', 'Factor', 'Business', 107),
('Dakota', 'Whitacre', 'Business', 101),
('Anthony', 'Mast', 'Business', 98),
('Samuel', 'Garcia', 'Sociology', 85),
('Charleigh', 'Riffle', 'Sociology', 110),
('Jenna', 'Hall', 'Sociology', 47),
('Sadie', 'Ahbel', 'Nursing', 80),
('Abigal', 'Coblentz', 'Nursing', 53),
('Vivian', 'Coblentz', 'Nursing', 40);

insert into instructor(first_name, last_name, dept_name, salary) values ('Mckenna', 'Grace', 'Biology', 120000);
insert into instructor(first_name, last_name, dept_name, salary) values ('Mason', 'Thames', 'Computer Science', 100000);
insert into instructor(first_name, last_name, dept_name, salary) values ('Dave', 'Franco', 'Nursing', 140000);
insert into instructor(first_name, last_name, dept_name, salary) values ('Dakota', 'Johnson', 'Psychology', 60000);
insert into instructor(first_name, last_name, dept_name, salary) values ('Jamie', 'Dorman', 'Engineering', 70000);

insert into instructor (first_name, last_name, dept_name, salary) values
('Alan', 'Turing', 'Computer Science', 99000),
('Ada', 'Lovelace', 'Computer Science', 95000),
('Frank', 'Wright', 'Architecture', 75000),
('Zaha', 'Hadid', 'Architecture', 70000),
('Charles', 'Darwin', 'Biology', 80000),
('Rachel', 'Carson', 'Biology', 75000),
('Marie', 'Curie', 'Chemistry', 95000),
('Dmitri', 'Mendeleev', 'Chemistry', 90000),
('Warren', 'Buffet', 'Business', 70000),
('Bill', 'Gates', 'Business', 65000),
('Auguste', 'Comte', 'Sociology', 65000),
('Emile', 'Durkheim', 'Sociology', 60000),
('Florence', 'Nightingale', 'Nursing', 98000),
('Clara', 'Barton', 'Nursing', 93000);

insert into course(course_id, title, dept_name, credits) values ('1003', 'Intro to Nursing', 'Nursing', 3);
insert into course(course_id, title, dept_name, credits) values ('1002', 'Intro to Database', 'Computer Science', 3);
insert into course(course_id, title, dept_name, credits) values ('1004', 'Anatomy', 'Biology', 3);
insert into course(course_id, title, dept_name, credits) values ('1005', 'Data Recognition', 'Psychology', 4);
insert into course(course_id, title, dept_name, credits) values ('2006', 'Solid Mechanics', 'Engineering', 4);
insert into course(course_id, title, dept_name, credits) values ('4505', 'Differential Equations', 'Engineering', 4);
insert into course(course_id, title, dept_name, credits) values ('3432', 'Linear Algebra', 'Computer Science', 4);

insert into course (course_id, title, dept_name, credits) values
('CS-101', 'Computer Science I', 'Computer Science', 4),
('CS-102', 'Computer Science II', 'Computer Science', 4),
('ARCH-101', 'Design Studio I', 'Architecture', 4),
('ARCH-102', 'Design Studio II', 'Architecture', 4),
('BIO-101', 'Biological Diversity', 'Biology', 4),
('BIO-102', 'Biological Foundations', 'Biology', 4),
('CHEM-101', 'General Chemistry I', 'Chemistry', 3),
('CHEM-102', 'General Chemistry II', 'Chemistry', 3),
('BUS-101', 'Introduction to Business', 'Business', 3),
('BUS-102', 'Introduction to Marketing', 'Business', 3),
('SOC-101', 'Introduction to Sociology', 'Sociology', 3),
('SOC-102', 'Social Problems', 'Sociology', 3),
('NURS-101', 'Introduction to Professional Nursing Practice', 'Nursing', 3),
('NURS-201', 'Clinical Calculations in Nursing I', 'Nursing', 3);

insert into time_slot (time_slot_id, days, start_hr, start_min, end_hr, end_min) values
('A', 'M,W,F', 09, 00, 09, 50),
('B', 'M,W,F', 11, 00, 11, 50),
('C', 'M,W,F', 12, 15, 13, 10),
('D', 'M,W,F', 14, 00, 14, 50),
('E', 'T,R', 09, 15, 10, 30),
('F', 'T,R', 11, 00, 12, 15),
('G', 'T,R', 13, 00, 14, 15),
('H', 'T,R', 15, 15, 16, 30);

insert into classroom(building,room_number,capacity) values ('William Hall', 21 , 100);
insert into classroom(building,room_number,capacity) values ('Steward Hall', 122 , 200);
insert into classroom(building,room_number,capacity) values ('Denise Hall', 217 , 250);
insert into classroom(building,room_number,capacity) values ('Henderson Hall', 54, 100);
insert into classroom(building,room_number,capacity) values ('Paris Hall', 312 , 145);

insert into classroom (building, room_number, capacity) values
('Mathematical Sciences Building', 210, 150),
('Center for Architecture and Environmental Design', 305, 150),
('Cunningham Hall', 110, 150),
('Integrated Sciences Building', 108, 150),
('Business Administration Building', 103, 150),
('Business Administration Building', 207, 150),
('Merrill Hall', 112, 30),
('Merrill Hall', 125, 30),
('Henderson Hall', 105, 30),
('Henderson Hall', 213, 30);

insert into section(course_id, semester, year, building, room_number, time_slot_id) values ('1003','Fall', 2025, 'Henderson Hall', 54,'A');
insert into section(course_id, semester, year, building, room_number, time_slot_id) values ('1002','Fall', 2025, 'William Hall', 21,'B');
insert into section(course_id, semester, year, building, room_number, time_slot_id) values ('1004','Fall', 2025, 'Steward Hall', 122,'A');
insert into section(course_id, semester, year, building, room_number, time_slot_id) values ('1005','Fall', 2025, 'Denise Hall', 217,'E');
insert into section(course_id, semester, year, building, room_number, time_slot_id) values ('2006','Spring', 2026, 'Paris Hall', 312,'D');
insert into section(course_id, semester, year, building, room_number, time_slot_id) values ('4505','Fall', 2025, 'Paris Hall', 312,'C');
insert into section(course_id, semester, year, building, room_number, time_slot_id) values ('3432','Spring', 2026, 'William Hall', 21,'B');

insert into section (course_id, semester, year, building, room_number, time_slot_id) values
('CS-101', 'Spring', 2026, 'Mathematical Sciences Building', 210, 'A'),
('CS-101', 'Spring', 2026, 'Mathematical Sciences Building', 210, 'E'),
('CS-102', 'Spring', 2026, 'Mathematical Sciences Building', 210, 'B'),
('CS-102', 'Spring', 2026, 'Mathematical Sciences Building', 210, 'F'),
('CS-101', 'Fall', 2026, 'Mathematical Sciences Building', 210, 'A'),
('CS-101', 'Fall', 2026, 'Mathematical Sciences Building', 210, 'E'),
('CS-102', 'Fall', 2026, 'Mathematical Sciences Building', 210, 'B'),
('CS-102', 'Fall', 2026, 'Mathematical Sciences Building', 210, 'F'),
('ARCH-101', 'Spring', 2026, 'Center for Architecture and Environmental Design', 305, 'A'),
('ARCH-102', 'Spring', 2026, 'Center for Architecture and Environmental Design', 305, 'H'),
('ARCH-101', 'Fall', 2026, 'Center for Architecture and Environmental Design', 305, 'A'),
('ARCH-102', 'Fall', 2026, 'Center for Architecture and Environmental Design', 305, 'H'),
('BIO-101', 'Spring', 2026, 'Cunningham Hall', 110, 'C'),
('BIO-101', 'Spring', 2026, 'Cunningham Hall', 110, 'G'),
('BIO-102', 'Spring', 2026, 'Cunningham Hall', 110, 'D'),
('BIO-102', 'Spring', 2026, 'Cunningham Hall', 110, 'H'),
('BIO-101', 'Fall', 2026, 'Cunningham Hall', 110, 'C'),
('BIO-101', 'Fall', 2026, 'Cunningham Hall', 110, 'G'),
('BIO-102', 'Fall', 2026, 'Cunningham Hall', 110, 'D'),
('BIO-102', 'Fall', 2026, 'Cunningham Hall', 110, 'H'),
('CHEM-101', 'Spring', 2026, 'Integrated Sciences Building', 108, 'A'),
('CHEM-101', 'Spring', 2026, 'Integrated Sciences Building', 108, 'E'),
('CHEM-102', 'Spring', 2026, 'Integrated Sciences Building', 108, 'B'),
('CHEM-102', 'Spring', 2026, 'Integrated Sciences Building', 108, 'F'),
('CHEM-101', 'Fall', 2026, 'Integrated Sciences Building', 108, 'A'),
('CHEM-101', 'Fall', 2026, 'Integrated Sciences Building', 108, 'E'),
('CHEM-102', 'Fall', 2026, 'Integrated Sciences Building', 108, 'B'),
('CHEM-102', 'Fall', 2026, 'Integrated Sciences Building', 108, 'F'),
('BUS-101', 'Spring', 2026, 'Business Administration Building', 207, 'B'),
('BUS-102', 'Spring', 2026, 'Business Administration Building', 103, 'G'),
('BUS-101', 'Fall', 2026, 'Business Administration Building', 207, 'B'),
('BUS-102', 'Fall', 2026, 'Business Administration Building', 103, 'G'),
('SOC-101', 'Spring', 2026, 'Merrill Hall', 112, 'C'),
('SOC-102', 'Spring', 2026, 'Merrill Hall', 125, 'F'),
('SOC-101', 'Fall', 2026, 'Merrill Hall', 112, 'C'),
('SOC-102', 'Fall', 2026, 'Merrill Hall', 125, 'F'),
('NURS-101', 'Spring', 2026, 'Henderson Hall', 213, 'D'),
('NURS-201', 'Spring', 2026, 'Henderson Hall', 105, 'E'),
('NURS-101', 'Fall', 2026, 'Henderson Hall', 213, 'D'),
('NURS-201', 'Fall', 2026, 'Henderson Hall', 105, 'E');

insert into prereq(prereq_id,course_id) values ('2006', '4505');
insert into prereq(prereq_id,course_id) values ('1002', '3432');
insert into prereq (course_id, prereq_id) values 
('CS-102', 'CS-101'),
('ARCH-102', 'ARCH-101'),
('BIO-102', 'BIO-101'),
('CHEM-102', 'CHEM-101'),
('BUS-102', 'BUS-101'),
('SOC-102', 'SOC-101'),
('NURS-201', 'NURS-101');




