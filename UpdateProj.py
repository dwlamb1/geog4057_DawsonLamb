# -*- coding: utf-8 -*-
import arcpy
import json
import os

def jason2shape(json_file, workspace, fcname, wkid):
    """Convert a JSON file with WKT geometries to a shapefile."""

    # Ensure shapefile name ends with .shp
    if not fcname.lower().endswith(".shp"):
        fcname += ".shp"
    fc_fullpath = os.path.join(workspace, fcname)

    # Load JSON
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Delete shapefile if it exists
    if arcpy.Exists(fc_fullpath):
        arcpy.management.Delete(fc_fullpath)

    # Create feature class with spatial reference
    sr = arcpy.SpatialReference(wkid)
    arcpy.management.CreateFeatureclass(
        out_path=workspace,
        out_name=fcname,
        geometry_type='POLYGON',
        spatial_reference=sr
    )

    # Convert WKT geometries
    polygons = []
    for row in data['data']:
        geom_wkt = row[8]  # assuming geometry is at index 8
        polygons.append(arcpy.FromWKT(geom_wkt) if geom_wkt else None)

    # Prepare fields
    fields = data['meta']['view']['columns']
    field_types = ['TEXT','TEXT','LONG','LONG','TEXT','LONG','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT']
    field_names = []
    for i, field in enumerate(fields):
        name = field['name']
        if name == 'the_geom':
            continue
        if name.lower() == 'id':
            name = f'id_{i}'
        name = name[:10].replace(" ", "_").replace(".", "_")
        field_names.append(name)

    # Add fields to shapefile
    for i, fname in enumerate(field_names):
        arcpy.management.AddField(fc_fullpath, fname, field_types[i])

    # Add SHAPE@ token for geometry
    field_names.append('SHAPE@')

    # Insert rows
    with arcpy.da.InsertCursor(fc_fullpath, field_names) as cursor:
        for idx, row in enumerate(data['data']):
            values = []
            for i, val in enumerate(row):
                if i == 8:  # skip geometry
                    continue
                values.append("" if val is None else val)
            values.append(polygons[idx])
            cursor.insertRow(values)

    print(f"Shapefile created successfully: {fc_fullpath}")


def main():
    # User parameters
    workspace = r"C:\Users\dlamb6\Desktop\Project1_GIS\ProjFolder"
    json_file = os.path.join(workspace, "no_tax.json")
    fcname = "no_tax"
    wkid = 4326  # WGS84

    # Call function
    jason2shape(json_file, workspace, fcname, wkid)


if __name__ == "__main__":
    main()
    print("Shapefile creation process completed.")

