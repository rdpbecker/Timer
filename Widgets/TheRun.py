from Widgets import WidgetBase
import datetime
import requests


class TheRun(WidgetBase.WidgetBase):
    # starttime = datetime.datetime.timestamp() * 1000

    def __init__(self, parent, state, config):
        super().__init__(parent, state, config)
        self.configure(bg="black")

        self.splitWebhook = "https://dspc6ekj2gjkfp44cjaffhjeue0fbswr.lambda-url.eu-west-1.on.aws/"
        self.uploadKey = config["uploadKey"]
        self.wasJustResumed = False
        self.headers = {
            "Content-Type": "application/json",
            'Content-Disposition': 'attachment',
            'Accept': "*/*",
        }

    def post_run_status(self):
        requests.post(self.splitWebhook, json=self.jsonify(), headers=self.headers)

    def clean_time_to_therun_api(self, time):
        return int(1000 * time) if type(time) in [float, int] else None

    def jsonify(self):
        is_reset = self.state.runEnded and self.state.splitnum < self.state.numSplits
        endtime = int(datetime.datetime.now().timestamp() * 1000)
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
            "isPaused": self.state.paused,
            "wasJustResumed": self.wasJustResumed,
            "uploadKey": self.uploadKey,
            "runData": runData
        }

    def onStarted(self):
        self.starttime = int(datetime.datetime.now().timestamp() * 1000)
        self.post_run_status()

    def onSplit(self):
        self.post_run_status()
        self.wasJustResumed = False

    def onPaused(self):
        if not self.state.paused:
            self.wasJustResumed = True
        self.post_run_status()

#     def onSplitSkipped(self):
#         pass

    def onReset(self):
        self.post_run_status()

#     def onRestart(self):
#         pass
