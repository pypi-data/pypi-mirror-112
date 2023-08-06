import { __awaiter, __generator, __read, __spreadArray } from "tslib";
import { mountWithTheme } from 'sentry-test/enzyme';
import { initializeOrg } from 'sentry-test/initializeOrg';
import { t } from 'app/locale';
import ProjectsStore from 'app/stores/projectsStore';
import EventView from 'app/utils/discover/eventView';
import { SPAN_OP_BREAKDOWN_FIELDS, SPAN_OP_RELATIVE_BREAKDOWN_FIELD, } from 'app/utils/discover/fields';
import EventsTable from 'app/views/performance/transactionSummary/transactionEvents/eventsTable';
function initializeData(_a) {
    var _b = _a.features, additionalFeatures = _b === void 0 ? [] : _b;
    var features = __spreadArray(['discover-basic', 'performance-view'], __read(additionalFeatures));
    // @ts-expect-error
    var organization = TestStubs.Organization({
        features: features,
        // @ts-expect-error
        projects: [TestStubs.Project()],
        apdexThreshold: 400,
    });
    var initialData = initializeOrg({
        organization: organization,
        router: {
            location: {
                query: {
                    transaction: '/performance',
                    project: 1,
                    transactionCursor: '1:0:0',
                },
            },
        },
        project: 1,
        projects: [],
    });
    ProjectsStore.loadInitialData(initialData.organization.projects);
    return initialData;
}
describe('Performance GridEditable Table', function () {
    var transactionsListTitles;
    var fields;
    var organization;
    var data;
    var transactionName;
    var query = 'transaction.duration:<15m event.type:transaction transaction:/api/0/organizations/{organization_slug}/eventsv2/';
    beforeEach(function () {
        transactionName = 'transactionName';
        transactionsListTitles = [
            t('event id'),
            t('user'),
            t('operation duration'),
            t('total duration'),
            t('trace id'),
            t('timestamp'),
        ];
        fields = __spreadArray([
            'id',
            'user.display',
            SPAN_OP_RELATIVE_BREAKDOWN_FIELD,
            'transaction.duration',
            'trace',
            'timestamp',
            'spans.total.time'
        ], __read(SPAN_OP_BREAKDOWN_FIELDS));
        // @ts-expect-error
        organization = TestStubs.Organization();
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/projects/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/is-key-transactions/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/prompts-activity/',
            body: {},
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/sdk-updates/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            method: 'GET',
            url: "/organizations/org-slug/legacy-key-transactions-count/",
            body: [],
        });
        data = [
            {
                id: 'deadbeef',
                'user.display': 'uhoh@example.com',
                'transaction.duration': 400,
                'project.id': 1,
                timestamp: '2020-05-21T15:31:18+00:00',
                trace: '1234',
                'span_ops_breakdown.relative': '',
                'spans.browser': 100,
                'spans.db': 30,
                'spans.http': 170,
                'spans.resource': 100,
                'spans.total.time': 400,
            },
            {
                id: 'moredeadbeef',
                'user.display': 'moreuhoh@example.com',
                'transaction.duration': 600,
                'project.id': 1,
                timestamp: '2020-05-22T15:31:18+00:00',
                trace: '4321',
                'span_ops_breakdown.relative': '',
                'spans.browser': 100,
                'spans.db': 300,
                'spans.http': 100,
                'spans.resource': 100,
                'spans.total.time': 600,
            },
        ];
        // Transaction list response
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/eventsv2/',
            headers: {
                Link: '<http://localhost/api/0/organizations/org-slug/eventsv2/?cursor=2:0:0>; rel="next"; results="true"; cursor="2:0:0",' +
                    '<http://localhost/api/0/organizations/org-slug/eventsv2/?cursor=1:0:0>; rel="previous"; results="false"; cursor="1:0:0"',
            },
            body: {
                meta: {
                    id: 'string',
                    'user.display': 'string',
                    'transaction.duration': 'duration',
                    'project.id': 'integer',
                    timestamp: 'date',
                },
                data: data,
            },
        }, {
            predicate: function (url, options) {
                var _a;
                return (url.includes('eventsv2') && ((_a = options.query) === null || _a === void 0 ? void 0 : _a.field.includes('user.display')));
            },
        });
    });
    afterEach(function () {
        // @ts-expect-error
        MockApiClient.clearMockResponses();
        ProjectsStore.reset();
        jest.clearAllMocks();
    });
    it('renders ops breakdown bar when querying for span_ops_breakdown.relative', function () {
        return __awaiter(this, void 0, void 0, function () {
            var initialData, eventView, wrapper;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        initialData = initializeData({ features: ['performance-events-page'] });
                        eventView = EventView.fromNewQueryWithLocation({
                            id: undefined,
                            version: 2,
                            name: 'transactionName',
                            fields: fields,
                            query: query,
                            projects: [],
                            orderby: '-timestamp',
                        }, initialData.router.location);
                        wrapper = mountWithTheme(<EventsTable eventView={eventView} organization={organization} location={initialData.router.location} setError={function () { }} columnTitles={transactionsListTitles} transactionName={transactionName}/>, initialData.routerContext);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _a.sent();
                        wrapper.update();
                        expect(wrapper.find('GridHeadCell')).toHaveLength(6);
                        expect(wrapper.find('GridHeadCellStatic')).toHaveLength(0);
                        expect(wrapper.find('OperationSort')).toHaveLength(1);
                        expect(wrapper.find('RelativeOpsBreakdown')).toHaveLength(2);
                        return [2 /*return*/];
                }
            });
        });
    });
    it('renders basic columns without ops breakdown when not querying for span_ops_breakdown.relative', function () {
        return __awaiter(this, void 0, void 0, function () {
            var initialData, eventView, wrapper;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        initialData = initializeData({ features: ['performance-events-page'] });
                        fields = [
                            'id',
                            'user.display',
                            'transaction.duration',
                            'trace',
                            'timestamp',
                            'spans.http',
                        ];
                        data.forEach(function (result) {
                            delete result['span_ops_breakdown.relative'];
                            delete result['spans.resource'];
                            delete result['spans.browser'];
                            delete result['spans.db'];
                            delete result['spans.total.time'];
                        });
                        eventView = EventView.fromNewQueryWithLocation({
                            id: undefined,
                            version: 2,
                            name: 'transactionName',
                            fields: fields,
                            query: query,
                            projects: [],
                            orderby: '-timestamp',
                        }, initialData.router.location);
                        wrapper = mountWithTheme(<EventsTable eventView={eventView} organization={organization} location={initialData.router.location} setError={function () { }} columnTitles={transactionsListTitles} transactionName={transactionName}/>, initialData.routerContext);
                        // @ts-expect-error
                        return [4 /*yield*/, tick()];
                    case 1:
                        // @ts-expect-error
                        _a.sent();
                        wrapper.update();
                        expect(wrapper.find('GridHeadCell')).toHaveLength(6);
                        expect(wrapper.find('GridHeadCellStatic')).toHaveLength(0);
                        expect(wrapper.find('OperationSort')).toHaveLength(0);
                        expect(wrapper.find('RelativeOpsBreakdown')).toHaveLength(0);
                        return [2 /*return*/];
                }
            });
        });
    });
});
//# sourceMappingURL=eventsTable.spec.jsx.map