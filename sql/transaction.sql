--enrolling into class
insert into enrollment(student_id,course_id,section_id,grade) values (1, '1004', 3, 'A');
insert into enrollment(student_id,course_id,section_id,grade) values (2, '2006', 5, 'C');
insert into enrollment(student_id,course_id,section_id,grade) values (3, '1003', 1, 'A');
insert into enrollment(student_id,course_id,section_id,grade) values (4, '1002', 2, 'B');
insert into enrollment(student_id,course_id,section_id,grade) values (5, '1005', 4, 'C');
insert into enrollment(student_id,course_id,section_id,grade) values (1, '1005',4, 'C');
insert into enrollment (student_id, course_id, section_id, grade) values
(8,'CS-101', 8 , 'A'),
(10,'CS-102', 10 ,'A'),
(12,'CS-101', 9, 'B+'),
(17,'ARCH-102', 19 , 'C'),
(13,'ARCH-101', 16 , 'B+'),
(17,'BIO-101', 20, 'A'),
(13,'BIO-102', 23,'A'),
(14,'BIO-101', 21, 'B-'),
(19,'CHEM-102', 30 ,'A-'),
(15,'CHEM-101', 33 , 'A'),
(19,'BUS-101', 38, 'B'),
(12,'BUS-102', 39 ,'A-'),
(15,'SOC-101', 40, 'A'),
(19,'SOC-102', 41,'A-'),
(12,'NURS-201', 45,'C'),
(9,'NURS-101', 46, 'B'),

--assigning advisor
insert into advisor(student_id,instructor_id) values (1, 3);
insert into advisor(student_id,instructor_id) values (2, 2);
insert into advisor(student_id,instructor_id) values (3, 1);
insert into advisor(student_id, instructor_id) values
(6, 14),
(7, 8),
(8, 6),
(9, 13),
(10, 19),
(11, 18),
(12, 15),
(13, 12),
(14, 11),
(15, 10),
(16, 9),
(17, 7),
(18, 6),
(19, 2),
(20, 9),
(21, 14),
(22, 17),
(23, 19),
(24, 20),
(25, 24);

--assigning instructor to class
update section set instructor_id = '3' where section_id = '1';

--dropping a section
delete from enrollment where student_id = '1' AND section_id = '4';

--give a grade to a person
update enrollment set grade = 'A' where student_id = '3' and section_id = '1';