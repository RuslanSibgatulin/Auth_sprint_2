-- There are for general rights
-- 1. create
-- 2. read
-- 3. update
-- 4. delete

-- TODO pass as env parmeters
INSERT INTO "user" (id, login, password_hash, email) VALUES ('908e33da-6f57-40a5-a8cf-5722dbeed1dc'::uuid, 'root', '0430bf47e87e4ee9b4bf0e0c0b63db44835693fdd54eeb62c9c376c407cdc9a3', 'root@mail.ru');  -- password: root

INSERT INTO user_role (user_id, role_id) VALUES ('908e33da-6f57-40a5-a8cf-5722dbeed1dc'::uuid, 5);
