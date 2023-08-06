import { __read, __spreadArray } from "tslib";
import pick from 'lodash/pick';
import round from 'lodash/round';
import moment from 'moment';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { PAGE_URL_PARAM, URL_PARAM } from 'app/constants/globalSelectionHeader';
import { tn } from 'app/locale';
import { ReleaseStatus } from 'app/types';
import { QueryResults } from 'app/utils/tokenizeSearch';
import { IssueSortOptions } from 'app/views/issueList/utils';
import { DisplayOption } from '../list/utils';
export var CRASH_FREE_DECIMAL_THRESHOLD = 95;
export var roundDuration = function (seconds) {
    return round(seconds, seconds > 60 ? 0 : 3);
};
export var getCrashFreePercent = function (percent, decimalThreshold, decimalPlaces) {
    if (decimalThreshold === void 0) { decimalThreshold = CRASH_FREE_DECIMAL_THRESHOLD; }
    if (decimalPlaces === void 0) { decimalPlaces = 3; }
    return round(percent, percent > decimalThreshold ? decimalPlaces : 0);
};
export var displayCrashFreePercent = function (percent, decimalThreshold, decimalPlaces) {
    if (decimalThreshold === void 0) { decimalThreshold = CRASH_FREE_DECIMAL_THRESHOLD; }
    if (decimalPlaces === void 0) { decimalPlaces = 3; }
    if (isNaN(percent)) {
        return '\u2015';
    }
    if (percent < 1 && percent > 0) {
        return "<1%";
    }
    var rounded = getCrashFreePercent(percent, decimalThreshold, decimalPlaces).toLocaleString();
    return rounded + "%";
};
export var getReleaseNewIssuesUrl = function (orgSlug, projectId, version) {
    return {
        pathname: "/organizations/" + orgSlug + "/issues/",
        query: {
            project: projectId,
            // we are resetting time selector because releases' new issues count doesn't take time selector into account
            statsPeriod: undefined,
            start: undefined,
            end: undefined,
            query: new QueryResults(["firstRelease:" + version]).formatString(),
            sort: IssueSortOptions.FREQ,
        },
    };
};
export var getReleaseUnhandledIssuesUrl = function (orgSlug, projectId, version) {
    return {
        pathname: "/organizations/" + orgSlug + "/issues/",
        query: {
            project: projectId,
            query: new QueryResults([
                "release:" + version,
                'error.unhandled:true',
            ]).formatString(),
            sort: IssueSortOptions.FREQ,
        },
    };
};
export var isReleaseArchived = function (release) {
    return release.status === ReleaseStatus.Archived;
};
export function releaseDisplayLabel(displayOption, count) {
    if (displayOption === DisplayOption.USERS) {
        return tn('user', 'users', count);
    }
    return tn('session', 'sessions', count);
}
export function getReleaseBounds(release) {
    var _a;
    var _b = release || {}, lastEvent = _b.lastEvent, currentProjectMeta = _b.currentProjectMeta, dateCreated = _b.dateCreated;
    var sessionsUpperBound = (currentProjectMeta || {}).sessionsUpperBound;
    return {
        releaseStart: dateCreated,
        releaseEnd: (_a = (moment(sessionsUpperBound).isAfter(lastEvent) ? sessionsUpperBound : lastEvent)) !== null && _a !== void 0 ? _a : moment().utc().format(),
    };
}
// these options are here only temporarily while we still support older and newer release details page
export function getReleaseParams(_a) {
    var location = _a.location, releaseBounds = _a.releaseBounds, defaultStatsPeriod = _a.defaultStatsPeriod, allowEmptyPeriod = _a.allowEmptyPeriod;
    var params = getParams(pick(location.query, __spreadArray(__spreadArray(__spreadArray([], __read(Object.values(URL_PARAM))), __read(Object.values(PAGE_URL_PARAM))), [
        'cursor',
    ])), {
        allowAbsolutePageDatetime: true,
        defaultStatsPeriod: defaultStatsPeriod,
        allowEmptyPeriod: allowEmptyPeriod,
    });
    if (!Object.keys(params).some(function (param) {
        return [URL_PARAM.START, URL_PARAM.END, URL_PARAM.UTC, URL_PARAM.PERIOD].includes(param);
    })) {
        params[URL_PARAM.START] = releaseBounds.releaseStart;
        params[URL_PARAM.END] = releaseBounds.releaseEnd;
    }
    return params;
}
//# sourceMappingURL=index.jsx.map