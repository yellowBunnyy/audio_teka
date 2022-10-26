from src.domain import events
from src.services_layer import handlers, unit_of_work


def handle(event:events.Event, uow: unit_of_work.AbstractUnitOfWork):
    results = []
    queuee = [event]
    while queuee:
        event = queuee.pop(0)
        for handler in HANDLERS[type(event)]:
            results.append(handler(event, uow))
            # queuee.extend(uow.collect_new_events())
    return results

HANDLERS = {
    events.AddBookTitle: [handlers.add_title],
    events.GetBookTitle: [handlers.get_title],
    events.DeleteSingleRow: [handlers.delete_single_row],
    events.DeleteAllRows: [handlers.delete_all_rows],
    events.SaveAllTitlesInDB: [handlers.save_all_titles_to_db]
} # type: Dict[Type[events.Event], List[Callable]]
