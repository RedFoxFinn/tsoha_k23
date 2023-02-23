CREATE TABLE Users (
  id SERIAL PRIMARY KEY,
  uname TEXT NOT NULL UNIQUE,
  pw_hash TEXT NOT NULL
);
CREATE TABLE Admins (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES Users (id),
  superuser BOOLEAN DEFAULT FALSE
);
CREATE TABLE Groups (
  id SERIAL PRIMARY KEY,
  gname TEXT NOT NULL UNIQUE,
  restriction TEXT NOT NULL
);
CREATE TABLE Topics (
  id SERIAL PRIMARY KEY,
  topic TEXT NOT NULL UNIQUE
);
CREATE TABLE Chats (
  id SERIAL PRIMARY KEY,
  cname TEXT NOT NULL,
  topic_id INTEGER REFERENCES Topics (id),
  group_id INTEGER REFERENCES Groups (id),
  link TEXT NOT NULL,
  moderator_ids INTEGER[]
);
CREATE TABLE Moderators (
  id SERIAL PRIMARY KEY,
  handle TEXT NOT NULL UNIQUE,
  chat_link TEXT NOT NULL
);
CREATE TABLE Requests (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES Users (id),
  info_table TEXT NOT NULL,
  info_id INTEGER NOT NULL,
  change_type TEXT NOT NULL,
  change_info TEXT[],
  datetime_of_request INTEGER
);