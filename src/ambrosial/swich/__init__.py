from typing import Optional

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.barplot import BarPlot
from ambrosial.swich.calendarplot import CalendarPlot
from ambrosial.swich.ghubmap import GitHubMap
from ambrosial.swich.heatmap import HeatMap
from ambrosial.swich.map import Map
from ambrosial.swich.regression import RegressionPlot
from ambrosial.swich.wordcloud import WordCloud


class SwiggyChart:
    def __init__(self, swan: Optional[SwiggyAnalytics] = None) -> None:
        self.swan = swan
        if self.swan is None:
            self.swan = SwiggyAnalytics()

        self.ghubmap = GitHubMap(self.swan)
        self.calplot = CalendarPlot(self.swan)
        self.wcloud = WordCloud(self.swan)
        self.regplot = RegressionPlot(self.swan)
        self.map = Map(self.swan)
        self.barplot = BarPlot(self.swan)
        self.heatmap = HeatMap(self.swan)

    def __repr__(self) -> str:
        return f"SwiggyChart({self.swan})"
