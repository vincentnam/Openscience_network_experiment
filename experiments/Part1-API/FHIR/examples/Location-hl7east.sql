CREATE DATABASE FHIR;
USE FHIR;

CREATE TABLE IF NOT EXISTS Location_hl7east (
    `resourceType` VARCHAR(8) CHARACTER SET utf8,
    `id` VARCHAR(7) CHARACTER SET utf8,
    `meta_extension_url` VARCHAR(60) CHARACTER SET utf8,
    `meta_extension_valueString` VARCHAR(15) CHARACTER SET utf8,
    `meta_extension_valueMarkdown` VARCHAR(61) CHARACTER SET utf8,
    `meta_profile` VARCHAR(64) CHARACTER SET utf8,
    `text_status` INT,
    `text_div` INT,
    `identifier_system` VARCHAR(28) CHARACTER SET utf8,
    `identifier_value` INT,
    `status` VARCHAR(6) CHARACTER SET utf8,
    `name` VARCHAR(42) CHARACTER SET utf8,
    `description` VARCHAR(23) CHARACTER SET utf8,
    `telecom_system` VARCHAR(5) CHARACTER SET utf8,
    `telecom_value` VARCHAR(17) CHARACTER SET utf8,
    `address_line` VARCHAR(32) CHARACTER SET utf8,
    `address_city` VARCHAR(7) CHARACTER SET utf8,
    `address_state` VARCHAR(2) CHARACTER SET utf8,
    `address_postalCode` INT,
    `address_country` VARCHAR(3) CHARACTER SET utf8,
    `position_longitude` NUMERIC(8, 6),
    `position_latitude` NUMERIC(8, 6),
    `managingOrganization_display` VARCHAR(32) CHARACTER SET utf8
);
INSERT INTO Location_hl7east VALUES ('Location','hl7east','http://hl7.org/fhir/StructureDefinition/instance-name','HL7East Example',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
	('Location','hl7east','http://hl7.org/fhir/StructureDefinition/instance-description','HL7East Example','This is a HL7East example for the *US Core Location Profile*.',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
	('Location','hl7east',NULL,NULL,NULL,'http://hl7.org/fhir/us/core/StructureDefinition/us-core-location',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
	('Location','hl7east',NULL,NULL,NULL,NULL,NULL,NULL,'http://www.acme.org/location',29,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
	('Location','hl7east',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'active','Health Level Seven International - Amherst','HL7 Headquarters - East','phone','(+1) 734-677-7777',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),
	('Location','hl7east',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'active','Health Level Seven International - Amherst','HL7 Headquarters - East',NULL,NULL,'3300 Washtenaw Avenue, Suite 227',NULL,NULL,NULL,NULL,NULL,NULL,NULL),
	('Location','hl7east',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'active','Health Level Seven International - Amherst','HL7 Headquarters - East',NULL,NULL,NULL,'Amherst','MA',01002,'USA',NULL,NULL,NULL),
	('Location','hl7east',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'active','Health Level Seven International - Amherst','HL7 Headquarters - East',NULL,NULL,NULL,NULL,NULL,NULL,NULL,-72.519854,42.373222,NULL),
	('Location','hl7east',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'active','Health Level Seven International - Amherst','HL7 Headquarters - East',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Health Level Seven International');
