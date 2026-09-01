from .dop_germany import DopGermanyPlugin

def classFactory(iface):
    return DopGermanyPlugin(iface)