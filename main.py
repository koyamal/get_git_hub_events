import requests
import datetime


class MethodBox:
    def __init__(self, username):
        self.username = username

    CommonUrl = "https://api.github.com"
    Accept = "application/vnd.github.v3+json"

    def get_public_events_for_a_user(self):
        url = self.CommonUrl + "/users/" + self.username + "/events/public?per_page=100"
        headers = {
            "Accept": self.Accept
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        #print(data)

        return data

    def to_jst_from_utc(self, iso8601):
        d = datetime.datetime.fromisoformat(iso8601.replace("Z", "+00:00"))
        d += datetime.timedelta(hours=9)
        return d

    def count_today_push_events(self):
        events = self.get_public_events_for_a_user()
        today = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
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

    def make_output_count_today_push_events(self):
        num = self.count_today_push_events()
        output = ""
        if num == 0:
            output = "本日はまだギットハブに、コードがコミットされていません"
        else:
            output = "本日は" + str(num) + "件、コミットされています"
        return output


if __name__ == "__main__":
    method = MethodBox("koyamal")
    speak_output = method.make_output_count_today_push_events()

    print(speak_output)
