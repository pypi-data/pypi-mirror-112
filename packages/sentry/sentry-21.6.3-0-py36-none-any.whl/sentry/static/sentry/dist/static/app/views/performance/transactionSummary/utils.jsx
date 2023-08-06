import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { generateEventSlug } from 'app/utils/discover/urls';
import { getTraceDetailsUrl } from 'app/views/performance/traceDetails/utils';
import { getTransactionDetailsUrl } from '../utils';
export var TransactionFilterOptions;
(function (TransactionFilterOptions) {
    TransactionFilterOptions["FASTEST"] = "fastest";
    TransactionFilterOptions["SLOW"] = "slow";
    TransactionFilterOptions["OUTLIER"] = "outlier";
    TransactionFilterOptions["RECENT"] = "recent";
})(TransactionFilterOptions || (TransactionFilterOptions = {}));
export function generateTransactionSummaryRoute(_a) {
    var orgSlug = _a.orgSlug;
    return "/organizations/" + orgSlug + "/performance/summary/";
}
export function transactionSummaryRouteWithQuery(_a) {
    var orgSlug = _a.orgSlug, transaction = _a.transaction, projectID = _a.projectID, query = _a.query, _b = _a.unselectedSeries, unselectedSeries = _b === void 0 ? 'p100()' : _b, display = _a.display, trendFunction = _a.trendFunction, trendColumn = _a.trendColumn, showTransactions = _a.showTransactions;
    var pathname = generateTransactionSummaryRoute({
        orgSlug: orgSlug,
    });
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
            unselectedSeries: unselectedSeries,
            showTransactions: showTransactions,
            display: display,
            trendFunction: trendFunction,
            trendColumn: trendColumn,
        },
    };
}
export function generateTraceLink(dateSelection) {
    return function (organization, tableRow, _query) {
        var traceId = "" + tableRow.trace;
        if (!traceId) {
            return {};
        }
        return getTraceDetailsUrl(organization, traceId, dateSelection, {});
    };
}
export function generateTransactionLink(transactionName) {
    return function (organization, tableRow, query) {
        var eventSlug = generateEventSlug(tableRow);
        return getTransactionDetailsUrl(organization, eventSlug, transactionName, query);
    };
}
export var SidebarSpacer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(3));
var templateObject_1;
//# sourceMappingURL=utils.jsx.map