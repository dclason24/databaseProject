--populating
insert into department(dept_name, building, budget) values ('Computer Science', 'William Hall', 100000);
insert into department(dept_name, building, budget) values ('Biology', 'Steward hall', 70000);
insert into department(dept_name, building, budget) values ('Psychology', 'Denise hall', 90000);
insert into department(dept_name, building, budget) values ('Nursing', 'Henderson hall', 120000);
insert into department(dept_name, building, budget) values ('Engineering', 'Paris hall', 89000);

insert into student (student_id, first_name, last_name, dept_name, tot_credits) values ('1', 'Will', 'Smith', 'Biology', 29);
insert into student (student_id, first_name, last_name, dept_name, tot_credits) values ('2', 'Ryan', 'Reynolds', 'Engineering', 48);
insert into student (student_id, first_name, last_name, dept_name, tot_credits) values ('3', 'Kevin', 'Hart', 'Nursing', 70);
insert into student (student_id, first_name, last_name, dept_name, tot_credits) values ('4', 'Jennifer', 'Lawrence', 'Computer Science', 14);
insert into student (student_id, first_name, last_name, dept_name, tot_credits) values ('5', 'Robert', 'Irwin', 'Psychology', 87);

insert into instructor(instructor_id, first_name, last_name, dept_name, salary) values ('21', 'Mckenna', 'Grace', 'Biology', 120000);
insert into instructor(instructor_id, first_name, last_name, dept_name, salary) values ('43', 'Mason', 'Thames', 'Computer Science', 100000);
insert into instructor(instructor_id, first_name, last_name, dept_name, salary) values ('324', 'Dave', 'Franco', 'Nursing', 140000);
insert into instructor(instructor_id, first_name, last_name, dept_name, salary) values ('423', 'Dakota', 'Johnson', 'Psychology', 60000);
insert into instructor(instructor_id, first_name, last_name, dept_name, salary) values ('765', 'Jamie', 'Dorman', 'Engineering', 70000);

insert into course(course_id, title, dept_name, credit) values ('1003', 'Intro to Nursing', 'Nursing', 3);
insert into course(course_id, title, dept_name, credit) values ('1002', 'Intro to Database', 'Computer Science', 3);
insert into course(course_id, title, dept_name, credit) values ('1004', 'Anatomy', 'Biology', 3);
insert into course(course_id, title, dept_name, credit) values ('1005', 'Data Recognition', 'Psychology', 4);
insert into course(course_id, title, dept_name, credit) values ('2006', 'Solid Mechanics', 'Engineering', 4);
insert into course(course_id, title, dept_name, credit) values ('4505', 'Differential Equations', 'Engineering', 4);
insert into course(course_id, title, dept_name, credit) values ('3432', 'Linear Algebra', 'Computer Science', 4);

insert into time_slot(time_slot_id, day, start_hr, start_min ,end_hr, end_min) values ('A', 'Monday', 12 , 30, 1, 45);
insert into time_slot(time_slot_id, day, start_hr, start_min ,end_hr, end_min) values ('B', 'Tuesday', 14 , 00, 15, 30);
insert into time_slot(time_slot_id, day, start_hr, start_min ,end_hr, end_min) values ('C', 'Wednesday', 8 , 30, 9, 30);
insert into time_slot(time_slot_id, day, start_hr, start_min ,end_hr, end_min) values ('E', 'Wednesday', 15 , 00, 17, 15);
insert into time_slot(time_slot_id, day, start_hr, start_min ,end_hr, end_min) values ('D', 'Thursday', 16 , 45, 17, 30);

insert into classroom(building,room_number,capacity) values ('William Hall', 21 , 100);
insert into classroom(building,room_number,capacity) values ('Steward Hall', 122 , 200);
insert into classroom(building,room_number,capacity) values ('Denise Hall', 217 , 250);
insert into classroom(building,room_number,capacity) values ('Henderson Hall', 54, 100);
insert into classroom(building,room_number,capacity) values ('Paris Hall', 312 , 145);

insert into section(section_id, course_id, instructor_id, semester, year, building, room_number, time_slot_id) values ('1', '1003', null, 'Fall', 2025, 'Henderson Hall', '54','A');
insert into section(section_id, course_id, instructor_id, semester, year, building, room_number, time_slot_id) values ('2', '1002', '43', 'Fall', 2025, 'William Hall', '21','B');
insert into section(section_id, course_id, instructor_id, semester, year, building, room_number, time_slot_id) values ('3', '1004', '21', 'Fall', 2025, 'Steward Hall', '122','A');
insert into section(section_id, course_id, instructor_id, semester, year, building, room_number, time_slot_id) values ('45', '1005', '423', 'Fall', 2025, 'Denise Hall', '217','E');
insert into section(section_id, course_id, instructor_id, semester, year, building, room_number, time_slot_id) values ('54', '2006', '765', 'Spring', 2026, 'Paris Hall', '312','D');
insert into section(section_id, course_id, instructor_id, semester, year, building, room_number, time_slot_id) values ('76', '4505', '765', 'Fall', 2025, 'Paris Hall', '312','C');
insert into section(section_id, course_id, instructor_id, semester, year, building, room_number, time_slot_id) values ('63', '3432', '43', 'Spring', 2026, 'William Hall', '21','B');

insert into prereq(prereq_id,course_id) values ('2006', '4505');
insert into prereq(prereq_id,course_id) values ('1002', '3432');

--transactions

--enrolling into class
insert into enrollment(student_id,section_id,grade) values ('1', '3', 'A');
insert into enrollment(student_id,section_id,grade) values ('2', '54', 'C');
insert into enrollment(student_id,section_id,grade) values ('3', '1', 'A');
insert into enrollment(student_id,section_id,grade) values ('4', '2', 'B');
insert into enrollment(student_id,section_id,grade) values ('5', '45', 'C');
insert into enrollment(student_id,section_id,grade) values ('1', '45', 'C');

--assigning advisor
insert into advisor(student_id,instructor_id) values ('1', '21');
insert into advisor(student_id,instructor_id) values ('2', '765');
insert into advisor(student_id,instructor_id) values ('3', '324');

--assigning instructor to class
update section set instructor_id = '324' where section_id = '1';

--dropping a section
delete from enrollment where student_id = '1' AND section_id = '45';

--give a grade to a person
update enrollment set grade = 'A' where student_id = '3' and section_id = '1';


