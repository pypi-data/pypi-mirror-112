import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import * as React from 'react';
import { withTheme } from '@emotion/react';
import styled from '@emotion/styled';
import Color from 'color';
import BaseChart from 'app/components/charts/baseChart';
import Legend from 'app/components/charts/components/legend';
import Tooltip from 'app/components/charts/components/tooltip';
import xAxis from 'app/components/charts/components/xAxis';
import barSeries from 'app/components/charts/series/barSeries';
import { ChartContainer, HeaderTitleLegend } from 'app/components/charts/styles';
import LoadingIndicator from 'app/components/loadingIndicator';
import Panel from 'app/components/panels/panel';
import Placeholder from 'app/components/placeholder';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { DataCategory, DataCategoryName } from 'app/types';
import { parsePeriodToHours, statsPeriodToDays } from 'app/utils/dates';
import { formatAbbreviatedNumber } from 'app/utils/formatters';
import commonTheme from 'app/utils/theme';
import { formatUsageWithUnits, GIGABYTE } from '../utils';
import { getTooltipFormatter, getXAxisDates, getXAxisLabelInterval } from './utils';
var COLOR_ERRORS = Color(commonTheme.dataCategory.errors).lighten(0.25).string();
var COLOR_TRANSACTIONS = Color(commonTheme.dataCategory.transactions)
    .lighten(0.35)
    .string();
var COLOR_ATTACHMENTS = Color(commonTheme.dataCategory.attachments)
    .lighten(0.65)
    .string();
var COLOR_DROPPED = commonTheme.red300;
var COLOR_PROJECTED = commonTheme.gray100;
export var CHART_OPTIONS_DATACATEGORY = [
    {
        label: DataCategoryName[DataCategory.ERRORS],
        value: DataCategory.ERRORS,
        disabled: false,
    },
    {
        label: DataCategoryName[DataCategory.TRANSACTIONS],
        value: DataCategory.TRANSACTIONS,
        disabled: false,
    },
    {
        label: DataCategoryName[DataCategory.ATTACHMENTS],
        value: DataCategory.ATTACHMENTS,
        disabled: false,
    },
];
export var ChartDataTransform;
(function (ChartDataTransform) {
    ChartDataTransform["CUMULATIVE"] = "cumulative";
    ChartDataTransform["PERIODIC"] = "periodic";
})(ChartDataTransform || (ChartDataTransform = {}));
export var CHART_OPTIONS_DATA_TRANSFORM = [
    {
        label: t('Cumulative'),
        value: ChartDataTransform.CUMULATIVE,
        disabled: false,
    },
    {
        label: t('Periodic'),
        value: ChartDataTransform.PERIODIC,
        disabled: false,
    },
];
export var SeriesTypes;
(function (SeriesTypes) {
    SeriesTypes["ACCEPTED"] = "Accepted";
    SeriesTypes["DROPPED"] = "Dropped";
    SeriesTypes["PROJECTED"] = "Projected";
})(SeriesTypes || (SeriesTypes = {}));
var UsageChart = /** @class */ (function (_super) {
    __extends(UsageChart, _super);
    function UsageChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            xAxisDates: [],
        };
        return _this;
    }
    /**
     * UsageChart needs to generate the X-Axis dates as props.usageStats may
     * not pass the complete range of X-Axis data points
     *
     * E.g. usageStats.accepted covers day 1-15 of a month, usageStats.projected
     * either covers day 16-30 or may not be available at all.
     */
    UsageChart.getDerivedStateFromProps = function (nextProps, prevState) {
        var usageDateStart = nextProps.usageDateStart, usageDateEnd = nextProps.usageDateEnd, usageDateShowUtc = nextProps.usageDateShowUtc, usageDateInterval = nextProps.usageDateInterval;
        return __assign(__assign({}, prevState), { xAxisDates: getXAxisDates(usageDateStart, usageDateEnd, usageDateShowUtc, usageDateInterval) });
    };
    Object.defineProperty(UsageChart.prototype, "chartColors", {
        get: function () {
            var dataCategory = this.props.dataCategory;
            if (dataCategory === DataCategory.ERRORS) {
                return [COLOR_ERRORS, COLOR_DROPPED, COLOR_PROJECTED];
            }
            if (dataCategory === DataCategory.ATTACHMENTS) {
                return [COLOR_ATTACHMENTS, COLOR_DROPPED, COLOR_PROJECTED];
            }
            return [COLOR_TRANSACTIONS, COLOR_DROPPED, COLOR_PROJECTED];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageChart.prototype, "chartMetadata", {
        get: function () {
            var _a = this.props, usageDateStart = _a.usageDateStart, usageDateEnd = _a.usageDateEnd;
            var _b = this.props, usageDateInterval = _b.usageDateInterval, usageStats = _b.usageStats, dataCategory = _b.dataCategory, dataTransform = _b.dataTransform, handleDataTransformation = _b.handleDataTransformation;
            var xAxisDates = this.state.xAxisDates;
            var selectDataCategory = CHART_OPTIONS_DATACATEGORY.find(function (o) { return o.value === dataCategory; });
            if (!selectDataCategory) {
                throw new Error('Selected item is not supported');
            }
            // Do not assume that handleDataTransformation is a pure function
            var chartData = __assign({}, handleDataTransformation(usageStats, dataTransform));
            Object.keys(chartData).forEach(function (k) {
                var isProjected = k === SeriesTypes.PROJECTED;
                // Map the array and destructure elements to avoid side-effects
                chartData[k] = chartData[k].map(function (stat) {
                    return __assign(__assign({}, stat), { tooltip: { show: false }, itemStyle: { opacity: isProjected ? 0.6 : 1 } });
                });
            });
            // Use hours as common units
            var dataPeriod = statsPeriodToDays(undefined, usageDateStart, usageDateEnd) * 24;
            var barPeriod = parsePeriodToHours(usageDateInterval);
            if (dataPeriod < 0 || barPeriod < 0) {
                throw new Error('UsageChart: Unable to parse data time period');
            }
            var _c = getXAxisLabelInterval(dataPeriod, dataPeriod / barPeriod), xAxisTickInterval = _c.xAxisTickInterval, xAxisLabelInterval = _c.xAxisLabelInterval;
            var label = selectDataCategory.label, value = selectDataCategory.value;
            if (value === DataCategory.ERRORS || value === DataCategory.TRANSACTIONS) {
                return {
                    chartLabel: label,
                    chartData: chartData,
                    xAxisData: xAxisDates,
                    xAxisTickInterval: xAxisTickInterval,
                    xAxisLabelInterval: xAxisLabelInterval,
                    yAxisMinInterval: 100,
                    yAxisFormatter: formatAbbreviatedNumber,
                    tooltipValueFormatter: getTooltipFormatter(dataCategory),
                };
            }
            return {
                chartLabel: label,
                chartData: chartData,
                xAxisData: xAxisDates,
                xAxisTickInterval: xAxisTickInterval,
                xAxisLabelInterval: xAxisLabelInterval,
                yAxisMinInterval: 0.5 * GIGABYTE,
                yAxisFormatter: function (val) {
                    return formatUsageWithUnits(val, DataCategory.ATTACHMENTS, {
                        isAbbreviated: true,
                        useUnitScaling: true,
                    });
                },
                tooltipValueFormatter: getTooltipFormatter(dataCategory),
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageChart.prototype, "chartSeries", {
        get: function () {
            var chartSeries = this.props.chartSeries;
            var chartData = this.chartMetadata.chartData;
            var series = [
                barSeries({
                    name: SeriesTypes.ACCEPTED,
                    data: chartData.accepted,
                    barMinHeight: 1,
                    stack: 'usage',
                    legendHoverLink: false,
                }),
                barSeries({
                    name: SeriesTypes.DROPPED,
                    data: chartData.dropped,
                    stack: 'usage',
                    legendHoverLink: false,
                }),
                barSeries({
                    name: SeriesTypes.PROJECTED,
                    data: chartData.projected,
                    barMinHeight: 1,
                    stack: 'usage',
                    legendHoverLink: false,
                }),
            ];
            // Additional series passed by parent component
            if (chartSeries) {
                series = series.concat(chartSeries);
            }
            return series;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageChart.prototype, "chartLegend", {
        get: function () {
            var chartData = this.chartMetadata.chartData;
            var legend = [
                {
                    name: SeriesTypes.ACCEPTED,
                },
            ];
            if (chartData.dropped.length > 0) {
                legend.push({
                    name: SeriesTypes.DROPPED,
                });
            }
            if (chartData.projected.length > 0) {
                legend.push({
                    name: SeriesTypes.PROJECTED,
                });
            }
            return legend;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageChart.prototype, "chartTooltip", {
        get: function () {
            var chartTooltip = this.props.chartTooltip;
            if (chartTooltip) {
                return chartTooltip;
            }
            var tooltipValueFormatter = this.chartMetadata.tooltipValueFormatter;
            return Tooltip({
                // Trigger to axis prevents tooltip from redrawing when hovering
                // over individual bars
                trigger: 'axis',
                valueFormatter: tooltipValueFormatter,
            });
        },
        enumerable: false,
        configurable: true
    });
    UsageChart.prototype.renderChart = function () {
        var _a = this.props, theme = _a.theme, title = _a.title, isLoading = _a.isLoading, isError = _a.isError, errors = _a.errors;
        if (isLoading) {
            return (<Placeholder height="200px">
          <LoadingIndicator mini/>
        </Placeholder>);
        }
        if (isError) {
            return (<Placeholder height="200px">
          <IconWarning size={theme.fontSizeExtraLarge}/>
          <ErrorMessages>
            {errors &&
                    Object.keys(errors).map(function (k) { var _a; return <span key={k}>{(_a = errors[k]) === null || _a === void 0 ? void 0 : _a.message}</span>; })}
          </ErrorMessages>
        </Placeholder>);
        }
        var _b = this.chartMetadata, xAxisData = _b.xAxisData, xAxisTickInterval = _b.xAxisTickInterval, xAxisLabelInterval = _b.xAxisLabelInterval, yAxisMinInterval = _b.yAxisMinInterval, yAxisFormatter = _b.yAxisFormatter;
        return (<React.Fragment>
        <HeaderTitleLegend>{title || t('Current Usage Period')}</HeaderTitleLegend>
        <BaseChart colors={this.chartColors} grid={{ bottom: '3px', left: '0px', right: '10px', top: '40px' }} xAxis={xAxis({
                show: true,
                type: 'category',
                name: 'Date',
                boundaryGap: true,
                data: xAxisData,
                axisTick: {
                    interval: xAxisTickInterval,
                    alignWithLabel: true,
                },
                axisLabel: {
                    interval: xAxisLabelInterval,
                    formatter: function (label) { return label.slice(0, 6); }, // Limit label to 6 chars
                },
                theme: theme,
            })} yAxis={{
                min: 0,
                minInterval: yAxisMinInterval,
                axisLabel: {
                    formatter: yAxisFormatter,
                    color: theme.chartLabel,
                },
            }} series={this.chartSeries} tooltip={this.chartTooltip} onLegendSelectChanged={function () { }} legend={Legend({
                right: 10,
                top: 5,
                data: this.chartLegend,
                theme: theme,
            })}/>
      </React.Fragment>);
    };
    UsageChart.prototype.render = function () {
        var footer = this.props.footer;
        return (<Panel id="usage-chart">
        <ChartContainer>{this.renderChart()}</ChartContainer>
        {footer}
      </Panel>);
    };
    UsageChart.defaultProps = {
        usageDateShowUtc: true,
        usageDateInterval: '1d',
        handleDataTransformation: function (stats, transform) {
            var chartData = {
                accepted: [],
                dropped: [],
                projected: [],
            };
            var isCumulative = transform === ChartDataTransform.CUMULATIVE;
            Object.keys(stats).forEach(function (k) {
                var count = 0;
                chartData[k] = stats[k].map(function (stat) {
                    var _a = __read(stat.value, 2), x = _a[0], y = _a[1];
                    count = isCumulative ? count + y : y;
                    return __assign(__assign({}, stat), { value: [x, count] });
                });
            });
            return chartData;
        },
    };
    return UsageChart;
}(React.Component));
export { UsageChart };
export default withTheme(UsageChart);
var ErrorMessages = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n\n  margin-top: ", ";\n  font-size: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n\n  margin-top: ", ";\n  font-size: ", ";\n"])), space(1), function (p) { return p.theme.fontSizeSmall; });
var templateObject_1;
//# sourceMappingURL=index.jsx.map