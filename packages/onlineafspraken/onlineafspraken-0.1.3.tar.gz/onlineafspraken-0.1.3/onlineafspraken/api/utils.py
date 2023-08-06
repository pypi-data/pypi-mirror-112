def build_signature(**kwargs):
    ret = ""
    sorted_kwargs_list = sorted(kwargs.items(), key=lambda t: t[0])
    for key, value in dict(sorted_kwargs_list).items():
        if value is None:
            continue
        ret += str(key) + str(value)
    return ret


def build_param(method, **kwargs):
    from datetime import datetime
    from decouple import config
    from hashlib import sha1

    api_key = config("ONLINE_AFSPRAKEN_KEY")
    api_secret = config("ONLINE_AFSPRAKEN_SECRET")

    salt = int(datetime.now().timestamp())
    signature_raw = (
        build_signature(**kwargs) + "method" + method + api_secret + str(salt)
    )
    signature_encoded = signature_raw.encode()
    signature = sha1(signature_encoded)

    params = {
        "api_key": api_key,
        "api_salt": salt,
        "api_signature": signature.hexdigest(),
        "method": method,
    }
    return dict(params, **kwargs)
