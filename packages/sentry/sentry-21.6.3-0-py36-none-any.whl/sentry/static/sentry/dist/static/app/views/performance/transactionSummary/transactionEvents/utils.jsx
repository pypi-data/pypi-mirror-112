import { t } from 'app/locale';
import { decodeScalar } from 'app/utils/queryString';
import { filterToField } from '../filter';
import { TransactionFilterOptions } from '../utils';
export var EventsDisplayFilterName;
(function (EventsDisplayFilterName) {
    EventsDisplayFilterName["p50"] = "p50";
    EventsDisplayFilterName["p75"] = "p75";
    EventsDisplayFilterName["p95"] = "p95";
    EventsDisplayFilterName["p99"] = "p99";
    EventsDisplayFilterName["p100"] = "p100";
})(EventsDisplayFilterName || (EventsDisplayFilterName = {}));
export function getEventsFilterOptions(spanOperationBreakdownFilter, percentileValues) {
    var _a;
    var _b = percentileValues
        ? percentileValues
        : { p99: 0, p95: 0, p75: 0, p50: 0 }, p99 = _b.p99, p95 = _b.p95, p75 = _b.p75, p50 = _b.p50;
    return _a = {},
        _a[EventsDisplayFilterName.p50] = {
            name: EventsDisplayFilterName.p50,
            query: p50 ? [['transaction.duration', "<=" + p50.toFixed(0)]] : undefined,
            sort: {
                kind: 'desc',
                field: filterToField(spanOperationBreakdownFilter) || 'transaction.duration',
            },
            label: t('p50'),
        },
        _a[EventsDisplayFilterName.p75] = {
            name: EventsDisplayFilterName.p75,
            query: p75 ? [['transaction.duration', "<=" + p75.toFixed(0)]] : undefined,
            sort: {
                kind: 'desc',
                field: filterToField(spanOperationBreakdownFilter) || 'transaction.duration',
            },
            label: t('p75'),
        },
        _a[EventsDisplayFilterName.p95] = {
            name: EventsDisplayFilterName.p95,
            query: p95 ? [['transaction.duration', "<=" + p95.toFixed(0)]] : undefined,
            sort: {
                kind: 'desc',
                field: filterToField(spanOperationBreakdownFilter) || 'transaction.duration',
            },
            label: t('p95'),
        },
        _a[EventsDisplayFilterName.p99] = {
            name: EventsDisplayFilterName.p99,
            query: p99 ? [['transaction.duration', "<=" + p99.toFixed(0)]] : undefined,
            sort: {
                kind: 'desc',
                field: filterToField(spanOperationBreakdownFilter) || 'transaction.duration',
            },
            label: t('p99'),
        },
        _a[EventsDisplayFilterName.p100] = {
            name: EventsDisplayFilterName.p100,
            label: t('p100'),
        },
        _a;
}
export function eventsRouteWithQuery(_a) {
    var orgSlug = _a.orgSlug, transaction = _a.transaction, projectID = _a.projectID, query = _a.query;
    var pathname = "/organizations/" + orgSlug + "/performance/summary/events/";
    return {
        pathname: pathname,
        query: {
            transaction: transaction,
            project: projectID,
            environment: query.environment,
            statsPeriod: query.statsPeriod,
            start: query.start,
            end: query.end,
            query: query.query,
        },
    };
}
function stringToFilter(option) {
    if (Object.values(EventsDisplayFilterName).includes(option)) {
        return option;
    }
    return EventsDisplayFilterName.p100;
}
export function decodeEventsDisplayFilterFromLocation(location) {
    return stringToFilter(decodeScalar(location.query.showTransactions, EventsDisplayFilterName.p100));
}
export function filterEventsDisplayToLocationQuery(option, spanOperationBreakdownFilter) {
    var _a, _b;
    var eventsFilterOptions = getEventsFilterOptions(spanOperationBreakdownFilter);
    var kind = (_a = eventsFilterOptions[option].sort) === null || _a === void 0 ? void 0 : _a.kind;
    var field = (_b = eventsFilterOptions[option].sort) === null || _b === void 0 ? void 0 : _b.field;
    var query = {
        showTransactions: option,
    };
    if (kind && field) {
        query.sort = "" + (kind === 'desc' ? '-' : '') + field;
    }
    return query;
}
export function mapShowTransactionToPercentile(showTransaction) {
    switch (showTransaction) {
        case TransactionFilterOptions.OUTLIER:
            return EventsDisplayFilterName.p100;
        case TransactionFilterOptions.SLOW:
            return EventsDisplayFilterName.p95;
        default:
            return undefined;
    }
}
//# sourceMappingURL=utils.jsx.map