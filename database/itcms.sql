-- MySQL Script generated by MySQL Workbench
-- 11/22/15 12:44:29
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema it_cms
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema it_cms
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `it_cms` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `it_cms` ;

-- -----------------------------------------------------
-- Table `it_cms`.`article`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `it_cms`.`article` (
  `idarticle` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `code` VARCHAR(50) NOT NULL COMMENT '',
  `searchable` TINYINT(1) NOT NULL COMMENT '',
  PRIMARY KEY (`idarticle`)  COMMENT '',
  UNIQUE INDEX `code_UNIQUE` (`code` ASC)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_cms`.`content`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `it_cms`.`content` (
  `idcontent` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `idarticle` INT NOT NULL COMMENT '',
  `parent` INT NULL COMMENT '',
  `code` VARCHAR(50) NOT NULL COMMENT '',
  `index` INT NULL COMMENT '',
  PRIMARY KEY (`idcontent`)  COMMENT '',
  INDEX `fk_content_content_idx` (`parent` ASC)  COMMENT '',
  INDEX `fk_content_article1_idx` (`idarticle` ASC)  COMMENT '',
  CONSTRAINT `fk_content_content`
    FOREIGN KEY (`parent`)
    REFERENCES `it_cms`.`content` (`idcontent`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_content_article1`
    FOREIGN KEY (`idarticle`)
    REFERENCES `it_cms`.`article` (`idarticle`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_cms`.`language`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `it_cms`.`language` (
  `idlanguage` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `abbr` VARCHAR(2) NOT NULL COMMENT '',
  `name` VARCHAR(30) NOT NULL COMMENT '',
  PRIMARY KEY (`idlanguage`)  COMMENT '',
  UNIQUE INDEX `abbr_UNIQUE` (`abbr` ASC)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_cms`.`page`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `it_cms`.`page` (
  `idpage` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `code` VARCHAR(50) NOT NULL COMMENT '',
  `url` VARCHAR(255) NOT NULL COMMENT '',
  PRIMARY KEY (`idpage`)  COMMENT '',
  UNIQUE INDEX `code_UNIQUE` (`code` ASC)  COMMENT '',
  UNIQUE INDEX `url_UNIQUE` (`url` ASC)  COMMENT '')
ENGINE = InnoDB
COMMENT = '					';


-- -----------------------------------------------------
-- Table `it_cms`.`located`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `it_cms`.`located` (
  `idlocated` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `idarticle` INT NOT NULL COMMENT '',
  `idpage` INT NOT NULL COMMENT '',
  PRIMARY KEY (`idlocated`)  COMMENT '',
  INDEX `fk_located_article1_idx` (`idarticle` ASC)  COMMENT '',
  INDEX `fk_located_page1_idx` (`idpage` ASC)  COMMENT '',
  CONSTRAINT `fk_located_article1`
    FOREIGN KEY (`idarticle`)
    REFERENCES `it_cms`.`article` (`idarticle`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_located_page1`
    FOREIGN KEY (`idpage`)
    REFERENCES `it_cms`.`page` (`idpage`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_cms`.`description`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `it_cms`.`description` (
  `iddescription` INT NOT NULL AUTO_INCREMENT COMMENT '',
  `idcontent` INT NOT NULL COMMENT '',
  `idlanguage` INT NOT NULL COMMENT '',
  `plaintext` TEXT NOT NULL COMMENT '',
  PRIMARY KEY (`iddescription`)  COMMENT '',
  INDEX `fk_description_content1_idx` (`idcontent` ASC)  COMMENT '',
  INDEX `fk_description_language1_idx` (`idlanguage` ASC)  COMMENT '',
  CONSTRAINT `fk_description_content1`
    FOREIGN KEY (`idcontent`)
    REFERENCES `it_cms`.`content` (`idcontent`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_description_language1`
    FOREIGN KEY (`idlanguage`)
    REFERENCES `it_cms`.`language` (`idlanguage`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;