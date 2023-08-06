function getSerieNameByGroups(groupByKeys, groupBy) {
    return groupByKeys.map(function (groupByKey) { return groupBy[groupByKey]; }).join('_');
}
export function getBreakdownChartData(_a) {
    var response = _a.response, sessionResponseIndex = _a.sessionResponseIndex, legend = _a.legend;
    return response.groups.reduce(function (groups, group, index) {
        var groupByKeys = Object.keys(group.by);
        if (!groupByKeys.length) {
            groups[index] = {
                seriesName: legend !== null && legend !== void 0 ? legend : "Query " + sessionResponseIndex,
                data: [],
            };
            return groups;
        }
        var serieNameByGroups = getSerieNameByGroups(groupByKeys, group.by);
        groups[serieNameByGroups] = {
            seriesName: legend ? legend + "_" + serieNameByGroups : serieNameByGroups,
            data: [],
        };
        return groups;
    }, {});
}
export function fillChartDataFromMetricsResponse(_a) {
    var response = _a.response, field = _a.field, chartData = _a.chartData, valueFormatter = _a.valueFormatter;
    response.intervals.forEach(function (interval, index) {
        for (var groupsIndex in response.groups) {
            var group = response.groups[groupsIndex];
            var groupByKeys = Object.keys(group.by);
            var value = group.series[field][index];
            if (!groupByKeys.length) {
                chartData[0].data.push({
                    name: interval,
                    value: typeof valueFormatter === 'function' ? valueFormatter(value) : value,
                });
                return;
            }
            var serieNameByGroups = getSerieNameByGroups(groupByKeys, group.by);
            chartData[serieNameByGroups].data.push({
                name: interval,
                value: typeof valueFormatter === 'function' ? valueFormatter(value) : value,
            });
        }
    });
    return chartData;
}
//# sourceMappingURL=utils.jsx.map