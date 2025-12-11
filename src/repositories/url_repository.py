# This file is maintained for backward compatibility
# Use the specific repositories instead:
# - CreateUrlRepository for creating short URLs
# - RedirectToUrlRepository for redirecting to original URLs
# - GetAllUrlsRepository for viewing all URLs
# - DeleteUrlRepository for deleting URLs

from .create_url_repository import CreateUrlRepository as URLRepository

# For backward compatibility with existing imports
__all__ = ["URLRepository"]