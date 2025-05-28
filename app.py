from flask import Flask, render_template, request
import requests  
import datetime

app = Flask(__name__)

# Determine zodiac sign from birth date
ZODIAC_DATES = [
    (120, 'capricorn'), (218, 'aquarius'), (320, 'pisces'),
    (420, 'aries'),     (521, 'taurus'),   (621, 'gemini'),
    (722, 'cancer'),    (823, 'leo'),      (923, 'virgo'),
    (1023, 'libra'),    (1122, 'scorpio'), (1222, 'sagittarius'),
    (1231, 'capricorn')
]

def get_zodiac_sign(month: int, day: int):
    mday = month * 100 + day
    for cutoff, sign in ZODIAC_DATES:
        if mday <= cutoff:
            return sign
    return 'capricorn'

# Fetch horoscope from Aztro API
def fetch_horoscope(sign: str, period: str):
    # period: 'today' or 'week'
    url = 'https://aztro.sameerkumar.website'
    params = {'sign': sign, 'day': period}
    response = requests.post(url, params=params)
    data = response.json()
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        dob = request.form.get('dob')  # YYYY-MM-DD
        period = request.form.get('period')

        # Parse date and get zodiac sign
        dt = datetime.datetime.strptime(dob, '%Y-%m-%d')
        sign = get_zodiac_sign(dt.month, dt.day)

        # Fetch horoscope
        hx = fetch_horoscope(sign, period)

        return render_template('result.html', name=name, dob=dob,
                               sign=sign.capitalize(), period=period,
                               horoscope=hx)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
