import { __assign, __extends, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import SearchBar from 'app/components/searchBar';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { IconAdd } from 'app/icons';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { decodeScalar } from 'app/utils/queryString';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import DashboardList from './dashboardList';
var SORT_OPTIONS = [
    { label: t('My Dashboards'), value: 'mydashboards' },
    { label: t('Dashboard Name (A-Z)'), value: 'title' },
    { label: t('Date Created (Newest)'), value: '-dateCreated' },
    { label: t('Date Created (Oldest)'), value: 'dateCreated' },
];
var ManageDashboards = /** @class */ (function (_super) {
    __extends(ManageDashboards, _super);
    function ManageDashboards() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSortChange = function (value) {
            var location = _this.props.location;
            trackAnalyticsEvent({
                eventKey: 'dashboards_manage.change_sort',
                eventName: 'Dashboards Manager: Sort By Changed',
                organization_id: parseInt(_this.props.organization.id, 10),
                sort: value,
            });
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { cursor: undefined, sort: value }),
            });
        };
        return _this;
    }
    ManageDashboards.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        return [
            [
                'dashboards',
                "/organizations/" + organization.slug + "/dashboards/",
                {
                    query: __assign(__assign({}, pick(location.query, ['cursor', 'query'])), { sort: this.getActiveSort().value, per_page: '9' }),
                },
            ],
        ];
    };
    ManageDashboards.prototype.getActiveSort = function () {
        var location = this.props.location;
        var urlSort = decodeScalar(location.query.sort, 'mydashboards');
        return SORT_OPTIONS.find(function (item) { return item.value === urlSort; }) || SORT_OPTIONS[0];
    };
    ManageDashboards.prototype.onDashboardsChange = function () {
        this.reloadData();
    };
    ManageDashboards.prototype.handleSearch = function (query) {
        var _a = this.props, location = _a.location, router = _a.router;
        trackAnalyticsEvent({
            eventKey: 'dashboards_manage.search',
            eventName: 'Dashboards Manager: Search',
            organization_id: parseInt(this.props.organization.id, 10),
        });
        router.push({
            pathname: location.pathname,
            query: __assign(__assign({}, location.query), { cursor: undefined, query: query }),
        });
    };
    ManageDashboards.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return typeof query === 'string' ? query : undefined;
    };
    ManageDashboards.prototype.renderActions = function () {
        var _this = this;
        var activeSort = this.getActiveSort();
        return (<StyledActions>
        <SearchBar defaultQuery="" query={this.getQuery()} placeholder={t('Search Dashboards')} onSearch={function (query) { return _this.handleSearch(query); }}/>
        <DropdownControl buttonProps={{ prefix: t('Sort By') }} label={activeSort.label}>
          {SORT_OPTIONS.map(function (_a) {
                var label = _a.label, value = _a.value;
                return (<DropdownItem key={value} onSelect={_this.handleSortChange} eventKey={value} isActive={value === activeSort.value}>
              {label}
            </DropdownItem>);
            })}
        </DropdownControl>
      </StyledActions>);
    };
    ManageDashboards.prototype.renderNoAccess = function () {
        return (<PageContent>
        <Alert type="warning">{t("You don't have access to this feature")}</Alert>
      </PageContent>);
    };
    ManageDashboards.prototype.renderDashboards = function () {
        var _this = this;
        var _a = this.state, dashboards = _a.dashboards, dashboardsPageLinks = _a.dashboardsPageLinks;
        var _b = this.props, organization = _b.organization, location = _b.location, api = _b.api;
        return (<DashboardList api={api} dashboards={dashboards} organization={organization} pageLinks={dashboardsPageLinks} location={location} onDashboardsChange={function () { return _this.onDashboardsChange(); }}/>);
    };
    ManageDashboards.prototype.getTitle = function () {
        return t('Dashboards');
    };
    ManageDashboards.prototype.onCreate = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        trackAnalyticsEvent({
            eventKey: 'dashboards_manage.create.start',
            eventName: 'Dashboards Manager: Dashboard Create Started',
            organization_id: parseInt(organization.id, 10),
        });
        browserHistory.push({
            pathname: "/organizations/" + organization.slug + "/dashboards/new/",
            query: location.query,
        });
    };
    ManageDashboards.prototype.renderBody = function () {
        var _this = this;
        var organization = this.props.organization;
        return (<Feature organization={organization} features={['dashboards-edit']} renderDisabled={this.renderNoAccess}>
        <SentryDocumentTitle title={t('Dashboards')} orgSlug={organization.slug}>
          <StyledPageContent>
            <LightWeightNoProjectMessage organization={organization}>
              <PageContent>
                <StyledPageHeader>
                  {t('Dashboards')}
                  <Button data-test-id="dashboard-create" onClick={function (event) {
                event.preventDefault();
                _this.onCreate();
            }} priority="primary" icon={<IconAdd size="xs" isCircled/>}>
                    {t('Create Dashboard')}
                  </Button>
                </StyledPageHeader>
                {this.renderActions()}
                {this.renderDashboards()}
              </PageContent>
            </LightWeightNoProjectMessage>
          </StyledPageContent>
        </SentryDocumentTitle>
      </Feature>);
    };
    return ManageDashboards;
}(AsyncView));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var StyledPageHeader = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-end;\n  font-size: ", ";\n  color: ", ";\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: flex-end;\n  font-size: ", ";\n  color: ", ";\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; }, space(2));
var StyledActions = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto max-content;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto max-content;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n  }\n"])), space(2), space(2), function (p) { return p.theme.breakpoints[0]; });
export default withApi(withOrganization(ManageDashboards));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map