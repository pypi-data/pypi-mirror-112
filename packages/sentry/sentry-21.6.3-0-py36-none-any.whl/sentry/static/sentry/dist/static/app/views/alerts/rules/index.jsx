import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __rest, __spreadArray } from "tslib";
import { Component } from 'react';
import styled from '@emotion/styled';
import flatten from 'lodash/flatten';
import { addErrorMessage } from 'app/actionCreators/indicator';
import AsyncComponent from 'app/components/asyncComponent';
import * as Layout from 'app/components/layouts/thirds';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import Pagination from 'app/components/pagination';
import { PanelTable } from 'app/components/panels';
import SearchBar from 'app/components/searchBar';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { IconArrow } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import Projects from 'app/utils/projects';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withTeams from 'app/utils/withTeams';
import AlertHeader from '../list/header';
import { isIssueAlert } from '../utils';
import RuleListRow from './row';
import TeamFilter, { getTeamParams } from './teamFilter';
var DOCS_URL = 'https://docs.sentry.io/product/alerts-notifications/metric-alerts/';
var AlertRulesList = /** @class */ (function (_super) {
    __extends(AlertRulesList, _super);
    function AlertRulesList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChangeFilter = function (_sectionId, activeFilters) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var _b = location.query, _cursor = _b.cursor, _page = _b.page, currentQuery = __rest(_b, ["cursor", "page"]);
            var teams = __spreadArray([], __read(activeFilters));
            router.push({
                pathname: location.pathname,
                query: __assign(__assign({}, currentQuery), { team: teams.length ? teams : '' }),
            });
        };
        _this.handleChangeSearch = function (name) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var _b = location.query, _cursor = _b.cursor, _page = _b.page, currentQuery = __rest(_b, ["cursor", "page"]);
            router.push({
                pathname: location.pathname,
                query: __assign(__assign({}, currentQuery), { name: name }),
            });
        };
        _this.handleDeleteRule = function (projectId, rule) { return __awaiter(_this, void 0, void 0, function () {
            var params, orgId, alertPath, _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        params = this.props.params;
                        orgId = params.orgId;
                        alertPath = isIssueAlert(rule) ? 'rules' : 'alert-rules';
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/" + alertPath + "/" + rule.id + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _a.sent();
                        this.reloadData();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        addErrorMessage(t('Error deleting rule'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AlertRulesList.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location, organization = _a.organization;
        var query = location.query;
        if (organization.features.includes('alert-details-redesign')) {
            query.expand = ['latestIncident'];
        }
        query.team = getTeamParams(query.team);
        if (organization.features.includes('alert-details-redesign') && !query.sort) {
            query.sort = ['incident_status', 'date_triggered'];
        }
        return [
            [
                'ruleList',
                "/organizations/" + (params && params.orgId) + "/combined-rules/",
                {
                    query: query,
                },
            ],
        ];
    };
    AlertRulesList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    AlertRulesList.prototype.renderFilterBar = function () {
        var _a;
        var _b = this.props, teams = _b.teams, location = _b.location;
        var selectedTeams = new Set(getTeamParams(location.query.team));
        return (<FilterWrapper>
        <TeamFilter teams={teams} selectedTeams={selectedTeams} handleChangeFilter={this.handleChangeFilter}/>
        <StyledSearchBar placeholder={t('Search by name')} query={(_a = location.query) === null || _a === void 0 ? void 0 : _a.name} onSearch={this.handleChangeSearch}/>
      </FilterWrapper>);
    };
    AlertRulesList.prototype.renderList = function () {
        var _this = this;
        var _a = this.props, orgId = _a.params.orgId, query = _a.location.query, organization = _a.organization, teams = _a.teams;
        var _b = this.state, loading = _b.loading, _c = _b.ruleList, ruleList = _c === void 0 ? [] : _c, ruleListPageLinks = _b.ruleListPageLinks;
        var allProjectsFromIncidents = new Set(flatten(ruleList === null || ruleList === void 0 ? void 0 : ruleList.map(function (_a) {
            var projects = _a.projects;
            return projects;
        })));
        var sort = {
            asc: query.asc === '1',
            field: query.sort || 'date_added',
        };
        var _cursor = query.cursor, _page = query.page, currentQuery = __rest(query, ["cursor", "page"]);
        var hasAlertList = organization.features.includes('alert-details-redesign');
        var isAlertRuleSort = sort.field.includes('incident_status') || sort.field.includes('date_triggered');
        var sortArrow = (<IconArrow color="gray300" size="xs" direction={sort.asc ? 'up' : 'down'}/>);
        var userTeams = new Set(teams.filter(function (_a) {
            var isMember = _a.isMember;
            return isMember;
        }).map(function (_a) {
            var id = _a.id;
            return id;
        }));
        return (<StyledLayoutBody>
        <Layout.Main fullWidth>
          {this.renderFilterBar()}
          <StyledPanelTable headers={__spreadArray(__spreadArray(__spreadArray(__spreadArray([], __read((hasAlertList
                ? [
                    // eslint-disable-next-line react/jsx-key
                    <StyledSortLink to={{
                            pathname: location.pathname,
                            query: __assign(__assign({}, currentQuery), { asc: sort.field === 'name' && !sort.asc ? '1' : undefined, sort: 'name' }),
                        }}>
                      {t('Alert Rule')} {sort.field === 'name' && sortArrow}
                    </StyledSortLink>,
                    // eslint-disable-next-line react/jsx-key
                    <StyledSortLink to={{
                            pathname: location.pathname,
                            query: __assign(__assign({}, currentQuery), { asc: isAlertRuleSort && !sort.asc ? '1' : undefined, sort: ['incident_status', 'date_triggered'] }),
                        }}>
                      {t('Status')} {isAlertRuleSort && sortArrow}
                    </StyledSortLink>,
                ]
                : [
                    t('Type'),
                    // eslint-disable-next-line react/jsx-key
                    <StyledSortLink to={{
                            pathname: location.pathname,
                            query: __assign(__assign({}, currentQuery), { asc: sort.field === 'name' && !sort.asc ? '1' : undefined, sort: 'name' }),
                        }}>
                      {t('Alert Name')} {sort.field === 'name' && sortArrow}
                    </StyledSortLink>,
                ]))), [
                t('Project'),
                t('Team')
            ]), __read((hasAlertList ? [] : [t('Created By')]))), [
                // eslint-disable-next-line react/jsx-key
                <StyledSortLink to={{
                        pathname: location.pathname,
                        query: __assign(__assign({}, currentQuery), { asc: sort.field === 'date_added' && !sort.asc ? '1' : undefined, sort: 'date_added' }),
                    }}>
                {t('Created')} {sort.field === 'date_added' && sortArrow}
              </StyledSortLink>,
                t('Actions'),
            ])} isLoading={loading} isEmpty={(ruleList === null || ruleList === void 0 ? void 0 : ruleList.length) === 0} emptyMessage={t('No alert rules found for the current query.')} emptyAction={<EmptyStateAction>
                {tct('Learn more about [link:Alerts]', {
                    link: <ExternalLink href={DOCS_URL}/>,
                })}
              </EmptyStateAction>} hasAlertList={hasAlertList}>
            <Projects orgId={orgId} slugs={Array.from(allProjectsFromIncidents)}>
              {function (_a) {
                var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
                return ruleList.map(function (rule) { return (<RuleListRow 
                // Metric and issue alerts can have the same id
                key={(isIssueAlert(rule) ? 'metric' : 'issue') + "-" + rule.id} projectsLoaded={initiallyLoaded} projects={projects} rule={rule} orgId={orgId} onDelete={_this.handleDeleteRule} organization={organization} userTeams={userTeams}/>); });
            }}
            </Projects>
          </StyledPanelTable>
          <Pagination pageLinks={ruleListPageLinks}/>
        </Layout.Main>
      </StyledLayoutBody>);
    };
    AlertRulesList.prototype.renderBody = function () {
        var _a = this.props, params = _a.params, organization = _a.organization, router = _a.router;
        var orgId = params.orgId;
        return (<SentryDocumentTitle title={t('Alerts')} orgSlug={orgId}>
        <GlobalSelectionHeader organization={organization} showDateSelector={false} showEnvironmentSelector={false}>
          <AlertHeader organization={organization} router={router} activeTab="rules"/>
          {this.renderList()}
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return AlertRulesList;
}(AsyncComponent));
var AlertRulesListContainer = /** @class */ (function (_super) {
    __extends(AlertRulesListContainer, _super);
    function AlertRulesListContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AlertRulesListContainer.prototype.componentDidMount = function () {
        this.trackView();
    };
    AlertRulesListContainer.prototype.componentDidUpdate = function (prevProps) {
        var _a, _b;
        var location = this.props.location;
        if (((_a = prevProps.location.query) === null || _a === void 0 ? void 0 : _a.sort) !== ((_b = location.query) === null || _b === void 0 ? void 0 : _b.sort)) {
            this.trackView();
        }
    };
    AlertRulesListContainer.prototype.trackView = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        trackAnalyticsEvent({
            eventKey: 'alert_rules.viewed',
            eventName: 'Alert Rules: Viewed',
            organization_id: organization.id,
            sort: Array.isArray(location.query.sort)
                ? location.query.sort.join(',')
                : location.query.sort,
        });
    };
    AlertRulesListContainer.prototype.render = function () {
        return <AlertRulesList {...this.props}/>;
    };
    return AlertRulesListContainer;
}(Component));
export default withGlobalSelection(withTeams(AlertRulesListContainer));
var StyledLayoutBody = styled(Layout.Body)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: -20px;\n"], ["\n  margin-bottom: -20px;\n"])));
var StyledSortLink = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: inherit;\n\n  :hover {\n    color: inherit;\n  }\n"], ["\n  color: inherit;\n\n  :hover {\n    color: inherit;\n  }\n"])));
var FilterWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  margin-bottom: ", ";\n"])), space(1.5));
var StyledSearchBar = styled(SearchBar)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex-grow: 1;\n  margin-left: ", ";\n"], ["\n  flex-grow: 1;\n  margin-left: ", ";\n"])), space(1.5));
var StyledPanelTable = styled(PanelTable)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  overflow: auto;\n  @media (min-width: ", ") {\n    overflow: initial;\n  }\n\n  grid-template-columns: auto 1.5fr 1fr 1fr ", " 1fr auto;\n  white-space: nowrap;\n  font-size: ", ";\n"], ["\n  overflow: auto;\n  @media (min-width: ", ") {\n    overflow: initial;\n  }\n\n  grid-template-columns: auto 1.5fr 1fr 1fr ", " 1fr auto;\n  white-space: nowrap;\n  font-size: ", ";\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return (!p.hasAlertList ? '1fr' : ''); }, function (p) { return p.theme.fontSizeMedium; });
var EmptyStateAction = styled('p')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map