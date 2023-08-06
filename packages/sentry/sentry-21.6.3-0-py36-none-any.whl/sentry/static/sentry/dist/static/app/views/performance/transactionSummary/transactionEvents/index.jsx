import { __assign, __extends, __read, __spreadArray } from "tslib";
import { Component } from 'react';
import { browserHistory } from 'react-router';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import EventView from 'app/utils/discover/eventView';
import { isAggregateField, SPAN_OP_BREAKDOWN_FIELDS, SPAN_OP_RELATIVE_BREAKDOWN_FIELD, WebVital, } from 'app/utils/discover/fields';
import { removeHistogramQueryStrings } from 'app/utils/performance/histogram';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import { getTransactionName } from '../../utils';
import { decodeFilterFromLocation, filterToLocationQuery, SpanOperationBreakdownFilter, } from '../filter';
import { ZOOM_END, ZOOM_START } from '../latencyChart';
import EventsPageContent from './content';
import { decodeEventsDisplayFilterFromLocation, EventsDisplayFilterName, filterEventsDisplayToLocationQuery, getEventsFilterOptions, } from './utils';
var TransactionEvents = /** @class */ (function (_super) {
    __extends(TransactionEvents, _super);
    function TransactionEvents() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            spanOperationBreakdownFilter: decodeFilterFromLocation(_this.props.location),
            eventsDisplayFilterName: decodeEventsDisplayFilterFromLocation(_this.props.location),
            eventView: generateEventsEventView(_this.props.location, getTransactionName(_this.props.location)),
        };
        _this.onChangeSpanOperationBreakdownFilter = function (newFilter) {
            var _a;
            var _b = _this.props, location = _b.location, organization = _b.organization;
            var _c = _this.state, spanOperationBreakdownFilter = _c.spanOperationBreakdownFilter, eventsDisplayFilterName = _c.eventsDisplayFilterName, eventView = _c.eventView;
            trackAnalyticsEvent({
                eventName: 'Performance Views: Transaction Events Ops Breakdown Filter Dropdown',
                eventKey: 'performance_views.transactionEvents.ops_filter_dropdown.selection',
                organization_id: parseInt(organization.id, 10),
                action: newFilter,
            });
            // Check to see if the current table sort matches the EventsDisplayFilter.
            // If it does, we can re-sort using the new SpanOperationBreakdownFilter
            var eventsFilterOptionSort = getEventsFilterOptions(spanOperationBreakdownFilter)[eventsDisplayFilterName].sort;
            var currentSort = (_a = eventView === null || eventView === void 0 ? void 0 : eventView.sorts) === null || _a === void 0 ? void 0 : _a[0];
            var sortQuery = {};
            if ((eventsFilterOptionSort === null || eventsFilterOptionSort === void 0 ? void 0 : eventsFilterOptionSort.kind) === (currentSort === null || currentSort === void 0 ? void 0 : currentSort.kind) &&
                (eventsFilterOptionSort === null || eventsFilterOptionSort === void 0 ? void 0 : eventsFilterOptionSort.field) === (currentSort === null || currentSort === void 0 ? void 0 : currentSort.field)) {
                sortQuery = filterEventsDisplayToLocationQuery(eventsDisplayFilterName, newFilter);
            }
            var nextQuery = __assign(__assign(__assign({}, removeHistogramQueryStrings(location, [ZOOM_START, ZOOM_END])), filterToLocationQuery(newFilter)), sortQuery);
            if (newFilter === SpanOperationBreakdownFilter.None) {
                delete nextQuery.breakdown;
            }
            browserHistory.push({
                pathname: location.pathname,
                query: nextQuery,
            });
        };
        _this.onChangeEventsDisplayFilter = function (newFilterName) {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventName: 'Performance Views: Transaction Events Display Filter Dropdown',
                eventKey: 'performance_views.transactionEvents.display_filter_dropdown.selection',
                organization_id: parseInt(organization.id, 10),
                action: newFilterName,
            });
            _this.filterDropdownSortEvents(newFilterName);
        };
        _this.filterDropdownSortEvents = function (newFilterName) {
            var location = _this.props.location;
            var spanOperationBreakdownFilter = _this.state.spanOperationBreakdownFilter;
            var nextQuery = __assign(__assign({}, removeHistogramQueryStrings(location, [ZOOM_START, ZOOM_END])), filterEventsDisplayToLocationQuery(newFilterName, spanOperationBreakdownFilter));
            if (newFilterName === EventsDisplayFilterName.p100) {
                delete nextQuery.showTransaction;
            }
            browserHistory.push({
                pathname: location.pathname,
                query: nextQuery,
            });
        };
        _this.getFilteredEventView = function (percentiles) {
            var _a = _this.state, eventsDisplayFilterName = _a.eventsDisplayFilterName, spanOperationBreakdownFilter = _a.spanOperationBreakdownFilter, eventView = _a.eventView;
            var filter = getEventsFilterOptions(spanOperationBreakdownFilter, percentiles)[eventsDisplayFilterName];
            var filteredEventView = eventView === null || eventView === void 0 ? void 0 : eventView.clone();
            if (filteredEventView && (filter === null || filter === void 0 ? void 0 : filter.query)) {
                var query_1 = tokenizeSearch(filteredEventView.query);
                filter.query.forEach(function (item) { return query_1.setTagValues(item[0], [item[1]]); });
                filteredEventView.query = query_1.formatString();
            }
            return filteredEventView;
        };
        _this.renderNoAccess = function () {
            return <Alert type="warning">{t("You don't have access to this feature")}</Alert>;
        };
        return _this;
    }
    TransactionEvents.getDerivedStateFromProps = function (nextProps, prevState) {
        return __assign(__assign({}, prevState), { spanOperationBreakdownFilter: decodeFilterFromLocation(nextProps.location), eventsDisplayFilterName: decodeEventsDisplayFilterFromLocation(nextProps.location), eventView: generateEventsEventView(nextProps.location, getTransactionName(nextProps.location)) });
    };
    TransactionEvents.prototype.getDocumentTitle = function () {
        var name = getTransactionName(this.props.location);
        var hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), t('Events')].join(' \u2014 ');
        }
        return [t('Summary'), t('Events')].join(' \u2014 ');
    };
    TransactionEvents.prototype.getPercentilesEventView = function (eventView) {
        var percentileColumns = [
            {
                kind: 'function',
                function: ['p100', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['p99', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['p95', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['p75', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['p50', '', undefined, undefined],
            },
        ];
        return eventView.withColumns(__spreadArray([], __read(percentileColumns)));
    };
    TransactionEvents.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, projects = _a.projects, location = _a.location;
        var eventView = this.state.eventView;
        var transactionName = getTransactionName(location);
        var webVital = getWebVital(location);
        if (!eventView || transactionName === undefined) {
            // If there is no transaction name, redirect to the Performance landing page
            browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: __assign({}, location.query),
            });
            return null;
        }
        var percentilesView = this.getPercentilesEventView(eventView);
        var shouldForceProject = eventView.project.length === 1;
        var forceProject = shouldForceProject
            ? projects.find(function (p) { return parseInt(p.id, 10) === eventView.project[0]; })
            : undefined;
        var projectSlugs = eventView.project
            .map(function (projectId) { return projects.find(function (p) { return parseInt(p.id, 10) === projectId; }); })
            .filter(function (p) { return p !== undefined; })
            .map(function (p) { return p.slug; });
        return (<SentryDocumentTitle title={this.getDocumentTitle()} orgSlug={organization.slug} projectSlug={forceProject === null || forceProject === void 0 ? void 0 : forceProject.slug}>
        <Feature features={['performance-events-page']} organization={organization} renderDisabled={this.renderNoAccess}>
          <GlobalSelectionHeader lockedMessageSubject={t('transaction')} shouldForceProject={shouldForceProject} forceProject={forceProject} specificProjectSlugs={projectSlugs} disableMultipleProjectSelection showProjectSettingsLink>
            <LightWeightNoProjectMessage organization={organization}>
              <DiscoverQuery eventView={percentilesView} orgSlug={organization.slug} location={location} referrer="api.performance.transaction-events">
                {function (_a) {
                var _b;
                var isLoading = _a.isLoading, tableData = _a.tableData;
                var percentiles = (_b = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _b === void 0 ? void 0 : _b[0];
                return (<EventsPageContent location={location} eventView={_this.getFilteredEventView(percentiles)} transactionName={transactionName} organization={organization} projects={projects} spanOperationBreakdownFilter={_this.state.spanOperationBreakdownFilter} onChangeSpanOperationBreakdownFilter={_this.onChangeSpanOperationBreakdownFilter} eventsDisplayFilterName={_this.state.eventsDisplayFilterName} onChangeEventsDisplayFilter={_this.onChangeEventsDisplayFilter} percentileValues={percentiles} isLoading={isLoading} webVital={webVital}/>);
            }}
              </DiscoverQuery>
            </LightWeightNoProjectMessage>
          </GlobalSelectionHeader>
        </Feature>
      </SentryDocumentTitle>);
    };
    return TransactionEvents;
}(Component));
function getWebVital(location) {
    var webVital = decodeScalar(location.query.webVital, '');
    if (Object.values(WebVital).includes(webVital)) {
        return webVital;
    }
    return undefined;
}
function generateEventsEventView(location, transactionName) {
    if (transactionName === undefined) {
        return undefined;
    }
    var query = decodeScalar(location.query.query, '');
    var conditions = tokenizeSearch(query);
    conditions
        .setTagValues('event.type', ['transaction'])
        .setTagValues('transaction', [transactionName]);
    Object.keys(conditions.tagValues).forEach(function (field) {
        if (isAggregateField(field))
            conditions.removeTag(field);
    });
    // Default fields for relative span view
    var fields = [
        'id',
        'user.display',
        SPAN_OP_RELATIVE_BREAKDOWN_FIELD,
        'transaction.duration',
        'trace',
        'timestamp',
    ];
    var breakdown = decodeFilterFromLocation(location);
    if (breakdown !== SpanOperationBreakdownFilter.None) {
        fields.splice(2, 1, "spans." + breakdown);
    }
    else {
        fields.push.apply(fields, __spreadArray(__spreadArray([], __read(SPAN_OP_BREAKDOWN_FIELDS)), ['spans.total.time']));
    }
    var webVital = getWebVital(location);
    if (webVital) {
        fields.splice(3, 0, webVital);
    }
    return EventView.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields: fields,
        query: conditions.formatString(),
        projects: [],
        orderby: decodeScalar(location.query.sort, '-timestamp'),
    }, location);
}
export default withGlobalSelection(withProjects(withOrganization(TransactionEvents)));
//# sourceMappingURL=index.jsx.map