import requests
import datetime


class MethodBox():
    CommonUrl = "https://api.github.com"
    Accept = "application/vnd.github.v3+json"

    def get_public_events_for_a_user(self, username):
        url = self.CommonUrl + "/users/" + username + "/events/public?per_page=100"
        headers = {
            "Accept": self.Accept
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        return data

    def count_today_push_events(self, events):
        today = datetime.datetime.today()
        output = 0
        for event in events:
            if event["type"] == "PushEvent":
                pushDate = self.to_jst_from_utc(event["created_at"])
                if today.year == pushDate.year and today.month == pushDate.month and today.day == pushDate.day:
                    output += 1
                else:
                    return output
            else:
                eventDate = self.to_jst_from_utc(event["created_at"])
                if today.year != eventDate.year or today.month != eventDate.month and today.day != eventDate.day:
                    return output

        return output

    def to_jst_from_utc(self, iso8601):
        d = datetime.datetime.fromisoformat(iso8601.replace("Z", "+00:00"))
        d += datetime.timedelta(hours=9)
        return d


if __name__ == "__main__":
    countTodayPushEvents = MethodBox()
    publicEventsForUser = countTodayPushEvents.get_public_events_for_a_user("koyamal")
    numTodayPushEvents = countTodayPushEvents.count_today_push_events(publicEventsForUser)

    print(numTodayPushEvents)
