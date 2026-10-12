import os
from dotenv import load_dotenv
import tidalapi
from datetime import date, timedelta
import jinja2
from tidalapi import Mix


load_dotenv()

token_type = os.getenv("TOKEN_TYPE")
access_token = os.getenv("ACCESS_TOKEN")
refresh_token = os.getenv("REFRESH_TOKEN")
expiry_time = os.getenv("EXPIRY_TIME")

session = tidalapi.Session()
session.load_oauth_session(token_type, access_token,
                           refresh_token, expiry_time)

# home = session.home()

page_path = "pages/HISTORY_MIXES/view-all"

response = session.request.request(
    "GET",
    f"https://api.tidal.com/v1/{page_path}",
    params={
        "countryCode": session.country_code,
        "deviceType": "BROWSER"
    }
)

if response.status_code == 200:
    data = response.json()
    data = data['rows'][0]['modules'][0]['pagedList']['items']


prev = date.today().replace(day=1) - timedelta(days=1)
year = str(date.today().year - 1)
month = prev.strftime('%B %Y')

# for category in home.categories:
#    if category.title == "Your listening history":
for item in data:
    # print(item)
    if item['title'] == year:
        print(f'Found: {item['title']}')
        last_year = Mix(session, mix_id=item['id'])
        last_year_thumbnail_url = last_year.image()
        tracks = last_year._items
        last_year_tracks = []
        for i in range(0, 5):
            last_year_tracks.append(tracks[i]._get(tracks[i].id))
    elif item['title'] == month:
        print(f'Found: {item['title']}')
        last_month = Mix(session, mix_id=item['id'])
        last_month_thumbnail_url = last_month.image()
        tracks = last_month._items
        last_month_tracks = []
        for i in range(0, 5):
            last_month_tracks.append(tracks[i]._get(tracks[i].id))


environment = jinja2.Environment(loader=jinja2.FileSystemLoader("./"))
output_file = "README.md"
readme_template = environment.get_template("template.md")
context = {
    "last_month_tracks": last_month_tracks,
    "last_year_tracks": last_year_tracks,
    "last_month_img": last_month_thumbnail_url,
    "last_year_img": last_year_thumbnail_url
}
with open(output_file, mode="w") as output:
    output.write(readme_template.render(context))
