from shield34_reporter.consts.shield34_properties import Shield34Properties
from shield34_reporter.utils.version_helper import VersionHelper


def get_sdk_contract(run_contract):
    Shield34Properties.initialize()
    atts = getAttributes(Shield34Properties)
    return {"version": VersionHelper().get_version(), "run_id": run_contract.id, "language": "PYTHON",
            "properties": atts}


def getAttributes(clazz):
    attrs = {}
    for name in vars(clazz):
        if name.startswith("__"):
            continue
        if name.startswith('api_'):
            continue
        if name.startswith("configParser"):
            continue
        attr = getattr(clazz, name)
        if callable(attr):
            continue
        attrs[name] = attr
    return attrs
