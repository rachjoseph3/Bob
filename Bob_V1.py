#Bob V1.00

#This script takes a shapefile with a collumn that contains a list of feature classes and adds them to a map document. Now with GUI!
#by Rachel Joseph

#Start: 1/3/2019
#Last Update: 1/7/2019

print("Starting Program")

import arcpy
import tkinter as tk

def clearTheField():
    e1.delete(0,tk.END)
    e2.delete(0,tk.END)
    e3.delete(0,tk.END)
    e4.delete(0,tk.END)

def runThe5KWeCallLife():
    #Parameters
    workspace = arcpy.env.workspace = e1.get()#gdb containing feature classes want to view (r"E:\ProductionTools\Bob\line_t6390\Line_T6390_Outputs\Test2HazardTree.gdb")
    shapeName = e2.get() #shapefile holding names of feature classes in workspace (r"E:\ProductionTools\Bob\Testgdb.gdb\nameHolder")
    mapdoc = e3.get() #map document to view data (r"E:\ProductionTools\Bob\ProductionToolTest.mxd")
    field = e4.get() #field that contains names of feature classes want to view (from ones held in workspace)("Name")

    #Set up map document
    mxd = arcpy.mapping.MapDocument(mapdoc)
    df = arcpy.mapping.ListDataFrames(mxd, "*")[0] #may also want to use (df = mxd.activeDataFrame)
    text.insert(tk.END,"Dataframe Found\n")

    #Feature Count
    fcCount = 1

    #parse through the shapefile holding the BobVfeature class names
    with arcpy.da.SearchCursor(shapeName, field) as cursor:
        for fc in cursor:
            #collect names of feature classes
            featureClassName = " ".join(fc)
            #path to the feature class
            featureClass = "{}\{}".format(workspace, featureClassName)
            #create and add layer from fc
            newLayer = arcpy.mapping.Layer(featureClass)
            arcpy.mapping.AddLayer(df, newLayer, "BOTTOM")
            text.insert(tk.INSERT, "Feature class number {} added to the data frame\n".format(fcCount))
            fcCount += 1

    del cursor

    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()
    text.insert(tk.END, "View Refreshed\n")

    df.zoomToSelectedFeatures()
    text.insert(tk.END, "Zoomed to Layer\n")

    mxd.save()

    del mxd

    text.insert(tk.END, "Feature Classes added to the following map document: {}\n".format(mapdoc))
    text.insert(tk.END, "Program Completed")
    
#GUI
master = tk.Tk()
master.title("Bob V 1.00")

tk.Label(master, text="Welcome to Bob. Your Shapefile/Feature Class showing assistant.", font=("System", 14)).grid(row=0)

tk.Label(master, text="Gdb or Folder containing the Feature Classes you want to view:").grid(row=2)
tk.Label(master, text="Shapefile or Feature Class with a collumn containing the name of your desired feature classes: ").grid(row=3)
tk.Label(master, text="Path to map document you want to view the feature classes on:").grid(row=4)
tk.Label(master, text="Name of the Collumn that lists the feature classes you want to view (must be exact):").grid(row=5)

e1 = tk.Entry(master, width=120)
e2 = tk.Entry(master, width=120)
e3 = tk.Entry(master, width=120)
e4 = tk.Entry(master, width=120)

e1.grid(row=2, column=1)
e2.grid(row=3, column=1)
e3.grid(row=4, column=1)
e4.grid(row=5, column=1)

tk.Button(master, text='Run', command=runThe5KWeCallLife).grid(row=7, column=0, sticky=tk.W, pady=4)
tk.Button(master, text='Clear', command=clearTheField).grid(row=7, column=1, sticky=tk.W, pady=4)

text = tk.Text(master)
text.grid(row=8)
text.insert(tk.INSERT, "Fill Out Parameters Above Then Hit Run Button To Start Program")

master.mainloop()
