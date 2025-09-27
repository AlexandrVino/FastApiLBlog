from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from application.transactions import Transaction, TransactionsGateway


class DatabaseTransaction(Transaction):
    """
    Реализация интерфейса Transaction для работы с транзакциями SQLAlchemy.

    Обеспечивает базовые операции commit и rollback для управления транзакциями.
    """

    def __init__(self, transaction: AsyncSessionTransaction):
        self._transaction = transaction

    async def commit(self):
        """Фиксирует текущую транзакцию в базе данных."""

        await self._transaction.commit()

    async def rollback(self):
        """Откатывает текущую транзакцию."""

        await self._transaction.rollback()


class TransactionsDatabaseGateway(TransactionsGateway):
    """
    Шлюз для управления транзакциями в базе данных.

    Поддерживает вложенные транзакции и автоматическое управление
    жизненным циклом транзакций через контекстный менеджер.
    """

    __transaction: AsyncSessionTransaction | None = None

    def __init__(
        self,
        session: AsyncSession,
        transaction: AsyncSessionTransaction | None = None,
    ):
        self._session = session
        self._transaction = transaction

    async def __aenter__(self) -> Transaction:
        self._transaction = self._session.begin_nested()
        await self._transaction.__aenter__()
        return DatabaseTransaction(self._transaction)

    def nested(self) -> "TransactionsDatabaseGateway":
        """Создает новый шлюз для вложенной транзакции."""

        return TransactionsDatabaseGateway(self._session, self._session.begin_nested())

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Обрабатывает завершение транзакции при выходе из контекста."""

        if self._transaction and self._transaction.is_active:
            if exc_type is None:
                await self._transaction.commit()
            else:
                await self._transaction.rollback()

        if self._transaction:
            await self._transaction.__aexit__(exc_type, exc_val, exc_tb)
        if self._session.in_nested_transaction():
            self._transaction = self._session.get_nested_transaction()
        else:
            self._transaction = None
