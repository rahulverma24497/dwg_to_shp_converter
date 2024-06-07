import tkinter as tk
from tkinter import filedialog, messagebox
import os
import geopandas as gpd
from shapely.geometry import Polygon, LineString, MultiLineString
from shapely.ops import linemerge
from ezdxf.addons import odafc

def convert_dwg_to_shp(input_location, output_location):

    #Check if input and output locations are not empty
    if not input_location:
        messagebox.showerror("Error", "Please specify the input file location")
        return

    if not output_location:
        messagebox.showerror("Error", "Please specify the output location")
        return

    try:
        # Read .dwg file
        dwg = odafc.readfile(input_location)
        msp = dwg.modelspace()

        polygons = []
        lines = []

        # Extract lines and polygons from dwg file
        for entity in msp:
            if entity.dxftype() == 'LINE':
                points = [entity.dxf.start, entity.dxf.end]
                lines.append(LineString(points))
            elif entity.dxftype() == 'LWPOLYLINE':
                points = entity.get_points('xy')
                if points[0] == points[-1]:
                    polygons.append(Polygon(points))
                else:
                    lines.append(LineString(points))
            elif entity.dxftype() == 'POLYLINE':
                points = [point[:2] for point in entity.points()]
                if points[0] == points[-1]:
                    polygons.append(Polygon(points))
                else:
                    lines.append(LineString(points))

        # Merge broken lines
        merged_lines = []
        merged = linemerge(lines)
        if isinstance(merged, LineString):
            merged_lines.append(merged)
        elif isinstance(merged, MultiLineString):
            merged_lines = list(merged.geoms)
        else:
            merged_lines = []

        # Close open polygons
        closed_polygons = []
        for poly in polygons:
            if not poly.is_valid or not poly.exterior.is_closed:
                closed_poly = Polygon(poly.exterior.coords)
                closed_polygons.append(closed_poly)
            else:
                closed_polygons.append(poly)

        # Combine merged lines and closed polygons
        combined_geometries = merged_lines + closed_polygons

        # Create GeoDataFrame with combined geometry
        combined_gdf = gpd.GeoDataFrame(geometry=combined_geometries)

        # Provide SHP file path
        shp_file_path = os.path.join(output_location, os.path.splitext(os.path.basename(input_location))[0] + ".shp")

        # Save to a Shapefile
        combined_gdf.to_file(shp_file_path, driver='ESRI Shapefile')

        # Show success message
        messagebox.showinfo("DWG Conversion Complete", "SHP file is available at specified location")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


#Browse input file
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("DWG files", "*.dwg")])
    if file_path:
        input_label["text"] = file_path

#Browse output file
def browse_output_location():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_label["text"] = folder_path

# GUI setup
window = tk.Tk()
window.title("DWG to SHP Converter")
window.geometry("500x250+500+200")

label = tk.Label(window, text="Select a DWG file to convert:")
label.pack()

input_label = tk.Label(window, text="")
input_label.pack()

browse_button = tk.Button(window, text="Browse", command=browse_file)
browse_button.pack(pady=10)


out_label = tk.Label(window, text="Output SHP file location:")
out_label.pack()

output_label = tk.Label(window, text="")
output_label.pack()

browse_output_button = tk.Button(window, text="Browse", command=browse_output_location)
browse_output_button.pack(pady=10)

convert_button = tk.Button(window, text="Convert", command=lambda: convert_dwg_to_shp(input_label.cget("text"), output_label.cget("text")))
convert_button.pack()

window.mainloop()
