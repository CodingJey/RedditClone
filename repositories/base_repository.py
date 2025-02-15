from infra import 

class BaseRepository:
    """Base repository class with database access."""
    def __init__(self, session: AsyncSession):
        self.session = session
