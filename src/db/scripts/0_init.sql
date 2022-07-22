CREATE DATABASE auth;
\c auth

CREATE TABLE IF NOT EXISTS role
(
    id          SERIAL PRIMARY KEY,
    name        TEXT      NOT NULL,
    description TEXT,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);
INSERT INTO role (name, description) VALUES ('user', 'Registered user.');
INSERT INTO role (name, description) VALUES ('premium_user', 'Registered user with a paid subscription.');
INSERT INTO role (name, description) VALUES ('moderator', 'Moderator.');
INSERT INTO role (name, description) VALUES ('admin', 'Admin.');
INSERT INTO role (name, description) VALUES ('superuser', 'Superuser.');


CREATE TABLE IF NOT EXISTS action
(
    id          SERIAL PRIMARY KEY,
    name        TEXT      NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);
INSERT INTO action (name) VALUES ('role_create');
INSERT INTO action (name) VALUES ('role_read');
INSERT INTO action (name) VALUES ('role_update');
INSERT INTO action (name) VALUES ('role_delete');
INSERT INTO action (name) VALUES ('role_assignment_create');
INSERT INTO action (name) VALUES ('role_assignment_delete');
INSERT INTO action (name) VALUES ('action_create');
INSERT INTO action (name) VALUES ('action_read');
INSERT INTO action (name) VALUES ('action_update');
INSERT INTO action (name) VALUES ('action_delete');
-- service actions
INSERT INTO action (name) VALUES ('write_comment');
INSERT INTO action (name) VALUES ('delete_own_comment');
INSERT INTO action (name) VALUES ('delete_any_comment');
INSERT INTO action (name) VALUES ('watch_trailer');
INSERT INTO action (name) VALUES ('watch_movie');

CREATE TABLE IF NOT EXISTS role_action
(
    role_id     INTEGER,
    action_id   INTEGER,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (role_id, action_id)
);
-- User
INSERT INTO role_action (role_id, action_id) VALUES (1, 11);
INSERT INTO role_action (role_id, action_id) VALUES (1, 12);
INSERT INTO role_action (role_id, action_id) VALUES (1, 13);
-- Premium User
INSERT INTO role_action (role_id, action_id) VALUES (2, 11);
INSERT INTO role_action (role_id, action_id) VALUES (2, 12);
INSERT INTO role_action (role_id, action_id) VALUES (2, 14);
INSERT INTO role_action (role_id, action_id) VALUES (2, 15);
-- Moderator
INSERT INTO role_action (role_id, action_id) VALUES (3, 5);
INSERT INTO role_action (role_id, action_id) VALUES (3, 6);
INSERT INTO role_action (role_id, action_id) VALUES (3, 11);
INSERT INTO role_action (role_id, action_id) VALUES (3, 12);
INSERT INTO role_action (role_id, action_id) VALUES (3, 13);
INSERT INTO role_action (role_id, action_id) VALUES (3, 14);
INSERT INTO role_action (role_id, action_id) VALUES (3, 15);
-- Admin
INSERT INTO role_action (role_id, action_id) VALUES (4, 5);
INSERT INTO role_action (role_id, action_id) VALUES (4, 6);
INSERT INTO role_action (role_id, action_id) VALUES (4, 7);
INSERT INTO role_action (role_id, action_id) VALUES (4, 8);
INSERT INTO role_action (role_id, action_id) VALUES (4, 9);
INSERT INTO role_action (role_id, action_id) VALUES (4, 10);
INSERT INTO role_action (role_id, action_id) VALUES (4, 11);
INSERT INTO role_action (role_id, action_id) VALUES (4, 12);
INSERT INTO role_action (role_id, action_id) VALUES (4, 13);
INSERT INTO role_action (role_id, action_id) VALUES (4, 14);
INSERT INTO role_action (role_id, action_id) VALUES (4, 15);

--Superuser
INSERT INTO role_action (role_id, action_id) VALUES (5, 1);
INSERT INTO role_action (role_id, action_id) VALUES (5, 2);
INSERT INTO role_action (role_id, action_id) VALUES (5, 3);
INSERT INTO role_action (role_id, action_id) VALUES (5, 4);
INSERT INTO role_action (role_id, action_id) VALUES (5, 5);
INSERT INTO role_action (role_id, action_id) VALUES (5, 6);
INSERT INTO role_action (role_id, action_id) VALUES (5, 7);
INSERT INTO role_action (role_id, action_id) VALUES (5, 8);
INSERT INTO role_action (role_id, action_id) VALUES (5, 9);
INSERT INTO role_action (role_id, action_id) VALUES (5, 10);
INSERT INTO role_action (role_id, action_id) VALUES (5, 11);
INSERT INTO role_action (role_id, action_id) VALUES (5, 12);
INSERT INTO role_action (role_id, action_id) VALUES (5, 13);
INSERT INTO role_action (role_id, action_id) VALUES (5, 14);
INSERT INTO role_action (role_id, action_id) VALUES (5, 15);

CREATE TABLE IF NOT EXISTS "user"
(
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    login         TEXT      NOT NULL UNIQUE,
    password_hash TEXT      NOT NULL,
    email         TEXT      NOT NULL UNIQUE,
    is_active     BOOLEAN   NOT NULL DEFAULT True,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS user_role
(
    user_id       UUID,
    role_id       INTEGER,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS login_history
(
    id           SERIAL PRIMARY KEY,
    user_id      UUID,
    platform     VARCHAR(100),
    ip           VARCHAR(100),
    login_at     TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS social_account
(
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       UUID NOT NULL,
    social_id     TEXT NOT NULL,
    social_name   TEXT NOT NULL,
    CONSTRAINT social_pk UNIQUE (social_id, social_name)
);
