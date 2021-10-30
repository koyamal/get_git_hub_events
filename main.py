import requests
import datetime

CommonUrl = "https://api.github.com"
Accept = "application/vnd.github.v3+json"


def get_public_events_for_a_user(username):
    url = CommonUrl + "/users/" + username + "/events/public"
    headers = {
        "Accept": Accept
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return data


def count_today_push_events(events):
    today = datetime.datetime.today()
    output = 0
    for event in events:
        if event["type"] == "PushEvent":
            pushDate = to_jst_from_utc(event["created_at"])
            if today.year == pushDate.year and today.month == pushDate.month and today.day == pushDate.day:
                output += 1
            else:
                return output
                break
    return output


def to_jst_from_utc(iso8601):
    d = datetime.datetime.fromisoformat(iso8601.replace("Z", "+00:00"))
    d += datetime.timedelta(hours=9)
    return d


if __name__ == "__main__":
    publicEventsForUser = get_public_events_for_a_user("koyamal")
    numTodayPushEvents = count_today_push_events(publicEventsForUser)

    print(numTodayPushEvents)
