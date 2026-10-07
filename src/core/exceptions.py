class ValidationError(Exception):
    """Exception levée lorsqu'une donnée est invalide."""
    pass


class RepositoryError(Exception):
    """Exception liée au repository."""
    pass