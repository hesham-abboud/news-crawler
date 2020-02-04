import hashlib


class Article:
    id = 0
    hashed_id = ""
    title = ""
    author = ""
    content = ""
    date = ""
    time = ""
    url = ""
    source = ""
    tags = []

    def generate_id(self):
        str = self.title + self.author + self.date + self.time + self.source
        self.hashed_id = hashlib.md5(str.encode()).hexdigest()
