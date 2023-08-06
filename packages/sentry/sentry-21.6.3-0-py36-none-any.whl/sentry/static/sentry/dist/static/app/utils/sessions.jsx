import compact from 'lodash/compact';
import { getDiffInMinutes, ONE_WEEK, TWO_WEEKS, } from 'app/components/charts/utils';
import { defined, percent } from 'app/utils';
import { getCrashFreePercent } from 'app/views/releases/utils';
export function getCount(groups, field) {
    if (groups === void 0) { groups = []; }
    return groups.reduce(function (acc, group) { return acc + group.totals[field]; }, 0);
}
export function getCrashCount(groups, field) {
    if (groups === void 0) { groups = []; }
    return getCount(groups.filter(function (_a) {
        var by = _a.by;
        return by['session.status'] === 'crashed';
    }), field);
}
export function getCrashFreeRate(groups, field) {
    if (groups === void 0) { groups = []; }
    var totalCount = groups.reduce(function (acc, group) { return acc + group.totals[field]; }, 0);
    var crashedCount = getCrashCount(groups, field);
    return !defined(totalCount) || totalCount === 0
        ? null
        : getCrashFreePercent(100 - percent(crashedCount !== null && crashedCount !== void 0 ? crashedCount : 0, totalCount !== null && totalCount !== void 0 ? totalCount : 0));
}
export function getCrashFreeSeries(groups, intervals, field) {
    if (groups === void 0) { groups = []; }
    if (intervals === void 0) { intervals = []; }
    return compact(intervals.map(function (interval, i) {
        var _a, _b;
        var intervalTotalSessions = groups.reduce(function (acc, group) { return acc + group.series[field][i]; }, 0);
        var intervalCrashedSessions = (_b = (_a = groups.find(function (group) { return group.by['session.status'] === 'crashed'; })) === null || _a === void 0 ? void 0 : _a.series[field][i]) !== null && _b !== void 0 ? _b : 0;
        var crashedSessionsPercent = percent(intervalCrashedSessions, intervalTotalSessions);
        if (intervalTotalSessions === 0) {
            return null;
        }
        return {
            name: interval,
            value: getCrashFreePercent(100 - crashedSessionsPercent),
        };
    }));
}
export function getSessionsInterval(datetimeObj, _a) {
    var _b = _a === void 0 ? {} : _a, highFidelity = _b.highFidelity;
    var diffInMinutes = getDiffInMinutes(datetimeObj);
    if (diffInMinutes > TWO_WEEKS) {
        return '1d';
    }
    if (diffInMinutes > ONE_WEEK) {
        return '6h';
    }
    // limit on backend for sub-hour session resolution is set to six hours
    if (highFidelity && diffInMinutes < 360) {
        if (diffInMinutes <= 30) {
            return '1m';
        }
        return '5m';
    }
    return '1h';
}
//# sourceMappingURL=sessions.jsx.map