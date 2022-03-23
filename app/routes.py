from app import views


def setup_routes(app):
    app.router.add_route('GET', '/api/v1/profile', views.get_profile)
    app.router.add_route('GET', '/api/v1/mile_transactions/{profile_id}', views.get_mile_transactions)
