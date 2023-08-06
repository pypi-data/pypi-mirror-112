import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed, pre_save, pre_delete, post_save
from django.dispatch import receiver

from ..models import Dictionary, RssFeed
from ..podle import PodleHelper

logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(pre_save, sender=Dictionary)
def create_or_update_dictionary_word(sender, instance, *args, **kwargs):
    response = PodleHelper().create_or_update_word(
        {"value": instance.pronunciation, "raw": instance.word}
    )
    if "added" not in response:
        logger.error(response)
        raise Exception(response)

    logger.info(response)


@receiver(pre_delete, sender=Dictionary)
def delete_dictionary_word(sender, instance, *args, **kwargs):
    response = PodleHelper().delete_word(instance.word)
    if "deleted" not in response:
        logger.error(response)
        raise Exception(response)

    logger.info(response)


@receiver(post_save, sender=RssFeed)
def create_rss_feed(sender, instance, created, *args, **kwargs):
    if not instance.feed:
        response = PodleHelper().create_private_rss(
            {
                "subscriberId": instance.user.pk,
                "newsletterName": settings.PODLE_NEWSLETTER_NAME,
            }
        )

        feed = response.get(str(instance.user.pk), None)

        if not feed:
            logger.error(response)
            raise Exception(response)

        instance.feed = feed
        instance.save()

        logger.info(response)


@receiver(signal=m2m_changed, sender=User.groups.through)
def handle_rss_feeds(instance, action, reverse, model, pk_set, using, *args, **kwargs):
    """Create or delete private rss feeds when adding users to the group defined in PODLE_RSS_FEED_GROUP_NAME"""

    # signal can have User (reverse=False) or Group (reverse=True) as sender
    group_pks = [instance.pk] if reverse else pk_set

    if action == "post_add" or action == "post_remove":
        if not Group.objects.filter(
            pk__in=group_pks, name=settings.PODLE_RSS_FEED_GROUP_NAME
        ).exists():
            return False

        users_pks = pk_set if reverse else [instance.pk]

        if action == "post_add":
            for user_pk in users_pks:
                RssFeed.objects.get_or_create(user_id=user_pk)
        else:
            rss_feeds = RssFeed.objects.filter(user_id__in=users_pks)
            rss_feeds.delete()


@receiver(pre_delete, sender=RssFeed)
def delete_rss_feed(sender, instance, *args, **kwargs):
    response = PodleHelper().delete_private_rss(
        instance.user.pk, settings.PODLE_NEWSLETTER_NAME
    )
    if "deleted" not in response.get(str(instance.user.pk)):
        logger.error(response)
        raise Exception(response)

    logger.info(response)
