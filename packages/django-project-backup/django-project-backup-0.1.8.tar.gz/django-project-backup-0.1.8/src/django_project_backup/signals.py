import logging

from django.db.models.signals import post_save, pre_delete, post_delete, m2m_changed, pre_save

from .utils.commons import do_backup, do_delete, get_serialized, object_should_backup, get_related_objects_lists, get_object_model_name

logger = logging.getLogger('django_project_backup.{}'.format(__name__))


def prepare_update_model(sender, instance, **kwargs):
    if not kwargs.get('raw', False) and not getattr(instance, '__dpb__updating', False) and instance.pk is not None:
        model_name = get_object_model_name(instance._meta.app_label, instance._meta.object_name)

        if object_should_backup(instance._meta.app_label, model_name):
            logger.debug('prepare_update_model {} {} {}'.format(sender, instance, kwargs))

            setattr(instance, '__dpb__related_objects_lists', get_related_objects_lists(instance))


def update_model(sender, instance, created, **kwargs):
    if not kwargs.get('raw', False) and not getattr(instance, '__dpb__updating', False):
        model_name = get_object_model_name(instance._meta.app_label, instance._meta.object_name)

        if object_should_backup(instance._meta.app_label, model_name):
            if created:
                logger.debug('create_model {} {} {}'.format(sender, instance, kwargs))
            else:
                logger.debug('update_model {} {} {}'.format(sender, instance, kwargs))

            do_backup(instance)


def prepare_delete_model(sender, instance, **kwargs):
    model_name = get_object_model_name(instance._meta.app_label, instance._meta.object_name)

    if object_should_backup(instance._meta.app_label, model_name):
        logger.debug('prepare_delete_model {} {} {}'.format(sender, instance, kwargs))

        setattr(instance, '__dpb__related_objects_lists', get_related_objects_lists(instance))
        setattr(instance, '__dpb__object', get_serialized(instance))


def delete_model(sender, instance, **kwargs):
    model_name = get_object_model_name(instance._meta.app_label, instance._meta.object_name)

    if object_should_backup(instance._meta.app_label, model_name):
        logger.debug('delete_model {} {} {}'.format(sender, instance, kwargs))

        do_delete(instance)


def update_model_relations(sender, instance, action, **kwargs):
    if not kwargs.get('raw', False):
        model_name = get_object_model_name(instance._meta.app_label, instance._meta.object_name)

        if object_should_backup(instance._meta.app_label, model_name):
            logger.debug('update_model_relations {} {} {} {}'.format(action, sender, instance, kwargs))

            do_backup(instance)


# https://docs.djangoproject.com/en/3.2/topics/signals/#listening-to-signals

pre_save.connect(prepare_update_model, weak=False)
post_save.connect(update_model, weak=False)
pre_delete.connect(prepare_delete_model, weak=False)
post_delete.connect(delete_model, weak=False)
m2m_changed.connect(update_model_relations, weak=False)
