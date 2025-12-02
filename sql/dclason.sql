-- phpMyAdmin SQL Dump
-- version 5.2.3-1.el10_2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 02, 2025 at 02:44 AM
-- Server version: 10.11.11-MariaDB
-- PHP Version: 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dclason`
--

-- --------------------------------------------------------

--
-- Table structure for table `advisor`
--

CREATE TABLE `advisor` (
  `student_id` int(11) NOT NULL,
  `instructor_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `advisor`
--

INSERT INTO `advisor` (`student_id`, `instructor_id`) VALUES
(1, 3),
(2, 2),
(3, 1),
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
(15, 12),
(16, 9),
(16, 12),
(17, 7),
(18, 6),
(19, 2),
(20, 9),
(21, 14),
(22, 17),
(23, 19),
(24, 15),
(25, 18);

-- --------------------------------------------------------

--
-- Table structure for table `classroom`
--

CREATE TABLE `classroom` (
  `building` varchar(50) NOT NULL,
  `room_number` decimal(4,0) NOT NULL,
  `capacity` decimal(5,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `classroom`
--

INSERT INTO `classroom` (`building`, `room_number`, `capacity`) VALUES
('Business Administration Building', 103, 150),
('Business Administration Building', 207, 150),
('Center for Architecture and Environmental Design', 305, 150),
('Cunningham Hall', 110, 150),
('Denise Hall', 217, 250),
('Henderson Hall', 54, 100),
('Henderson Hall', 105, 30),
('Henderson Hall', 213, 30),
('Integrated Sciences Building', 108, 150),
('Mathematical Sciences Building', 210, 150),
('Merrill Hall', 112, 30),
('Merrill Hall', 125, 30),
('Paris Hall', 312, 145),
('Steward Hall', 122, 200),
('William Hall', 21, 100);

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `course_id` varchar(8) NOT NULL,
  `title` varchar(80) DEFAULT NULL,
  `dept_name` varchar(20) DEFAULT NULL,
  `credits` decimal(3,0) DEFAULT NULL CHECK (`credits` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`course_id`, `title`, `dept_name`, `credits`) VALUES
('1002', 'Introduction to Database Management', 'Computer Science', 3),
('1003', 'Introduction to Nursing', 'Nursing', 3),
('1004', 'Anatomy', 'Biology', 3),
('1005', 'General Psychology', 'Psychology', 3),
('2006', 'Solid Mechanics', 'Engineering', 4),
('3432', 'Linear Algebra', 'Computer Science', 4),
('4505', 'Differential Equations', 'Engineering', 4),
('ARCH-101', 'Design Studio I', 'Architecture', 4),
('ARCH-102', 'Design Studio II', 'Architecture', 4),
('BIO-101', 'Biological Diversity', 'Biology', 4),
('BIO-102', 'Biological Foundations', 'Biology', 4),
('BUS-101', 'Introduction to Business', 'Business', 3),
('BUS-102', 'Introduction to Marketing', 'Business', 3),
('CHEM-101', 'General Chemistry I', 'Chemistry', 4),
('CHEM-102', 'General Chemistry II', 'Chemistry', 4),
('CS-101', 'Computer Science I', 'Computer Science', 4),
('CS-102', 'Computer Science II', 'Computer Science', 4),
('NURS-101', 'Introduction to Pharmacology', 'Nursing', 3),
('NURS-201', 'Clinical Calculations', 'Nursing', 3),
('SOC-101', 'Introduction to Sociology', 'Sociology', 3),
('SOC-102', 'Social Problems', 'Sociology', 3);

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department` (
  `dept_name` varchar(30) NOT NULL,
  `building` varchar(50) DEFAULT NULL,
  `budget` decimal(10,2) DEFAULT NULL CHECK (`budget` > 0)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`dept_name`, `building`, `budget`) VALUES
('Architecture', 'Center for Architecture and Environmental Design', 750000.00),
('Biology', 'Cunningham Hall', 800000.00),
('Business', 'Business Administration Building', 700000.00),
('Chemistry', 'Integrated Sciences Building', 950000.00),
('Computer Science', 'Mathematical Sciences Building', 99000000.00),
('Engineering', 'Paris Hall', 89000.00),
('Nursing', 'Henderson Hall', 980000.00),
('Psychology', 'Denise Hall', 90000.00),
('Sociology', 'Merrill Hall', 650000.00);

-- --------------------------------------------------------

--
-- Table structure for table `enrollment`
--

CREATE TABLE `enrollment` (
  `student_id` int(11) NOT NULL,
  `course_id` varchar(8) DEFAULT NULL,
  `section_id` int(11) NOT NULL,
  `grade` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `enrollment`
--

INSERT INTO `enrollment` (`student_id`, `course_id`, `section_id`, `grade`) VALUES
(1, '1003', 1, NULL),
(1, 'CS-101', 2, 'B'),
(1, '1004', 3, 'A'),
(1, 'NURS-201', 47, NULL),
(1, 'ARCH-101', 49, NULL),
(2, '2006', 3, 'B'),
(2, 'CHEM-101', 4, 'A'),
(2, '2006', 5, 'C'),
(3, '1003', 1, 'A'),
(3, 'NURS-101', 5, 'A'),
(3, 'ARCH-101', 6, 'C'),
(4, '1002', 2, 'B'),
(4, 'CS-101', 7, 'B'),
(4, 'BIO-102', 8, 'A'),
(5, '1005', 4, 'C'),
(5, '1005', 9, 'B'),
(5, 'CS-102', 10, 'C'),
(6, '3432', 11, 'A'),
(6, 'CHEM-102', 12, 'B'),
(7, '1004', 3, NULL),
(7, '3432', 7, NULL),
(7, 'CS-102', 13, 'A'),
(7, 'SOC-101', 14, 'C'),
(7, 'BUS-102', 39, NULL),
(8, 'CS-101', 8, 'A'),
(8, '1002', 15, 'B'),
(8, 'BIO-101', 16, 'A'),
(9, 'ARCH-102', 17, 'B'),
(9, 'BUS-101', 18, 'A'),
(9, 'NURS-101', 46, 'B'),
(10, 'CS-102', 10, 'A'),
(10, 'ARCH-101', 19, 'C'),
(10, '1003', 20, 'B'),
(11, 'SOC-101', 21, 'A'),
(11, 'BUS-102', 22, 'B'),
(12, 'CS-101', 9, 'B+'),
(12, 'BIO-101', 23, 'C'),
(12, 'CHEM-101', 24, 'A'),
(12, 'BUS-102', 39, 'A-'),
(12, 'NURS-201', 45, 'C'),
(13, 'ARCH-101', 16, 'B+'),
(13, 'BIO-102', 23, 'A'),
(13, 'BIO-102', 25, 'B'),
(13, 'CS-101', 26, 'C'),
(14, 'BIO-101', 21, 'B-'),
(14, 'BIO-102', 27, 'A'),
(14, 'ARCH-102', 28, NULL),
(15, 'CHEM-101', 29, 'C'),
(15, 'CHEM-101', 33, 'A'),
(15, 'SOC-101', 40, 'A'),
(16, 'CHEM-102', 31, 'B'),
(16, 'BIO-101', 32, 'C'),
(17, 'ARCH-102', 19, 'C'),
(17, 'BIO-101', 20, 'A'),
(17, 'CHEM-101', 33, 'A'),
(17, 'NURS-201', 34, 'B'),
(18, 'BUS-101', 35, 'A'),
(18, 'ARCH-101', 36, 'B'),
(19, 'CHEM-102', 30, 'A-'),
(19, 'BUS-102', 37, 'C'),
(19, 'BUS-101', 38, 'B'),
(19, 'SOC-102', 41, 'A-'),
(20, 'BUS-101', 39, 'B'),
(20, 'CHEM-102', 40, 'C'),
(21, 'SOC-101', 41, 'A'),
(21, 'CS-101', 42, 'B'),
(22, 'SOC-102', 43, 'B'),
(22, 'BUS-102', 44, 'C'),
(23, 'SOC-101', 45, 'A'),
(23, 'ARCH-101', 46, 'B'),
(24, 'NURS-101', 47, 'B');

-- --------------------------------------------------------

--
-- Table structure for table `instructor`
--

CREATE TABLE `instructor` (
  `instructor_id` int(11) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `dept_name` varchar(30) DEFAULT NULL,
  `salary` decimal(8,2) DEFAULT NULL CHECK (`salary` > 40000)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `instructor`
--

INSERT INTO `instructor` (`instructor_id`, `first_name`, `last_name`, `dept_name`, `salary`) VALUES
(1, 'Mckenna', 'Grace', 'Biology', 120000.00),
(2, 'Mason', 'Thames', 'Computer Science', 100000.00),
(3, 'Dave', 'Franco', 'Nursing', 140000.00),
(4, 'Dakota', 'Johnson', 'Psychology', 60000.00),
(5, 'Jamie', 'Dorman', 'Engineering', 70000.00),
(6, 'Alan', 'Turing', 'Computer Science', 99000.00),
(7, 'Ada', 'Lovelace', 'Computer Science', 95000.00),
(8, 'Frank', 'Wright', 'Architecture', 75000.00),
(9, 'Zaha', 'Hadid', 'Architecture', 70000.00),
(10, 'Charles', 'Darwin', 'Biology', 80000.00),
(11, 'Rachel', 'Carson', 'Biology', 75000.00),
(12, 'Marie', 'Curie', 'Chemistry', 95000.00),
(13, 'Dmitri', 'Mendeleev', 'Chemistry', 90000.00),
(14, 'Warren', 'Buffet', 'Business', 70000.00),
(15, 'Bill', 'Gates', 'Business', 65000.00),
(16, 'Auguste', 'Comte', 'Sociology', 65000.00),
(17, 'Emile', 'Durkheim', 'Sociology', 60000.00),
(18, 'Florence', 'Nightingale', 'Nursing', 98000.00),
(19, 'Clara', 'Barton', 'Nursing', 93000.00);

-- --------------------------------------------------------

--
-- Table structure for table `prereq`
--

CREATE TABLE `prereq` (
  `course_id` varchar(8) NOT NULL,
  `prereq_id` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `prereq`
--

INSERT INTO `prereq` (`course_id`, `prereq_id`) VALUES
('3432', '1002'),
('4505', '2006'),
('ARCH-102', 'ARCH-101'),
('BIO-102', 'BIO-101'),
('BUS-102', 'BUS-101'),
('CHEM-102', 'CHEM-101'),
('CS-102', 'CS-101'),
('NURS-201', 'NURS-101'),
('SOC-102', 'SOC-101');

-- --------------------------------------------------------

--
-- Table structure for table `section`
--

CREATE TABLE `section` (
  `section_id` int(11) NOT NULL,
  `course_id` varchar(8) DEFAULT NULL,
  `instructor_id` int(11) DEFAULT NULL,
  `semester` varchar(6) DEFAULT NULL CHECK (`semester` in ('Fall','Winter','Spring','Summer')),
  `year` decimal(4,0) DEFAULT NULL CHECK (`year` > 2010 and `year` < 2100),
  `building` varchar(50) DEFAULT NULL,
  `room_number` decimal(4,0) DEFAULT NULL,
  `time_slot_id` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `section`
--

INSERT INTO `section` (`section_id`, `course_id`, `instructor_id`, `semester`, `year`, `building`, `room_number`, `time_slot_id`) VALUES
(1, '1003', 18, 'Fall', 2025, 'Henderson Hall', 54, 'A'),
(2, '1002', 6, 'Fall', 2025, 'William Hall', 21, 'B'),
(3, '1004', 10, 'Fall', 2025, 'Steward Hall', 122, 'A'),
(4, '1005', 4, 'Fall', 2025, 'Denise Hall', 217, 'E'),
(5, '2006', 5, 'Spring', 2026, 'Paris Hall', 312, 'D'),
(6, '4505', 5, 'Fall', 2025, 'Paris Hall', 312, 'C'),
(7, '3432', 2, 'Spring', 2026, 'William Hall', 21, 'B'),
(8, 'CS-101', 7, 'Spring', 2026, 'Mathematical Sciences Building', 210, 'A'),
(9, 'CS-101', 6, 'Spring', 2026, 'Mathematical Sciences Building', 210, 'E'),
(10, 'CS-102', 2, 'Spring', 2026, 'Mathematical Sciences Building', 210, 'B'),
(11, 'CS-102', 2, 'Spring', 2026, 'Mathematical Sciences Building', 210, 'F'),
(12, 'CS-101', 2, 'Fall', 2026, 'Mathematical Sciences Building', 210, 'A'),
(13, 'CS-101', 6, 'Fall', 2026, 'Mathematical Sciences Building', 210, 'E'),
(14, 'CS-102', 7, 'Fall', 2026, 'Mathematical Sciences Building', 210, 'B'),
(15, 'CS-102', 7, 'Fall', 2026, 'Mathematical Sciences Building', 210, 'F'),
(16, 'ARCH-101', 8, 'Spring', 2026, 'Center for Architecture and Environmental Design', 305, 'A'),
(17, 'ARCH-102', 9, 'Spring', 2026, 'Center for Architecture and Environmental Design', 305, 'H'),
(18, 'ARCH-101', 8, 'Fall', 2026, 'Center for Architecture and Environmental Design', 305, 'A'),
(19, 'ARCH-102', 9, 'Fall', 2026, 'Center for Architecture and Environmental Design', 305, 'H'),
(20, 'BIO-101', NULL, 'Spring', 2026, 'Cunningham Hall', 110, 'C'),
(21, 'BIO-101', NULL, 'Spring', 2026, 'Cunningham Hall', 110, 'G'),
(22, 'BIO-102', 10, 'Spring', 2026, 'Cunningham Hall', 110, 'D'),
(23, 'BIO-102', 10, 'Spring', 2026, 'Cunningham Hall', 110, 'H'),
(24, 'BIO-101', NULL, 'Fall', 2026, 'Cunningham Hall', 110, 'C'),
(25, 'BIO-101', NULL, 'Fall', 2026, 'Cunningham Hall', 110, 'G'),
(26, 'BIO-102', 11, 'Fall', 2026, 'Cunningham Hall', 110, 'D'),
(27, 'BIO-102', 11, 'Fall', 2026, 'Cunningham Hall', 110, 'H'),
(28, 'CHEM-101', 12, 'Spring', 2026, 'Integrated Sciences Building', 108, 'A'),
(29, 'CHEM-101', 12, 'Spring', 2026, 'Integrated Sciences Building', 108, 'E'),
(30, 'CHEM-102', 12, 'Spring', 2026, 'Integrated Sciences Building', 108, 'B'),
(31, 'CHEM-102', 13, 'Spring', 2026, 'Integrated Sciences Building', 108, 'F'),
(32, 'CHEM-101', 12, 'Fall', 2026, 'Integrated Sciences Building', 108, 'A'),
(33, 'CHEM-101', 12, 'Fall', 2026, 'Integrated Sciences Building', 108, 'E'),
(34, 'CHEM-102', 12, 'Fall', 2026, 'Integrated Sciences Building', 108, 'B'),
(35, 'CHEM-102', 13, 'Fall', 2026, 'Integrated Sciences Building', 108, 'F'),
(36, 'BUS-101', 14, 'Spring', 2026, 'Business Administration Building', 207, 'B'),
(37, 'BUS-102', 15, 'Spring', 2026, 'Business Administration Building', 103, 'G'),
(38, 'BUS-101', 14, 'Fall', 2026, 'Business Administration Building', 207, 'B'),
(39, 'BUS-102', 15, 'Fall', 2026, 'Business Administration Building', 103, 'G'),
(40, 'SOC-101', 16, 'Spring', 2026, 'Merrill Hall', 112, 'C'),
(41, 'SOC-102', 16, 'Spring', 2026, 'Merrill Hall', 125, 'F'),
(42, 'SOC-101', 17, 'Fall', 2026, 'Merrill Hall', 112, 'C'),
(43, 'SOC-102', 17, 'Fall', 2026, 'Merrill Hall', 125, 'F'),
(44, 'NURS-101', 3, 'Spring', 2026, 'Henderson Hall', 213, 'D'),
(45, 'NURS-201', 19, 'Spring', 2026, 'Henderson Hall', 105, 'E'),
(46, 'NURS-101', 3, 'Fall', 2026, 'Henderson Hall', 213, 'D'),
(47, 'NURS-201', 19, 'Fall', 2026, 'Henderson Hall', 105, 'E'),
(49, 'ARCH-101', 8, 'Summer', 2026, 'Center for Architecture and Environmental Design', 305, 'D');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `student_id` int(11) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `dept_name` varchar(30) DEFAULT NULL,
  `tot_credits` decimal(3,0) DEFAULT NULL CHECK (`tot_credits` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`student_id`, `first_name`, `last_name`, `dept_name`, `tot_credits`) VALUES
(1, 'Will', 'Smith', 'Biology', 29),
(2, 'Ryan', 'Reynolds', 'Engineering', 48),
(3, 'Kevin', 'Hart', 'Nursing', 70),
(4, 'Jennifer', 'Lawrence', 'Computer Science', 14),
(5, 'Robert', 'Irwin', 'Psychology', 87),
(6, 'Danielle', 'Clason', 'Computer Science', 94),
(7, 'Tessa', 'Wood', 'Computer Science', 103),
(8, 'Ashlee', 'Cunningham', 'Computer Science', 99),
(9, 'Leah', 'Brechtelsbauer', 'Architecture', 45),
(10, 'Mikayla', 'Zagar', 'Architecture', 60),
(11, 'Anthony', 'Maricocchi', 'Architecture', 65),
(12, 'Madelyn', 'Lawrence', 'Biology', 94),
(13, 'Sarah', 'Becker', 'Biology', 87),
(14, 'Marley', 'Nash', 'Biology', 93),
(15, 'Sofia', 'DeCola', 'Chemistry', 105),
(16, 'Riley', 'Kuwatch', 'Chemistry', 104),
(17, 'Giana', 'Nakoul', 'Chemistry', 95),
(18, 'Payton', 'Factor', 'Business', 107),
(19, 'Dakota', 'Whitacre', 'Business', 101),
(20, 'Anthony', 'Mast', 'Business', 98),
(21, 'Samuel', 'Garcia', 'Sociology', 85),
(22, 'Charleigh', 'Riffle', 'Sociology', 110),
(23, 'Jenna', 'Hall', 'Sociology', 47),
(24, 'Sadie', 'Ahbel', 'Nursing', 80),
(25, 'Abigal', 'Coblentz', 'Nursing', 53),
(26, 'Vivian', 'Coblentz', 'Nursing', 40);

-- --------------------------------------------------------

--
-- Table structure for table `time_slot`
--

CREATE TABLE `time_slot` (
  `time_slot_id` varchar(4) NOT NULL,
  `days` varchar(10) DEFAULT NULL,
  `start_hr` decimal(2,0) DEFAULT NULL CHECK (`start_hr` >= 0 and `start_hr` < 24),
  `start_min` decimal(2,0) DEFAULT NULL CHECK (`start_min` >= 0 and `start_min` < 60),
  `end_hr` decimal(2,0) DEFAULT NULL CHECK (`end_hr` >= 0 and `end_hr` < 24),
  `end_min` decimal(2,0) DEFAULT NULL CHECK (`end_min` >= 0 and `end_min` < 60)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `time_slot`
--

INSERT INTO `time_slot` (`time_slot_id`, `days`, `start_hr`, `start_min`, `end_hr`, `end_min`) VALUES
('A', 'M,W,F', 9, 0, 9, 50),
('B', 'M,W,F', 11, 0, 11, 50),
('C', 'M,W,F', 12, 15, 13, 10),
('D', 'M,W,F', 14, 0, 14, 50),
('E', 'T,R', 9, 15, 10, 30),
('F', 'T,R', 11, 0, 12, 15),
('G', 'T,R', 13, 0, 14, 15),
('H', 'T,R', 15, 15, 16, 30);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('student','instructor','admin') NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `instructor_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `email`, `password`, `role`, `student_id`, `instructor_id`) VALUES
(1, 'danielle@kent.edu', 'scrypt:32768:8:1$newu6siMFlkK1OTl$a5611dc435c64cc50b9914a97b57899b01c7ff4d418e21cfd30efdfb8706ab790615a5929b419e473df22ef2353a91afdea015183618a7f3348f8b43ae7a5e16', 'admin', NULL, NULL),
(2, 'madelyn@kent.edu', 'scrypt:32768:8:1$XfkcjADfDSdmlM6i$262ad3a14c12e19f54d4b9d4827dd6b64e0865fa4c024ae53db996117cc76d881b79b653e1c17372ff15daec2fdc214a73d85609c58e1c2e0732b3eccb211635', 'admin', NULL, NULL),
(3, 'wsmith@kent.edu', 'scrypt:32768:8:1$ZtfWKQD6yizhD47n$0d0dcfcb8d16e83748784b0816346cf0848f05ac6e164be2f8144bddafbb640f9bc55120d815eeaf1e766376ba8c6dec006fb620c64fb2ad9298b7767deb3770', 'student', 1, NULL),
(4, 'twood@kent.edu', 'scrypt:32768:8:1$JgjuCqAgrXfNIoNE$0086f4d388588cb70f96f2e284ca1f575b02947106aa5aa1fa5e8b89bfe55b2b0fe1a28b655c5f0175f61bfd5fa5c235342a8bf75d88e0a592f42b54ab078374', 'student', 7, NULL),
(5, 'dfranco@kent.edu', 'scrypt:32768:8:1$tiqACmoAuqntwCyj$4a231d60bfd69677ce55a53a19df476e8c0f99f4094838f1f235b464ac153c7a595d53b95a2cf1961b422f04acefaa23f5df7afadf16e9f2ee886bf61e173a70', 'instructor', NULL, 3),
(6, 'mcurie@kent.edu', 'scrypt:32768:8:1$pHmyA5OCTTlpKfX9$a38ad5c12885e18c08efbb5f0f52d454ccaa6ee0dd020ccd5ee02252e1d3f34581c05f5edc699bb773fca2acce2a8ea34a2c0e5935d51e0ef902d9148cad938f', 'instructor', NULL, 12);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `advisor`
--
ALTER TABLE `advisor`
  ADD PRIMARY KEY (`student_id`,`instructor_id`),
  ADD KEY `instructor_id` (`instructor_id`);

--
-- Indexes for table `classroom`
--
ALTER TABLE `classroom`
  ADD PRIMARY KEY (`building`,`room_number`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`course_id`),
  ADD KEY `dept_name` (`dept_name`);

--
-- Indexes for table `department`
--
ALTER TABLE `department`
  ADD PRIMARY KEY (`dept_name`);

--
-- Indexes for table `enrollment`
--
ALTER TABLE `enrollment`
  ADD PRIMARY KEY (`student_id`,`section_id`),
  ADD KEY `section_id` (`section_id`);

--
-- Indexes for table `instructor`
--
ALTER TABLE `instructor`
  ADD PRIMARY KEY (`instructor_id`),
  ADD KEY `dept_name` (`dept_name`);

--
-- Indexes for table `prereq`
--
ALTER TABLE `prereq`
  ADD PRIMARY KEY (`course_id`,`prereq_id`),
  ADD KEY `prereq_id` (`prereq_id`);

--
-- Indexes for table `section`
--
ALTER TABLE `section`
  ADD PRIMARY KEY (`section_id`),
  ADD KEY `course_id` (`course_id`),
  ADD KEY `instructor_id` (`instructor_id`),
  ADD KEY `building` (`building`,`room_number`),
  ADD KEY `time_slot_id` (`time_slot_id`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`student_id`),
  ADD KEY `dept_name` (`dept_name`);

--
-- Indexes for table `time_slot`
--
ALTER TABLE `time_slot`
  ADD PRIMARY KEY (`time_slot_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `instructor_id` (`instructor_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `instructor`
--
ALTER TABLE `instructor`
  MODIFY `instructor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `section`
--
ALTER TABLE `section`
  MODIFY `section_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `advisor`
--
ALTER TABLE `advisor`
  ADD CONSTRAINT `advisor_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `advisor_ibfk_2` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`instructor_id`) ON DELETE CASCADE;

--
-- Constraints for table `course`
--
ALTER TABLE `course`
  ADD CONSTRAINT `course_ibfk_1` FOREIGN KEY (`dept_name`) REFERENCES `department` (`dept_name`) ON DELETE SET NULL;

--
-- Constraints for table `enrollment`
--
ALTER TABLE `enrollment`
  ADD CONSTRAINT `enrollment_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `enrollment_ibfk_2` FOREIGN KEY (`section_id`) REFERENCES `section` (`section_id`) ON DELETE CASCADE;

--
-- Constraints for table `instructor`
--
ALTER TABLE `instructor`
  ADD CONSTRAINT `instructor_ibfk_1` FOREIGN KEY (`dept_name`) REFERENCES `department` (`dept_name`) ON DELETE SET NULL;

--
-- Constraints for table `prereq`
--
ALTER TABLE `prereq`
  ADD CONSTRAINT `prereq_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `prereq_ibfk_2` FOREIGN KEY (`prereq_id`) REFERENCES `course` (`course_id`);

--
-- Constraints for table `section`
--
ALTER TABLE `section`
  ADD CONSTRAINT `section_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `section_ibfk_2` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`instructor_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `section_ibfk_3` FOREIGN KEY (`building`,`room_number`) REFERENCES `classroom` (`building`, `room_number`) ON DELETE SET NULL,
  ADD CONSTRAINT `section_ibfk_4` FOREIGN KEY (`time_slot_id`) REFERENCES `time_slot` (`time_slot_id`) ON DELETE SET NULL;

--
-- Constraints for table `student`
--
ALTER TABLE `student`
  ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY (`dept_name`) REFERENCES `department` (`dept_name`) ON DELETE SET NULL;

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `fk_user_instructor` FOREIGN KEY (`instructor_id`) REFERENCES `instructor` (`instructor_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_user_student` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

