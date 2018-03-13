from flask import Flask, render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from model import TT_Location, TT_Report
from sqlalchemy.sql import join
import os

app = Flask(__name__, template_folder="./templates", static_folder='img', static_url_path='/img')
app.config['GOOGLEMAPS_KEY'] = os.environ["GOOGLEMAPS_KEY"]

GoogleMaps(app)

columns = [TT_Report.img_file, TT_Report.comment, TT_Location.location, TT_Location.long, TT_Location.lat]

q = join(TT_Report, TT_Location, TT_Report.location_id == TT_Location.id).select()
q = q.with_only_columns(columns)

res_arr = []
for row in q.execute():
    arr = {}
    arr['infobox'] = "<img src='img/{0}' width='50px'></img><br><b>Comment:</b> {1}".format(row["img_file"], row["comment"])
    arr['lat'] = row["lat"]
    arr['lng'] = row["long"]
    # arr['icon'] = './img/{0}'.format(row['img_file'])
    res_arr.append(arr)

@app.route("/")
def mapview():
    # creating a map in the view
    map = Map(
        zoom=6,
        identifier="map",
        lat=35.637004,
        lng=139.446307,
        markers=res_arr,
        style="height:700px;width:1200px"
    )
    return render_template('app.html', map=map)


if __name__ == "__main__":
    app.run(debug=True)