from sqlalchemy import Column, BigInteger, Integer, UniqueConstraint, DateTime, text

from bot.models.base import Base


class StatsMessageCount(Base):
    __tablename__ = "messages_count"

    id = Column(Integer, primary_key=True)

    from_chat_id = Column(BigInteger, nullable=False)
    from_user_id = Column(BigInteger, nullable=False)
    count = Column(Integer, nullable=False)

    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    __table_args__ = (
        UniqueConstraint(
            "from_chat_id",
            "from_user_id",
            name="unq_user_from_chat_id_from_user_id",
        ),
    )

    @staticmethod
    async def increase_count(session, from_chat_id=False, from_user_id=False):
        query = text(
            """
            INSERT INTO messages_count (from_chat_id, from_user_id, count)
            VALUES (:from_chat_id, :from_user_id, 1)
            ON CONFLICT ON CONSTRAINT unq_user_from_chat_id_from_user_id
            DO
            UPDATE
            SET
                count = messages_count.count + 1,
                updated_at = CURRENT_TIMESTAMP
        """
        )
        try:
            await session.execute(
                query,
                params={"from_chat_id": from_chat_id, "from_user_id": from_user_id},
            )
            await session.commit()
        except Exception as e:
            print("Error: %s", e)
            await session.rollback()
