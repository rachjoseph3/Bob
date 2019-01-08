#Bob V1.01

#This script takes a shapefile with a collumn that contains a list of feature classes and adds them to a map document. ArcTool Version!
#by Rachel Joseph

#Start: 1/3/2019
#Last Update: 1/8/2019

print("Starting Program")

import arcpy, sys

#Parameters
workspace = arcpy.env.workspace = arcpy.GetParameterAsText(0)#gdb containing feature classes want to view (r"E:\ProductionTools\Bob\line_t6390\Line_T6390_Outputs\Test2HazardTree.gdb")
shapeName = arcpy.GetParameterAsText(1) #shapefile holding names of feature classes in workspace (r"E:\ProductionTools\Bob\Testgdb.gdb\nameHolder")
mapdoc = arcpy.GetParameterAsText(2) #map document to view data (r"E:\ProductionTools\Bob\ProductionToolTest.mxd")
field = arcpy.GetParameterAsText(3) #field that contains names of feature classes want to view (from ones held in workspace)("Name")

#Set up map document
mxd = arcpy.mapping.MapDocument(mapdoc)
df = arcpy.mapping.ListDataFrames(mxd, "*")[0] #may also want to use (df = mxd.activeDataFrame)
arcpy.AddMessage("Dataframe Found\n")

#Feature Count
fcCount = 1

#parse through the shapefile holding the BobVfeature class names
try:
    with arcpy.da.SearchCursor(shapeName, field) as cursor:
        for fc in cursor:
            #collect names of feature classes
            featureClassName = " ".join(fc)
            #path to the feature class
            featureClass = "{}\{}".format(workspace, featureClassName)
            #create and add layer from fc
            newLayer = arcpy.mapping.Layer(featureClass)
            arcpy.mapping.AddLayer(df, newLayer, "BOTTOM")
            arcpy.AddMessage("Feature class number {} added to the data frame\n".format(fcCount))
            fcCount += 1

    del cursor
except Exception as e:
    arcpy.AddMessage("The Following Error has Occured: {}".format(e))
    sys.exit()

arcpy.RefreshActiveView()
arcpy.RefreshTOC()
arcpy.AddMessage("View Refreshed\n")

df.zoomToSelectedFeatures()
arcpy.AddMessage("Zoomed to Layer\n")

mxd.save()

del mxd

arcpy.AddMessage("Feature Classes added to the following map document: {}\n".format(mapdoc))
arcpy.AddMessage("Program Completed")
