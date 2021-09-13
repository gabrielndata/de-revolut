from settings import AUTH


def verify_auth_data(username: str, password: str) -> bool:
    """Verify username and password """
    if not (username and password):
        return False
    return AUTH[username] == password
