import { __extends, __makeTemplateObject, __read, __rest, __spreadArray } from "tslib";
import * as React from 'react';
import { withRouter } from 'react-router';
import styled from '@emotion/styled';
import color from 'color';
import moment from 'moment';
import momentTimezone from 'moment-timezone';
import Feature from 'app/components/acl/feature';
import Button from 'app/components/button';
import ChartZoom from 'app/components/charts/chartZoom';
import Graphic from 'app/components/charts/components/graphic';
import MarkArea from 'app/components/charts/components/markArea';
import MarkLine from 'app/components/charts/components/markLine';
import EventsRequest from 'app/components/charts/eventsRequest';
import LineChart from 'app/components/charts/lineChart';
import { SectionHeading } from 'app/components/charts/styles';
import { parseStatsPeriod, } from 'app/components/organizations/globalSelectionHeader/getParams';
import { Panel, PanelBody, PanelFooter } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import { IconCheckmark, IconFire, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import space from 'app/styles/space';
import { getUtcDateString } from 'app/utils/dates';
import theme from 'app/utils/theme';
import { alertDetailsLink } from 'app/views/alerts/details';
import { makeDefaultCta } from 'app/views/alerts/incidentRules/incidentRulePresets';
import { AlertWizardAlertNames } from 'app/views/alerts/wizard/options';
import { getAlertTypeFromAggregateDataset } from 'app/views/alerts/wizard/utils';
import { IncidentActivityType, IncidentStatus } from '../../types';
var X_AXIS_BOUNDARY_GAP = 20;
var VERTICAL_PADDING = 22;
function formatTooltipDate(date, format) {
    var timezone = ConfigStore.get('user').options.timezone;
    return momentTimezone.tz(date, timezone).format(format);
}
function createThresholdSeries(lineColor, threshold) {
    return {
        seriesName: 'Threshold Line',
        type: 'line',
        markLine: MarkLine({
            silent: true,
            lineStyle: { color: lineColor, type: 'dashed', width: 1 },
            data: [{ yAxis: threshold }],
            label: {
                show: false,
            },
        }),
        data: [],
    };
}
function createStatusAreaSeries(lineColor, startTime, endTime) {
    return {
        seriesName: 'Status Area',
        type: 'line',
        markLine: MarkLine({
            silent: true,
            lineStyle: { color: lineColor, type: 'solid', width: 4 },
            data: [[{ coord: [startTime, 0] }, { coord: [endTime, 0] }]],
        }),
        data: [],
    };
}
function createIncidentSeries(router, organization, lineColor, incidentTimestamp, incident, dataPoint, seriesName) {
    var series = {
        seriesName: 'Incident Line',
        type: 'line',
        markLine: MarkLine({
            silent: false,
            lineStyle: { color: lineColor, type: 'solid' },
            data: [
                {
                    xAxis: incidentTimestamp,
                    onClick: function () {
                        router.push({
                            pathname: alertDetailsLink(organization, incident),
                            query: { alert: incident.identifier },
                        });
                    },
                },
            ],
            label: {
                show: incident.identifier,
                position: 'insideEndBottom',
                formatter: incident.identifier,
                color: lineColor,
                fontSize: 10,
                fontFamily: 'Rubik',
            },
        }),
        data: [],
    };
    // tooltip conflicts with MarkLine types
    series.markLine.tooltip = {
        trigger: 'item',
        alwaysShowContent: true,
        formatter: function (_a) {
            var _b;
            var value = _a.value, marker = _a.marker;
            var time = formatTooltipDate(moment(value), 'MMM D, YYYY LT');
            return [
                "<div class=\"tooltip-series\"><div>",
                "<span class=\"tooltip-label\">" + marker + " <strong>" + t('Alert') + " #" + incident.identifier + "</strong></span>" + seriesName + " " + ((_b = dataPoint === null || dataPoint === void 0 ? void 0 : dataPoint.value) === null || _b === void 0 ? void 0 : _b.toLocaleString()),
                "</div></div>",
                "<div class=\"tooltip-date\">" + time + "</div>",
                "<div class=\"tooltip-arrow\"></div>",
            ].join('');
        },
    };
    return series;
}
var MetricChart = /** @class */ (function (_super) {
    __extends(MetricChart, _super);
    function MetricChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            width: -1,
            height: -1,
        };
        _this.ref = null;
        /**
         * Syncs component state with the chart's width/heights
         */
        _this.updateDimensions = function () {
            var _a, _b;
            var chartRef = (_b = (_a = _this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (!chartRef) {
                return;
            }
            var width = chartRef.getWidth();
            var height = chartRef.getHeight();
            if (width !== _this.state.width || height !== _this.state.height) {
                _this.setState({
                    width: width,
                    height: height,
                });
            }
        };
        _this.handleRef = function (ref) {
            if (ref && !_this.ref) {
                _this.ref = ref;
                _this.updateDimensions();
            }
            if (!ref) {
                _this.ref = null;
            }
        };
        _this.getRuleChangeThresholdElements = function (data) {
            var _a = _this.state, height = _a.height, width = _a.width;
            var dateModified = (_this.props.rule || {}).dateModified;
            if (!data.length || !data[0].data.length || !dateModified) {
                return [];
            }
            var seriesData = data[0].data;
            var seriesStart = seriesData[0].name;
            var seriesEnd = seriesData[seriesData.length - 1].name;
            var ruleChanged = moment(dateModified).valueOf();
            if (ruleChanged < seriesStart) {
                return [];
            }
            var chartWidth = width - X_AXIS_BOUNDARY_GAP;
            var position = X_AXIS_BOUNDARY_GAP +
                Math.round((chartWidth * (ruleChanged - seriesStart)) / (seriesEnd - seriesStart));
            return [
                {
                    type: 'line',
                    draggable: false,
                    position: [position, 0],
                    shape: { y1: 0, y2: height - VERTICAL_PADDING, x1: 1, x2: 1 },
                    style: {
                        stroke: theme.gray200,
                    },
                },
                {
                    type: 'rect',
                    draggable: false,
                    position: [X_AXIS_BOUNDARY_GAP, 0],
                    shape: {
                        // +1 makes the gray area go midway onto the dashed line above
                        width: position - X_AXIS_BOUNDARY_GAP + 1,
                        height: height - VERTICAL_PADDING,
                    },
                    style: {
                        fill: color(theme.gray100).alpha(0.42).rgb().string(),
                    },
                },
            ];
        };
        return _this;
    }
    MetricChart.prototype.renderChartActions = function (totalDuration, criticalDuration, warningDuration) {
        var _a = this.props, rule = _a.rule, orgId = _a.orgId, projects = _a.projects, timePeriod = _a.timePeriod, query = _a.query;
        var ctaOpts = {
            orgSlug: orgId,
            projects: projects,
            rule: rule,
            eventType: query,
            start: timePeriod.start,
            end: timePeriod.end,
        };
        var _b = makeDefaultCta(ctaOpts), buttonText = _b.buttonText, props = __rest(_b, ["buttonText"]);
        var resolvedPercent = ((100 * Math.max(totalDuration - criticalDuration - warningDuration, 0)) /
            totalDuration).toFixed(2);
        var criticalPercent = (100 * Math.min(criticalDuration / totalDuration, 1)).toFixed(2);
        var warningPercent = (100 * Math.min(warningDuration / totalDuration, 1)).toFixed(2);
        return (<ChartActions>
        <ChartSummary>
          <SummaryText>{t('SUMMARY')}</SummaryText>
          <SummaryStats>
            <StatItem>
              <IconCheckmark color="green300" isCircled/>
              <StatCount>{resolvedPercent}%</StatCount>
            </StatItem>
            <StatItem>
              <IconWarning color="yellow300"/>
              <StatCount>{warningPercent}%</StatCount>
            </StatItem>
            <StatItem>
              <IconFire color="red300"/>
              <StatCount>{criticalPercent}%</StatCount>
            </StatItem>
          </SummaryStats>
        </ChartSummary>
        <Feature features={['discover-basic']}>
          <Button size="small" {...props}>
            {buttonText}
          </Button>
        </Feature>
      </ChartActions>);
    };
    MetricChart.prototype.renderChart = function (data, series, areaSeries, maxThresholdValue, maxSeriesValue) {
        var _this = this;
        var _a = this.props, router = _a.router, interval = _a.interval, handleZoom = _a.handleZoom, _b = _a.timePeriod, start = _b.start, end = _b.end;
        var _c = this.props.rule || {}, dateModified = _c.dateModified, timeWindow = _c.timeWindow;
        return (<ChartZoom router={router} start={start} end={end} onZoom={function (zoomArgs) { return handleZoom(zoomArgs.start, zoomArgs.end); }}>
        {function (zoomRenderProps) { return (<LineChart {...zoomRenderProps} isGroupedByDate showTimeInTooltip forwardedRef={_this.handleRef} grid={{
                    left: 0,
                    right: space(2),
                    top: space(2),
                    bottom: 0,
                }} yAxis={maxThresholdValue > maxSeriesValue ? { max: maxThresholdValue } : undefined} series={__spreadArray(__spreadArray([], __read(series)), __read(areaSeries))} graphic={Graphic({
                    elements: _this.getRuleChangeThresholdElements(data),
                })} tooltip={{
                    formatter: function (seriesParams) {
                        var _a;
                        // seriesParams can be object instead of array
                        var pointSeries = Array.isArray(seriesParams)
                            ? seriesParams
                            : [seriesParams];
                        var _b = pointSeries[0], marker = _b.marker, pointData = _b.data, seriesName = _b.seriesName;
                        var _c = __read(pointData, 2), pointX = _c[0], pointY = _c[1];
                        var isModified = dateModified && pointX <= new Date(dateModified).getTime();
                        var startTime = formatTooltipDate(moment(pointX), 'MMM D LT');
                        var _d = (_a = parseStatsPeriod(interval)) !== null && _a !== void 0 ? _a : {
                            periodLength: 'm',
                            period: "" + timeWindow,
                        }, period = _d.period, periodLength = _d.periodLength;
                        var endTime = formatTooltipDate(moment(pointX).add(parseInt(period, 10), periodLength), 'MMM D LT');
                        var title = isModified
                            ? "<strong>" + t('Alert Rule Modified') + "</strong>"
                            : marker + " <strong>" + seriesName + "</strong>";
                        var value = isModified
                            ? seriesName + " " + pointY.toLocaleString()
                            : pointY.toLocaleString();
                        return [
                            "<div class=\"tooltip-series\"><div>",
                            "<span class=\"tooltip-label\">" + title + "</span>" + value,
                            "</div></div>",
                            "<div class=\"tooltip-date\">" + startTime + " &mdash; " + endTime + "</div>",
                            "<div class=\"tooltip-arrow\"></div>",
                        ].join('');
                    },
                }} onFinished={function () {
                    // We want to do this whenever the chart finishes re-rendering so that we can update the dimensions of
                    // any graphics related to the triggers (e.g. the threshold areas + boundaries)
                    _this.updateDimensions();
                }}/>); }}
      </ChartZoom>);
    };
    MetricChart.prototype.renderEmpty = function () {
        return (<ChartPanel>
        <PanelBody withPadding>
          <Placeholder height="200px"/>
        </PanelBody>
      </ChartPanel>);
    };
    MetricChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, router = _a.router, rule = _a.rule, organization = _a.organization, timePeriod = _a.timePeriod, selectedIncident = _a.selectedIncident, projects = _a.projects, interval = _a.interval, filter = _a.filter, query = _a.query, incidents = _a.incidents;
        var criticalTrigger = rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTrigger = rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'warning';
        });
        // If the chart duration isn't as long as the rollup duration the events-stats
        // endpoint will return an invalid timeseriesData data set
        var viableStartDate = getUtcDateString(moment.min(moment.utc(timePeriod.start), moment.utc(timePeriod.end).subtract(rule.timeWindow, 'minutes')));
        var viableEndDate = getUtcDateString(moment.utc(timePeriod.end).add(rule.timeWindow, 'minutes'));
        return (<EventsRequest api={api} organization={organization} query={query} environment={rule.environment ? [rule.environment] : undefined} project={projects
                .filter(function (p) { return p && p.slug; })
                .map(function (project) { return Number(project.id); })} interval={interval} start={viableStartDate} end={viableEndDate} yAxis={rule.aggregate} includePrevious={false} currentSeriesName={rule.aggregate} partial={false}>
        {function (_a) {
                var loading = _a.loading, timeseriesData = _a.timeseriesData;
                if (loading || !timeseriesData) {
                    return _this.renderEmpty();
                }
                var series = __spreadArray([], __read(timeseriesData));
                var areaSeries = [];
                // Ensure series data appears above incident lines
                series[0].z = 100;
                var dataArr = timeseriesData[0].data;
                var maxSeriesValue = dataArr.reduce(function (currMax, coord) { return Math.max(currMax, coord.value); }, 0);
                var firstPoint = Number(dataArr[0].name);
                var lastPoint = dataArr[dataArr.length - 1].name;
                var totalDuration = lastPoint - firstPoint;
                var criticalDuration = 0;
                var warningDuration = 0;
                series.push(createStatusAreaSeries(theme.green300, firstPoint, lastPoint));
                if (incidents) {
                    // select incidents that fall within the graph range
                    var periodStart_1 = moment.utc(firstPoint);
                    incidents
                        .filter(function (incident) {
                        return !incident.dateClosed || moment(incident.dateClosed).isAfter(periodStart_1);
                    })
                        .forEach(function (incident) {
                        var _a, _b;
                        var statusChanges = (_a = incident.activities) === null || _a === void 0 ? void 0 : _a.filter(function (_a) {
                            var type = _a.type, value = _a.value;
                            return type === IncidentActivityType.STATUS_CHANGE &&
                                value &&
                                [
                                    "" + IncidentStatus.WARNING,
                                    "" + IncidentStatus.CRITICAL,
                                ].includes(value);
                        }).sort(function (a, b) {
                            return moment(a.dateCreated).valueOf() - moment(b.dateCreated).valueOf();
                        });
                        var incidentEnd = (_b = incident.dateClosed) !== null && _b !== void 0 ? _b : moment().valueOf();
                        var timeWindowMs = rule.timeWindow * 60 * 1000;
                        var incidentColor = warningTrigger &&
                            statusChanges &&
                            !statusChanges.find(function (_a) {
                                var value = _a.value;
                                return value === "" + IncidentStatus.CRITICAL;
                            })
                            ? theme.yellow300
                            : theme.red300;
                        var incidentStartDate = moment(incident.dateStarted).valueOf();
                        var incidentCloseDate = incident.dateClosed
                            ? moment(incident.dateClosed).valueOf()
                            : lastPoint;
                        var incidentStartValue = dataArr.find(function (point) { return point.name >= incidentStartDate; });
                        series.push(createIncidentSeries(router, organization, incidentColor, incidentStartDate, incident, incidentStartValue, series[0].seriesName));
                        var areaStart = Math.max(moment(incident.dateStarted).valueOf(), firstPoint);
                        var areaEnd = Math.min((statusChanges === null || statusChanges === void 0 ? void 0 : statusChanges.length) && statusChanges[0].dateCreated
                            ? moment(statusChanges[0].dateCreated).valueOf() - timeWindowMs
                            : moment(incidentEnd).valueOf(), lastPoint);
                        var areaColor = warningTrigger ? theme.yellow300 : theme.red300;
                        if (areaEnd > areaStart) {
                            series.push(createStatusAreaSeries(areaColor, areaStart, areaEnd));
                            if (areaColor === theme.yellow300) {
                                warningDuration += Math.abs(areaEnd - areaStart);
                            }
                            else {
                                criticalDuration += Math.abs(areaEnd - areaStart);
                            }
                        }
                        statusChanges === null || statusChanges === void 0 ? void 0 : statusChanges.forEach(function (activity, idx) {
                            var statusAreaStart = Math.max(moment(activity.dateCreated).valueOf() - timeWindowMs, firstPoint);
                            var statusAreaEnd = Math.min(idx === statusChanges.length - 1
                                ? moment(incidentEnd).valueOf()
                                : moment(statusChanges[idx + 1].dateCreated).valueOf() -
                                    timeWindowMs, lastPoint);
                            var statusAreaColor = activity.value === "" + IncidentStatus.CRITICAL
                                ? theme.red300
                                : theme.yellow300;
                            if (statusAreaEnd > statusAreaStart) {
                                series.push(createStatusAreaSeries(statusAreaColor, statusAreaStart, statusAreaEnd));
                                if (statusAreaColor === theme.yellow300) {
                                    warningDuration += Math.abs(statusAreaEnd - statusAreaStart);
                                }
                                else {
                                    criticalDuration += Math.abs(statusAreaEnd - statusAreaStart);
                                }
                            }
                        });
                        if (selectedIncident && incident.id === selectedIncident.id) {
                            var selectedIncidentColor = incidentColor === theme.yellow300 ? theme.yellow100 : theme.red100;
                            areaSeries.push({
                                type: 'line',
                                markArea: MarkArea({
                                    silent: true,
                                    itemStyle: {
                                        color: color(selectedIncidentColor).alpha(0.42).rgb().string(),
                                    },
                                    data: [
                                        [{ xAxis: incidentStartDate }, { xAxis: incidentCloseDate }],
                                    ],
                                }),
                                data: [],
                            });
                        }
                    });
                }
                var maxThresholdValue = 0;
                if (warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold) {
                    var alertThreshold = warningTrigger.alertThreshold;
                    var warningThresholdLine = createThresholdSeries(theme.yellow300, alertThreshold);
                    series.push(warningThresholdLine);
                    maxThresholdValue = Math.max(maxThresholdValue, alertThreshold);
                }
                if (criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold) {
                    var alertThreshold = criticalTrigger.alertThreshold;
                    var criticalThresholdLine = createThresholdSeries(theme.red300, alertThreshold);
                    series.push(criticalThresholdLine);
                    maxThresholdValue = Math.max(maxThresholdValue, alertThreshold);
                }
                return (<ChartPanel>
              <StyledPanelBody withPadding>
                <ChartHeader>
                  <ChartTitle>
                    {AlertWizardAlertNames[getAlertTypeFromAggregateDataset(rule)]}
                  </ChartTitle>
                  {filter}
                </ChartHeader>
                {_this.renderChart(timeseriesData, series, areaSeries, maxThresholdValue, maxSeriesValue)}
              </StyledPanelBody>
              {_this.renderChartActions(totalDuration, criticalDuration, warningDuration)}
            </ChartPanel>);
            }}
      </EventsRequest>);
    };
    return MetricChart;
}(React.PureComponent));
export default withRouter(MetricChart);
var ChartPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(2));
var ChartHeader = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var ChartTitle = styled('header')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n"], ["\n  display: flex;\n  flex-direction: row;\n"])));
var ChartActions = styled(PanelFooter)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  padding: ", " 20px;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  padding: ", " 20px;\n"])), space(1));
var ChartSummary = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  margin-right: auto;\n"], ["\n  display: flex;\n  margin-right: auto;\n"])));
var SummaryText = styled(SectionHeading)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  flex: 1;\n  display: flex;\n  align-items: center;\n  margin: 0;\n  font-weight: bold;\n  font-size: ", ";\n  line-height: 1;\n"], ["\n  flex: 1;\n  display: flex;\n  align-items: center;\n  margin: 0;\n  font-weight: bold;\n  font-size: ", ";\n  line-height: 1;\n"])), function (p) { return p.theme.fontSizeSmall; });
var SummaryStats = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0 ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0 ", ";\n"])), space(2));
var StatItem = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0 ", " 0 0;\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0 ", " 0 0;\n"])), space(2));
/* Override padding to make chart appear centered */
var StyledPanelBody = styled(PanelBody)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  padding-right: 6px;\n"], ["\n  padding-right: 6px;\n"])));
var StatCount = styled('span')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  margin-left: ", ";\n  margin-top: ", ";\n  color: ", ";\n"], ["\n  margin-left: ", ";\n  margin-top: ", ";\n  color: ", ";\n"])), space(0.5), space(0.25), function (p) { return p.theme.textColor; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=metricChart.jsx.map