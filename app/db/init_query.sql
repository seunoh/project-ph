CREATE TABLE IF NOT EXISTS users
(
    id              INT NOT NULL AUTO_INCREMENT,
    email           VARCHAR(255),
    hashed_password VARCHAR(255),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE = innodb
  CHARSET = utf8;


CREATE TABLE IF NOT EXISTS account_books
(
    id          INT       NOT NULL AUTO_INCREMENT,
    amount      FLOAT              DEFAULT 0.0,
    description TEXT,
    date        DATE,
    user_id     INT,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
) ENGINE = InnoDB
  CHARSET = utf8;


CREATE TABLE IF NOT EXISTS tokens
(
    id            INT       NOT NULL AUTO_INCREMENT,
    token         TEXT,
    refresh_token TEXT,
    user_id       INT,
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
) ENGINE = InnoDB
  CHARSET = utf8;


CREATE TABLE IF NOT EXISTS short_urls
(
    id           INT       NOT NULL AUTO_INCREMENT,
    original_url TEXT,
    short_url    TEXT,
    expire       DATE,
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) ENGINE = InnoDB
  CHARSET = utf8;


