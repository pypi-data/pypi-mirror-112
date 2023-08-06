import { __assign, __awaiter, __generator, __read, __spreadArray } from "tslib";
import { mountWithTheme } from 'sentry-test/enzyme';
import { initializeOrg } from 'sentry-test/initializeOrg';
import EventView from 'app/utils/discover/eventView';
import SummaryContent from 'app/views/performance/transactionSummary/content';
import { SpanOperationBreakdownFilter } from 'app/views/performance/transactionSummary/filter';
function initialize(projects, query, additionalFeatures) {
    if (additionalFeatures === void 0) { additionalFeatures = []; }
    var features = __spreadArray(['transaction-event', 'performance-view'], __read(additionalFeatures));
    // @ts-expect-error
    var organization = TestStubs.Organization({
        features: features,
        projects: projects,
    });
    var initialOrgData = {
        organization: organization,
        router: {
            location: {
                query: __assign({}, query),
            },
        },
        project: 1,
        projects: [],
    };
    var initialData = initializeOrg(initialOrgData);
    var eventView = EventView.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: 'test-transaction',
        fields: ['id', 'user.display', 'transaction.duration', 'trace', 'timestamp'],
        projects: [],
    }, initialData.router.location);
    var spanOperationBreakdownFilter = SpanOperationBreakdownFilter.None;
    var transactionName = 'example-transaction';
    return __assign(__assign({}, initialData), { spanOperationBreakdownFilter: spanOperationBreakdownFilter, transactionName: transactionName, location: initialData.router.location, eventView: eventView });
}
describe('Transaction Summary Content', function () {
    beforeEach(function () {
        // @ts-expect-error
        MockApiClient.addMockResponse({
            method: 'GET',
            url: '/prompts-activity/',
            body: {},
        });
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/sdk-updates/',
        body: [],
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/eventsv2/',
        body: { data: [{ 'event.type': 'error' }], meta: { 'event.type': 'string' } },
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/users/',
        body: [],
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/issues/?limit=5&query=is%3Aunresolved%20transaction%3Aexample-transaction&sort=new&statsPeriod=14d',
        body: [],
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/events-facets/',
        body: [],
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/releases/stats/',
        body: [],
    });
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: '/organizations/org-slug/events-stats/',
        body: [],
    });
    it('Basic Rendering', function () {
        return __awaiter(this, void 0, void 0, function () {
            var projects, _a, organization, location, eventView, spanOperationBreakdownFilter, transactionName, routerContext, wrapper, transactionListProps;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        projects = [TestStubs.Project()];
                        _a = initialize(projects, {}), organization = _a.organization, location = _a.location, eventView = _a.eventView, spanOperationBreakdownFilter = _a.spanOperationBreakdownFilter, transactionName = _a.transactionName;
                        routerContext = TestStubs.routerContext([{ organization: organization }]);
                        wrapper = mountWithTheme(<SummaryContent location={location} organization={organization} eventView={eventView} transactionName={transactionName} isLoading={false} totalValues={null} spanOperationBreakdownFilter={spanOperationBreakdownFilter} error={null} onChangeFilter={function () { }}/>, routerContext);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _b.sent();
                        wrapper.update();
                        expect(wrapper.find('TransactionHeader')).toHaveLength(1);
                        expect(wrapper.find('Filter')).toHaveLength(1);
                        expect(wrapper.find('StyledSearchBar')).toHaveLength(1);
                        expect(wrapper.find('TransactionSummaryCharts')).toHaveLength(1);
                        expect(wrapper.find('TransactionsList')).toHaveLength(1);
                        expect(wrapper.find('UserStats')).toHaveLength(1);
                        expect(wrapper.find('StatusBreakdown')).toHaveLength(1);
                        expect(wrapper.find('SidebarCharts')).toHaveLength(1);
                        expect(wrapper.find('DiscoverQuery')).toHaveLength(2);
                        transactionListProps = wrapper.find('TransactionsList').first().props();
                        expect(transactionListProps.generateDiscoverEventView).toBeDefined();
                        expect(transactionListProps.handleOpenInDiscoverClick).toBeDefined();
                        expect(transactionListProps.generatePerformanceTransactionEventsView).toBeUndefined();
                        expect(transactionListProps.handleOpenAllEventsClick).toBeUndefined();
                        return [2 /*return*/];
                }
            });
        });
    });
    it('Renders with generatePerformanceTransactionEventsView instead when feature flagged', function () {
        return __awaiter(this, void 0, void 0, function () {
            var projects, _a, organization, location, eventView, spanOperationBreakdownFilter, transactionName, routerContext, wrapper, transactionListProps;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        projects = [TestStubs.Project()];
                        _a = initialize(projects, {}, ['performance-events-page']), organization = _a.organization, location = _a.location, eventView = _a.eventView, spanOperationBreakdownFilter = _a.spanOperationBreakdownFilter, transactionName = _a.transactionName;
                        routerContext = TestStubs.routerContext([{ organization: organization }]);
                        wrapper = mountWithTheme(<SummaryContent location={location} organization={organization} eventView={eventView} transactionName={transactionName} isLoading={false} totalValues={null} spanOperationBreakdownFilter={spanOperationBreakdownFilter} error={null} onChangeFilter={function () { }}/>, routerContext);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _b.sent();
                        wrapper.update();
                        expect(wrapper.find('TransactionHeader')).toHaveLength(1);
                        expect(wrapper.find('Filter')).toHaveLength(1);
                        expect(wrapper.find('StyledSearchBar')).toHaveLength(1);
                        expect(wrapper.find('TransactionSummaryCharts')).toHaveLength(1);
                        expect(wrapper.find('TransactionsList')).toHaveLength(1);
                        expect(wrapper.find('UserStats')).toHaveLength(1);
                        expect(wrapper.find('StatusBreakdown')).toHaveLength(1);
                        expect(wrapper.find('SidebarCharts')).toHaveLength(1);
                        expect(wrapper.find('DiscoverQuery')).toHaveLength(2);
                        transactionListProps = wrapper.find('TransactionsList').first().props();
                        expect(transactionListProps.generateDiscoverEventView).toBeUndefined();
                        expect(transactionListProps.handleOpenInDiscoverClick).toBeUndefined();
                        expect(transactionListProps.generatePerformanceTransactionEventsView).toBeDefined();
                        expect(transactionListProps.handleOpenAllEventsClick).toBeDefined();
                        return [2 /*return*/];
                }
            });
        });
    });
});
//# sourceMappingURL=content.spec.jsx.map