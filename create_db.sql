CREATE SEQUENCE grid_id_seq START 1;

CREATE TABLE IF NOT EXISTS grid (
    id INT PRIMARY KEY NOT NULL DEFAULT nextval('grid_id_seq'),
    size INT NOT NULL,
    grid_values VARCHAR NOT NULL,
    scores JSONB);


