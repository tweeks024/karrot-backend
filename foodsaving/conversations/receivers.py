from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from foodsaving.conversations import tasks, stats
from foodsaving.conversations.models import ConversationParticipant, ConversationMessage, ConversationMessageReaction


@receiver(post_save, sender=ConversationMessage)
def mark_as_read(sender, instance, **kwargs):
    """Mark sent messages as read for the author"""

    message = instance
    participant = ConversationParticipant.objects.get(
        user=message.author,
        conversation=message.conversation
    )

    participant.seen_up_to = message
    participant.save()


@receiver(post_save, sender=ConversationMessage)
def notify_participants(sender, instance, **kwargs):
    message = instance

    if not message.conversation.target:
        return

    tasks.notify_participants(message)


@receiver(post_save, sender=ConversationMessage)
def message_created(sender, instance, created, **kwargs):
    if not created:
        return
    stats.message_written(instance)


@receiver(post_save, sender=ConversationMessageReaction)
def reaction_created(sender, instance, created, **kwargs):
    if not created:
        return
    stats.reaction_given(instance)


@receiver(post_save, sender=ConversationParticipant)
def set_conversation_updated_at_on_create(sender, instance, **kwargs):
    if kwargs['created']:
        participant = instance
        participant.conversation.save()


@receiver(pre_delete, sender=ConversationParticipant)
def set_conversation_updated_at_on_delete(sender, instance, **kwargs):
    participant = instance
    participant.conversation.save()
