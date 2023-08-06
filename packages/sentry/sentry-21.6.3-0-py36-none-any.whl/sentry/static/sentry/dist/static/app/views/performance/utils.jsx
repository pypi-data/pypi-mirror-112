import { __assign, __read, __spreadArray } from "tslib";
import Duration from 'app/components/duration';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { backend, frontend } from 'app/data/platformCategories';
import { defined } from 'app/utils';
import { statsPeriodToDays } from 'app/utils/dates';
import { getDuration } from 'app/utils/formatters';
import getCurrentSentryReactTransaction from 'app/utils/getCurrentSentryReactTransaction';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
/**
 * Performance type can used to determine a default view or which specific field should be used by default on pages
 * where we don't want to wait for transaction data to return to determine how to display aspects of a page.
 */
export var PROJECT_PERFORMANCE_TYPE;
(function (PROJECT_PERFORMANCE_TYPE) {
    PROJECT_PERFORMANCE_TYPE["ANY"] = "any";
    PROJECT_PERFORMANCE_TYPE["FRONTEND"] = "frontend";
    PROJECT_PERFORMANCE_TYPE["BACKEND"] = "backend";
    PROJECT_PERFORMANCE_TYPE["FRONTEND_OTHER"] = "frontend_other";
})(PROJECT_PERFORMANCE_TYPE || (PROJECT_PERFORMANCE_TYPE = {}));
var FRONTEND_PLATFORMS = __spreadArray([], __read(frontend));
var BACKEND_PLATFORMS = __spreadArray([], __read(backend));
export function platformToPerformanceType(projects, projectIds) {
    if (projectIds.length === 0 || projectIds[0] === ALL_ACCESS_PROJECTS) {
        return PROJECT_PERFORMANCE_TYPE.ANY;
    }
    var selectedProjects = projects.filter(function (p) { return projectIds.includes(parseInt(p.id, 10)); });
    if (selectedProjects.length === 0 || selectedProjects.some(function (p) { return !p.platform; })) {
        return PROJECT_PERFORMANCE_TYPE.ANY;
    }
    if (selectedProjects.every(function (project) {
        return FRONTEND_PLATFORMS.includes(project.platform);
    })) {
        return PROJECT_PERFORMANCE_TYPE.FRONTEND;
    }
    if (selectedProjects.every(function (project) {
        return BACKEND_PLATFORMS.includes(project.platform);
    })) {
        return PROJECT_PERFORMANCE_TYPE.BACKEND;
    }
    return PROJECT_PERFORMANCE_TYPE.ANY;
}
/**
 * Used for transaction summary to determine appropriate columns on a page, since there is no display field set for the page.
 */
export function platformAndConditionsToPerformanceType(projects, eventView) {
    var performanceType = platformToPerformanceType(projects, eventView.project);
    if (performanceType === PROJECT_PERFORMANCE_TYPE.FRONTEND) {
        var conditions = tokenizeSearch(eventView.query);
        var ops = conditions.getTagValues('!transaction.op');
        if (ops.some(function (op) { return op === 'pageload'; })) {
            return PROJECT_PERFORMANCE_TYPE.FRONTEND_OTHER;
        }
    }
    return performanceType;
}
/**
 * Used for transaction summary to check the view itself, since it can have conditions which would exclude it from having vitals aside from platform.
 */
export function isSummaryViewFrontendPageLoad(eventView, projects) {
    return (platformAndConditionsToPerformanceType(projects, eventView) ===
        PROJECT_PERFORMANCE_TYPE.FRONTEND);
}
export function getPerformanceLandingUrl(organization) {
    return "/organizations/" + organization.slug + "/performance/";
}
export function getPerformanceTrendsUrl(organization) {
    return "/organizations/" + organization.slug + "/performance/trends/";
}
export function getTransactionSearchQuery(location, query) {
    if (query === void 0) { query = ''; }
    return decodeScalar(location.query.query, query).trim();
}
export function getTransactionDetailsUrl(organization, eventSlug, transaction, query) {
    return {
        pathname: "/organizations/" + organization.slug + "/performance/" + eventSlug + "/",
        query: __assign(__assign({}, query), { transaction: transaction }),
    };
}
export function getTransactionComparisonUrl(_a) {
    var organization = _a.organization, baselineEventSlug = _a.baselineEventSlug, regressionEventSlug = _a.regressionEventSlug, transaction = _a.transaction, query = _a.query;
    return {
        pathname: "/organizations/" + organization.slug + "/performance/compare/" + baselineEventSlug + "/" + regressionEventSlug + "/",
        query: __assign(__assign({}, query), { transaction: transaction }),
    };
}
export function addRoutePerformanceContext(selection) {
    var transaction = getCurrentSentryReactTransaction();
    var days = statsPeriodToDays(selection.datetime.period, selection.datetime.start, selection.datetime.end);
    var oneDay = 86400;
    var seconds = Math.floor(days * oneDay);
    transaction === null || transaction === void 0 ? void 0 : transaction.setTag('query.period', seconds.toString());
    var groupedPeriod = '>30d';
    if (seconds <= oneDay)
        groupedPeriod = '<=1d';
    else if (seconds <= oneDay * 7)
        groupedPeriod = '<=7d';
    else if (seconds <= oneDay * 14)
        groupedPeriod = '<=14d';
    else if (seconds <= oneDay * 30)
        groupedPeriod = '<=30d';
    transaction === null || transaction === void 0 ? void 0 : transaction.setTag('query.period.grouped', groupedPeriod);
}
export function getTransactionName(location) {
    var transaction = location.query.transaction;
    return decodeScalar(transaction);
}
var hasMilliseconds = function (props) {
    return defined(props.milliseconds);
};
export function PerformanceDuration(props) {
    var normalizedSeconds = hasMilliseconds(props)
        ? props.milliseconds / 1000
        : props.seconds;
    return (<Duration abbreviation={props.abbreviation} seconds={normalizedSeconds} fixedDigits={normalizedSeconds > 1 ? 2 : 0}/>);
}
export function getPerformanceDuration(milliseconds) {
    return getDuration(milliseconds / 1000, milliseconds > 1000 ? 2 : 0, true);
}
//# sourceMappingURL=utils.jsx.map