import os

class File:
    def __init__(self, fullpath, keywords=None):
        self.fullpath = fullpath
        self.keywords = keywords

    @property
    def fullpath(self):
        return self._fullpath

    @fullpath.setter
    def fullpath(self, val):
        self._fullpath = val

    @property
    def filename(self):
        return os.path.split(self.fullpath)[0]

    @property
    def dir(self):
        return os.path.split(self.fullpath)[1]

    def rename(self, new_fullpath):
        os.rename(self.fullpath, new_fullpath)
        self.fullpath = new_fullpath

    def rename_to_keywords(self):
        keywords_line = ""
        cur_root, cur_ext = os.path.splitext(self.fullpath)
        for kw in self.keywords:
            to_add = "__" + kw
            keywords_line = keywords_line + to_add
        new_fullpath = cur_root + keywords_line + cur_ext
        self.rename(new_fullpath)
