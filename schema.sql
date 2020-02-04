CREATE TABLE news (
    `id` INT NOT NULL AUTO_INCREMENT,
    `hashed_id` varchar(32) NOT NULL,
    `title` TEXT NOT NULL,
    `author` TEXT NOT NULL,
    `content` TEXT NOT NULL,
    `date` varchar(50) NOT NULL,
    `time` varchar(50) NOT NULL,
    `url` TEXT NOT NULL,
    `source` varchar(50) NOT NULL,
    `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY (`hashed_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE news ADD FULLTEXT (title, content, author);

CREATE TABLE tags (
    `id` INT NOT NULL AUTO_INCREMENT,
    `tag` varchar(50) NOT NULL,
    `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY (`tag`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE news_tags (
    `id` INT NOT NULL AUTO_INCREMENT,
    `news_id` INT NOT NULL,
    `tag_id` INT NOT NULL,
    `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (`news_id`) REFERENCES news(`id`),
    FOREIGN KEY (`tag_id`) REFERENCES tags(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;