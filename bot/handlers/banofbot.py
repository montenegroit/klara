import logging
import asyncio

from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from bot.states.states import Poll
from bot.keyboards.keyboard_utils import create_ban_vote_keyboard
from bot.services.banofbot import ban_user

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command(commands="ban"), StateFilter(default_state))
async def ban_handler(message: types.Message, state: FSMContext) -> None:
    try:
        user = message.reply_to_message.from_user
    except AttributeError:
        msg = "Эта команда работает только на реплай сообщения"
        await message.reply(msg)
    else:
        msg = f"Забанить пользователя {user.first_name}?"
        yes_votes, no_votes = 0, 0
        message_to_delete = message.reply_to_message.message_id
        data = {
            "yes_votes": yes_votes,
            "no_votes": no_votes,
            "user_to_ban": user.id,
            "message_to_delete": message_to_delete,
        }
        to_do = [
            asyncio.ensure_future(
                message.reply(msg, reply_markup=create_ban_vote_keyboard(yes_votes, no_votes))
            ),
            state.update_data(data),
            state.set_state(Poll.start_poll),
        ]
        await asyncio.gather(*to_do)


min_count_of_votes = 10


@router.callback_query(StateFilter(Poll.start_poll))
async def polling_process(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    yes_votes = data.get("yes_votes", 0)
    no_votes = data.get("no_votes", 0)
    voter_ids = data.get("voter_ids", [])

    if callback_query.data == "yes":
        yes_votes += 1
    if callback_query.data == "no":
        no_votes += 1

    user_id = callback_query.from_user.id
    if user_id in voter_ids:
        return
    voter_ids.append(user_id)

    to_do = [
        state.update_data(yes_votes=yes_votes, no_votes=no_votes, voter_ids=voter_ids),
        asyncio.ensure_future(
            callback_query.message.edit_reply_markup(reply_markup=create_ban_vote_keyboard(yes_votes, no_votes))
        ),
    ]
    await asyncio.gather(*to_do)

    if yes_votes + no_votes >= min_count_of_votes:
        await state.set_state(Poll.finish_poll)


@router.callback_query(StateFilter(Poll.finish_poll))
async def end_polling(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    result = await ban_user(data)
    if result:
        await callback_query.message.answer("Пользователь забанен")
    else:
        await callback_query.message.answer("Бан отменяется")
    to_do = [asyncio.ensure_future(callback_query.message.delete()), state.clear()]
    await asyncio.gather(*to_do)
