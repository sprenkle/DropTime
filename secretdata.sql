INSERT INTO users (userid, first, last, username, userpassword)VALUES
('','','','','');

INSERT INTO tags (tagid, userid, name, description) VALUES
('','','','');

INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('','','');

INSERT INTO activities (userid, name, color, show, integration, dailygoals, dailytimeSec) VALUES
('','','','','','','');

Insert INTO reminders (userid, start='',stop='', showled= , sunday=, monday= , tuesday=,
                      wednesday=, thursday=, friday=, saturday=, integration=,
                      ledpattern='[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]');

INSERT INTO devices (name, description) VALUES ('','','');

INSERT INTO devices (deviceid, name, description) VALUES ('08f98cd6-3602-41ee-aa27-a6768412254e','white tower', 'First attempt white tower');

DELETE FROM users;
INSERT INTO users (userid, first, last, username, userpassword)VALUES
('72be6ab4-727b-4257-ba1d-ef58a3349bfc','David','Sprenkle','NDcwMDBfYTgyNzU2MDE3Y2E4NDBlNmI4ZWViOTMwMGI1MTZhYzI=','YmZmNTFhNmRmYzUxNDVhMGE2MDdlNjkzMjJlMTZiYzE=');

INSERT INTO users (userid, first, last, username, userpassword)VALUES
('5ac96611-98b2-4711-b703-f6f3a16e7a53','Lakeida','Sprenkle','NDY5ODFfNTFlNDA3NTRlZGFmNGNmMGE2NjgyZTRmNGVlMmM5ZmU=','ZWNjZTdjMmVjZWI3NGYxMzlmY2UxODVmNTZiYzFlZmU=');





DELETE FROM tags;
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110893782','72be6ab4-727b-4257-ba1d-ef58a3349bfc','greydice1','testing');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110835958','72be6ab4-727b-4257-ba1d-ef58a3349bfc','greydice2','testing');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110893686','72be6ab4-727b-4257-ba1d-ef58a3349bfc','greydice3','testing');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110945990','72be6ab4-727b-4257-ba1d-ef58a3349bfc','greydice4','testing');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110945814','72be6ab4-727b-4257-ba1d-ef58a3349bfc','greydice5','testing');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110835862','72be6ab4-727b-4257-ba1d-ef58a3349bfc','lsgreydice6','testing');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110893430','72be6ab4-727b-4257-ba1d-ef58a3349bfc','Black Knight','testing');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1111043878','72be6ab4-727b-4257-ba1d-ef58a3349bfc','David from Aliens','testing');
-- Lakeida tags
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110641398','5ac96611-98b2-4711-b703-f6f3a16e7a53','Writing','');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110708406','5ac96611-98b2-4711-b703-f6f3a16e7a53','Reading','');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110708598','5ac96611-98b2-4711-b703-f6f3a16e7a53','Photos','');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110708502','5ac96611-98b2-4711-b703-f6f3a16e7a53','D365 CCC','');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110835526','5ac96611-98b2-4711-b703-f6f3a16e7a53','D365 CTAP','');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110833798','5ac96611-98b2-4711-b703-f6f3a16e7a53','D365 SD','');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110835718','5ac96611-98b2-4711-b703-f6f3a16e7a53','Games','');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110833894','5ac96611-98b2-4711-b703-f6f3a16e7a53','DIY','');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110835622','5ac96611-98b2-4711-b703-f6f3a16e7a53','Admin','');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110833990','5ac96611-98b2-4711-b703-f6f3a16e7a53','R&D','');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110895622','5ac96611-98b2-4711-b703-f6f3a16e7a53','Training','');
INSERT INTO tags (tagid, userid, name, description) VALUES
('1110772870','5ac96611-98b2-4711-b703-f6f3a16e7a53','BI','');


DELETE FROM tagstoactions;
-- Added test actions to test die
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110893782','1','379734');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110835958','1','379735');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110893686','1','379736');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110945990','1','379737');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110945814','1','379740');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110835862','1','379741');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110893430','1','369008');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1111043878','1','369007');
-- Lakeida
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110835718','1','377661');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110833894','1','377662');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110835526','1','377654');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110708598','1','369399');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110835622','1','368519');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110708502','1','377655');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110708406','1','377660');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110895622','1','369396');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110833990','1','367720');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110641398','1','369400');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110772870','1','368743');
INSERT INTO tagstoactions (tagid, actiontype, identifier) VALUES
('1110833798','1','377657');

DELETE FROM activities;
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec)
VALUES
('369007','72be6ab4-727b-4257-ba1d-ef58a3349bfc',
'DropTime','',1,1,30);
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec)
VALUES
('379734','72be6ab4-727b-4257-ba1d-ef58a3349bfc',
'test1','',1,1,120);
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec)
VALUES
('379735','72be6ab4-727b-4257-ba1d-ef58a3349bfc',
'test2','','1','2','60');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec)
VALUES
('379736','72be6ab4-727b-4257-ba1d-ef58a3349bfc',
'test3','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec)
VALUES
('379737','72be6ab4-727b-4257-ba1d-ef58a3349bfc',
'test4','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec)
VALUES
('379740','72be6ab4-727b-4257-ba1d-ef58a3349bfc',
'test5','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec)
VALUES
('379741','72be6ab4-727b-4257-ba1d-ef58a3349bfc',
'test6','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec)
VALUES
('369008','72be6ab4-727b-4257-ba1d-ef58a3349bfc',
'Wondermachine','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec) VALUES
('377661', '5ac96611-98b2-4711-b703-f6f3a16e7a53','something','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec) VALUES
('377662', '5ac96611-98b2-4711-b703-f6f3a16e7a53','something','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec) VALUES
('377654', '5ac96611-98b2-4711-b703-f6f3a16e7a53','something','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec) VALUES
('369399', '5ac96611-98b2-4711-b703-f6f3a16e7a53','something','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec) VALUES
('368519', '5ac96611-98b2-4711-b703-f6f3a16e7a53','something','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec) VALUES
('377655', '5ac96611-98b2-4711-b703-f6f3a16e7a53','something','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec) VALUES
('377660', '5ac96611-98b2-4711-b703-f6f3a16e7a53','something','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec) VALUES
('369396', '5ac96611-98b2-4711-b703-f6f3a16e7a53','something','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec) VALUES
('367720', '5ac96611-98b2-4711-b703-f6f3a16e7a53','something','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec) VALUES
('369400', '5ac96611-98b2-4711-b703-f6f3a16e7a53','something','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec) VALUES
('368743', '5ac96611-98b2-4711-b703-f6f3a16e7a53','something','','','','');
INSERT INTO activities (activityid, userid, name, color, show, dailygoals, dailytimeSec) VALUES
('377657', '5ac96611-98b2-4711-b703-f6f3a16e7a53','something','','','','');

Insert INTO reminders (reminderid, userid, start, stop, showled , sunday, monday, tuesday,
                      wednesday, thursday, friday, saturday, integration,
                      ledpattern='[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]');





377263c0-57ae-4c7a-82e8-3c6b2a60a077
40a5cd95-592b-4aa7-b875-07010e97e6d7
9412e34d-68ff-48c1-be65-fd3df3256a24
