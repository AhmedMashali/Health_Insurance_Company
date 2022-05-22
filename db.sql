CREATE SCHEMA IF NOT EXISTS `company` DEFAULT CHARACTER SET utf8 ;

CREATE TABLE IF NOT EXISTS `company`.`customers` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `national_id` VARCHAR(15) NULL,
  `f_name` VARCHAR(45) NULL,
  `l_name` VARCHAR(45) NULL,
  `phone_number` VARCHAR(13) NULL,
  `age` INT NULL,
  `city` VARCHAR(45) NULL,
  `street` VARCHAR(45) NULL,
  `gender` VARCHAR(45) NULL,
  PRIMARY KEY (`customer_id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `company`.`dependents` (
  `dependent_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(60) NULL,
  `gender` VARCHAR(45) NULL,
  `relation` VARCHAR(45) NULL,
  `customer_id` INT NOT NULL,
  PRIMARY KEY (`dependent_id`, `customer_id`),
  INDEX `fk_dependents_customers_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_dependents_customers`
    FOREIGN KEY (`customer_id`)
    REFERENCES `company`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `company`.`plan_type` (
  `type` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `cost` INT NULL,
  PRIMARY KEY (`type`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `company`.`plans` (
  `plan_id` INT NOT NULL AUTO_INCREMENT,
  `beneficiary` VARCHAR(45) NULL,
  `customer_id` INT NOT NULL,
  `plan_type` INT NOT NULL,
  PRIMARY KEY (`plan_id`),
  INDEX `fk_plans_customers1_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_plans_plan_type1_idx` (`plan_type` ASC) VISIBLE,
  CONSTRAINT `fk_plans_customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `company`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_plans_plan_type1`
    FOREIGN KEY (`plan_type`)
    REFERENCES `company`.`plan_type` (`type`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `company`.`claims` (
  `claim_id` INT NOT NULL AUTO_INCREMENT,
  `expense_amount` VARCHAR(45) NULL,
  `expense_details` VARCHAR(70) NULL,
  `resolved` TINYINT NULL,
  `beneficiry` VARCHAR(45) NULL,
  `hospital` VARCHAR(45) NULL,
  `customer_id` INT NOT NULL,
  `plan_id` INT NOT NULL,
  PRIMARY KEY (`claim_id`),
  INDEX `fk_claims_customers1_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_claims_plans1_idx` (`plan_id` ASC) VISIBLE,
  CONSTRAINT `fk_claims_customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `company`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_claims_plans1`
    FOREIGN KEY (`plan_id`)
    REFERENCES `company`.`plans` (`plan_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `company`.`hospitals` (
  `hospital_id` INT NOT NULL AUTO_INCREMENT,
  `hospital_name` VARCHAR(60) NULL,
  `city` VARCHAR(45) NULL,
  `street` VARCHAR(45) NULL,
  PRIMARY KEY (`hospital_id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `company`.`covers` (
  `p_t` INT NOT NULL,
  `h_id` INT NOT NULL,
  PRIMARY KEY (`p_t`, `h_id`),
  INDEX `fk_plan_type_has_hospitals_hospitals1_idx` (`h_id` ASC) VISIBLE,
  INDEX `fk_plan_type_has_hospitals_plan_type1_idx` (`p_t` ASC) VISIBLE,
  CONSTRAINT `fk_plan_type_has_hospitals_plan_type1`
    FOREIGN KEY (`p_t`)
    REFERENCES `company`.`plan_type` (`type`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_plan_type_has_hospitals_hospitals1`
    FOREIGN KEY (`h_id`)
    REFERENCES `company`.`hospitals` (`hospital_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

use company;
insert into plan_type values (1, "Basic", 3000);
insert into plan_type values (2, "Premium", 5000);
insert into plan_type values (3, "Golden", 10000);