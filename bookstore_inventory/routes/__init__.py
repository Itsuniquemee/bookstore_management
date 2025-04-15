# routes/__init__.py
from .user_portal import show as show_user_portal
from .seller_portal import show as show_seller_portal
# from .admin_portal import show as show_admin_portal  # Uncomment when ready

# Optional: Keep your existing imports if needed elsewhere
from . import inventory, sales, customers

__all__ = [
    'show_user_portal', 
    'show_seller_portal',
    # 'show_admin_portal',
    'inventory',
    'sales',
    'customers'
]