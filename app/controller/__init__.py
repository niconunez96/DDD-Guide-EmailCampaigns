from .campaign import campaign_endpoint
from .contact_list import contact_list_endpoint
from .sendgrid import sengrid_endpoint
from .user import user_endpoint

endpoints = [campaign_endpoint, sengrid_endpoint, contact_list_endpoint, user_endpoint]
