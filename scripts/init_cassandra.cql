CREATE KEYSPACE IF NOT EXISTS pa195 WITH REPLICATION = { 
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
};

USE pa195;

CREATE TABLE IF NOT EXISTS charts (
    title TEXT,
    rank INT,
    date DATE,
    artist TEXT,
    url TEXT,
    region TEXT,
    chart TEXT,
    trend TEXT,
    streams INT,
    PRIMARY KEY ((region), date, title, artist)
);