-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 27, 2021 at 03:36 PM
-- Server version: 10.4.20-MariaDB
-- PHP Version: 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `online_election`
--

-- --------------------------------------------------------

--
-- Table structure for table `address_new`
--

CREATE TABLE `address_new` (
  `Plot_No` varchar(100) NOT NULL,
  `Colony` varchar(100) NOT NULL,
  `Area` varchar(20) NOT NULL,
  `City` varchar(50) NOT NULL,
  `State` varchar(20) NOT NULL,
  `Pin_Code` varchar(8) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Mobile_No` varchar(12) NOT NULL,
  `Map_link` text NOT NULL,
  `ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `address_new`
--

INSERT INTO `address_new` (`Plot_No`, `Colony`, `Area`, `City`, `State`, `Pin_Code`, `Email`, `Mobile_No`, `Map_link`, `ID`) VALUES
('1', 'xyz colony', 'xyz area', 'a city', 'abc', '123456', 'elect.online@gmail.com', '9876543210', 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3504.1953265685984!2d77.11761261485658!3d28.563896793935278!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390d1d647f095b01%3A0x746ea1d935fd9c18!2sDelhi%20Airport!5e0!3m2!1sen!2sin!4v1627392747990!5m2!1sen!2sin', 11);

-- --------------------------------------------------------

--
-- Table structure for table `candidate_registration`
--

CREATE TABLE `candidate_registration` (
  `ID` int(11) NOT NULL,
  `Profile_pic` varchar(200) NOT NULL DEFAULT 'dummy',
  `Fname` varchar(20) NOT NULL,
  `Lname` varchar(20) NOT NULL,
  `Dob` date NOT NULL,
  `Mobile_NO` varchar(12) NOT NULL,
  `Gender` varchar(10) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `Introduction` text NOT NULL,
  `Status` varchar(10) NOT NULL DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `due_voters`
--

CREATE TABLE `due_voters` (
  `ID` int(11) NOT NULL,
  `fname` varchar(20) NOT NULL,
  `lname` varchar(20) NOT NULL,
  `Email` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `release_election`
--

CREATE TABLE `release_election` (
  `EID` int(11) NOT NULL,
  `ETitle` text NOT NULL,
  `Cstart` datetime NOT NULL,
  `Cend` datetime NOT NULL,
  `Vstart` datetime NOT NULL,
  `Vend` datetime NOT NULL,
  `Rdeclare` datetime NOT NULL,
  `About` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `shortlist_candidate`
--

CREATE TABLE `shortlist_candidate` (
  `ID` int(11) NOT NULL,
  `Profile_pic` varchar(200) NOT NULL DEFAULT 'dummy',
  `Fname` varchar(20) NOT NULL,
  `Lname` varchar(20) NOT NULL,
  `Dob` text NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Gender` varchar(10) NOT NULL,
  `VoteCount` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `voter_registration`
--

CREATE TABLE `voter_registration` (
  `ID` int(11) NOT NULL,
  `Profile_pic` varchar(200) NOT NULL DEFAULT 'dummy',
  `Fname` varchar(20) NOT NULL,
  `Lname` varchar(20) NOT NULL,
  `Dob` date NOT NULL,
  `Mobile_NO` varchar(12) NOT NULL,
  `Gender` varchar(10) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `Status` varchar(10) NOT NULL DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `address_new`
--
ALTER TABLE `address_new`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `candidate_registration`
--
ALTER TABLE `candidate_registration`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `due_voters`
--
ALTER TABLE `due_voters`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `release_election`
--
ALTER TABLE `release_election`
  ADD PRIMARY KEY (`EID`);

--
-- Indexes for table `shortlist_candidate`
--
ALTER TABLE `shortlist_candidate`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `voter_registration`
--
ALTER TABLE `voter_registration`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `address_new`
--
ALTER TABLE `address_new`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `candidate_registration`
--
ALTER TABLE `candidate_registration`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `due_voters`
--
ALTER TABLE `due_voters`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `release_election`
--
ALTER TABLE `release_election`
  MODIFY `EID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `shortlist_candidate`
--
ALTER TABLE `shortlist_candidate`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `voter_registration`
--
ALTER TABLE `voter_registration`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
