import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import { Component } from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import { defined } from 'app/utils';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import EventView from 'app/utils/discover/eventView';
import { isAggregateField, } from 'app/utils/discover/fields';
import { removeHistogramQueryStrings } from 'app/utils/performance/histogram';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import { addRoutePerformanceContext, getTransactionName } from '../utils';
import { PERCENTILE as VITAL_PERCENTILE, VITAL_GROUPS, } from './transactionVitals/constants';
import SummaryContent from './content';
import { decodeFilterFromLocation, filterToLocationQuery, SpanOperationBreakdownFilter, } from './filter';
import { ZOOM_END, ZOOM_START } from './latencyChart';
var TransactionSummary = /** @class */ (function (_super) {
    __extends(TransactionSummary, _super);
    function TransactionSummary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            transactionThreshold: undefined,
            transactionThresholdMetric: undefined,
            loadingThreshold: false,
            spanOperationBreakdownFilter: decodeFilterFromLocation(_this.props.location),
            eventView: generateSummaryEventView(_this.props.location, getTransactionName(_this.props.location)),
        };
        _this.onChangeFilter = function (newFilter) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            trackAnalyticsEvent({
                eventName: 'Performance Views: Filter Dropdown',
                eventKey: 'performance_views.filter_dropdown.selection',
                organization_id: parseInt(organization.id, 10),
                action: newFilter,
            });
            var nextQuery = __assign(__assign({}, removeHistogramQueryStrings(location, [ZOOM_START, ZOOM_END])), filterToLocationQuery(newFilter));
            if (newFilter === SpanOperationBreakdownFilter.None) {
                delete nextQuery.breakdown;
            }
            browserHistory.push({
                pathname: location.pathname,
                query: nextQuery,
            });
        };
        _this.fetchTransactionThreshold = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, location = _a.location;
            var transactionName = getTransactionName(location);
            var project = _this.getProject();
            if (!defined(project)) {
                return;
            }
            var transactionThresholdUrl = "/organizations/" + organization.slug + "/project-transaction-threshold-override/";
            _this.setState({ loadingThreshold: true });
            api
                .requestPromise(transactionThresholdUrl, {
                method: 'GET',
                includeAllArgs: true,
                query: {
                    project: project.id,
                    transaction: transactionName,
                },
            })
                .then(function (_a) {
                var _b = __read(_a, 1), data = _b[0];
                _this.setState({
                    loadingThreshold: false,
                    transactionThreshold: data.threshold,
                    transactionThresholdMetric: data.metric,
                });
            })
                .catch(function () {
                var projectThresholdUrl = "/projects/" + organization.slug + "/" + project.slug + "/transaction-threshold/configure/";
                _this.props.api
                    .requestPromise(projectThresholdUrl, {
                    method: 'GET',
                    includeAllArgs: true,
                    query: {
                        project: project.id,
                    },
                })
                    .then(function (_a) {
                    var _b = __read(_a, 1), data = _b[0];
                    _this.setState({
                        loadingThreshold: false,
                        transactionThreshold: data.threshold,
                        transactionThresholdMetric: data.metric,
                    });
                })
                    .catch(function (err) {
                    var _a, _b;
                    _this.setState({ loadingThreshold: false });
                    var errorMessage = (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.threshold) !== null && _b !== void 0 ? _b : null;
                    addErrorMessage(errorMessage);
                });
            });
        };
        return _this;
    }
    TransactionSummary.getDerivedStateFromProps = function (nextProps, prevState) {
        return __assign(__assign({}, prevState), { spanOperationBreakdownFilter: decodeFilterFromLocation(nextProps.location), eventView: generateSummaryEventView(nextProps.location, getTransactionName(nextProps.location)) });
    };
    TransactionSummary.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        loadOrganizationTags(api, organization.slug, selection);
        if (organization.features.includes('project-transaction-threshold-override')) {
            this.fetchTransactionThreshold();
        }
        addRoutePerformanceContext(selection);
    };
    TransactionSummary.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        if (!isEqual(prevProps.selection.projects, selection.projects) ||
            !isEqual(prevProps.selection.datetime, selection.datetime)) {
            loadOrganizationTags(api, organization.slug, selection);
            addRoutePerformanceContext(selection);
        }
    };
    TransactionSummary.prototype.getProject = function () {
        var projects = this.props.projects;
        var eventView = this.state.eventView;
        if (!defined(eventView)) {
            return undefined;
        }
        var projectId = String(eventView.project[0]);
        var project = projects.find(function (proj) { return proj.id === projectId; });
        return project;
    };
    TransactionSummary.prototype.getDocumentTitle = function () {
        var name = getTransactionName(this.props.location);
        var hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), t('Performance')].join(' - ');
        }
        return [t('Summary'), t('Performance')].join(' - ');
    };
    TransactionSummary.prototype.getTotalsEventView = function (organization, eventView) {
        var threshold = organization.apdexThreshold.toString();
        var vitals = VITAL_GROUPS.map(function (_a) {
            var vs = _a.vitals;
            return vs;
        }).reduce(function (keys, vs) {
            vs.forEach(function (vital) { return keys.push(vital); });
            return keys;
        }, []);
        var totalsColumns = [
            {
                kind: 'function',
                function: ['p95', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['count', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['count_unique', 'user', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['failure_rate', '', undefined, undefined],
            },
            {
                kind: 'function',
                function: ['tpm', '', undefined, undefined],
            },
        ];
        var featureColumns = organization.features.includes('project-transaction-threshold')
            ? [
                {
                    kind: 'function',
                    function: ['count_miserable', 'user', undefined, undefined],
                },
                {
                    kind: 'function',
                    function: ['user_misery', '', undefined, undefined],
                },
                {
                    kind: 'function',
                    function: ['apdex', '', undefined, undefined],
                },
            ]
            : [
                {
                    kind: 'function',
                    function: ['count_miserable', 'user', threshold, undefined],
                },
                {
                    kind: 'function',
                    function: ['user_misery', threshold, undefined, undefined],
                },
                {
                    kind: 'function',
                    function: ['apdex', threshold, undefined, undefined],
                },
            ];
        return eventView.withColumns(__spreadArray(__spreadArray(__spreadArray([], __read(totalsColumns)), __read(featureColumns)), __read(vitals.map(function (vital) {
            return ({
                kind: 'function',
                function: ['percentile', vital, VITAL_PERCENTILE.toString(), undefined],
            });
        }))));
    };
    TransactionSummary.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, projects = _a.projects, location = _a.location;
        var _b = this.state, eventView = _b.eventView, transactionThreshold = _b.transactionThreshold, transactionThresholdMetric = _b.transactionThresholdMetric, loadingThreshold = _b.loadingThreshold;
        var transactionName = getTransactionName(location);
        if (!eventView || transactionName === undefined) {
            // If there is no transaction name, redirect to the Performance landing page
            browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: __assign({}, location.query),
            });
            return null;
        }
        var totalsView = this.getTotalsEventView(organization, eventView);
        var shouldForceProject = eventView.project.length === 1;
        var forceProject = shouldForceProject
            ? projects.find(function (p) { return parseInt(p.id, 10) === eventView.project[0]; })
            : undefined;
        var projectSlugs = eventView.project
            .map(function (projectId) { return projects.find(function (p) { return parseInt(p.id, 10) === projectId; }); })
            .filter(function (p) { return p !== undefined; })
            .map(function (p) { return p.slug; });
        return (<SentryDocumentTitle title={this.getDocumentTitle()} orgSlug={organization.slug} projectSlug={forceProject === null || forceProject === void 0 ? void 0 : forceProject.slug}>
        <GlobalSelectionHeader lockedMessageSubject={t('transaction')} shouldForceProject={shouldForceProject} forceProject={forceProject} specificProjectSlugs={projectSlugs} disableMultipleProjectSelection showProjectSettingsLink>
          <StyledPageContent>
            <LightWeightNoProjectMessage organization={organization}>
              <DiscoverQuery eventView={totalsView} orgSlug={organization.slug} location={location} transactionThreshold={transactionThreshold} transactionThresholdMetric={transactionThresholdMetric} referrer="api.performance.transaction-summary">
                {function (_a) {
                var _b, _c;
                var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
                var totals = (_c = (_b = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _b === void 0 ? void 0 : _b[0]) !== null && _c !== void 0 ? _c : null;
                return (<SummaryContent location={location} organization={organization} eventView={eventView} transactionName={transactionName} isLoading={isLoading} error={error} totalValues={totals} onChangeFilter={_this.onChangeFilter} spanOperationBreakdownFilter={_this.state.spanOperationBreakdownFilter} onChangeThreshold={function (threshold, metric) {
                        return _this.setState({
                            transactionThreshold: threshold,
                            transactionThresholdMetric: metric,
                        });
                    }} transactionThreshold={transactionThreshold} transactionThresholdMetric={transactionThresholdMetric} loadingThreshold={loadingThreshold}/>);
            }}
              </DiscoverQuery>
            </LightWeightNoProjectMessage>
          </StyledPageContent>
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return TransactionSummary;
}(Component));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
function generateSummaryEventView(location, transactionName) {
    if (transactionName === undefined) {
        return undefined;
    }
    // Use the user supplied query but overwrite any transaction or event type
    // conditions they applied.
    var query = decodeScalar(location.query.query, '');
    var conditions = tokenizeSearch(query);
    conditions
        .setTagValues('event.type', ['transaction'])
        .setTagValues('transaction', [transactionName]);
    Object.keys(conditions.tagValues).forEach(function (field) {
        if (isAggregateField(field))
            conditions.removeTag(field);
    });
    var fields = ['id', 'user.display', 'transaction.duration', 'trace', 'timestamp'];
    return EventView.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields: fields,
        query: conditions.formatString(),
        projects: [],
    }, location);
}
export default withApi(withGlobalSelection(withProjects(withOrganization(TransactionSummary))));
var templateObject_1;
//# sourceMappingURL=index.jsx.map