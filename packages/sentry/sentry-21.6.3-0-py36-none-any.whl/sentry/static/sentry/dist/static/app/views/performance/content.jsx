import { __assign, __extends } from "tslib";
import { Component } from 'react';
import { browserHistory } from 'react-router';
import isEqual from 'lodash/isEqual';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import GlobalSdkUpdateAlert from 'app/components/globalSdkUpdateAlert';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import PageHeading from 'app/components/pageHeading';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { IconFlag } from 'app/icons';
import { t } from 'app/locale';
import { PageContent, PageHeader } from 'app/styles/organization';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { decodeScalar } from 'app/utils/queryString';
import { QueryResults, tokenizeSearch } from 'app/utils/tokenizeSearch';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import LandingContent from './landing/content';
import { DEFAULT_MAX_DURATION } from './trends/utils';
import { DEFAULT_STATS_PERIOD, generatePerformanceEventView } from './data';
import Onboarding from './onboarding';
import { addRoutePerformanceContext, getPerformanceTrendsUrl } from './utils';
var PerformanceContent = /** @class */ (function (_super) {
    __extends(PerformanceContent, _super);
    function PerformanceContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: generatePerformanceEventView(_this.props.organization, _this.props.location, _this.props.projects),
            error: undefined,
        };
        _this.setError = function (error) {
            _this.setState({ error: error });
        };
        _this.handleSearch = function (searchQuery) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.overview.search',
                eventName: 'Performance Views: Transaction overview search',
                organization_id: parseInt(organization.id, 10),
            });
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { cursor: undefined, query: String(searchQuery).trim() || undefined }),
            });
        };
        return _this;
    }
    PerformanceContent.getDerivedStateFromProps = function (nextProps, prevState) {
        return __assign(__assign({}, prevState), { eventView: generatePerformanceEventView(nextProps.organization, nextProps.location, nextProps.projects) });
    };
    PerformanceContent.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        loadOrganizationTags(api, organization.slug, selection);
        addRoutePerformanceContext(selection);
        trackAnalyticsEvent({
            eventKey: 'performance_views.overview.view',
            eventName: 'Performance Views: Transaction overview view',
            organization_id: parseInt(organization.id, 10),
        });
    };
    PerformanceContent.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        if (!isEqual(prevProps.selection.projects, selection.projects) ||
            !isEqual(prevProps.selection.datetime, selection.datetime)) {
            loadOrganizationTags(api, organization.slug, selection);
            addRoutePerformanceContext(selection);
        }
    };
    PerformanceContent.prototype.renderError = function () {
        var error = this.state.error;
        if (!error) {
            return null;
        }
        return (<Alert type="error" icon={<IconFlag size="md"/>}>
        {error}
      </Alert>);
    };
    PerformanceContent.prototype.handleTrendsClick = function () {
        var _a = this.props, location = _a.location, organization = _a.organization;
        var newQuery = __assign({}, location.query);
        var query = decodeScalar(location.query.query, '');
        var conditions = tokenizeSearch(query);
        trackAnalyticsEvent({
            eventKey: 'performance_views.change_view',
            eventName: 'Performance Views: Change View',
            organization_id: parseInt(organization.id, 10),
            view_name: 'TRENDS',
        });
        var modifiedConditions = new QueryResults([]);
        if (conditions.hasTag('tpm()')) {
            modifiedConditions.setTagValues('tpm()', conditions.getTagValues('tpm()'));
        }
        else {
            modifiedConditions.setTagValues('tpm()', ['>0.01']);
        }
        if (conditions.hasTag('transaction.duration')) {
            modifiedConditions.setTagValues('transaction.duration', conditions.getTagValues('transaction.duration'));
        }
        else {
            modifiedConditions.setTagValues('transaction.duration', [
                '>0',
                "<" + DEFAULT_MAX_DURATION,
            ]);
        }
        newQuery.query = modifiedConditions.formatString();
        browserHistory.push({
            pathname: getPerformanceTrendsUrl(organization),
            query: __assign({}, newQuery),
        });
    };
    PerformanceContent.prototype.shouldShowOnboarding = function () {
        var _a = this.props, projects = _a.projects, demoMode = _a.demoMode;
        var eventView = this.state.eventView;
        // XXX used by getsentry to bypass onboarding for the upsell demo state.
        if (demoMode) {
            return false;
        }
        if (projects.length === 0) {
            return false;
        }
        // Current selection is 'my projects' or 'all projects'
        if (eventView.project.length === 0 || eventView.project === [ALL_ACCESS_PROJECTS]) {
            return (projects.filter(function (p) { return p.firstTransactionEvent === false; }).length === projects.length);
        }
        // Any other subset of projects.
        return (projects.filter(function (p) {
            return eventView.project.includes(parseInt(p.id, 10)) &&
                p.firstTransactionEvent === false;
        }).length === eventView.project.length);
    };
    PerformanceContent.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, projects = _a.projects;
        var eventView = this.state.eventView;
        var showOnboarding = this.shouldShowOnboarding();
        return (<PageContent>
        <LightWeightNoProjectMessage organization={organization}>
          <PageHeader>
            <PageHeading>{t('Performance')}</PageHeading>
            {!showOnboarding && (<Button priority="primary" data-test-id="landing-header-trends" onClick={function () { return _this.handleTrendsClick(); }}>
                {t('View Trends')}
              </Button>)}
          </PageHeader>
          <GlobalSdkUpdateAlert />
          {this.renderError()}
          {showOnboarding ? (<Onboarding organization={organization}/>) : (<LandingContent eventView={eventView} projects={projects} organization={organization} setError={this.setError} handleSearch={this.handleSearch}/>)}
        </LightWeightNoProjectMessage>
      </PageContent>);
    };
    PerformanceContent.prototype.render = function () {
        var organization = this.props.organization;
        return (<SentryDocumentTitle title={t('Performance')} orgSlug={organization.slug}>
        <GlobalSelectionHeader defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: DEFAULT_STATS_PERIOD,
                },
            }}>
          {this.renderBody()}
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return PerformanceContent;
}(Component));
export default withApi(withOrganization(withProjects(withGlobalSelection(PerformanceContent))));
//# sourceMappingURL=content.jsx.map