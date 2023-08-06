import { t } from 'app/locale';
import { formatAbbreviatedNumber, formatFloat, formatPercentage, getDuration, } from 'app/utils/formatters';
import { decodeScalar } from 'app/utils/queryString';
import { getTermHelp, PERFORMANCE_TERM } from '../data';
import { platformToPerformanceType, PROJECT_PERFORMANCE_TYPE } from '../utils';
export var LEFT_AXIS_QUERY_KEY = 'left';
export var RIGHT_AXIS_QUERY_KEY = 'right';
export var LandingDisplayField;
(function (LandingDisplayField) {
    LandingDisplayField["ALL"] = "all";
    LandingDisplayField["FRONTEND_PAGELOAD"] = "frontend_pageload";
    LandingDisplayField["FRONTEND_OTHER"] = "frontend_other";
    LandingDisplayField["BACKEND"] = "backend";
    LandingDisplayField["MOBILE"] = "mobile";
})(LandingDisplayField || (LandingDisplayField = {}));
export var LANDING_DISPLAYS = [
    {
        label: 'All Transactions',
        field: LandingDisplayField.ALL,
    },
    {
        label: 'Frontend (Pageload)',
        field: LandingDisplayField.FRONTEND_PAGELOAD,
    },
    {
        label: 'Frontend (Other)',
        field: LandingDisplayField.FRONTEND_OTHER,
    },
    {
        label: 'Backend',
        field: LandingDisplayField.BACKEND,
    },
    {
        label: 'Mobile',
        field: LandingDisplayField.MOBILE,
        isShown: function (organization) {
            return organization.features.includes('performance-mobile-vitals');
        },
        alpha: true,
    },
];
export function getCurrentLandingDisplay(location, projects, eventView) {
    var _a;
    var landingField = decodeScalar((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.landingDisplay);
    var display = LANDING_DISPLAYS.find(function (_a) {
        var field = _a.field;
        return field === landingField;
    });
    if (display) {
        return display;
    }
    var defaultDisplayField = getDefaultDisplayFieldForPlatform(projects, eventView);
    var defaultDisplay = LANDING_DISPLAYS.find(function (_a) {
        var field = _a.field;
        return field === defaultDisplayField;
    });
    return defaultDisplay || LANDING_DISPLAYS[0];
}
export function getChartWidth(chartData, refPixelRect) {
    var distance = refPixelRect ? refPixelRect.point2.x - refPixelRect.point1.x : 0;
    var chartWidth = chartData.length * distance;
    return {
        chartWidth: chartWidth,
    };
}
export function getBackendFunction(functionName, organization) {
    switch (functionName) {
        case 'p75':
            return {
                kind: 'function',
                function: ['p75', 'transaction.duration', undefined, undefined],
            };
        case 'tpm':
            return { kind: 'function', function: ['tpm', '', undefined, undefined] };
        case 'failure_rate':
            return { kind: 'function', function: ['failure_rate', '', undefined, undefined] };
        case 'apdex':
            if (organization.features.includes('project-transaction-threshold')) {
                return {
                    kind: 'function',
                    function: ['apdex', '', undefined, undefined],
                };
            }
            return {
                kind: 'function',
                function: ['apdex', "" + organization.apdexThreshold, undefined, undefined],
            };
        default:
            throw new Error("Unsupported backend function: " + functionName);
    }
}
export function getDefaultDisplayFieldForPlatform(projects, eventView) {
    var _a;
    var _b;
    if (!eventView) {
        return LandingDisplayField.ALL;
    }
    var projectIds = eventView.project;
    var performanceTypeToDisplay = (_a = {},
        _a[PROJECT_PERFORMANCE_TYPE.ANY] = LandingDisplayField.ALL,
        _a[PROJECT_PERFORMANCE_TYPE.FRONTEND] = LandingDisplayField.FRONTEND_PAGELOAD,
        _a[PROJECT_PERFORMANCE_TYPE.BACKEND] = LandingDisplayField.BACKEND,
        _a);
    var performanceType = platformToPerformanceType(projects, projectIds);
    var landingField = (_b = performanceTypeToDisplay[performanceType]) !== null && _b !== void 0 ? _b : LandingDisplayField.ALL;
    return landingField;
}
export var backendCardDetails = function (organization) {
    return {
        p75: {
            title: t('Duration (p75)'),
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P75),
            formatter: function (value) { return getDuration(value / 1000, value >= 1000 ? 3 : 0, true); },
        },
        tpm: {
            title: t('Throughput'),
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.THROUGHPUT),
            formatter: formatAbbreviatedNumber,
        },
        failure_rate: {
            title: t('Failure Rate'),
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE),
            formatter: function (value) { return formatPercentage(value, 2); },
        },
        apdex: {
            title: t('Apdex'),
            tooltip: organization.features.includes('project-transaction-threshold')
                ? getTermHelp(organization, PERFORMANCE_TERM.APDEX_NEW)
                : getTermHelp(organization, PERFORMANCE_TERM.APDEX),
            formatter: function (value) { return formatFloat(value, 4); },
        },
    };
};
export function getDisplayAxes(options, location) {
    var leftDefault = options.find(function (opt) { return opt.isLeftDefault; }) || options[0];
    var rightDefault = options.find(function (opt) { return opt.isRightDefault; }) || options[1];
    var leftAxis = options.find(function (opt) { return opt.value === location.query[LEFT_AXIS_QUERY_KEY]; }) || leftDefault;
    var rightAxis = options.find(function (opt) { return opt.value === location.query[RIGHT_AXIS_QUERY_KEY]; }) ||
        rightDefault;
    return {
        leftAxis: leftAxis,
        rightAxis: rightAxis,
    };
}
//# sourceMappingURL=utils.jsx.map