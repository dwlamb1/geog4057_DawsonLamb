import ee
import pandas as pd
import geopandas as gpd
import arcpy
import os

# ee.Authenticate()  # Uncomment if first time

def proj2(csv_path, raster_path, shapefile_path, project_name):
    # Initialize Google Earth Engine
    ee.Initialize(project=project_name)
    dem = ee.Image('USGS/3DEP/10m')

    # Set ArcPy workspace to folder containing shapefile
    shapefile_folder = os.path.dirname(shapefile_path)
    arcpy.env.workspace = shapefile_folder
    arcpy.ClearWorkspaceCache_management()  # Ensure ArcPy sees new files

    # Read CSV
    table = pd.read_csv(csv_path)

    # Read raster to get CRS
    ra1 = arcpy.Raster(raster_path)
    raster_epsg = ra1.spatialReference.factoryCode

    # Create GeoDataFrame from CSV with raster CRS
    gdf = gpd.GeoDataFrame(
        table,
        geometry=gpd.points_from_xy(table['X'], table['Y']),
        crs=f'EPSG:{raster_epsg}'
    )

    # If shapefile exists, read it; otherwise, save the new one
    if os.path.exists(shapefile_path):
        print("Existing shapefile found. Using it.")
        gdf = gpd.read_file(shapefile_path)
    else:
        print("Shapefile does not exist. Creating a new one.")
        gdf.to_file(shapefile_path)
        arcpy.ClearWorkspaceCache_management()  # Ensure ArcPy sees it

    # Add elevation field if it doesn't exist
    if 'elevation' not in [f.name for f in arcpy.ListFields(shapefile_path)]:
        arcpy.management.AddField(shapefile_path, 'elevation', 'FLOAT')

    # Convert points to WGS84 for GEE
    gdf_wgs = gdf.to_crs(epsg=4326)
    geom_list = [ee.Geometry.Point(xy) for xy in zip(gdf_wgs.geometry.x, gdf_wgs.geometry.y)]
    geom_col = ee.FeatureCollection(geom_list)

    # Sample elevation from DEM
    elev_features = dem.sampleRegions(geom_col).getInfo().get('features')

    # Update shapefile with elevation
    with arcpy.da.UpdateCursor(shapefile_path, ['elevation']) as cursor:
        for i, row in enumerate(cursor):
            row[0] = elev_features[i]['properties']['elevation']
            cursor.updateRow(row)

    print("Elevation values successfully added to shapefile.")

if __name__ == "__main__":
    csv_path = r"C:\Users\dlamb6\Desktop\GISProgrammingProject\boundary.csv"
    raster_path = r"C:\Users\dlamb6\Desktop\GISProgrammingProject\flood_2class.tif"
    shapefile_path = r"C:\Users\dlamb6\Desktop\GISProgrammingProject\boundary_2.shp"
    project_name = "dlamb6-2"

    proj2(csv_path, raster_path, shapefile_path, project_name)


