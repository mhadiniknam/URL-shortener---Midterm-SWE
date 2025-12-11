# This file is maintained for backward compatibility
# Use the specific services instead:
# - CreateUrlService for creating short URLs
# - RedirectToUrlService for redirecting to original URLs
# - GetAllUrlsService for viewing all URLs
# - DeleteUrlService for deleting URLs

from .create_url_service import CreateUrlService as URLService

# For backward compatibility with existing imports
__all__ = ["URLService"]