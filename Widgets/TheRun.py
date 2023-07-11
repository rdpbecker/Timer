from Widgets import WidgetBase
import http.client
import json
import datetime


class TheRun(WidgetBase.WidgetBase):
    # starttime = datetime.datetime.timestamp() * 1000

    def __init__(self, parent, state, config):
        super().__init__(parent, state, config)
        self.configure(bg="black")

        self.splitWebhook = "dspc6ekj2gjkfp44cjaffhjeue0fbswr.lambda-url.eu-west-1.on.aws"
        self.uploadKey = config["uploadKey"]
        self.headers = {
            "Content-Type": "application/json",
            'Content-Disposition': 'attachment',
            'Accept': "*/*",
        }

    def post_run_status(self):
        connection = http.client.HTTPSConnection(self.splitWebhook)
        http.client.HTTPSConnection.debuglevel = 1

        connection.request('POST', '/', json.dumps(self.jsonify()), self.headers)

        # response = connection.getresponse()
        # print(response.status, response.reason)
        # print(response.headers)

    def clean_time_to_therun_api(self, time):
        return int(1000 * time) if type(time) in [float, int] else None

    def jsonify(self):
        is_reset = self.state.runEnded and self.state.splitnum < self.state.numSplits
        self.starttime = int(datetime.datetime.now().timestamp() * 1000)
        endtime = self.starttime
        runData = []
        for i, name in enumerate(self.state.splitnames):
            runData.append({
                "name": name,
                "splitTime": self.clean_time_to_therun_api(self.state.currentRun.totals[i]) if len(self.state.currentRun.totals) > i and not is_reset else None,
                "pbSplitTime": self.clean_time_to_therun_api(self.state.comparisons[2].totals[i]),
                "bestPossible": self.clean_time_to_therun_api(self.state.comparisons[0].segments[i]),
                "comparisons": [{
                    "name": comparison.totalHeader,
                    "time": self.clean_time_to_therun_api(comparison.totals[i])
                } for comparison in self.state.comparisons]
            })
        return {
          "metadata": {
            "game": self.state.game,
            "category": self.state.category
          },
          "currentTime": self.clean_time_to_therun_api(self.state.totalTime),
          "currentSplitName": self.state.splitnames[self.state.splitnum] if not is_reset else "",
          "currentSplitIndex": self.state.splitnum if not is_reset else -1,
          "currentComparison": self.state.currentComparison.totalHeader,
          "startTime": f"/Date({self.starttime})/",
          "endTime": f"/Date({endtime})/",
          "uploadKey": self.uploadKey,
          "runData": runData
        }

    def onStarted(self):
        self.post_run_status()

    def onSplit(self):
        self.post_run_status()

#     def onPaused(self):
#         pass

#     def onSplitSkipped(self):
#         pass

    def onReset(self):
        self.post_run_status()

#     def onRestart(self):
#         pass
