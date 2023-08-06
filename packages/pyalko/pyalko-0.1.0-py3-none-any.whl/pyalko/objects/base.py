"""AL-KO: Base"""
import logging


class AlkoBase:
    """Base class for AL-KO."""

    logger = logging.getLogger(__name__)

    def __init__(self, attributes) -> None:
        """Initialize."""
        self.attributes = attributes


class AlkoBaseClient(AlkoBase):
    """Base class for Alko."""

    def __init__(self, client, attributes: dict) -> None:
        """Initialise."""
        super().__init__(attributes)
        self.client = client
