import logging
import os
import json

from urllib.parse import quote
from requests.exceptions import HTTPError

from django.db.models.fields.reverse_related import ManyToManyRel, ManyToOneRel, OneToOneRel
from django.utils.timezone import now

from django_project_backup.utils.couchdb.serializers import Serializer
from django_project_backup.utils.couchdb.stream import CouchdbStream

from ..settings import EXCLUDED_MODELS, \
                       DO_FAILSAFE_BACKUP, FAILSAFE_BACKUP_PATH_UPDATE, FAILSAFE_BACKUP_PATH_DELETE, \
                       DO_REALTIME_LOG_BACKUP, DO_REALTIME_COUCHDB_BACKUP, \
                       PROJECT_NAME, SHARD_NAME

logger = logging.getLogger('django_project_backup.utils.{}'.format(__name__))
backup_logger = logging.getLogger('django_project_backup.backup_logger')
_DPB_STREAM = None


def get_stream():
    global _DPB_STREAM
    if _DPB_STREAM is None:
        _DPB_STREAM = CouchdbStream()
    return _DPB_STREAM


def memoize(func):
    cache = dict()

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func


@memoize
def get_object_model_name(app_label, object_name):
    # logger.debug('Getting object model name for: {}, {}'.format(app_label, object_name))
    model_name = '%s.%s' % (app_label, object_name)

    return model_name.lower()


@memoize
def object_should_backup(app_label, model_name):
    logger.debug('Checking if "{}" model "{}" should backup'.format(app_label, model_name))

    return model_name not in EXCLUDED_MODELS and not app_label.startswith('migration')  # !noqa


def get_serialized(instance):
    serializer = Serializer()
    # using freshly obtained queryset should prevent faulty transactions to be backed up
    objects = instance.__class__.objects.filter(pk=instance.pk)
    serialized = json.loads(serializer.serialize(objects,
                                                 use_natural_foreign_keys=True))[0]

    return serialized


"""
def get_object_id(instance):
    # get object model name
    model_name = get_object_model_name(instance._meta.app_label, instance._meta.object_name)

    # Get object id
    try:
        object_id = str(instance.natural_key())
    except AttributeError:
        object_id = instance.pk

    dump_object_id = '{}:{}'.format(model_name, object_id)

    return dump_object_id
"""


def get_event_representation(serialized, action):
    return {
        'type': 'django_project_backup',
        'project': PROJECT_NAME,
        'shard': SHARD_NAME,
        'action': action,
        'timestamp': now().timestamp(),
        'object': serialized
    }


def get_related_objects_lists(instance):
    """

    Args:
        instance: Django model instance

    Returns:
        List of related objects queryset and/or lists (lazy)
    """
    related_objects_lists = []
    instance_fields = instance._meta.get_fields(include_hidden=True)

    related_m2m_fields = [f.related_name or f.name + '_set'
                          for f in instance_fields
                          if type(f) == ManyToManyRel]  # !noqa '_set'
    related_many_to_one_fields = [f.related_name
                                  for f in instance_fields
                                  if type(f) == ManyToOneRel and f.related_name is not None and not f.related_name.endswith('+')]
    related_one_to_one_fields = [f.related_name
                                 for f in instance_fields
                                 if type(f) == OneToOneRel and f.related_name is not None]

    for f in related_m2m_fields:
        objs = getattr(instance, f).all()
        logger.debug('related_m2m {}:{}'.format(f, objs))
        related_objects_lists.append(list(objs))  # ! noqa should use generator
    for f in related_many_to_one_fields:
        objs = getattr(instance, f).all()
        logger.debug('related_many_to_one {}:{}'.format(f, objs))
        related_objects_lists.append(list(objs))  # ! noqa should use generator
    for f in related_one_to_one_fields:
        obj = getattr(instance, f, None)
        if obj is not None:
            logger.debug('related_one_to_one {}:{}'.format(f, obj))
            related_objects_lists.append([obj])

    return related_objects_lists


def do_failsafe_backup(serialized):
    file_name = quote(serialized['_id'], safe='')  # safe filename path
    with open(os.path.join(FAILSAFE_BACKUP_PATH_UPDATE,
                           '{}.json'.format(file_name)), 'w') as fd:
        json.dump(serialized, fd)


def do_backup(instance):
    serialized = get_serialized(instance)

    logger.debug('Backing up model "{}"'.format(serialized['_id']))

    if DO_REALTIME_LOG_BACKUP:
        backup_logger.info(json.dumps(get_event_representation(serialized, action='backup_model')))

    if DO_REALTIME_COUCHDB_BACKUP:
        try:
            stream = get_stream()
            stream.send(serialized)
        except:
            logger.exception('Error backing up serialized model')
            if DO_FAILSAFE_BACKUP:
                do_failsafe_backup(serialized)
            return

        related_objects_lists = getattr(instance, '__dpb__related_objects_lists', None)
        logger.info('RELATED: {}'.format(related_objects_lists))
        if related_objects_lists is not None:
            for list in related_objects_lists:
                logger.info('checking list: {}'.format(list))
                for obj in list:
                    model_name = get_object_model_name(obj._meta.app_label, obj._meta.object_name)
                    if object_should_backup(obj._meta.app_label, model_name):
                        logger.debug('Backing up related model: {}'.format(obj))
                        obj.refresh_from_db()
                        obj.save()


def do_failsafe_delete(serialized):
    file_name = quote(serialized['_id'], safe='')  # safe filename path
    with open(os.path.join(FAILSAFE_BACKUP_PATH_DELETE,
                           '{}.json'.format(file_name)), 'w') as fd:
        json.dump(fd, serialized)


def do_delete(instance):
    serialized = getattr(instance, '__dpb__object', None)

    if serialized is not None:
        logger.info('Deleting backed up model "{}"'.format(serialized['_id']))

        if DO_REALTIME_LOG_BACKUP:
            backup_logger.info(json.dumps(get_event_representation(serialized, action='delete_model')))

        if DO_REALTIME_COUCHDB_BACKUP:
            try:
                stream = get_stream()
                stream.db.delete_document(serialized['_id'])
            except KeyError:
                logger.warning('Document "{}" has not been backed up'.format(serialized['_id']))
                pass
            except HTTPError as e:
                if getattr(e, 'code', None) == 404:
                    logger.warning('Document "{}" has not been backed up'.format(serialized['_id']))
                    pass
                else:
                    logger.exception('Error deleting model')
                    if DO_FAILSAFE_BACKUP:
                        do_failsafe_delete(serialized)
                    return
            except Exception as e:
                logger.exception('Error ({}) deleting model'.format(e))
                if DO_FAILSAFE_BACKUP:
                    do_failsafe_delete(serialized)
                return

            related_objects_lists = getattr(instance, '__dpb__related_objects_lists', None)
            logger.info('RELATED: {}'.format(related_objects_lists))
            if related_objects_lists is not None:
                for list in related_objects_lists:
                    logger.info('checking list: {}'.format(list))
                    for obj in list:
                        model_name = get_object_model_name(obj._meta.app_label, obj._meta.object_name)
                        if object_should_backup(obj._meta.app_label, model_name):
                            logger.debug('Backing up related model: {}'.format(obj))
                            obj.refresh_from_db()
                            obj.save()
