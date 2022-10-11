--CREATE DATABASE debato default CHARACTER SET UTF8;
use debato;
CREATE TABLE usertbl(
    userid VARCHAR(300) PRIMARY KEY NOT NULL,
    userpw VARCHAR(300) NOT NULL,
    useremail VARCHAR(300),
    username VARCHAR(300) NOT NULL,
    ua VARCHAR(300) NOT NULL,
    ip VARCHAR(300) NOT NULL,
    userdate DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=INNODB;
CREATE TABLE posttbl(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    boardname VARCHAR(300) NOT NULL,
    userid VARCHAR(300) NOT NULL,
    username VARCHAR(300),
    title VARCHAR(300) NOT NULL,
    content VARCHAR(300) NOT NULL,
    likecount INT NOT NULL,
    ua VARCHAR(300) NOT NULL,
    ip VARCHAR(300) NOT NULL,
    posttime DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=INNODB;
CREATE TABLE commenttbl(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    postid VARCHAR(300) NOT NULL,
    userid VARCHAR(300) NOT NULL,
    username VARCHAR(300),
    content VARCHAR(300) NOT NULL,
    ua VARCHAR(300) NOT NULL,
    ip VARCHAR(300) NOT NULL,
    commenttime DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=INNODB;
CREATE TABLE boardtbl(
    id VARCHAR(300) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    board VARCHAR(300) NOT NULL,
) ENGINE=INNODB;
CREATE TABLE siteinfo(
    sitename VARCHAR(300) PRIMARY KEY NOT NULL,
    footer VARCHAR(300),
    adminid VARCHAR(300) NOT NULL,
    adminpw VARCHAR(300) NOT NULL,
) ENGINE=INNODB;
INSERT INTO siteinfo(sitename, footer, adminid, adminpw) VALUE(1,1,1,1);
INSERT INTO posttbl(boardname, userid, username, title, content, likecount, ip, ua) VALUE("free", "dd", "dd", "게시물테스트", "테스트입니다.", "12", "1.1.1.1", "1");
INSERT INTO posttbl(boardname, userid, username, title, content, likecount, ip, ua) VALUE("free", "dd", "dd", "게시물테스트", "테스트입니다.", "12", "1.1.1.1", "1");
INSERT INTO posttbl(boardname, userid, username, title, content, likecount, ip, ua) VALUE("free", "dd", "dd", "게시물테스트", "테스트입니다.", "12", "1.1.1.1", "1");
INSERT INTO posttbl(boardname, userid, username, title, content, likecount, ip, ua) VALUE("free", "dd", "dd", "게시물테스트", "테스트입니다.", "12", "1.1.1.1", "1");
INSERT INTO posttbl(boardname, userid, username, title, content, likecount, ip, ua) VALUE("free", "dd", "dd", "게시물테스트", "테스트입니다.", "12", "1.1.1.1", "1");
INSERT INTO posttbl(boardname, userid, username, title, content, likecount, ip, ua) VALUE("free", "dd", "dd", "게시물테스트", "테스트입니다.", "12", "1.1.1.1", "1");
INSERT INTO posttbl(boardname, userid, username, title, content, likecount, ip, ua) VALUE("free", "dd", "dd", "게시물테스트", "테스트입니다.", "12", "1.1.1.1", "1");
INSERT INTO posttbl(boardname, userid, username, title, content, likecount, ip, ua) VALUE("free", "dd", "dd", "게시물테스트", "테스트입니다.", "12", "1.1.1.1", "1");
INSERT INTO posttbl(boardname, userid, username, title, content, likecount, ip, ua) VALUE("free", "dd", "dd", "게시물테스트", "테스트입니다.", "12", "1.1.1.1", "1");
INSERT INTO posttbl(boardname, userid, username, title, content, likecount, ip, ua) VALUE("free", "dd", "dd", "게시물테스트", "테스트입니다.", "12", "1.1.1.1", "1");
INSERT INTO posttbl(boardname, userid, username, title, content, likecount, ip, ua) VALUE("free", "dd", "dd", "게시물테스트", "테스트입니다.", "12", "1.1.1.1", "1");