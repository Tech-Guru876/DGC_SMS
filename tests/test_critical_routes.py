from app.models import Role
from tests.conftest import _create_user, _login


def test_samples_route_smoke(app, client):
    with app.app_context():
        _create_user(role=Role.OFFICER, username='officer', must_change_password=False)

    _login(client, username='officer')
    resp = client.get('/samples/')

    assert resp.status_code == 200
    assert b'Samples' in resp.data


def test_roles_permissions_route_smoke(app, client):
    with app.app_context():
        _create_user(role=Role.ADMIN, username='admin', must_change_password=False)

    _login(client, username='admin')
    resp = client.get('/auth/roles-permissions')

    assert resp.status_code == 200
    assert b'Roles &amp; Permissions' in resp.data


def test_admin_dropdowns_list_smoke(app, client):
    """GET /admin/dropdowns must return 200 for an admin user (regression for
    the db.create_all() ordering bug that caused a 500 when dropdown_configs
    table was absent)."""
    with app.app_context():
        _create_user(role=Role.ADMIN, username='admin', must_change_password=False)

    _login(client, username='admin')
    resp = client.get('/admin/dropdowns')

    assert resp.status_code == 200
    assert b'Dropdown Configuration' in resp.data


def test_admin_dropdown_add_smoke(app, client):
    """POST /admin/dropdowns/add must add an entry and redirect."""
    with app.app_context():
        _create_user(role=Role.ADMIN, username='admin', must_change_password=False)

    _login(client, username='admin')
    resp = client.post('/admin/dropdowns/add', data={
        'category': 'api',
        'value': 'TestCompound',
        'label': 'Test Compound',
        'branch': '',
        'sort_order': '0',
        'is_active': 'y',
    }, follow_redirects=True)

    assert resp.status_code == 200
    assert b'added' in resp.data.lower()

    # Verify the entry was actually persisted to the database.
    with app.app_context():
        from app.models import DropdownConfig
        entry = DropdownConfig.query.filter_by(category='api', value='TestCompound').first()
        assert entry is not None
        assert entry.label == 'Test Compound'
        assert entry.branch is None
        assert entry.sort_order == 0
        assert entry.is_active is True
