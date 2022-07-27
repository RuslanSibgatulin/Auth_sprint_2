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
INSERT INTO role_action (role_id, action_id) VALUES (1, 14);

-- Premium User
INSERT INTO role_action (role_id, action_id) VALUES (2, 11);
INSERT INTO role_action (role_id, action_id) VALUES (2, 12);
INSERT INTO role_action (role_id, action_id) VALUES (2, 14);
INSERT INTO role_action (role_id, action_id) VALUES (2, 15);

-- Moderator
INSERT INTO role_action (role_id, action_id) 
SELECT 3, i FROM generate_series(5, 6) AS i;
INSERT INTO role_action (role_id, action_id) 
SELECT 3, i FROM generate_series(11, 15) AS i;

-- Admin
INSERT INTO role_action (role_id, action_id) 
SELECT 4, i FROM generate_series(5, 15) AS i;

--Superuser
INSERT INTO role_action (role_id, action_id) 
SELECT 5, i FROM generate_series(1, 15) AS i;

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
    user_id      UUID REFERENCES "user" (id),
    platform     VARCHAR(100),
    ip           VARCHAR(100),
    login_at     TIMESTAMP NOT NULL DEFAULT NOW()
) PARTITION BY HASH (user_id);

-- Create partitions for table login_history
CREATE TABLE IF NOT EXISTS login_history_hash1 PARTITION OF login_history
(
    CONSTRAINT pk_login_history1 PRIMARY KEY(user_id, login_at)
) FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE IF NOT EXISTS login_history_hash2 PARTITION OF login_history
(
    CONSTRAINT pk_login_history2 PRIMARY KEY(user_id, login_at)
) FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE IF NOT EXISTS login_history_hash3 PARTITION OF login_history
(
    CONSTRAINT pk_login_history3 PRIMARY KEY(user_id, login_at)
) FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE IF NOT EXISTS login_history_hash4 PARTITION OF login_history
(
    CONSTRAINT pk_login_history4 PRIMARY KEY(user_id, login_at)
) FOR VALUES WITH (MODULUS 4, REMAINDER 3);

CREATE TABLE IF NOT EXISTS social_account
(
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id       UUID NOT NULL,
    social_id     TEXT NOT NULL,
    social_name   TEXT NOT NULL,
    CONSTRAINT social_pk UNIQUE (social_id, social_name)
);
