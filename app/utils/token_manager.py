revoked_tokens = set()

def is_token_revoked(jti):
    return jti in revoked_tokens

def revoke_token(jti):
    revoked_tokens.add(jti)