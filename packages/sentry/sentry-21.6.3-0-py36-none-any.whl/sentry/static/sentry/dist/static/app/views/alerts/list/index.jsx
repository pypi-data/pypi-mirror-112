import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __rest, __spreadArray } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import flatten from 'lodash/flatten';
import { promptsCheck, promptsUpdate } from 'app/actionCreators/prompts';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import CreateAlertButton from 'app/components/createAlertButton';
import * as Layout from 'app/components/layouts/thirds';
import ExternalLink from 'app/components/links/externalLink';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import Pagination from 'app/components/pagination';
import { PanelTable } from 'app/components/panels';
import SearchBar from 'app/components/searchBar';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { IconInfo } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import Projects from 'app/utils/projects';
import withOrganization from 'app/utils/withOrganization';
import withTeams from 'app/utils/withTeams';
import TeamFilter, { getTeamParams } from '../rules/teamFilter';
import AlertHeader from './header';
import Onboarding from './onboarding';
import AlertListRow from './row';
var DOCS_URL = 'https://docs.sentry.io/workflow/alerts-notifications/alerts/?_ga=2.21848383.580096147.1592364314-1444595810.1582160976';
var IncidentsList = /** @class */ (function (_super) {
    __extends(IncidentsList, _super);
    function IncidentsList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChangeSearch = function (title) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var _b = location.query, _cursor = _b.cursor, _page = _b.page, currentQuery = __rest(_b, ["cursor", "page"]);
            router.push({
                pathname: location.pathname,
                query: __assign(__assign({}, currentQuery), { title: title }),
            });
        };
        _this.handleChangeFilter = function (sectionId, activeFilters) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var _b = location.query, _cursor = _b.cursor, _page = _b.page, currentQuery = __rest(_b, ["cursor", "page"]);
            var team = currentQuery.team;
            if (sectionId === 'teams') {
                team = activeFilters.size ? __spreadArray([], __read(activeFilters)) : '';
            }
            var status = currentQuery.status;
            if (sectionId === 'status') {
                status = activeFilters.size ? __spreadArray([], __read(activeFilters)) : '';
            }
            router.push({
                pathname: location.pathname,
                query: __assign(__assign({}, currentQuery), { status: status, 
                    // Preserve empty team query parameter
                    team: team.length === 0 ? '' : team }),
            });
        };
        return _this;
    }
    IncidentsList.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location, organization = _a.organization;
        var query = location.query;
        var status = this.getQueryStatus(query.status);
        // Filtering by one status, both does nothing
        if (status.length === 1) {
            query.status = status;
        }
        query.team = getTeamParams(query.team);
        if (organization.features.includes('alert-details-redesign')) {
            query.expand = ['original_alert_rule'];
        }
        return [['incidentList', "/organizations/" + (params === null || params === void 0 ? void 0 : params.orgId) + "/incidents/", { query: query }]];
    };
    IncidentsList.prototype.getQueryStatus = function (status) {
        if (Array.isArray(status)) {
            return status;
        }
        if (status === '') {
            return [];
        }
        return ['open', 'closed'].includes(status) ? [status] : [];
    };
    /**
     * If our incidentList is empty, determine if we've configured alert rules or
     * if the user has seen the welcome prompt.
     */
    IncidentsList.prototype.onLoadAllEndpointsSuccess = function () {
        return __awaiter(this, void 0, void 0, function () {
            var incidentList, _a, params, location, organization, alertRules, hasAlertRule, prompt, firstVisitShown;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        incidentList = this.state.incidentList;
                        if (!incidentList || incidentList.length !== 0) {
                            this.setState({ hasAlertRule: true, firstVisitShown: false });
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        _a = this.props, params = _a.params, location = _a.location, organization = _a.organization;
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + (params === null || params === void 0 ? void 0 : params.orgId) + "/alert-rules/", {
                                method: 'GET',
                                query: location.query,
                            })];
                    case 1:
                        alertRules = _b.sent();
                        hasAlertRule = alertRules.length > 0;
                        // We've already configured alert rules, no need to check if we should show
                        // the "first time welcome" prompt
                        if (hasAlertRule) {
                            this.setState({ hasAlertRule: hasAlertRule, firstVisitShown: false, loading: false });
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, promptsCheck(this.api, {
                                organizationId: organization.id,
                                feature: 'alert_stream',
                            })];
                    case 2:
                        prompt = _b.sent();
                        firstVisitShown = !(prompt === null || prompt === void 0 ? void 0 : prompt.dismissedTime);
                        if (firstVisitShown) {
                            // Prompt has not been seen, mark the prompt as seen immediately so they
                            // don't see it again
                            promptsUpdate(this.api, {
                                feature: 'alert_stream',
                                organizationId: organization.id,
                                status: 'dismissed',
                            });
                        }
                        this.setState({ hasAlertRule: hasAlertRule, firstVisitShown: firstVisitShown, loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    IncidentsList.prototype.renderFilterBar = function () {
        var _a;
        var _b = this.props, teams = _b.teams, location = _b.location;
        var selectedTeams = new Set(getTeamParams(location.query.team));
        var selectedStatus = new Set(this.getQueryStatus(location.query.status));
        return (<FilterWrapper>
        <TeamFilter showStatus teams={teams} selectedStatus={selectedStatus} selectedTeams={selectedTeams} handleChangeFilter={this.handleChangeFilter}/>
        <StyledSearchBar placeholder={t('Search by name')} query={(_a = location.query) === null || _a === void 0 ? void 0 : _a.name} onSearch={this.handleChangeSearch}/>
      </FilterWrapper>);
    };
    IncidentsList.prototype.tryRenderOnboarding = function () {
        var firstVisitShown = this.state.firstVisitShown;
        var organization = this.props.organization;
        if (!firstVisitShown) {
            return null;
        }
        var actions = (<Fragment>
        <Button size="small" external href={DOCS_URL}>
          {t('View Features')}
        </Button>
        <CreateAlertButton organization={organization} iconProps={{ size: 'xs' }} size="small" priority="primary" referrer="alert_stream">
          {t('Create Alert Rule')}
        </CreateAlertButton>
      </Fragment>);
        return <Onboarding actions={actions}/>;
    };
    IncidentsList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    IncidentsList.prototype.renderList = function () {
        var _a;
        var _b = this.state, loading = _b.loading, incidentList = _b.incidentList, incidentListPageLinks = _b.incidentListPageLinks, hasAlertRule = _b.hasAlertRule;
        var _c = this.props, orgId = _c.params.orgId, organization = _c.organization;
        var allProjectsFromIncidents = new Set(flatten(incidentList === null || incidentList === void 0 ? void 0 : incidentList.map(function (_a) {
            var projects = _a.projects;
            return projects;
        })));
        var checkingForAlertRules = incidentList && incidentList.length === 0 && hasAlertRule === undefined
            ? true
            : false;
        var showLoadingIndicator = loading || checkingForAlertRules;
        return (<Fragment>
        {(_a = this.tryRenderOnboarding()) !== null && _a !== void 0 ? _a : (<PanelTable isLoading={showLoadingIndicator} isEmpty={(incidentList === null || incidentList === void 0 ? void 0 : incidentList.length) === 0} emptyMessage={t('No incidents exist for the current query.')} emptyAction={<EmptyStateAction>
                {tct('Learn more about [link:Metric Alerts]', {
                        link: <ExternalLink href={DOCS_URL}/>,
                    })}
              </EmptyStateAction>} headers={[
                    t('Alert Rule'),
                    t('Triggered'),
                    t('Duration'),
                    t('Project'),
                    t('Alert ID'),
                    t('Team'),
                ]}>
            <Projects orgId={orgId} slugs={Array.from(allProjectsFromIncidents)}>
              {function (_a) {
                    var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
                    return incidentList.map(function (incident) { return (<AlertListRow key={incident.id} projectsLoaded={initiallyLoaded} projects={projects} incident={incident} orgId={orgId} organization={organization}/>); });
                }}
            </Projects>
          </PanelTable>)}
        <Pagination pageLinks={incidentListPageLinks}/>
      </Fragment>);
    };
    IncidentsList.prototype.renderBody = function () {
        var _a = this.props, params = _a.params, organization = _a.organization, router = _a.router;
        var orgId = params.orgId;
        return (<SentryDocumentTitle title={t('Alerts')} orgSlug={orgId}>
        <GlobalSelectionHeader organization={organization} showDateSelector={false}>
          <AlertHeader organization={organization} router={router} activeTab="stream"/>
          <StyledLayoutBody>
            <Layout.Main fullWidth>
              {!this.tryRenderOnboarding() && (<Fragment>
                  <Feature features={['alert-details-redesign']} organization={organization}>
                    <StyledAlert icon={<IconInfo />}>
                      {t('This page only shows metric alerts.')}
                    </StyledAlert>
                  </Feature>
                  {this.renderFilterBar()}
                </Fragment>)}
              {this.renderList()}
            </Layout.Main>
          </StyledLayoutBody>
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return IncidentsList;
}(AsyncComponent));
var IncidentsListContainer = /** @class */ (function (_super) {
    __extends(IncidentsListContainer, _super);
    function IncidentsListContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IncidentsListContainer.prototype.componentDidMount = function () {
        this.trackView();
    };
    IncidentsListContainer.prototype.componentDidUpdate = function (nextProps) {
        var _a, _b;
        if (((_a = nextProps.location.query) === null || _a === void 0 ? void 0 : _a.status) !== ((_b = this.props.location.query) === null || _b === void 0 ? void 0 : _b.status)) {
            this.trackView();
        }
    };
    IncidentsListContainer.prototype.trackView = function () {
        var organization = this.props.organization;
        trackAnalyticsEvent({
            eventKey: 'alert_stream.viewed',
            eventName: 'Alert Stream: Viewed',
            organization_id: organization.id,
        });
    };
    IncidentsListContainer.prototype.renderNoAccess = function () {
        return (<Layout.Body>
        <Layout.Main fullWidth>
          <Alert type="warning">{t("You don't have access to this feature")}</Alert>
        </Layout.Main>
      </Layout.Body>);
    };
    IncidentsListContainer.prototype.render = function () {
        var organization = this.props.organization;
        return (<Feature features={['organizations:incidents']} organization={organization} hookName="feature-disabled:alerts-page" renderDisabled={this.renderNoAccess}>
        <IncidentsList {...this.props}/>
      </Feature>);
    };
    return IncidentsListContainer;
}(Component));
var StyledAlert = styled(Alert)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(1.5));
var FilterWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  margin-bottom: ", ";\n"])), space(1.5));
var StyledSearchBar = styled(SearchBar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-grow: 1;\n  margin-left: ", ";\n"], ["\n  flex-grow: 1;\n  margin-left: ", ";\n"])), space(1.5));
var StyledLayoutBody = styled(Layout.Body)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: -20px;\n"], ["\n  margin-bottom: -20px;\n"])));
var EmptyStateAction = styled('p')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
export default withOrganization(withTeams(IncidentsListContainer));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map