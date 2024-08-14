-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
Use LingoAmigo;
-- -----------------------------------------------------
-- Schema LingoAmigo
-- -----------------------------------------------------
DROP TABLE IF EXISTS `VideoComments`;
DROP TABLE IF EXISTS `StudentAnswer`;
DROP TABLE IF EXISTS `Post`;
DROP TABLE IF EXISTS `Video`;
DROP TABLE IF EXISTS `Question`;
DROP TABLE IF EXISTS `Quiz`;
DROP TABLE IF EXISTS `Section`;
DROP TABLE IF EXISTS `Session`;
DROP TABLE IF EXISTS `Order`;
DROP TABLE IF EXISTS `Resource`;
DROP TABLE IF EXISTS `DiscussionBoard`;
DROP TABLE IF EXISTS `Course`;
DROP TABLE IF EXISTS `Student`;
DROP TABLE IF EXISTS `Teacher`;
DROP TABLE IF EXISTS `Expert`;
DROP TABLE IF EXISTS `Administrator`;
DROP TABLE IF EXISTS `Language`;
DROP TABLE IF EXISTS `User`;

-- -----------------------------------------------------
-- Schema LingoAmigo
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `LingoAmigo` DEFAULT CHARACTER SET utf8 ;
USE `LingoAmigo` ;

-- -----------------------------------------------------
-- Table `LingoAmigo`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`User` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `role` VARCHAR(255) NOT NULL COMMENT 'role: Student, Teacher, Expert, Administrator',
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Student` (
  `student_id` INT NOT NULL,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `date_birth` DATE NULL,
  `phone` VARCHAR(15) NOT NULL,
  `image_url` VARCHAR(255) NULL,
  `status` VARCHAR(255) NOT NULL COMMENT 'Status: Active, Inactive',
  PRIMARY KEY (`student_id`),
  CONSTRAINT `fk_student_id`
    FOREIGN KEY (`student_id`)
    REFERENCES `LingoAmigo`.`User` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Teacher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Teacher` (
  `teacher_id` INT NOT NULL,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `nationality` VARCHAR(255) NOT NULL,
  `description` TEXT NULL,
  `phone` VARCHAR(15) NOT NULL,
  `image_url` VARCHAR(255) NULL,
  `status` VARCHAR(255) NOT NULL COMMENT 'Status: Active, Inactive',
  `date_join` DATE NULL,
  PRIMARY KEY (`teacher_id`),
  CONSTRAINT `fk_teacher_id`
    FOREIGN KEY (`teacher_id`)
    REFERENCES `LingoAmigo`.`User` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Expert`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Expert` (
  `expert_id` INT NOT NULL,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `nationality` VARCHAR(255) NOT NULL,
  `description` TEXT NULL,
  `phone` VARCHAR(15) NOT NULL,
  `image_url` VARCHAR(255) NULL,
  `status` VARCHAR(255) NOT NULL COMMENT 'Status: Active, Inactive',
  `date_join` DATE NULL,
  PRIMARY KEY (`expert_id`),
  CONSTRAINT `fk_expert_id`
    FOREIGN KEY (`expert_id`)
    REFERENCES `LingoAmigo`.`User` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Administrator`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Administrator` (
  `admin_id` INT NOT NULL,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `description` TEXT NULL,
  `phone` VARCHAR(15) NOT NULL,
  `image_url` VARCHAR(255) NULL,
  `status` VARCHAR(255) NOT NULL COMMENT 'Status: Active, Inactive',
  PRIMARY KEY (`admin_id`),
  CONSTRAINT `fk_admin_id`
    FOREIGN KEY (`admin_id`)
    REFERENCES `LingoAmigo`.`User` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Language`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Language` (
  `language_id` INT NOT NULL AUTO_INCREMENT,
  `language_name` VARCHAR(255) NOT NULL,
  `image_url` VARCHAR(255) NULL,
  PRIMARY KEY (`language_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Course`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Course` (
  `course_id` INT NOT NULL AUTO_INCREMENT,
  `course_name` VARCHAR(255) NOT NULL,
  `description` TEXT NULL,
  `duration` INT NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `image_url` VARCHAR(255) NULL,
  `status` VARCHAR(255) NOT NULL COMMENT 'Status: Active, Inactive, Pending',
  `creator_id` INT NOT NULL,
  `language_id` INT NOT NULL,
  PRIMARY KEY (`course_id`),
  INDEX `fk_creator_id_idx` (`creator_id` ASC) VISIBLE,
  INDEX `fk_language_id_idx` (`language_id` ASC) VISIBLE,
  CONSTRAINT `fk_creator_id`
    FOREIGN KEY (`creator_id`)
    REFERENCES `LingoAmigo`.`User` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_language_id`
    FOREIGN KEY (`language_id`)
    REFERENCES `LingoAmigo`.`Language` (`language_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Section`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Section` (
  `section_id` INT NOT NULL AUTO_INCREMENT,
  `course_id` INT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `content` TEXT NULL,
  PRIMARY KEY (`section_id`),
  INDEX `fk_course_id_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_course_id`
    FOREIGN KEY (`course_id`)
    REFERENCES `LingoAmigo`.`Course` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Video`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Video` (
  `video_id` INT NOT NULL AUTO_INCREMENT,
  `section_id` INT NOT NULL,
  `video_url` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`video_id`),
  INDEX `fk_section_id_idx` (`section_id` ASC) VISIBLE,
  CONSTRAINT `fk_section_id`
    FOREIGN KEY (`section_id`)
    REFERENCES `LingoAmigo`.`Section` (`section_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Quiz`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Quiz` (
  `quiz_id` INT NOT NULL AUTO_INCREMENT,
  `course_id` INT NOT NULL,
  `description` TEXT NULL,
  PRIMARY KEY (`quiz_id`),
  INDEX `fk_quiz_course_id_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_quiz_course_id`
    FOREIGN KEY (`course_id`)
    REFERENCES `LingoAmigo`.`Course` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Question`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Question` (
  `question_id` INT NOT NULL AUTO_INCREMENT,
  `quiz_id` INT NOT NULL,
  `content` TEXT NOT NULL,
  `answer` TEXT NOT NULL,
  PRIMARY KEY (`question_id`),
  INDEX `fk_quiz_id_idx` (`quiz_id` ASC) VISIBLE,
  CONSTRAINT `fk_quiz_id`
    FOREIGN KEY (`quiz_id`)
    REFERENCES `LingoAmigo`.`Quiz` (`quiz_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`StudentAnswer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`StudentAnswer` (
  `answer_id` INT NOT NULL AUTO_INCREMENT,
  `question_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `student_answer` TEXT NOT NULL,
  PRIMARY KEY (`answer_id`),
  INDEX `fk_question_id_idx` (`question_id` ASC) VISIBLE,
  INDEX `fk_answer_user_id_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_question_id`
    FOREIGN KEY (`question_id`)
    REFERENCES `LingoAmigo`.`Question` (`question_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_answer_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `LingoAmigo`.`User` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`VideoComments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`VideoComments` (
  `comment_id` INT NOT NULL AUTO_INCREMENT,
  `video_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `content` TEXT NOT NULL,
  `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_id`),
  INDEX `fk_video_id_idx` (`video_id` ASC) VISIBLE,
  INDEX `fk_comment_user_id_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_video_id`
    FOREIGN KEY (`video_id`)
    REFERENCES `LingoAmigo`.`Video` (`video_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comment_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `LingoAmigo`.`User` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`DiscussionBoard`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`DiscussionBoard` (
  `discussion_id` INT NOT NULL AUTO_INCREMENT,
  `course_id` INT NOT NULL,
  `description` TEXT NULL,
  `language_id` INT NOT NULL,
  PRIMARY KEY (`discussion_id`),
  INDEX `fk_discussion_course_id_idx` (`course_id` ASC) VISIBLE,
  INDEX `fk_discussion_language_id_idx` (`language_id` ASC) VISIBLE,
  CONSTRAINT `fk_discussion_course_id`
    FOREIGN KEY (`course_id`)
    REFERENCES `LingoAmigo`.`Course` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_discussion_language_id`
    FOREIGN KEY (`language_id`)
    REFERENCES `LingoAmigo`.`Language` (`language_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Post` (
  `post_id` INT NOT NULL AUTO_INCREMENT,
  `discussion_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `topic` TEXT NOT NULL,
  `content` TEXT NOT NULL,
  `timestamp` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`post_id`),
  INDEX `fk_discussion_id_idx` (`discussion_id` ASC) VISIBLE,
  INDEX `fk_discussion_user_id_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_discussion_id`
    FOREIGN KEY (`discussion_id`)
    REFERENCES `LingoAmigo`.`DiscussionBoard` (`discussion_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_discussion_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `LingoAmigo`.`User` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Order` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `course_id` INT NOT NULL,
  `order_date` DATE NOT NULL,
  `status` VARCHAR(255) NOT NULL COMMENT 'Status:  Pending, Completed, Cancelled, InCart',
  PRIMARY KEY (`order_id`),
  INDEX `fk_order_user_id_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_order_course_id_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `fk_order_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `LingoAmigo`.`User` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_course_id`
    FOREIGN KEY (`course_id`)
    REFERENCES `LingoAmigo`.`Course` (`course_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Resource`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Resource` (
  `resource_id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(255) NOT NULL COMMENT 'News, Research, Article, Tutorial',
  `topic` TEXT NOT NULL,
  `content` TEXT NOT NULL,
  `published_date` DATE NOT NULL,
  `creator_id` INT NOT NULL,
  `image_url` VARCHAR(255) NULL,
  `details` TEXT NOT NULL,
  PRIMARY KEY (`resource_id`),
  INDEX `fk_resource_creator_id_idx` (`creator_id` ASC) VISIBLE,
  CONSTRAINT `fk_resource_creator_id`
    FOREIGN KEY (`creator_id`)
    REFERENCES `LingoAmigo`.`User` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LingoAmigo`.`Session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LingoAmigo`.`Session` (
  `session_id` INT NOT NULL AUTO_INCREMENT,
  `student_id` INT NOT NULL,
  `expert_id` INT NOT NULL,
  `start_time` DATETIME NOT NULL,
  `end_time` DATETIME NULL,
  `status` VARCHAR(255) NULL COMMENT 'Scheduled, InProgress, Completed, Cancelled',
  PRIMARY KEY (`session_id`),
  INDEX `fk_session_student_id_idx` (`student_id` ASC) VISIBLE,
  INDEX `fk_session_expert_id_idx` (`expert_id` ASC) VISIBLE,
  CONSTRAINT `fk_session_student_id`
    FOREIGN KEY (`student_id`)
    REFERENCES `LingoAmigo`.`Student` (`student_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_session_expert_id`
    FOREIGN KEY (`expert_id`)
    REFERENCES `LingoAmigo`.`Expert` (`expert_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

INSERT INTO `User` (`user_id`, `username`, `password`, `role`)
VALUES
    (1, 'student1', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (2, 'student2', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (3, 'student3', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (4, 'student4', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (5, 'student5', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (6, 'student6', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (7, 'student7', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (8, 'student8', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (9, 'student9', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (10, 'student10', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (11, 'student11', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (12, 'student12', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (13, 'student13', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (14, 'student14', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (15, 'student15', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Student'),
    (16, 'teacher1', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Teacher'),
    (17, 'teacher2', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Teacher'),
    (18, 'teacher3', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Teacher'),
    (19, 'teacher4', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Teacher'),
    (20, 'teacher5', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Teacher'),
    (21, 'teacher6', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Teacher'),
    (22, 'teacher7', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Teacher'),
    (23, 'expert1', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Expert'),
    (24, 'expert2', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Expert'),
    (25, 'expert3', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Expert'),
    (26, 'admin1', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Administrator'),
    (27, 'admin2', '63dadcbaca62ede48501b131fa0841d136b4ccda56d8732184fba08f457c9bab', 'Administrator');


INSERT INTO `Student` 
(`student_id`, `first_name`, `last_name`, `email`, `date_birth`, `phone`, `image_url`, `status`) 
VALUES 
(1, 'Sophia', 'Lin', 'sophialin@example.com', '1993-01-02', '0230234789', 'sophialin.jpg', 'Active'),
(2, 'Aya', 'Tanaka', 'ayatanaka@example.com', '1995-03-03', '0211234256', 'ayatanaka.jpg', 'Active'),
(3, 'Yuta', 'Nakamoto', 'yutanakamoto@example.com', '1999-02-24', '0212345267', 'yutanakamoto.jpg', 'Active'),
(4, 'Mason', 'Jones', 'masonjones@example.com', '1993-04-23', '0234667833', 'masonjones.jpg', 'Active'),
(5, 'Ethan', 'Weber', 'ethanweber@example.com', '1994-07-12', '0221234567', 'ethanweber.jpg', 'Active'),
(6, 'Taeyong', 'Lee', 'taeyonglee@example.com', '1996-05-23', '0212222787', 'taeyonglee.jpg', 'Active'),
(7, 'Dejun', 'Xiao', 'dejunxiao@example.com', '1999-06-18', '0271277866', 'dejunxiao.jpg', 'Active'),
(8, 'Seoyeon', 'Yoon', 'seoyeonyoon@example.com', '1992-12-11', '0291234897', 'seoyeonyoon.jpg', 'Active'),
(9, 'Kotone', 'Kamimoto', 'kotonekamimoto@example.com', '1999-01-12', '0231784567', 'kotonekamimoto.jpg', 'Active'),
(10, 'Xinyu', 'Zhou', 'xinyuzhou@example.com', '1998-11-25', '0231745367', 'xinyuzhou.jpg', 'Active'),
(11, 'Sohyun', 'Park', 'sohyunpark@example.com', '1996-12-11', '0232154789', 'sohyunpark.jpg', 'Active'),
(12, 'Chenle', 'Zhong', 'chenlezhong@example.com', '1994-07-28', '0221356789', 'chenlezhong.jpg', 'Active'),
(13, 'Hina', 'Terasaki', 'hinaterasaki@example.com', '1995-09-06', '02263474876', 'hinaterasaki.jpg', 'Active'),
(14, 'Moka', 'Shima', 'mokashima@example.com', '1997-05-07', '0232675835', 'mokashima.jpg', 'Active'),
(15, 'Yaning', 'Fu', 'yaningfu@example.com', '1993-06-18', '0211234569', 'yaningfu.jpg', 'Active');

INSERT INTO `Teacher` 
(`teacher_id`, `first_name`, `last_name`, `email`, `title`, `nationality`, `description`, `phone`, `image_url`, `status`, `date_join`) 
VALUES 
(16, 'Henry', 'Moore', 'henrymoore@example.com', 'Mr', 'English', 'Henry Moore is an experienced English teacher known for his dynamic teaching style and passion for language education. With a background in linguistics and several years of teaching experience both domestically and abroad, Henry specializes in creating engaging lesson plans that cater to the diverse needs of his students. ', '0211234123', 'henrymoore.jpg', 'Active', '2023-09-01'),
(17, 'Lusi', 'Wu', 'lusiwu@example.com', 'Miss', 'Chinese', 'Lusi Wu is a dedicated Chinese language teacher with a strong background in Mandarin education. After earning her degree in Chinese Language and Literature, she has been actively teaching Mandarin in various settings for over a decade. ', '0271256178', 'lusiwu.jpg', 'Active', '2023-10-08'),
(18, 'Chaewon', 'Kim', 'chaewonkim@example.com', 'Miss', 'Korean', 'Chaewon Kim is an enthusiastic Korean language teacher with extensive experience in language instruction. She holds a master degree in Korean as a Foreign Language and has been teaching Korean to international students for several years. ', '0221236278', 'chaewonkim.jpg', 'Active', '2023-08-10'),
(19, 'Sakura', 'Miyawaki', 'sakuramiyawaki@example.com', 'Ms', 'Japanese', 'Sakura is a passionate Japanese language teacher with a deep understanding of both the language and its cultural context. She has a bachelor degree in Japanese Studies and has spent several years teaching Japanese at various language institutes.', '0271928765', 'sakuramiyawaki.jpg', 'Active', '2023-09-22'),
(20, 'Amelie', 'Gautier', 'ameliegautier@example.com', 'Ms', 'French', 'Amelie Gautier is a dedicated French teacher with a strong passion for language education and cultural exchange. She holds a Master degree in French Literature and has been teaching French for over ten years in various international settings. ', '0211235765', 'ameliegautier.jpg', 'Active', '2023-06-21'),
(21, 'Oskar', 'Krause', 'oskarkrause@example.com', 'Mr', 'German', 'Oskar Krause is an experienced German language teacher with a profound knowledge of German literature and linguistics. He earned his Master degree in German Studies and has been teaching German in various educational settings for over a decade. ', '0226578456', 'oskarkrause.jpg', 'Active', '2023-11-15'),
(22, 'Matteo', 'Torres', 'matteotorres@example.com', 'Mr', 'Spanish', 'Matteo Torres is a dynamic Spanish language teacher with extensive experience in language instruction. Originally from Spain, he holds a degree in Hispanic Studies and has taught Spanish at various academic institutions for over fifteen years. ', '0219865345', 'matteotorres.jpg', 'Active', '2023-12-19');

INSERT INTO `Expert` 
(`expert_id`, `first_name`, `last_name`, `email`, `title`, `nationality`, `description`, `phone`, `image_url`, `status`, `date_join`) 
VALUES 
(23, 'Tom', 'Williams', 'tomwilliams@example.com', 'Mr', 'American', 'Tom Williams is a multilingual language expert proficient in English, German, and Spanish. With a background in Applied Linguistics, Tom has over twenty years of experience teaching these languages in various international contexts. He is known for his comprehensive and adaptable teaching methods that cater to diverse learning styles. Toms lessons are engaging and focus on practical language use, intercultural communication, and professional language applications, helping students to become confident and versatile language users.', '0214567345', 'tomwilliams.jpg', 'Active', '2023-01-04'),
(24, 'Lily', 'Evans', 'lilyevans@example.com', 'Ms', 'English', 'Lily Evans is a skilled polyglot and language instructor proficient in English, German, French, and Japanese. She holds advanced degrees in Modern Languages and has been teaching these languages at universities and private institutions for over fifteen years. Lilys approach to teaching is highly personalized, focusing on each students individual goals and learning pace. She incorporates a blend of traditional and innovative teaching methods, aiming to make language learning accessible and enjoyable for everyone. Her expertise in multiple languages allows her to provide unique insights into language structure and culture.', '0234563546', 'lilyevans.jpg', 'Active', '2023-01-08'),
(25, 'Lanzhu', 'Ruan', 'lanzhuruan@example.com', 'Mr', 'Chinese', 'Ruan is a multilingual language expert proficient in Chinese, Korean, Japanese, and English. With a Ph.D. in Language Education, Ruan has been teaching these languages at both university and corporate levels for over two decades. His teaching philosophy emphasizes practical usage and deep cultural immersion. Ruans classes are renowned for their interactive nature and focus on real-world applications. He excels in adapting his teaching strategies to accommodate the diverse needs of his students, ensuring that they not only learn the languages but also understand the cultural nuances that come with them.', '0273452678', 'lanzhuruan.jpg', 'Active', '2023-01-17');

INSERT INTO `Administrator` 
(`admin_id`, `first_name`, `last_name`, `email`, `title`, `description`, `phone`, `image_url`, `status`) 
VALUES 
(26, 'Olivia', 'Benson', 'oliviabenson@example.com', 'Ms', 'Administrator, manage site content, handle user inquiries and feedback, and ensure the website runs smoothly. ', '0222364789', 'oliviabenson.jpg', 'Active'),
(27, 'Dexter', 'Morgan', 'dextermorgan@example.com', 'Mr', 'Administrator, manage site content, handle user inquiries and feedback, and ensure the website runs smoothly. ', '0212321889', 'dextermorgan.jpg', 'Active');

INSERT INTO `Language`
(`language_name`, `image_url`)
VALUES
('English', 'English.jpg'),
('Chinese', 'Chinese.jpg'),
('Korean', 'Korean.jpg'),
('Japanese', 'Japanese.jpg'),
('French', 'French.jpg'),
('German', 'German.jpg'),
('Spanish', 'Spanish.jpg');

INSERT INTO `Course`
(`course_name`, `description`, `duration`, `price`, `image_url`, `status`, `creator_id`, `language_id`)
VALUES
('Beginner English', 'Learn the basics of English grammar, pronunciation, and vocabulary to kickstart your language journey.', 5, 50.00, 'Beginner English.jpg', 'Active', 16, 1),
('Business English', 'Enhance your English communication skills in professional settings, focusing on business vocabulary and formal expressions.', 10, 70.00,'Business English.jpg', 'Active', 16, 1),
('Beginner Chinese', 'Introductory course to Mandarin Chinese, covering fundamental phrases and characters for daily communication.', 5, 50.00,'Beginner Chinese.jpg', 'Active', 17, 2),
('Business Chinese', 'Develop proficiency in Chinese for business contexts, learning specific terminology and cultural etiquette.', 10, 70.00,'Business Chinese.jpg', 'Active', 17, 2),
('Advanced Chinese', 'Deepen your understanding of Chinese through advanced vocabulary and grammar suitable for fluent speakers.', 5, 50.00,'Advanced Chinese.jpg', 'Active', 17, 2),
('Beginner Korean', 'Start your exploration of Korean with essential grammar and vocabulary for beginners.', 5, 50.00,'Beginner Korean.jpg', 'Active', 18, 3),
('Business Korean', 'Tailored for professionals, this course focuses on Korean business language and cultural insights.', 10, 70.00,'Business Korean.jpg', 'Active', 18, 3),
('Travel Korean', 'Prepare for travel in Korea by learning key phrases and cultural tips that enhance your travel experience.', 5, 50.00,'Travel Korean.jpg', 'Active', 18, 3),
('Beginner Japanese', 'Foundation course in Japanese, emphasizing basic expressions and everyday vocabulary.', 5, 50.00,'Beginner Japanese.jpg', 'Active', 19, 4),
('Business Japanese', 'Improve your business communication in Japanese, covering industry-specific terms and professional etiquette.', 10, 70.00,'Business Japanese.jpg', 'Active', 19, 4),
('Travel Japanese', 'Learn practical Japanese for tourists, including navigation, dining, and shopping essentials.', 10, 70.00,'Travel Japanese.jpg', 'Active', 19, 4),
('Beginner French', 'Discover the basics of French language and culture through engaging and practical scenarios.', 5, 50.00,'Beginner French.jpg', 'Active', 20, 5),
('Business French', 'Focuses on French used in business environments, helping you communicate effectively with French-speaking colleagues.', 10, 70.00,'Business French.jpg', 'Active', 20, 5),
('Beginner German', 'An introduction to German focusing on the essentials of grammar, vocabulary, and pronunciation.', 5, 50.00,'Beginner German.jpg', 'Active', 21, 6),
('Business German', 'Specialized course designed to enhance your German language skills in a business context.', 10, 70.00,'Business German.jpg', 'Active', 21, 6),
('Beginner Spanish', 'Learn Spanish from the ground up, focusing on the fundamental skills necessary for basic communication.', 5, 50.00,'Beginner Spanish.jpg', 'Active', 22, 7),
('Business Spanish', 'Equip yourself with the Spanish needed for professional success, focusing on business interactions and vocabulary.', 10, 70.00,'Business Spanish.jpg', 'Active', 22, 7),
('Conversational English', 'Develop fluency and conversational skills in everyday English.', 5, 35.00, 'Conversational English.jpg', 'Active', 16, 1),
('English for Tourism', 'Learn English language skills specifically tailored for tourism and hospitality.', 7, 65.00, 'English for Tourism.jpg', 'Active', 16, 1),
('English Literature', 'Explore classic and contemporary English literature to improve language and analytical skills.', 6, 40.00, 'English Literature.jpg', 'Active', 16, 1),
('Intermediate Chinese', 'Build on basic skills with more complex sentences and grammar in Mandarin.', 6, 25.00, 'Intermediate Chinese.jpg', 'Active', 17, 2),
('Chinese for Kids', 'Fun and engaging course designed for young learners to start Mandarin Chinese.', 5, 75.00, 'Chinese for Kids.jpg', 'Active', 17, 2),
('Chinese Calligraphy', 'Learn the art of Chinese calligraphy and its cultural significance.', 8, 40.00, 'Chinese Calligraphy.jpg', 'Active', 17, 2),
('Basic Korean', 'An introductory course for learning basic Korean phrases and grammar.', 6, 35.00, 'Basic Korean.jpg', 'Active', 18, 3),
('Korean Drama', 'Learn Korean by watching and discussing popular Korean dramas.', 5, 40.00, 'Korean Drama.jpg', 'Active', 18, 3),
('Korean History', 'Understand historical contexts to improve language and knowledge of Korean culture.', 6, 80.00, 'Korean History.jpg', 'Active', 18, 3),
('Japanese Culture', 'Deep dive into Japanese culture through language learning.', 5, 25.00, 'Japanese Culture.jpg', 'Active', 19, 4),
('Anime Japanese', 'Learn Japanese by analyzing language used in popular anime.', 6, 35.00, 'Anime Japanese.jpg', 'Active', 19, 4),
('Japanese Cooking Terms', 'Explore the culinary world of Japan by learning specific cooking terms.', 5, 60.00, 'Japanese Cooking Terms.jpg', 'Active', 19, 4);

INSERT INTO `Section`
(`course_id`, `title`, `content`)
VALUES
(1, 'Introduction to English', 'Overview of English language basics, including pronunciation and simple phrases.'),
(1, 'Basic Vocabulary', 'Learn essential everyday vocabulary that forms the foundation of basic communication.'),
(1, 'Grammar Essentials', 'Introduction to key grammatical structures, focusing on verb tenses and sentence construction.'),
(1, 'Practical Sentences', 'Practice forming simple sentences for everyday situations like shopping and dining.'),
(2, 'Workplace Communication', 'Techniques and vocabulary for effective communication in English-speaking business environments.'),
(2, 'Email and Report Writing', 'Skills for writing professional emails and business reports in English.'),
(2, 'Meeting and Negotiations', 'Language and strategies for conducting meetings and negotiations in English.'),
(2, 'Presentation Skills', 'Developing skills to deliver clear and impactful presentations in a professional setting.'),
(3, 'Introduction to Mandarin', 'Basic sounds, tones, and character recognition in Mandarin Chinese.'),
(3, 'Essential Phrases', 'Common phrases used in daily interactions, focusing on greetings and basic questions.'),
(3, 'Chinese Characters', 'Introduction to writing basic Chinese characters and understanding their structure.'),
(3, 'Everyday Conversations', 'Practical dialogue scenarios to practice daily communication in Chinese.'),
(4, 'Business Etiquette', 'Understanding the cultural nuances and etiquette essential for doing business in China.'),
(4, 'Formal Language', 'Learn formal expressions and vocabulary specific to Chinese business contexts.'),
(4, 'Negotiating in Chinese', 'Key phrases and strategies for negotiation settings.'),
(4, 'Business Writing', 'Techniques for writing formal business documents such as proposals and emails.'),
(5, 'Advanced Grammar', 'In-depth exploration of complex grammatical structures used in sophisticated Chinese.'),
(5, 'Literary Chinese', 'Study of classical Chinese texts and their modern interpretations.'),
(5, 'Professional Vocabulary', 'Expansion of vocabulary to include industry-specific terms.'),
(5, 'Fluency Practices', 'Activities designed to improve fluency and comprehension of advanced spoken and written Chinese.'),
(6, 'Korean Alphabet', 'Learning the Hangul alphabet and its pronunciation basics.'),
(6, 'Basic Expressions', 'Essential expressions for greetings, farewells, and common questions.'),
(6, 'Grammar Fundamentals', 'Overview of basic Korean grammar, including verb conjugations.'),
(6, 'Korean Culture', 'Insights into Korean culture and customs relevant to everyday communication.'),
(7, 'Corporate Culture in Korea', 'Understanding the workplace norms and business practices unique to Korea.'),
(7, 'Formal and Informal Speech', 'Learning to distinguish between formal and informal speech in a business setting.'),
(7, 'Business Terminology', 'Key terms and phrases used in the Korean business world.'),
(7, 'Client Interaction', 'Language skills for interacting with Korean clients, including hospitality and respect.'),
(8, 'Travel Phrases', 'Must-know phrases for navigating travel in Korea, from transportation to accommodations.'),
(8, 'Eating Out', 'Language for ordering food and understanding menus in Korean restaurants.'),
(8, 'Shopping in Korea', 'Vocabulary and phrases for shopping, bargaining, and understanding prices.'),
(8, 'Cultural Tips', 'Helpful cultural knowledge that will enhance the travel experience in Korea.'),
(9, 'Introduction to Japanese', 'Learn the basics of Japanese pronunciation and the writing systems: Hiragana, Katakana, and introductory Kanji.'),
(9, 'Daily Expressions', 'Essential phrases for everyday situations including greetings, thanks, and apologies.'),
(9, 'Basic Grammar', 'Foundational Japanese grammar, focusing on particle usage and verb conjugation.'),
(9, 'Cultural Insights', 'An introduction to Japanese culture through language, understanding social norms and practices.'),
(10, 'Professional Etiquette', 'Key cultural and language considerations for maintaining professionalism in Japan.'),
(10, 'Business Vocabulary', 'Specific vocabulary and phrases used in Japanese business settings.'),
(10, 'Formal Communications', 'Writing and speaking formally in Japanese, including keigo (honorific language).'),
(10, 'Meeting Protocols', 'Language and strategies for participating effectively in business meetings in Japan.'),
(11, 'Navigational Phrases', 'Learn key phrases to ask for directions, use public transport, and navigate cities.'),
(11, 'Tourist Transaction', 'Communicating in hotels, restaurants, and tourist spots effectively.'),
(11, 'Cultural Dos and Donts', 'Understanding important cultural etiquette to enhance interaction with locals.'),
(11, 'Emergency Situations', 'Essential language skills for handling emergencies while traveling in Japan.'),
(12, 'French Basics', 'Introduction to basic French phrases, numbers, and important verbs.'),
(12, 'Conversational French', 'Practical language skills for engaging in simple conversations with native speakers.'),
(12, 'French Pronunciation', 'Guidance on mastering French pronunciation to enhance clarity in communication.'),
(12, 'French Culture 101', 'Exploring French traditions, cultural nuances, and lifestyle through language.'),
(13, 'Corporate French', 'Specialized vocabulary and structures for a French-speaking professional environment.'),
(13, 'Client Communication', 'Effective techniques for communicating with French-speaking clients and partners.'),
(13, 'Report Writing', 'Skills for composing clear and professional reports in French.'),
(13, 'Negotiation in French', 'Language and cultural tips for successful negotiations in French business settings.'),
(14, 'Getting Started with German', 'An introduction to German sounds, alphabet, and simple sentence structure.'),
(14, 'Essential German Vocabulary', 'Key words and phrases to start building your German language foundation.'),
(14, 'Basic German Grammar', 'An overview of German grammatical rules, including cases and verb conjugations.'),
(14, 'German Cultural Norms', 'Insights into the German way of life and everyday cultural practices.'),
(15, 'German for the Workplace', 'Language skills tailored for the German business environment, focusing on formal speech.'),
(15, 'Professional Writing', 'Techniques for writing business emails, letters, and reports in German.'),
(15, 'Business Meetings', 'Vocabulary and phrases for participating in meetings, presentations, and business discussions.'),
(15, 'Cultural Competence in Business', 'Understanding German business etiquette and cultural expectations.'),
(16, 'Spanish Fundamentals', 'Core Spanish vocabulary and grammar for beginners, focusing on practical usage.'),
(16, 'Conversational Spanish', 'Basic conversational skills for everyday interactions in Spanish.'),
(16, 'Listening and Pronunciation', 'Exercises to improve listening skills and pronunciation accuracy.'),
(16, 'Hispanic Cultural Introduction', 'An overview of the diverse cultures and traditions across Spanish-speaking countries.'),
(17, 'Spanish in the Office', 'Language essentials for navigating a Spanish-speaking business environment.'),
(17, 'Business Correspondence', 'Skills for crafting professional emails and other business communications in Spanish.'),
(17, 'Presentations in Spanish', 'Developing the ability to deliver clear and effective business presentations.'),
(17, 'Networking in Spanish', 'Phrases and strategies for building and maintaining professional relationships in Spanish.'),
(18, 'Speaking Practice', 'Engage in interactive speaking exercises to enhance conversational fluency.'),
(18, 'Listening Skills', 'Improve comprehension through listening to native speakers in various scenarios.'),
(18, 'Everyday Vocabulary', 'Expand your vocabulary with words and phrases used in everyday communication.'),
(18, 'Dialogue Construction', 'Learn to construct and understand dialogues in everyday contexts.'),
(19, 'Hospitality Phrases', 'Learn key phrases used in the tourism and hospitality industry.'),
(19, 'Customer Interactions', 'Practice language skills necessary for customer service and guest interactions.'),
(19, 'Cultural Tips', 'Gain insights into cultural norms and etiquette relevant to English-speaking tourists.'),
(19, 'Guided Tour Language', 'Develop skills to organize and give guided tours in English.'),
(20, 'Introduction to Literature', 'Overview of significant English literary works and authors.'),
(20, 'Analyzing Texts', 'Techniques for literary analysis, focusing on themes, motifs, and character development.'),
(20, 'Modern English Literature', 'Exploration of contemporary works and their relevance to modern society.'),
(20, 'Literary Criticism', 'Introduction to various schools of thought in literary criticism.'),
(21, 'Complex Grammar', 'Study more complex grammatical structures to improve sentence formation.'),
(21, 'Reading Comprehension', 'Enhance reading skills with intermediate-level texts.'),
(21, 'Writing Improvement', 'Practice writing paragraphs and short essays.'),
(21, 'Conversational Phrases', 'Learn phrases suitable for more nuanced conversations.'),
(22, 'Basic Words and Phrases', 'Simple and fun introduction to Mandarin words and phrases.'),
(22, 'Songs and Games', 'Learning through songs and games to keep young students engaged.'),
(22, 'Character Recognition', 'Begin to recognize and write basic Chinese characters.'),
(22, 'Everyday Conversations', 'Practice simple conversations suitable for young learners.'),
(23, 'Introduction to Calligraphy', 'Basics of Chinese calligraphy, including brush handling and strokes.'),
(23, 'Calligraphic Styles', 'Study different styles of calligraphy from classical to modern.'),
(23, 'Practice Sessions', 'Guided practice sessions to refine brush control and form.'),
(23, 'Cultural Significance', 'Understanding the historical and cultural context of calligraphy in China.'),
(24, 'Korean Alphabet', 'Introduction to Hangul, the Korean alphabet, and its pronunciation.'),
(24, 'Essential Grammar', 'Foundations of Korean grammar needed for basic communication.'),
(24, 'Building Vocabulary', 'Key vocabulary necessary for day-to-day conversations.'),
(24, 'Practical Phrases', 'Phrases useful for navigating daily activities and interactions.'),
(25, 'Drama Selection', 'Choose dramas that offer rich learning opportunities.'),
(25, 'Language in Context', 'Analyzing the language used in different scenes and contexts.'),
(25, 'Cultural Insights', 'Exploring cultural elements presented in dramas.'),
(25, 'Discussion and Review', 'Group discussions to reinforce language learning and comprehension.'),
(26, 'Historic Periods', 'Overview of key periods in Korean history.'),
(26, 'Significant Events', 'Study of major events and their impact on Korean society.'),
(26, 'Historical Figures', 'Learn about influential figures in Korean history and their contributions.'),
(26, 'Language of History', 'Specialized vocabulary related to historical descriptions and narratives.'),
(27, 'Traditional vs Modern', 'Contrast traditional and modern aspects of Japanese culture.'),
(27, 'Cultural Practices', 'Deep dive into unique cultural practices and their language expressions.'),
(27, 'Festivals and Ceremonies', 'Learn about important Japanese festivals and ceremonies and related vocabulary.'),
(27, 'Cultural Icons', 'Introduction to iconic cultural symbols and their significance.'),
(28, 'Anime Genres', 'Explore different genres of anime and their specific linguistic styles.'),
(28, 'Character Archetypes', 'Study the language used by different types of anime characters.'),
(28, 'Slang and Expressions', 'Learn slang and unique expressions commonly found in anime.'),
(28, 'Narrative Analysis', 'Analyzing storytelling techniques and dialogue in popular anime.'),
(29, 'Basic Cooking Terms', 'Introduction to essential cooking terms used in Japanese cuisine.'),
(29, 'Ingredient Names', 'Learn the names of common and specialty ingredients found in Japanese dishes.'),
(29, 'Cooking Techniques', 'Detailed explanation of cooking techniques unique to Japanese food.'),
(29, 'Recipe Language', 'Language skills needed to follow and understand Japanese recipes.');


INSERT INTO `Order`
(`user_id`, `course_id`, `order_date`, `status`)
VALUES
(1, 18, '2024-08-01', 'Completed'),
(2, 19, '2024-07-21', 'Completed'),
(3, 20, '2024-08-01', 'Pending'),
(4, 21, '2024-07-23', 'Completed'),
(1, 22, '2024-08-01', 'Pending'),
(2, 23, '2024-07-22', 'Pending'),
(3, 24, '2024-06-26', 'Completed'),
(4, 25, '2024-08-01', 'Pending'),
(1, 26, '2024-06-19', 'Completed'),
(2, 27, '2024-05-28', 'Completed'),
(3, 28, '2024-07-18', 'Completed'),
(4, 18, '2024-07-17', 'Completed'),
(1, 19, '2024-08-01', 'Pending'),
(2, 20, '2024-07-19', 'Cancelled'),
(3, 21, '2024-06-29', 'Completed'),
(4, 22, '2024-07-22', 'Completed'),
(1, 23, '2024-06-16', 'Completed'),
(2, 24, '2024-07-16', 'Completed');

INSERT INTO `Resource`
(`type`, `topic`, `content`, `published_date`, `creator_id`, `image_url`, `details`)
VALUES
('News', 'Emerging Trends in Language Learning Technology', 'Exploring cutting-edge technologies such as AI-driven language tutors and adaptive learning platforms that personalize the language learning experience for each user.', '2024-07-01', 26, 'Emerging Trends in Language Learning Technology.jpg', 'Language learning has evolved significantly in recent years, with new technologies shaping how we acquire and master languages. From innovative applications to immersive experiences, these advancements promise to make language acquisition more effective, engaging, and accessible for learners worldwide. As we look ahead, it is essential to explore the emerging technologies and trends that will revolutionize the future of language learning. The landscape of language learning is rapidly evolving with the integration of artificial intelligence (AI) and machine learning technologies.
AI-driven language tutors are becoming increasingly sophisticated, capable of offering personalized lessons and feedback that adapt to the individual learning pace and style of each user. Additionally, adaptive learning platforms utilize algorithms to adjust content difficulty and topics in real-time, ensuring that learners remain engaged and challenged. Such technologies not only make learning more accessible and efficient but also significantly enhance the retention and application of new languages.'),
('News', 'New Study Reveals Effective Language Learning Techniques', 'Recent research highlights the effectiveness of spaced repetition and immersive methods in language acquisition, offering valuable insights for learners.', '2024-07-05', 27, 'New Study Reveals Effective Language Learning Techniques.jpg', 'Learning strategies are procedures that facilitate a learning task. Strategies are most often conscious and goal-driven, especially in the beginning stages of tackling an unfamiliar language task. Once a learning strategy becomes familiar through repeated use, it may be used with some automaticity, but most learners will, if required, be able to call the strategy to conscious awareness. Learning strategies are important in second language learning and teaching for two major reasons. First, by examining the strategies used by second language learners during the language learning process, we gain insights into the metacognitive, cognitive, social, and affective processes involved in language learning. The second reason supporting research into language learning strategies is that less successful language learners can be taught new strategies, thus helping them become better language learners (Grenfell & Harris, 1999). Numerous descriptive studies have addressed the goal of understanding the range and type of learning strategies used by good language learners and the differences in learning strategy use between more and less effective learners. However, until relatively recently there have been fewer studies focusing on the second goal of trying to teach language learning strategies in classroom settings.'),
('News', 'Government Initiatives to Promote Multilingual Education', 'Governments worldwide are launching new programs to encourage multilingual education in schools, aiming to foster global communication skills among young learners.', '2024-07-12', 27, 'Government Initiatives to Promote Multilingual Education.jpg', 'In todays world, multilingual contexts are the norm rather than the exception. The United Nations Educational, Scientific and Cultural Organization (UNESCO) World Atlas of Languages reveals that there are around 7,000 spoken or signed languages in use around the world. It is estimated that at least half of the global population is bilingual, navigating daily life in two or more languages or dialects.'),
('News', 'Celebrating Cultural Diversity through Language', 'A fun and meaningful activity can help early elementary students appreciate the different languages in their backgrounds.', '2024-07-16', 26, 'Celebrating Cultural Diversity through Language.jpg', 'Language diversity has never been more real in classrooms around the world. With globalization comes increased mobility, and the language of instruction may not be the one our students choose when they think; speak to their parents, grandparents, and friends; watch TV; read; and listen to music. Acknowledging our students language backgrounds and experiences can be powerful: Not only does it contribute to fostering a sense of belonging, but also it supports learners in building their self-identity and celebrating each others differences.'),
('News', 'The Impact of Language Learning on Career Opportunities', 'Insights into how proficiency in multiple languages can open up diverse career paths in international business, diplomacy, and beyond.', '2024-07-19', 26, 'The Impact of Language Learning on Career Opportunities.jpg', 'You have probably heard that being multilingual is a great resume builder and a valuable asset to promote career growth. Being able to speak a language that is in demand may even result in a promotion or a higher salary, especially in a competitive industry like the technology sector. I wanted to move beyond anecdotal information and quantify the value of speaking another language in the workplace.
To be clear, these benefits translate to advantages for all language learners, no matter the platform they use to learn their language of choice. Whether you ere using one of the many enterprise solutions available or you have opted for a DIY approach with mobile apps — some of which are free or freemium — or books and websites, many surveys and studies indicate the power of language can pay real dividends for your career.'),
('News', 'Language Learning Apps: Which Ones Work Best?', 'A comparative review of popular language learning apps, focusing on user experiences, affordability, and overall effectiveness in real-world scenarios.', '2024-07-22', 27, 'Language Learning Apps.jpg', 'If you are traveling soon to a place where you do not know the language well (or at all), then you will want to download a language learning app to your smartphone before you embark on your journey. These apps can help you whether you are on your latest family vacation, an unforgettable trip with friends or even a honeymoon.
“I always advise clients who book trips with us to use a language learning app if they do not already know the language where they are going. I have done it myself on my vacations,” says travel agent Liz Harnos, co-owner of Burr Travel, a Northport, New York-based travel agency. “These apps can help you learn enough that you willll be able to order food, ask for directions and other basic things during your trip.”
Even if you have no travel plans in the near future and you just want to learn a new language for your own betterment, then using a language learning app on your smartphone or laptop can be the right choice for you. To find the best one, we tested five candidates over the course of five weeks. On our list were the premium (i.e., paid) versions of Babbel, Busuu Premium Plus, Memrise, Rosetta Stone and Super Duolingo. We tested each of them for ease of setup, design and features.
We learned two important things during testing: 1) some of the apps are easier to use than others, and 2) these apps can teach you the basics for up to 38 different languages, depending on the app. When all our testing was done, we found that Rosetta Stone emerged as the winner because of its easy-to-use design and the way it presented its lessons in the most logical manner.'),
('Research', 'Neurological Effects of Bilingualism', 'This study examines how managing two languages influences cognitive processes and brain structure, suggesting enhanced executive functions among bilinguals.', '2024-07-15', 24, 'Neurological Effects of Bilingualism.jpg', 'Bilingualism affects the structure of the brain in adults, as evidenced by experience-dependent grey and white matter changes in brain structures implicated in language learning, processing, and control. However, limited evidence exists on how bilingualism may influence brain development. We examined the developmental patterns of both grey and white matter structures in a cross-sectional study of a large sample (n=711 for grey matter, n=637 for white matter) of bilingual and monolingual participants, aged 3 to 21 years.
Metrics of grey matter (thickness, volume, and surface area) and white matter (fractional anisotropy and mean diffusivity) were examined across 41 cortical and subcortical brain structures and 20 tracts, respectively. We used generalized additive modelling to analyze whether, how, and where the developmental trajectories of bilinguals and monolinguals might differ. Bilingual and monolingual participants manifested distinct developmental trajectories in both grey and white matter structures. As compared to monolinguals, bilinguals showed: (a) more grey matter (less developmental loss) starting during late childhood and adolescence, mainly in frontal and parietal regions (particularly in the inferior frontal gyrus pars opercularis, superior frontal cortex, inferior and superior parietal cortex, and precuneus); and (b) higher white matter integrity (greater developmental increase) starting during mid-late adolescence, specifically in striatal inferior frontal fibers. The data suggest that there may be a developmental basis to the well-documented structural differences in the brain between bilingual and monolingual adults.'),
('Research', 'Efficiency of Mobile Apps in Language Acquisition', 'Research analyzing the effectiveness of mobile applications in facilitating language learning, focusing on user retention and language skills improvement over time.', '2024-07-18', 23, 'Efficiency of Mobile Apps in Language Acquisition.jpg', 'The advancements in communication technology enable learners to use mobile technology anytime and anywhere to access up-to-date educational resources tailored to their individual needs. Thus, mobile learning offers the potential for personalised, informal and ubiquitous learning processes, which is particularly important for language learning. Mobile-Assisted Language Learning leveraged by accessible mobile apps is an ideal setup for time and location independent language learning at an individual learning speed.
This paper analyses the effectiveness of three of the highest-trending language learning mobile apps of 2021/2022 by comparing their most current efficacy studies. Babbel, Busuu and Duolingo have been selected for this purpose. Although limiting the ranking of the apps language teaching effectiveness to the studies discussed is not advised, a critical analysis of the three efficacy studies showed Busuu to be in the lead. Its research provided the most comprehensive and outstanding results for reading/grammar and oral proficiency based on its design and the variables considered. Duolingo achieved even higher results for the receptive skills reading and listening, but it was considered second in line due its study design and the lack of control over various influencing factors (e.g. study time and prior proficiency). Finally, Babbel was considered the least effective, as most learners did not exceed the beginner level even though the duration of the study exceeded Busuus by four weeks.'),
('Research', 'Social Interaction and Language Proficiency', 'A detailed look at how social interactions can accelerate language learning, enhancing both fluency and conversational skills.', '2024-07-09', 25, 'Social Interaction and Language Proficiency.jpg', 'There is now considerable evidence that social interaction plays a critical role in language acquisition: Typically developing infants learning of new language material is excellent when language is experienced during social interaction with a live person, but virtually nonexistent when that same information is presented via a non-interactive machine; moreover, studies of children with autism implicate dual impairments in social and linguistic processing. These data have led to the theoretical hypothesis that social interaction “gates” language learning (Kuhl, 2007; 2011). However, the underlying brain mechanisms by which the social gating hypothesis might work are not well understood. This chapter reviews the brain and behavioral data on the effects of social interaction on language acquisition in children, and relates these findings to work on the acquisition of communicative repertoires in non-human animals.
We then review candidate brain systems that could explain the existing results. Finally, the chapter discusses new neuroscience approaches to the question, including studies that shed light on how the infant brain responds to speech, which may provide breakthrough data regarding social factors influencing language acquisition.'),
('Research', 'Age and Language Learning: A Comparative Study', 'Exploring the impact of age on language learning capabilities, with insights into critical periods for language acquisition.', '2024-06-21', 24, 'Age and Language Learning.jpg', 'The age a person has when they begin to acquire or learn a language is one of the most important factors influencing language acquisition. The critical period hypothesis is one well-known hypothesis that helps explain the effects of age and second language acquisition. Hartshorne and colleagues (2018) refer to the critical period as the time when adults ability to acquire a language diminishes. 
However, the researchers point out that a persons ability to acquire a language does not mean that ability disappears. A study in 2018 by Hartshorne and colleagues pointed out that children who begin to learn a language before the age of 10 to 12 can acquire the language better than older peers. Consequently, language learners under 12 are in the period for language acquisition.'),
('Research', 'The Role of Cultural Immersion in Language Education', 'This paper delves into how cultural immersion programs affect language learning outcomes, including linguistic competence and cultural understanding.', '2024-07-25', 25, 'The Role of Cultural Immersion in Language Education.jpg', 'Discover the significance of cultural immersion in language learning and learn how it can transform your language skills and those of your students.
This article explores why cultural immersion is essential to language learning, offering insights into its benefits and practical tips for integrating cultural experiences into your learning journey.
Imagine stepping into a bustling market in London, where every interaction, from haggling over prices to sharing a cup of tea with a local, deepens your understanding of English far beyond any textbook dialogue. This is cultural immersion, learning that transcends the confines of a classroom and taps into the vibrant heart of everyday life.
Cultural immersion does more than teach language; it breathes life into the words, embedding phrases and idioms in their rich, authentic contexts. As you laugh at a British sitcom or navigate the subtleties of local etiquette, you are not just learning English, you are living it.'),
('Research', 'Language Learning Strategies Among Polyglots', 'Investigating common techniques and patterns used by polyglots to master multiple languages, offering strategies that can be adopted by learners worldwide.', '2024-06-28', 25, 'Language Learning Strategies Among Polyglots.jpg', 'What sets a polyglot apart is not just the number of languages they speak, but their fervent passion for language and their strategic approach to learning. A polyglot dives into learning with a sense of exploration, smart planning, and an unyielding drive for real-world practice. They rarely depend on traditional classes alone; instead, they immerse themselves in the language, embrace modern tools, and often use creative resources like flashcard apps. Listening intently and speaking without fear, polyglots integrate vocabulary-building into their day-to-day lives, treating grammar as a puzzle to solve. At their core is a persistent, patient spirit and a choice to connect with language-speaking communities. These methods are the heartbeats of how polyglots learn languages, and with some dedication, you too can adopt these strategies to become a language maestro.'),
('Article', 'Top 5 Mistakes to Avoid in Language Learning', 'Uncover the common pitfalls that language learners face, from over-reliance on translation to neglecting speaking practice, and learn how to avoid them for more effective learning.', '2024-07-29', 23, 'Top 5 Mistakes to Avoid in Language Learning.jpg', '1. First language interference.
2. Pronunciation.
3. Grammar.
4. Vocabulary.
5. Imbalance of skills.'),
('Article', 'How to Choose the Right Language Learning Platform', 'Guidance on selecting the best language learning platform tailored to your needs, considering factors like learning style, goals, and available features.', '2024-07-18', 24, 'How to Choose the Right Language Learning Platform.jpg', 'Learning a new language brings many benefits to our lives, both personally and in the workplace. More and more users are beginning their language studies on language learning platforms.
If you are still confused about how to choose the best platform to learn languages, trust us, you are not alone. Sometimes you might lose interest due to a lack of information. We will help you figure it out. Here is how you can choose the best language learning platform: 1.Time/2.Quality of the study platform./3.Environment./4.Course content./5.Motivation./6.Level of training.'),
('Article', 'The Benefits of Multilingualism in Personal and Professional Life', 'Exploring the myriad benefits of learning multiple languages, including cognitive advantages, career opportunities, and enhanced social connections.', '2024-07-11', 25, 'The Benefits of Multilingualism in Personal and Professional Life.jpg', 'In the past two decades, new research on multilingualism has changed our understanding of the consequences of learning and using two or more languages for cognition, for the brain, and for success and well-being across the entire lifespan. Far from the stereotype that exposure to multiple languages in infancy complicates language and cognitive development, the new findings suggest that individuals benefit from that exposure, with greater openness to other languages and to new learning itself. At the other end of the lifespan, in old age, the active use of two or more languages appears to provide protection against cognitive decline. That protection is seen in healthy aging and most dramatically in compensating for the symptoms of pathology in those who develop dementia or are recovering from stroke. In this article we briefly review the most exciting of these new research developments and consider their implications.'),
('Article', 'Leveraging Technology in Language Education', 'An overview of how technological tools, from language learning apps to virtual reality environments, are transforming traditional language education.', '2024-07-06', 24, 'Leveraging Technology in Language Education.jpg', 'As technology use has become the norm in education, this bibliometric analysis of technology-enhanced language learning (TELL) aims to reveal its current state-of-the-art and emerging trends. Analysis of 1,816 publications (1,745 articles and 71 reviews) from Web of Science demonstrated growing interests in the field and core publications in the field. Bibliographic coupling identified eight research fronts, with a particular emphasis on the established flipped learning (FL) pedagogy and expanding influence of mobile assisted language learning (MALL) and digital game-based learning (DGBL).
These approaches are at the forefront in shaping English language skill acquisition, especially in writing, with the rise of technology multimodality and informal digital learning as nascent yet significant areas for future research. Anchored in the bioecological model, the research highlights the integral role of student outcomes across various competencies influenced by systemic factors. The study stresses the necessity for education stakeholders to blend technology with pedagogical strategies, a need further accentuated by the COVID-19 pandemic. The studys major contribution lies in its comprehensive synthesis of TELLs current landscape and for both future research and education endeavours in the field of English TELL.'),
('Article', 'Language Learning Success Stories: Inspiring Case Studies', 'Real-life success stories from individuals who mastered new languages, highlighting their methods, challenges, and the impact of their achievements.', '2024-07-03', 24, 'Language Learning Success Stories.jpg', 'Language learning is a profoundly personal journey that charts a course through new sounds, structures, and cultural landscapes. Engaging with Personal Language Learning Experiences offers rich insight into the transformative potential of acquiring a new tongue. In this article, we will delve into a few anecdotes and methodologies that unveil the essence of this intimate endeavor.
The technological era has unfolded a new chapter in Personal Language Learning Experiences. With countless resources at our fingertips, learners can now immerse themselves in authentic linguistic environments without ever leaving their homes. Talkio, for example, is a platform that creatively augments the traditional learning model by simulating conversations with native speakers. This innovative approach embodies the trend of integrating practical communication into everyday study, offering learners the chance to refine their oral language skills in realistic scenarios.
Using such digital tools can turn idle moments into golden opportunities for language practice. Instead of scrolling through social media feeds, language learners can engage in simulated dialogues, effectively using their time to foster real-world speaking competencies. The accessibility of these tools means that consistent practice is more feasible than ever, granting the flexibility to tailor language experiences to individual schedules and needs.'),
('Tutorial', 'Basic Spanish Phrases for Beginners', 'A step-by-step tutorial on essential Spanish phrases for beginners, covering greetings, common questions, and simple responses to help you start conversing immediately.', '2024-07-06', 23, 'Basic Spanish Phrases for Beginners.jpg', 'Buenos días — Good morning
Buenas tardes — Good afternoon
Buenas noches — Good evening / Good night
¿Cómo está usted? — How are you? (formal)
¿Cómo estás? — How are you? (informal)
¿Qué tal? — How are you? (informal) / Whats up?'),
('Tutorial', 'Pronunciation Techniques for French Learners', 'Learn key pronunciation techniques that will help you sound more like a native French speaker, focusing on nasal vowels, liaison, and the French R', '2024-07-05', 25, 'Pronunciation Techniques for French Learners.jpg', 'Practicing is fundamental to getting you sound like a French native. If you would like to read more about French pronunciation, check out our French pronunciation lessons designed to help you learn and improve your French pronunciation. In practice, to improve your French pronunciation:
Get curious about pronunciation tips
Learn the French IPA: the international phonetic alphabet
Master silent letters in French
Practice the pronunciation of difficult words
Take the time every day to learn and repeat
Follow the rhythm and intonation of the French language
Understand liaisons and enchainement in French 
Apprehend the mechanism of assimilation in French'),
('Tutorial', 'Writing Japanese Characters: A Beginners Guide', 'This tutorial walks you through the basics of writing Hiragana and Katakana, the two phonetic scripts used in Japanese, with tips for proper stroke order and practice techniques.', '2024-07-27', 25, 'Writing Japanese Characters.jpg', 'The Japanese writing system consists of two types of characters: the syllabic kana – hiragana (平仮名) and katakana (片仮名) – and kanji (漢字), the adopted Chinese characters. Each have different usages, purposes and characteristics and all are necessary in Japanese writing.
Most Japanese sentences will have combinations of hiragana and kanji and occasionally, katakana. Hiragana and katakana are unique to the Japanese language and we highly recommend students master these two systems first before beginning their Japanese language studies in Japan.
Because of the three distinct characters and the varying usage, the Japanese written language is described as one of the most difficult languages to master. Read on to find out all about Japanese characters: hiragana, katakana and kanji.
You can write Japanese characters in two ways. Firstly, they can be in columns going from top to bottom, right to left (like in Chinese). Or horizontally from left to right, top to bottom (like in English).  That iss why you will find some books open with the spine of the book to the right, while some open to the left.'),
('Tutorial', 'Mastering German Grammar: The Case System', 'An in-depth look at the German case system, explaining the four cases used in German grammar with examples to clarify usage in sentences.', '2024-07-28', 23, 'Mastering German Grammar.jpg', 'Immerse Yourself in German Content: Surround yourself with German language materials that interest you, such as books, movies, TV shows, and podcasts. Choose content that is slightly above your current level to challenge yourself while still being comprehensible.
Focus on Meaningful Input: Instead of memorizing grammar rules, focus on understanding the meaning of what you are reading or listening to. Pay attention to how sentences are structured and how words are used in context.
Practice Active Listening: Actively listen to German audio materials, such as podcasts or audiobooks, and try to understand the main ideas and key vocabulary. Do not worry about understanding every word; focus on grasping the overall message.
Engage in Conversations: Practice speaking German with native speakers or language exchange partners. Engaging in conversations allows you to apply grammar rules in real-life situations and receive feedback on your language usage.
Use Contextual Learning: Learn grammar in context by paying attention to how sentences are formed in the materials you are consuming. Notice patterns and recurring structures, and try to mimic them in your own speech and writing.
Be Patient and Persistent: Language learning takes time, so be patient with yourself and celebrate small victories along the way. Stay consistent with your learning routine and trust in the natural process of language acquisition.');

INSERT INTO  `Video`
(`section_id`, `video_url`)
VALUES
(1,'English'),
(2,'English'),
(3,'English'),
(4,'English'),
(5,'English'),
(6,'English'),
(7,'English'),
(8,'English'),
(9,'Chinese'),
(10,'Chinese'),
(11,'Chinese'),
(12,'Chinese'),
(13,'Chinese'),
(14,'Chinese'),
(15,'Chinese'),
(16,'Chinese'),
(17,'Chinese'),
(18,'Chinese'),
(19,'Chinese'),
(20,'Chinese'),
(21,'Korean'),
(22,'Korean'),
(23,'Korean'),
(24,'Korean'),
(25,'Korean'),
(26,'Korean'),
(27,'Korean'),
(28,'Korean'),
(29,'Korean'),
(30,'Korean'),
(31,'Korean'),
(32,'Korean'),
(33,'Japanese'),
(34,'Japanese'),
(35,'Japanese'),
(36,'Japanese'),
(37,'Japanese'),
(38,'Japanese'),
(39,'Japanese'),
(40,'Japanese'),
(41,'Japanese'),
(42,'Japanese'),
(43,'Japanese'),
(44,'Japanese'),
(45,'French'),
(46,'French'),
(47,'French'),
(48,'French'),
(49,'French'),
(50,'French'),
(51,'French'),
(52,'French'),
(53,'German'),
(54,'German'),
(55,'German'),
(56,'German'),
(57,'German'),
(58,'German'),
(59,'German'),
(60,'German'),
(61,'Spanish'),
(62,'Spanish'),
(63,'Spanish'),
(64,'Spanish'),
(65,'Spanish'),
(66,'Spanish'),
(67,'Spanish'),
(68,'Spanish'),
(69,'English'),
(70,'English'),
(71,'English'),
(72,'English'),
(73,'English'),
(74,'English'),
(75,'English'),
(76,'English'),
(77,'English'),
(78,'English'),
(79,'English'),
(80,'English'),
(81,'Chinese'),
(82,'Chinese'),
(83,'Chinese'),
(84,'Chinese'),
(85,'Chinese'),
(86,'Chinese'),
(87,'Chinese'),
(88,'Chinese'),
(89,'Chinese'),
(90,'Chinese'),
(91,'Chinese'),
(92,'Chinese'),
(93,'Korean'),
(94,'Korean'),
(95,'Korean'),
(96,'Korean'),
(97,'Korean'),
(98,'Korean'),
(99,'Korean'),
(100,'Korean'),
(101,'Korean'),
(102,'Korean'),
(103,'Korean'),
(104,'Korean'),
(105,'Japanese'),
(106,'Japanese'),
(107,'Japanese'),
(108,'Japanese'),
(109,'Japanese'),
(110,'Japanese'),
(111,'Japanese'),
(112,'Japanese'),
(113,'Japanese'),
(114,'Japanese'),
(115,'Japanese'),
(116,'Japanese');