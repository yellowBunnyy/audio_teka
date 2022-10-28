from dataclasses import dataclass

class Event():
    pass

@dataclass
class AddBookTitle(Event):
    title: str

@dataclass
class GetBookTitle(Event):
    title: str


@dataclass
class DeleteSingleRow(Event):
    title: str

@dataclass
class DeleteAllRows(Event):
    pass

@dataclass
class SaveAllTitlesInDB(Event):
    pass

@dataclass
class NextFakeEvent(Event):
    message: str