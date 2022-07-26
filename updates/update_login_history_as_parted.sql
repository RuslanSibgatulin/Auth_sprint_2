-- Rename existing table
ALTER TABLE IF EXISTS login_history RENAME TO login_history_backup;

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

-- Move data from unparted table
INSERT INTO login_history (user_id, platform, ip, login_at)
SELECT user_id, platform, ip, login_at
from login_history_backup ON CONFLICT DO NOTHING;

-- Drop backup table
DROP TABLE login_history_backup;