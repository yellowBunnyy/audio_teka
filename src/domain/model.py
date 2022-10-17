class Title:
    def __init__(self, title):
        self.title = title

    def __eq__(self, other):
        if not isinstance(other, Title):
            return False
        return self.title == other.title
