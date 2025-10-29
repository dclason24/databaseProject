create table department(
    dept_name   varchar(20),
    building    varchar(20),
    budget      numeric(8,0),
    primary key(dept_name)
)

create table student(
    student_id varchar(5),
    first_name varchar(30) not null,
    last_name varchar(30) not null,
    dept_name  varchar(20),
    tot_credits numeric(3,0),
    primary key(student_id),
    foreign key(dept_name) references department(dept_name)
)

create table course(
    course_id   varchar(5),
    title       varchar(20),
    dept_name   varchar(20),
    credit     numeric(3,0),
    primary key(course_id),
    foreign key(dept_name) references department(dept_name)
)

create table instructor(
    instructor_id varchar(5),
    first_name    varchar(20) not null,
    last_name     varchar(20) not null,
    dept_name     varchar(20),
    salary        numeric(8,2),
    primary key(instructor_id),
    foreign key(dept_name) references department(dept_name)
)

create table advisor(
    student_id      varchar(5),
    instructor_id   varchar(5),
    primary key(student_id, instructor_id),
    foreign key(student_id) references student(student_id),
    foreign key(instructor_id) references instructor(instructor_id)
)


create table classroom(
    building     varchar(20),
    room_number  numeric(4,0),
    capacity     numeric (5,0),
    primary key(building,room_number)
)
    

create table time_slot(
    time_slot_id    varchar(5),
    day             varchar(8),
    start_hr        numeric(2,0),
    start_min       numeric(2,0),
    end_hr          numeric(2,0),
    end_min         numeric(2,0),
    primary key(time_slot_id)
)

create table prereq(
    prereq_id   varchar(5),
    course_id   varchar(5),
    primary key(prereq_id,course_id),
    foreign ket(prereq_id) references course(course_id),
    foreign key(course_id) references course(course_id);
)

create table section(
    section_id          varchar(5),
    course_id           varchar(5),
    instructor_id       varchar(5),
    semester            varchar(6),
    year                numeric(4,0),
    building       varchar(5),
    room_number     varchar(5),
    time_slot_id        varchar(5),
    primary key(section_id),
    foreign key(course_id) references course(course_id),
    foreign key(instructor_id) references instructor(instructor_id),
    foreign key(building) references classroom(building),
    foreign key(room_number) references classroom(room_number),
    foreign key(time_slot_id) references time_slot(time_slot_id)
)

create table enrollment(
    student_id    varchar(5),
    section_id    varchar(5),
    grade         varchar(2),
    primary key(student_id,section_id),
    foreign key(student_id) references student(student_id),
    foreign key(section_id) references section(section_id)
)