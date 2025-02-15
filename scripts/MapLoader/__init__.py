from .MapLoader import MapLoaderPlugin

def classFactory(iface):
    return MapLoaderPlugin(iface)
