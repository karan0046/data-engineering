import os, fiona, rasterio as rio, geopandas as gpd
import math
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import numpy as np


list_of_tuples = []



def create_tuple(src, col):

    df = gpd.read_file(src)
    df = df.set_crs("EPSG:4326")

    dic = {}
    dic.__setitem__(1.0, [])
    dic.__setitem__(2.0, [])
    dic.__setitem__(3.0, [])

    for index, row in df.iterrows():
        if math.isnan(df[col][index]) or df[col][index] == 0:
            continue
        dic[df[col][index]].append(index)

    cnt = 0
    res = []
    for i in dic[1.0]:
        for j in dic[2.0]:
            for k in dic[3.0]:
                res.append([df['geometry'][i], df['geometry'][j], df['geometry'][k]])
                cnt += 1
                if cnt == 5:
                    return res

    return res

    pass

fig, ax = plt.subplots()

def plot_polygons(res):
    col_pattern = {
        1 : 'b',
        2 : 'y',
        3 : 'r'
    }
    for row in res:
        index = 0
        for poly in row:
            index += 1
            poly = Polygon(poly)
            x, y = poly.exterior.xy
            x = np.array(x)
            y = np.array(y)
            ax.fill(x, y, col_pattern[index])
            ax.plot(np.append(x, x[0]), np.append(y, y[0]), 'k-')
            #plt.show()
            print(poly.bounds)

    plt.show()
    pass


if __name__ == "__main__":
    src = './shp/WBEP_woodlands_condition.shp'
    res = create_tuple(src, 'C1')
    plot_polygons(res)

    pass