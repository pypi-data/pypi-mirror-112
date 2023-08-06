import requests

version = ""


def isUpdates(file_url, clientVersion):
    get_json = requests.get(file_url)
    json = get_json.json()
    actualClient = json['version']['client_version']
    if actualClient != clientVersion:
        return True
    else:
        return False


def isUpdatesMsb(file_url):
    global version
    try:
        from pip._internal.utils.misc import get_installed_distributions
    except ImportError:
        from pip import get_installed_distributions
    get_json = requests.get(file_url)
    json = get_json.json()
    installed = get_installed_distributions()
    actualVersion = json['version']['msb_pkg_version']
    for i in installed:
        if i.key == "msb":
            version = i.version
    #version = "0.1"
    if actualVersion != version:
        return True
    else:
        return False
