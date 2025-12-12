# -*- coding: utf-8 -*-
import arcpy
import os
from UpdateProj import jason2shape


class Toolbox:
    def __init__(self):
        self.label = "no_tax_toolbox"
        self.alias = "no_tax_toolbox"
        self.tools = [Tool]


class Tool:
    def __init__(self):
        self.label = "no_tax_tool"
        self.description = "Convert JSON file to Shapefile"

    def getParameterInfo(self):
        param0 = arcpy.Parameter(
            displayName="JSON File Path",
            name="input_json",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="Workspace Folder",
            name="workspace",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="WKID",
            name="wkid",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Output Shapefile",
            name="fcname",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output"
        )
        return [param0, param1, param2, param3]

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        input_json = parameters[0].valueAsText
        workspace = parameters[1].valueAsText
        wkid = int(parameters[2].valueAsText)

        fc_full_path = parameters[3].valueAsText
        fcname = os.path.splitext(os.path.basename(fc_full_path))[0]

        jason2shape(input_json, workspace, fcname, wkid)

    def postExecute(self, parameters):
        return

