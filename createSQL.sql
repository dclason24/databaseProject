create table department(
    dept_name   varchar(30),
    building    varchar(50),
    budget      numeric(10,2) check (budget > 0),
    primary key(dept_name)
);

create table student(
    student_id INT AUTO_INCREMENT,
    first_name varchar(30) not null,
    last_name varchar(30) not null,
    dept_name  varchar(30),
    tot_credits numeric(3,0) check (tot_credits >= 0),
    primary key(student_id),
    foreign key(dept_name) references department(dept_name) on delete set null
);

--check that credits -> tot_credit

create table course(
    course_id   varchar(5),
    title       varchar(20),
    dept_name   varchar(20),
    credits     numeric(3,0) check (credits > 0),
    primary key(course_id),
    foreign key(dept_name) references department(dept_name) on delete set null
);

--check credit->credits

create table instructor(
    instructor_id INT AUTO_INCREMENT,
    first_name    varchar(30) not null,
    last_name     varchar(30) not null,
    dept_name     varchar(30),
    salary        numeric(8,2) check (salary > 40000),
    primary key(instructor_id),
    foreign key(dept_name) references department(dept_name) on delete set null
);

create table advisor(
    student_id      varchar(5),
    instructor_id   varchar(5),
    primary key(student_id, instructor_id),
    foreign key(student_id) references student(student_id) on delete cascade,
    foreign key(instructor_id) references instructor(instructor_id) on delete cascade
);


create table classroom(
    building     varchar(50),
    room_number  numeric(4,0),
    capacity     numeric (5,0),
    primary key(building,room_number)
);
    

create table time_slot(
    time_slot_id    varchar(4),
    days            varchar(10),
    start_hr        numeric(2,0) check (start_hr >= 0 and start_hr < 24),
    start_min       numeric(2,0) check (start_min >= 0 and start_min < 60),
    end_hr          numeric(2,0) check (end_hr >= 0 and end_hr < 24),
    end_min         numeric(2,0) check (end_min >= 0 and end_min < 60),
    primary key(time_slot_id)
);

create table prereq(
    course_id   varchar(8),
    prereq_id   varchar(8),
    primary key(course_id, prereq_id),
    foreign key(course_id) references course(course_id) on delete cascade,
    foreign key(prereq_id) references course(course_id)
);

create table section(
    section_id          INT AUTO_INCREMENT,
    course_id           varchar(5),
    instructor_id       varchar(5),
    semester            varchar(6) check (semester in ('Fall', 'Winter', 'Spring', 'Summer')),
    year                numeric(4,0) check (year > 2010 and year < 2100),
    building       varchar(50),
    room_number     numeric(4,0),
    time_slot_id        varchar(5),
    primary key(section_id),
    foreign key(course_id) references course(course_id) on delete cascade,
    foreign key(instructor_id) references instructor(instructor_id)on delete set null,
    foreign key(building,room_number) references classroom(building,room_number)on delete set null,
    foreign key(time_slot_id) references time_slot(time_slot_id)on delete set null
);

create table enrollment(
    student_id    INT,
    course_id     varchar(5),  
    section_id    INT,
    grade         varchar(2),
    primary key(student_id,section_id),
    foreign key(student_id) references student(student_id) on delete cascade,
    foreign key(section_id) references section(section_id) on delete cascade,
);