import { __assign, __extends, __makeTemplateObject, __read } from "tslib";
import styled from '@emotion/styled';
import compact from 'lodash/compact';
import pick from 'lodash/pick';
import moment from 'moment';
import AsyncComponent from 'app/components/asyncComponent';
import ChartZoom from 'app/components/charts/chartZoom';
import LineChart from 'app/components/charts/lineChart';
import { HeaderTitleLegend, InlineContainer, SectionHeading, SectionValue, } from 'app/components/charts/styles';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getDiffInMinutes, ONE_WEEK, truncationFormatter, } from 'app/components/charts/utils';
import Count from 'app/components/count';
import { getParams, parseStatsPeriod, } from 'app/components/organizations/globalSelectionHeader/getParams';
import { Panel, PanelBody, PanelFooter } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { t, tct, tn } from 'app/locale';
import space from 'app/styles/space';
import { percent } from 'app/utils';
import { formatVersion } from 'app/utils/formatters';
import withApi from 'app/utils/withApi';
import { DisplayOption } from 'app/views/releases/list/utils';
import { reduceTimeSeriesGroups, sessionDisplayToField, } from 'app/views/releases/utils/releaseHealthRequest';
var ReleaseAdoptionChart = /** @class */ (function (_super) {
    __extends(ReleaseAdoptionChart, _super);
    function ReleaseAdoptionChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        _this.handleClick = function (params) {
            var _a = _this.props, organization = _a.organization, router = _a.router, selection = _a.selection, location = _a.location;
            var project = selection.projects[0];
            router.push({
                pathname: "/organizations/" + (organization === null || organization === void 0 ? void 0 : organization.slug) + "/releases/" + encodeURIComponent(params.seriesId) + "/",
                query: { project: project, environment: location.query.environment },
            });
        };
        return _this;
    }
    // TODO(release-adoption-chart): refactor duplication
    ReleaseAdoptionChart.prototype.getInterval = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var datetimeObj = {
            start: location.query.start,
            end: location.query.end,
            period: location.query.statsPeriod,
            utc: location.query.utc,
        };
        var diffInMinutes = getDiffInMinutes(datetimeObj);
        // use high fidelity intervals when available
        // limit on backend is set to six hour
        if (organization.features.includes('minute-resolution-sessions') &&
            diffInMinutes < 360) {
            return '10m';
        }
        if (diffInMinutes >= ONE_WEEK) {
            return '1d';
        }
        else {
            return '1h';
        }
    };
    ReleaseAdoptionChart.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, activeDisplay = _a.activeDisplay;
        var hasSemverFeature = organization.features.includes('semver');
        return [
            [
                'sessions',
                "/organizations/" + organization.slug + "/sessions/",
                {
                    query: __assign(__assign({ interval: this.getInterval() }, getParams(pick(location.query, Object.values(URL_PARAM)))), { groupBy: ['release'], field: [sessionDisplayToField(activeDisplay)], query: location.query.query
                            ? hasSemverFeature
                                ? location.query.query
                                : "release:" + location.query.query
                            : undefined }),
                },
            ],
        ];
    };
    ReleaseAdoptionChart.prototype.getReleasesSeries = function () {
        var _a;
        var activeDisplay = this.props.activeDisplay;
        var sessions = this.state.sessions;
        var releases = sessions === null || sessions === void 0 ? void 0 : sessions.groups.map(function (group) { return group.by.release; });
        if (!releases) {
            return null;
        }
        var totalData = (_a = sessions === null || sessions === void 0 ? void 0 : sessions.groups) === null || _a === void 0 ? void 0 : _a.reduce(function (acc, group) {
            return reduceTimeSeriesGroups(acc, group, sessionDisplayToField(activeDisplay));
        }, []);
        return releases.map(function (release) {
            var _a, _b;
            var releaseData = (_a = sessions === null || sessions === void 0 ? void 0 : sessions.groups.find(function (_a) {
                var by = _a.by;
                return by.release === release;
            })) === null || _a === void 0 ? void 0 : _a.series[sessionDisplayToField(activeDisplay)];
            return {
                id: release,
                seriesName: formatVersion(release),
                data: (_b = sessions === null || sessions === void 0 ? void 0 : sessions.intervals.map(function (interval, index) {
                    var _a, _b;
                    return ({
                        name: moment(interval).valueOf(),
                        value: percent((_a = releaseData === null || releaseData === void 0 ? void 0 : releaseData[index]) !== null && _a !== void 0 ? _a : 0, (_b = totalData === null || totalData === void 0 ? void 0 : totalData[index]) !== null && _b !== void 0 ? _b : 0),
                    });
                })) !== null && _b !== void 0 ? _b : [],
            };
        });
    };
    ReleaseAdoptionChart.prototype.getTotal = function () {
        var activeDisplay = this.props.activeDisplay;
        var sessions = this.state.sessions;
        return ((sessions === null || sessions === void 0 ? void 0 : sessions.groups.reduce(function (acc, group) { return acc + group.totals[sessionDisplayToField(activeDisplay)]; }, 0)) || 0);
    };
    ReleaseAdoptionChart.prototype.renderEmpty = function () {
        return (<Panel>
        <PanelBody withPadding>
          <ChartHeader>
            <Placeholder height="24px"/>
          </ChartHeader>
          <Placeholder height="200px"/>
        </PanelBody>
        <ChartFooter>
          <Placeholder height="34px"/>
        </ChartFooter>
      </Panel>);
    };
    ReleaseAdoptionChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, activeDisplay = _a.activeDisplay, router = _a.router, selection = _a.selection;
        var _b = selection.datetime, start = _b.start, end = _b.end, period = _b.period, utc = _b.utc;
        var _c = this.state, loading = _c.loading, reloading = _c.reloading, sessions = _c.sessions;
        var releasesSeries = this.getReleasesSeries();
        var totalCount = this.getTotal();
        if ((loading && !reloading) || (reloading && totalCount === 0) || !sessions) {
            return this.renderEmpty();
        }
        if (!(releasesSeries === null || releasesSeries === void 0 ? void 0 : releasesSeries.length)) {
            return null;
        }
        var interval = this.getInterval();
        var numDataPoints = releasesSeries[0].data.length;
        return (<Panel>
        <PanelBody withPadding>
          <ChartHeader>
            <ChartTitle>{t('Release Adoption')}</ChartTitle>
          </ChartHeader>
          <TransitionChart loading={loading} reloading={reloading}>
            <TransparentLoadingMask visible={reloading}/>
            <ChartZoom router={router} period={period} utc={utc} start={start} end={end}>
              {function (zoomRenderProps) { return (<LineChart {...zoomRenderProps} grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }} series={releasesSeries} yAxis={{
                    min: 0,
                    max: 100,
                    type: 'value',
                    interval: 10,
                    splitNumber: 10,
                    data: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                    axisLabel: {
                        formatter: '{value}%',
                    },
                }} tooltip={{
                    formatter: function (seriesParams) {
                        var series = Array.isArray(seriesParams)
                            ? seriesParams
                            : [seriesParams];
                        var timestamp = series[0].data[0];
                        var _a = __read(series
                            .filter(function (s) { return s.data[1] > 0; })
                            .sort(function (a, b) { return b.data[1] - a.data[1]; })), first = _a[0], second = _a[1], third = _a[2], rest = _a.slice(3);
                        var restSum = rest.reduce(function (acc, s) { return acc + s.data[1]; }, 0);
                        var seriesToRender = compact([first, second, third]);
                        if (rest.length) {
                            seriesToRender.push({
                                seriesName: tn('%s Other', '%s Others', rest.length),
                                data: [timestamp, restSum],
                                marker: '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;"></span>',
                            });
                        }
                        if (!seriesToRender.length) {
                            return '<div/>';
                        }
                        var periodObj = parseStatsPeriod(interval) || {
                            periodLength: 'd',
                            period: '1',
                        };
                        var intervalStart = moment(timestamp).format('MMM D LT');
                        var intervalEnd = (series[0].dataIndex === numDataPoints - 1
                            ? moment(sessions.end)
                            : moment(timestamp).add(parseInt(periodObj.period, 10), periodObj.periodLength)).format('MMM D LT');
                        return [
                            '<div class="tooltip-series">',
                            seriesToRender
                                .map(function (s) {
                                return "<div><span class=\"tooltip-label\">" + s.marker + "<strong>" + (s.seriesName && truncationFormatter(s.seriesName, 12)) + "</strong></span>" + s.data[1].toFixed(2) + "%</div>";
                            })
                                .join(''),
                            '</div>',
                            "<div class=\"tooltip-date\">" + intervalStart + " &mdash; " + intervalEnd + "</div>",
                            "<div class=\"tooltip-arrow\"></div>",
                        ].join('');
                    },
                }} onClick={_this.handleClick}/>); }}
            </ChartZoom>
          </TransitionChart>
        </PanelBody>
        <ChartFooter>
          <InlineContainer>
            <SectionHeading>
              {tct('Total [display]', {
                display: activeDisplay === DisplayOption.USERS ? 'Users' : 'Sessions',
            })}
            </SectionHeading>
            <SectionValue>
              <Count value={totalCount || 0}/>
            </SectionValue>
          </InlineContainer>
        </ChartFooter>
      </Panel>);
    };
    return ReleaseAdoptionChart;
}(AsyncComponent));
export default withApi(ReleaseAdoptionChart);
var ChartHeader = styled(HeaderTitleLegend)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1));
var ChartTitle = styled('header')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n"], ["\n  display: flex;\n  flex-direction: row;\n"])));
var ChartFooter = styled(PanelFooter)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", " 20px;\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", " 20px;\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=releaseAdoptionChart.jsx.map