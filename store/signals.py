from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import CreateProfile

@receiver(user_signed_up)
def create_profile_for_social_user(sender, request, user, **kwargs):
    """
    Automatically create a CreateProfile instance for users who sign up via third-party providers.
    """
    if not hasattr(user, 'profile'):  # Check if the profile already exists
        # Retrieve first name and last name from the social account
        first_name = user.first_name or ''
        last_name = user.last_name or ''
        
        # If the social account provides additional data (e.g., phone), retrieve it
        extra_data = kwargs.get('sociallogin').account.extra_data if 'sociallogin' in kwargs else {}
        phone = extra_data.get('phone', None)  # Replace 'phone' with the correct key if available

        # Create the profile
        CreateProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )