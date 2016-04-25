# conda execute
# channels:
#  - openhydrology
#  - conda-forge
# env:
#  - python >=3
#  - floodestimation
#  - pyproj >=1.9.5
#  - jinja2
# run_with: python

from floodestimation.entities import Catchment, Point
from floodestimation import db
from floodestimation import loaders
import pyproj
from jinja2 import Environment, FileSystemLoader


# Coordinate systems
COORDS = {
    # OSGB_1936_To_WGS_1984_Petroleum transformation
    'gb': pyproj.Proj('+proj=tmerc +lat_0=49 +lon_0=-2 +k=0.9996012717 +x_0=400000 +y_0=-100000 +ellps=airy ' +
                      '+towgs84=446.448000,-125.157000,542.060000,0.150000,0.247000,0.842000,-20.489000 ' +
                      '+units=m +no_defs'),
    # TM75_To_WGS_1984_2 transformation
    'ni': pyproj.Proj('+proj=tmerc +lat_0=53.5 +lon_0=-8 +k=1.000035 +x_0=200000 +y_0=250000 +ellps=mod_airy ' +
                      '+towgs84=482.530000,-130.596000,564.557000,-1.042000,-0.214000,-0.631000,8.150000 ' +
                      '+units=m +no_defs'),
    'wgs84': pyproj.Proj(init='epsg:4326')
}


def build_all_stations():
    session = db.Session()

    # Load catchments
    db.empty_db_tables()
    loaders.folder_to_db('./data', session, autocommit=True, incl_pot=False)
    catchments = session.query(Catchment).order_by(Catchment.id).all()

    # Add WGS84 transformed points
    for catchment in catchments:
        lon, lat = pyproj.transform(COORDS[catchment.country], COORDS['wgs84'],
                                    catchment.descriptors.ihdtm_ngr.x, catchment.descriptors.ihdtm_ngr.y)
        catchment.point_wgs84 = Point(lon, lat)

    # Put through jinja template
    env = Environment(loader=FileSystemLoader('./json'))
    template = env.get_template('stations.txt')
    content = template.render(catchments=catchments)
    with open('./json/updated_stations.geojson', 'w', encoding='utf-8') as f:
        f.write(content)

    session.close()


if __name__ == '__main__':
    build_all_stations()
