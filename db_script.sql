DROP TABLE IF EXISTS Events;

CREATE TABLE Events (
    name TEXT NOT NULL,
    organization TEXT NOT NULL,
    eventDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    eventDescription TEXT NOT NULL
);