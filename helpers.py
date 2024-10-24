import requests
import urllib
import uuid

from flask import redirect, render_template, request, session
from functools import wraps

def apology(message, code=400):
    def escape(s):

        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(number):

    # Prepare API request
    number = int(number)

    #ENter API access key
    api_key ="f14bd99ff1b6659e6bbdb7adfad474b4"


    # NumVerify API numbers
    url = (
        f"https://apilayer.net/api/validate?access_key={api_key}&number={urllib.parse.quote_plus(str(number))}"
    )

    # Query API
    try:
        response = requests.get(
            url,
            cookies={"session": str(uuid.uuid4())},
            headers={"Accept": "*/*", "User-Agent": request.headers.get("User-Agent")},
        )
        response.raise_for_status()

        # Process the response
        data = response.json()
        return data if data.get("valid") else None

    except (KeyError, IndexError, requests.RequestException, ValueError) as e:
        print(f"Error: {e}")
        return None


