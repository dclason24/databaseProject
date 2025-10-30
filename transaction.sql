--enrolling into class
insert into enrollment(student_id,course_id,section_id,grade) values (1, '1004','3', 'A');
insert into enrollment(student_id,course_id,section_id,grade) values (2, '2006', '54', 'C');
insert into enrollment(student_id,course_id,section_id,grade) values (3, '1003','1', 'A');
insert into enrollment(student_id,course_id,section_id,grade) values (4, '1002','2', 'B');
insert into enrollment(student_id,course_id,section_id,grade) values (5, '1005', '45', 'C');
insert into enrollment(student_id,course_id,section_id,grade) values (1, '1005','45', 'C');
insert into enrollment (student_id, course_id, section_id, grade) values
(8,'10001', 'CS-101', '1', 'Spring', 2026, 'A'),
(10,'10001', 'CS-102', '2', 'Fall', 2026, 'A'),
(12,'10002', 'CS-101', '2', 'Spring', 2026, 'B+'),
(15,'10002', 'CS-102', '1', 'Fall', 2026, 'A-'),
(4,'10003', 'CS-102', '2', 'Spring', 2026, 'B'),
(17,'10004', 'ARCH-102', '1', 'Spring', 2026, 'C'),
(13,'10005', 'ARCH-101', '1', 'Spring', 2026, 'B+'),
(1,'10005', 'ARCH-102', '1', 'Fall', 2026, 'C-'),
(13,'10006', 'ARCH-102', '1', 'Spring', 2026, 'D'),
(17,'10007', 'BIO-101', '2', 'Spring', 2026, 'A'),
(13,'10007', 'BIO-102', '2', 'Fall', 2026, 'A'),
(14,'10008', 'BIO-101', '1', 'Spring', 2026, 'B-'),
(18,'10008', 'BIO-102', '2', 'Fall', 2026, 'C'),
(15,'10009', 'BIO-101', '1', 'Spring', 2026, 'C+'),
(18,'10009', 'BIO-102', '1', 'Fall', 2026, 'B'),
(19,'10010', 'CHEM-102', '2', 'Spring', 2026, 'A-'),
(15,'10012', 'CHEM-101', '2', 'Spring', 2026, 'A'),
(4,'10012', 'CHEM-102', '2', 'Fall', 2026, 'A-'),
(19,'10014', 'BUS-101', '1', 'Spring', 2026, 'B'),
(12,'10014', 'BUS-102', '1', 'Fall', 2026, 'A-'),
(14,'10015', 'BUS-102', '1', 'Spring', 2026, 'A'),
(15,'10016', 'SOC-101', '1', 'Spring', 2026, 'A'),
(19,'10016', 'SOC-102', '1', 'Fall', 2026, 'A-'),
(12,'10019', 'NURS-201', '1', 'Fall', 2026, 'C'),
(9,'10020', 'NURS-101', '1', 'Spring', 2026, 'B'),
(8'10020', 'NURS-201', '1', 'Fall', 2026, 'B+');

--assigning advisor
insert into advisor(student_id,instructor_id) values ('1', '21');
insert into advisor(student_id,instructor_id) values ('2', '765');
insert into advisor(student_id,instructor_id) values ('3', '324');
insert into advisor(student_id, instructor_id) values
('10001', '90001'),
('10002', '90001'),
('10003', '90001'),
('10004', '90003'),
('10005', '90003'),
('10006', '90003'),
('10007', '90006'),
('10008', '90005'),
('10009', '90005'),
('10010', '90007'),
('10011', '90007'),
('10012', '90007'),
('10013', '90009'),
('10014', '90009'),
('10015', '90010'),
('10016', '90012'),
('10017', '90011'),
('10018', '90011'),
('10019', '90013'),
('10020', '90014'),
('10021', '90013');

--assigning instructor to class
update section set instructor_id = '324' where section_id = '1';

--dropping a section
delete from enrollment where student_id = '1' AND section_id = '45';

--give a grade to a person
update enrollment set grade = 'A' where student_id = '3' and section_id = '1';