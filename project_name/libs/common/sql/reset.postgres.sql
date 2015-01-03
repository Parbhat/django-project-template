DROP DATABASE IF EXISTS {{ project_name }};
CREATE DATABASE {{ project_name }}
    ENCODING 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8';
DROP USER IF EXISTS {{ project_name }};
CREATE USER {{ project_name }} WITH PASSWORD '';
GRANT ALL PRIVILEGES ON DATABASE {{ project_name }} to {{ project_name }};
