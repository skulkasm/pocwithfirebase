from flask import current_app

from google.cloud import firestore


builtin_list = list


def init_app(app):
    pass


def add_data(data):
    db = firestore.Client(current_app.config['PROJECT_ID'])
   # db = firebase.database()
    db.collection(u'kycdocs').document().set(data)


def update(data, id=None):
    ds = firestore.Client(current_app.config['PROJECT_ID'])
    if id:
        key = ds.key('doc', int(id))
    else:
        key = ds.key('doc')

    entity = firestore.collection(
        key=key,
        exclude_from_indexes=['department'])

    entity.update(data)
    ds.put(entity)

    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity