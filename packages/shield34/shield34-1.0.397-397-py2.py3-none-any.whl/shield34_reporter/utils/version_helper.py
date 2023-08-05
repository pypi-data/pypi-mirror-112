import pkg_resources


class VersionHelper(object):
    def get_version(self):
        try:
            return pkg_resources.get_distribution('shield34').version
        except Exception:
            return "Unknown"
