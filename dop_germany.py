import os
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject, QgsLayerDefinition

def classFactory(iface):
    return DopGermanyPlugin(iface)

class DopGermanyPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.action = None
        self.toolbar = None

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        icon = QIcon(icon_path)

        # Create the action for your toolbar and menu
        self.action = QAction(icon, "DOP Germany: Load WMS", self.iface.mainWindow())
        self.action.triggered.connect(self.run)

        # Create a dedicated toolbar for your plugin
        self.toolbar = self.iface.addToolBar("DOP Germany Toolbar")
        self.toolbar.setObjectName("DopGermanyToolbar")
        self.toolbar.addAction(self.action)

        # Add to the Plugins menu as well
        self.iface.addPluginToMenu("&DOP Germany", self.action)

    def unload(self):
        # Clean up toolbar and menu when QGIS closes
        del self.toolbar
        self.iface.removePluginMenu("&DOP Germany", self.action)

    def run(self):
        # Automatically look for the .qlr file inside your plugin folder
        qlr_path = os.path.join(self.plugin_dir, "WMS DOP Deutschland.qlr")
        
        if not os.path.exists(qlr_path):
            self.iface.messageBar().pushCritical("Error", f"Could not find .qlr file at:\n{qlr_path}")
            return

        # Load the .qlr file into the project
        success, error = QgsLayerDefinition.loadLayerDefinition(
            qlr_path,
            QgsProject.instance(),
            QgsProject.instance().layerTreeRoot()
        )

        if success:
            root = QgsProject.instance().layerTreeRoot()
            
            # === 1. Disable mutually exclusive groups so layers don't hide each other ===
            for group in root.findGroups():
                group.setIsMutuallyExclusive(False)
                
            # === 2. Automatically check/turn on all groups and layers ===
            for group in root.findGroups():
                group.setItemVisibilityChecked(True)
                
            for node in root.findLayers():
                node.setItemVisibilityChecked(True)

            self.iface.messageBar().pushSuccess("Success", "DOP Germany: WMS layers loaded, exclusivity removed, and all layers checked!")
        else:
            self.iface.messageBar().pushCritical("Error", f"Could not load the .qlr file:\n{error}")