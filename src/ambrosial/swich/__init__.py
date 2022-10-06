from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.calendarplot import CalendarPlot
from ambrosial.swich.heatmap import HeatMap
from ambrosial.swich.regression import RegressionPlot
from ambrosial.swich.wordcloud import WordCloud


class SwiggyChart:
    def __init__(self, swan: SwiggyAnalytics = None) -> None:
        self.swan = swan
        if self.swan is None:
            self.swan = SwiggyAnalytics()
        self.heatmap = HeatMap(self.swan)
        self.calplot = CalendarPlot(self.swan)
        self.wcloud = WordCloud(self.swan)
        self.regplot = RegressionPlot(self.swan)

    def __repr__(self) -> str:
        return f"SwiggyChart({self.swan})"
