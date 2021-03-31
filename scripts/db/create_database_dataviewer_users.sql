SELECT 'CREATE DATABASE dataviewer_users'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'dataviewer_users')\gexec
	
\c dataviewer_users;

CREATE TABLE IF NOT EXISTS users_api (
	"username" VARCHAR(40) NOT NULL,
	"password_hash" VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS users_students (
	"username" VARCHAR(40) NOT NULL,
	"password_hash" VARCHAR(150) NOT NULL,
	"user" VARCHAR(70) NULL,
	"name" VARCHAR(100) NOT NULL,
	"registration" VARCHAR (30) NOT NULL,
	"email" VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS users_teachers (
	"username" VARCHAR(40) NOT NULL,
	"password_hash" VARCHAR(150) NOT NULL,
	"name_teacher" VARCHAR(100) NOT NULL,
	"id_teacher" VARCHAR(36) NOT NULL, 
	"email" VARCHAR(100) NOT NULL
);