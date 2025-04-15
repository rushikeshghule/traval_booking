def get_placeholder_image(category):
    """Get a placeholder image URL based on category"""
    
    images = {
        'bus': [
            'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957',
            'https://images.unsplash.com/photo-1570125909232-eb263c188f7e',
        ],
        'flight': [
            'https://images.unsplash.com/photo-1436491865332-7a61a109cc05',
            'https://images.unsplash.com/photo-1542296332-2e4473faf563',
        ],
        'train': [
            'https://images.unsplash.com/photo-1474487548417-781cb71495f3',
            'https://images.unsplash.com/photo-1532105956626-9569c03602f6',
        ],
        'hotel': [
            'https://images.unsplash.com/photo-1566073771259-6a8506099945',
            'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa',
            'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b',
        ],
        'user': [
            'https://ui-avatars.com/api/?background=3498db&color=fff',
        ],
        'destination': [
            'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9',
            'https://images.unsplash.com/photo-1502602898657-3e91760cbb34',
            'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e',
        ],
    }
    
    import random
    category_images = images.get(category, images['destination'])
    return f"{random.choice(category_images)}?w=500&h=300&fit=crop" 