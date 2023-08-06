import { __assign, __read, __spreadArray } from "tslib";
import { useEffect, useState } from 'react';
import pick from 'lodash/pick';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { t } from 'app/locale';
import { QueryResults } from 'app/utils/tokenizeSearch';
import { getInterval } from 'app/views/releases/detail/overview/chart/utils';
import { roundDuration } from 'app/views/releases/utils';
import { fillChartDataFromMetricsResponse, getBreakdownChartData } from './utils';
function StatsRequest(_a) {
    var api = _a.api, organization = _a.organization, projectSlug = _a.projectSlug, groupings = _a.groupings, environments = _a.environments, datetime = _a.datetime, location = _a.location, children = _a.children, searchQuery = _a.searchQuery;
    var _b = __read(useState(false), 2), isLoading = _b[0], setIsLoading = _b[1];
    var _c = __read(useState(false), 2), errored = _c[0], setErrored = _c[1];
    var _d = __read(useState([]), 2), series = _d[0], setSeries = _d[1];
    var filteredGroupings = groupings.filter(function (_a) {
        var aggregation = _a.aggregation, metricMeta = _a.metricMeta;
        return !!(metricMeta === null || metricMeta === void 0 ? void 0 : metricMeta.name) && !!aggregation;
    });
    useEffect(function () {
        fetchData();
    }, [projectSlug, environments, datetime, groupings, searchQuery]);
    function fetchData() {
        if (!filteredGroupings.length) {
            return;
        }
        setErrored(false);
        setIsLoading(true);
        var requestExtraParams = getParams(pick(location.query, Object.values(URL_PARAM).filter(function (param) { return param !== URL_PARAM.PROJECT; })));
        var promises = filteredGroupings.map(function (_a) {
            var metricMeta = _a.metricMeta, aggregation = _a.aggregation, groupBy = _a.groupBy;
            var query = __assign({ field: aggregation + "(" + metricMeta.name + ")", interval: getInterval(datetime) }, requestExtraParams);
            if (searchQuery) {
                var tagsWithDoubleQuotes = searchQuery
                    .split(' ')
                    .filter(function (tag) { return !!tag; })
                    .map(function (tag) {
                    var _a = __read(tag.split(':'), 2), key = _a[0], value = _a[1];
                    if (key && value) {
                        return key + ":\"" + value + "\"";
                    }
                    return '';
                })
                    .filter(function (tag) { return !!tag; });
                if (!!tagsWithDoubleQuotes.length) {
                    query.query = new QueryResults(tagsWithDoubleQuotes).formatString();
                }
            }
            var metricDataEndpoint = "/projects/" + organization.slug + "/" + projectSlug + "/metrics/data/";
            if (!!(groupBy === null || groupBy === void 0 ? void 0 : groupBy.length)) {
                var groupByParameter = __spreadArray([], __read(groupBy)).join('&groupBy=');
                return api.requestPromise(metricDataEndpoint + "?groupBy=" + groupByParameter, {
                    query: query,
                });
            }
            return api.requestPromise(metricDataEndpoint, {
                query: query,
            });
        });
        Promise.all(promises)
            .then(function (results) {
            getChartData(results);
        })
            .catch(function (error) {
            var _a, _b;
            addErrorMessage((_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : t('Error loading chart data'));
            setErrored(true);
        });
    }
    function getChartData(sessionReponses) {
        if (!sessionReponses.length) {
            setIsLoading(false);
            return;
        }
        var seriesData = sessionReponses.map(function (sessionResponse, index) {
            var _a = filteredGroupings[index], aggregation = _a.aggregation, legend = _a.legend, metricMeta = _a.metricMeta;
            var field = aggregation + "(" + metricMeta.name + ")";
            var breakDownChartData = getBreakdownChartData({
                response: sessionResponse,
                sessionResponseIndex: index + 1,
                legend: legend,
            });
            var chartData = fillChartDataFromMetricsResponse({
                response: sessionResponse,
                field: field,
                chartData: breakDownChartData,
                valueFormatter: metricMeta.name === 'session.duration'
                    ? function (duration) { return roundDuration(duration ? duration / 1000 : 0); }
                    : undefined,
            });
            return __spreadArray([], __read(Object.values(chartData)));
        });
        var newSeries = seriesData.reduce(function (mergedSeries, chartDataSeries) {
            return mergedSeries.concat(chartDataSeries);
        }, []);
        setSeries(newSeries);
        setIsLoading(false);
    }
    return children({ isLoading: isLoading, errored: errored, series: series });
}
export default StatsRequest;
//# sourceMappingURL=statsRequest.jsx.map