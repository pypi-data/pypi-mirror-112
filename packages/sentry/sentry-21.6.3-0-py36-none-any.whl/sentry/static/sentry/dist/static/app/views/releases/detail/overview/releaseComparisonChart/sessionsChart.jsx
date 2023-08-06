import { __extends, __read, __spreadArray } from "tslib";
import * as React from 'react';
import { withTheme } from '@emotion/react';
import AreaChart from 'app/components/charts/areaChart';
import StackedAreaChart from 'app/components/charts/stackedAreaChart';
import { HeaderTitleLegend } from 'app/components/charts/styles';
import QuestionTooltip from 'app/components/questionTooltip';
import { ReleaseComparisonChartType } from 'app/types';
import { defined } from 'app/utils';
import { displayCrashFreePercent } from 'app/views/releases/utils';
import { releaseComparisonChartHelp, releaseComparisonChartLabels } from '../../utils';
var SessionsChart = /** @class */ (function (_super) {
    __extends(SessionsChart, _super);
    function SessionsChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.formatTooltipValue = function (value) {
            var chartType = _this.props.chartType;
            if (value === null) {
                return '\u2015';
            }
            switch (chartType) {
                case ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
                case ReleaseComparisonChartType.CRASH_FREE_USERS:
                    return defined(value) ? value + "%" : '\u2015';
                case ReleaseComparisonChartType.SESSION_COUNT:
                case ReleaseComparisonChartType.USER_COUNT:
                default:
                    return typeof value === 'number' ? value.toLocaleString() : value;
            }
        };
        return _this;
    }
    SessionsChart.prototype.configureYAxis = function () {
        var _a = this.props, theme = _a.theme, chartType = _a.chartType;
        switch (chartType) {
            case ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
            case ReleaseComparisonChartType.CRASH_FREE_USERS:
                return {
                    max: 100,
                    scale: true,
                    axisLabel: {
                        formatter: function (value) { return displayCrashFreePercent(value); },
                        color: theme.chartLabel,
                    },
                };
            case ReleaseComparisonChartType.SESSION_COUNT:
            case ReleaseComparisonChartType.USER_COUNT:
            default:
                return undefined;
        }
    };
    SessionsChart.prototype.getChart = function () {
        var chartType = this.props.chartType;
        switch (chartType) {
            case ReleaseComparisonChartType.CRASH_FREE_SESSIONS:
            case ReleaseComparisonChartType.CRASH_FREE_USERS:
            default:
                return AreaChart;
            case ReleaseComparisonChartType.SESSION_COUNT:
            case ReleaseComparisonChartType.USER_COUNT:
                return StackedAreaChart;
        }
    };
    SessionsChart.prototype.render = function () {
        var _a = this.props, series = _a.series, previousSeries = _a.previousSeries, chartType = _a.chartType;
        var Chart = this.getChart();
        var legend = {
            right: 10,
            top: 0,
            // do not show adoption markers in the legend
            data: __spreadArray(__spreadArray([], __read(series)), __read(previousSeries)).filter(function (s) { return !s.markLine; })
                .map(function (s) { return s.seriesName; }),
        };
        return (<React.Fragment>
        <HeaderTitleLegend>
          {releaseComparisonChartLabels[chartType]}
          {releaseComparisonChartHelp[chartType] && (<QuestionTooltip size="sm" position="top" title={releaseComparisonChartHelp[chartType]}/>)}
        </HeaderTitleLegend>

        <Chart legend={legend} series={series} previousPeriod={previousSeries} isGroupedByDate showTimeInTooltip grid={{
                left: '10px',
                right: '10px',
                top: '40px',
                bottom: '0px',
            }} yAxis={this.configureYAxis()} tooltip={{ valueFormatter: this.formatTooltipValue }} transformSinglePointToBar/>
      </React.Fragment>);
    };
    return SessionsChart;
}(React.Component));
export default withTheme(SessionsChart);
//# sourceMappingURL=sessionsChart.jsx.map