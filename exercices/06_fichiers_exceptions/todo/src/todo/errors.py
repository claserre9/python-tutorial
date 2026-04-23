"""Exceptions applicatives."""


class AppError(Exception):
    """Racine des erreurs applicatives."""


class TaskNotFoundError(AppError):
    """Soulevée quand un ID de tâche n'existe pas."""
    # TODO


class InvalidTaskError(AppError):
    """Soulevée quand une tâche est invalide (titre vide, etc.)."""
    # TODO


class StorageError(AppError):
    """Soulevée quand le fichier de stockage est illisible/corrompu."""
    # TODO
