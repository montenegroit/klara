from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from bot.models.stats.models import StatsMessageCount


class IncreaseCountUserMessagesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        print(
            f"income msg from user: {event.from_user.id} {event.from_user.username} : {event.text}"
        )
        """
        message_id=18
        date=datetime.datetime(2023, 9, 22, 12, 53, 22, tzinfo=TzInfo(UTC))
        chat=Chat(
            id=-4081188855, 
            type='group', 
            title='klara_test_group', 
            username=None, 
            first_name=None, 
            last_name=None, 
            is_forum=None, 
            photo=None, 
            active_usernames=None, 
            emoji_status_custom_emoji_id=None, 
            emoji_status_expiration_date=None, 
            bio=None, 
            has_private_forwards=None, 
            has_restricted_voice_and_video_messages=None, 
            join_to_send_messages=None, 
            join_by_request=None, 
            description=None, 
            invite_link=None, 
            pinned_message=None, 
            permissions=None, 
            slow_mode_delay=None, 
            message_auto_delete_time=None, 
            has_aggressive_anti_spam_enabled=None, 
            has_hidden_members=None, 
            has_protected_content=None, 
            sticker_set_name=None, 
            can_set_sticker_set=None, 
            linked_chat_id=None, 
            location=None, 
            all_members_are_administrators=True
        ) 
        message_thread_id=None 
        from_user=User(
            id=5330519913, 
            is_bot=False, 
            first_name='Andrey', 
            last_name=None, 
            username='andreydmitr22',
            language_code=None, 
            is_premium=None, 
            added_to_attachment_menu=None, 
            can_join_groups=None, 
            can_read_all_group_messages=None, 
            supports_inline_queries=None
        ) 
        sender_chat=None 
        forward_from=None 
        forward_from_chat=None 
        forward_from_message_id=None 
        forward_signature=None 
        forward_sender_name=None 
        forward_date=None 
        is_topic_message=None 
        is_automatic_forward=None 
        reply_to_message=None 
        via_bot=None 
        edit_date=None 
        has_protected_content=None 
        media_group_id=None 
        author_signature=None 
        
        text='4' 
        
        entities=None 
        animation=None 
        audio=None 
        document=None 
        photo=None 
        sticker=None 
        story=None 
        video=None 
        video_note=None 
        voice=None 
        caption=None 
        caption_entities=None 
        has_media_spoiler=None 
        contact=None 
        dice=None 
        game=None 
        poll=None 
        venue=None 
        location=None 
        new_chat_members=None 
        left_chat_member=None 
        new_chat_title=None 
        new_chat_photo=None 
        delete_chat_photo=None 
        group_chat_created=None 
        supergroup_chat_created=None 
        channel_chat_created=None 
        message_auto_delete_timer_changed=None 
        migrate_to_chat_id=None 
        migrate_from_chat_id=None 
        pinned_message=None 
        invoice=None 
        successful_payment=None 
        user_shared=None 
        chat_shared=None 
        connected_website=None 
        write_access_allowed=None 
        passport_data=None 
        proximity_alert_triggered=None 
        forum_topic_created=None 
        forum_topic_edited=None 
        forum_topic_closed=None 
        forum_topic_reopened=None 
        general_forum_topic_hidden=None 
        general_forum_topic_unhidden=None 
        video_chat_scheduled=None 
        video_chat_started=None 
        video_chat_ended=None 
        video_chat_participants_invited=None 
        web_app_data=None 
        reply_markup=None
        """
        await StatsMessageCount.increase_count(
            session=data["session"],
            from_chat_id=event.chat.id,
            from_user_id=event.from_user.id,
        )
