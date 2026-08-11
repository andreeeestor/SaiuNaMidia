import cloudinary
import cloudinary.uploader
import cloudinary.api
from core.config import settings


def init_cloudinary():
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )


# Automatically initialize Cloudinary client on import
init_cloudinary()
