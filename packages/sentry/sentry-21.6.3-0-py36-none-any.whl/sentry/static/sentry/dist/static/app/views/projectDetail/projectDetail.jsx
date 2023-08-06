import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import styled from '@emotion/styled';
import { updateProjects } from 'app/actionCreators/globalSelection';
import { fetchTagValues } from 'app/actionCreators/tags';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import Breadcrumbs from 'app/components/breadcrumbs';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import CreateAlertButton from 'app/components/createAlertButton';
import GlobalAppStoreConnectUpdateAlert from 'app/components/globalAppStoreConnectUpdateAlert';
import GlobalSdkUpdateAlert from 'app/components/globalSdkUpdateAlert';
import IdBadge from 'app/components/idBadge';
import * as Layout from 'app/components/layouts/thirds';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import MissingProjectMembership from 'app/components/projects/missingProjectMembership';
import TextOverflow from 'app/components/textOverflow';
import { IconSettings, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import routeTitleGen from 'app/utils/routeTitle';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withProjects from 'app/utils/withProjects';
import AsyncView from 'app/views/asyncView';
import ProjectScoreCards from './projectScoreCards/projectScoreCards';
import ProjectCharts from './projectCharts';
import ProjectFilters from './projectFilters';
import ProjectIssues from './projectIssues';
import ProjectLatestAlerts from './projectLatestAlerts';
import ProjectLatestReleases from './projectLatestReleases';
import ProjectQuickLinks from './projectQuickLinks';
import ProjectTeamAccess from './projectTeamAccess';
var ProjectDetail = /** @class */ (function (_super) {
    __extends(ProjectDetail, _super);
    function ProjectDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleProjectChange = function (selectedProjects) {
            var _a = _this.props, projects = _a.projects, router = _a.router, location = _a.location, organization = _a.organization;
            var newlySelectedProject = projects.find(function (p) { return p.id === String(selectedProjects[0]); });
            // if we change project in global header, we need to sync the project slug in the URL
            if (newlySelectedProject === null || newlySelectedProject === void 0 ? void 0 : newlySelectedProject.id) {
                router.replace({
                    pathname: "/organizations/" + organization.slug + "/projects/" + newlySelectedProject.slug + "/",
                    query: __assign(__assign({}, location.query), { project: newlySelectedProject.id, environment: undefined }),
                });
            }
        };
        _this.handleSearch = function (query) {
            var _a = _this.props, router = _a.router, location = _a.location;
            router.replace({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { query: query }),
            });
        };
        _this.tagValueLoader = function (key, search) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            var projectId = location.query.project;
            return fetchTagValues(_this.api, organization.slug, key, search, projectId ? [projectId] : null, location.query);
        };
        return _this;
    }
    ProjectDetail.prototype.getTitle = function () {
        var params = this.props.params;
        return routeTitleGen(t('Project %s', params.projectId), params.orgId, false);
    };
    ProjectDetail.prototype.componentDidMount = function () {
        this.syncProjectWithSlug();
        if (this.props.location.query.project) {
            this.fetchSessionsExistence();
        }
    };
    ProjectDetail.prototype.componentDidUpdate = function (prevProps) {
        this.syncProjectWithSlug();
        if (prevProps.location.query.project !== this.props.location.query.project) {
            this.fetchSessionsExistence();
        }
    };
    Object.defineProperty(ProjectDetail.prototype, "project", {
        get: function () {
            var _a = this.props, projects = _a.projects, params = _a.params;
            return projects.find(function (p) { return p.slug === params.projectId; });
        },
        enumerable: false,
        configurable: true
    });
    ProjectDetail.prototype.fetchSessionsExistence = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, organization, location, _b, projectId, query, response, _c;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, location = _a.location;
                        _b = location.query, projectId = _b.project, query = _b.query;
                        if (!projectId) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            hasSessions: null,
                        });
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + organization.slug + "/sessions/", {
                                query: {
                                    project: projectId,
                                    field: 'sum(session)',
                                    statsPeriod: '90d',
                                    interval: '1d',
                                    query: query,
                                },
                            })];
                    case 2:
                        response = _d.sent();
                        this.setState({
                            hasSessions: response.groups[0].totals['sum(session)'] > 0,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _c = _d.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ProjectDetail.prototype.syncProjectWithSlug = function () {
        var _a;
        var _b = this.props, router = _b.router, location = _b.location;
        var projectId = (_a = this.project) === null || _a === void 0 ? void 0 : _a.id;
        if (projectId && projectId !== location.query.project) {
            // if someone visits /organizations/sentry/projects/javascript/ (without ?project=XXX) we need to update URL and globalSelection with the right project ID
            updateProjects([Number(projectId)], router);
        }
    };
    ProjectDetail.prototype.isProjectStabilized = function () {
        var _a;
        var _b = this.props, selection = _b.selection, location = _b.location;
        var projectId = (_a = this.project) === null || _a === void 0 ? void 0 : _a.id;
        return (defined(projectId) &&
            projectId === location.query.project &&
            projectId === String(selection.projects[0]));
    };
    ProjectDetail.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectDetail.prototype.renderNoAccess = function (project) {
        var organization = this.props.organization;
        return (<PageContent>
        <MissingProjectMembership organization={organization} projectSlug={project.slug}/>
      </PageContent>);
    };
    ProjectDetail.prototype.renderProjectNotFound = function () {
        return (<PageContent>
        <Alert type="error" icon={<IconWarning />}>
          {t('This project could not be found.')}
        </Alert>
      </PageContent>);
    };
    ProjectDetail.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, params = _a.params, location = _a.location, router = _a.router, loadingProjects = _a.loadingProjects, selection = _a.selection;
        var project = this.project;
        var hasSessions = this.state.hasSessions;
        var query = location.query.query;
        var hasPerformance = organization.features.includes('performance-view');
        var hasTransactions = hasPerformance && (project === null || project === void 0 ? void 0 : project.firstTransactionEvent);
        var isProjectStabilized = this.isProjectStabilized();
        var visibleCharts = ['chart1'];
        if (hasTransactions || hasSessions) {
            visibleCharts.push('chart2');
        }
        if (!loadingProjects && !project) {
            return this.renderProjectNotFound();
        }
        if (!loadingProjects && project && !project.hasAccess) {
            return this.renderNoAccess(project);
        }
        return (<GlobalSelectionHeader disableMultipleProjectSelection skipLoadLastUsed onUpdateProjects={this.handleProjectChange}>
        <LightWeightNoProjectMessage organization={organization}>
          <StyledPageContent>
            <Layout.Header>
              <Layout.HeaderContent>
                <Breadcrumbs crumbs={[
                {
                    to: "/organizations/" + params.orgId + "/projects/",
                    label: t('Projects'),
                },
                { label: t('Project Details') },
            ]}/>
                <Layout.Title>
                  <TextOverflow>
                    {project && (<IdBadge project={project} avatarSize={28} displayName={params.projectId} disableLink/>)}
                  </TextOverflow>
                </Layout.Title>
              </Layout.HeaderContent>

              <Layout.HeaderActions>
                <ButtonBar gap={1}>
                  <Button to={
            // if we are still fetching project, we can use project slug to build issue stream url and let the redirect handle it
            (project === null || project === void 0 ? void 0 : project.id)
                ? "/organizations/" + params.orgId + "/issues/?project=" + project.id
                : "/" + params.orgId + "/" + params.projectId}>
                    {t('View All Issues')}
                  </Button>
                  <CreateAlertButton organization={organization} projectSlug={params.projectId}/>
                  <Button icon={<IconSettings />} label={t('Settings')} to={"/settings/" + params.orgId + "/projects/" + params.projectId + "/"}/>
                </ButtonBar>
              </Layout.HeaderActions>
            </Layout.Header>

            <Layout.Body>
              <StyledSdkUpdatesAlert />
              <StyledGlobalAppStoreConnectUpdateAlert project={project} organization={organization}/>
              <Layout.Main>
                <Feature features={['semver']} organization={organization}>
                  <ProjectFiltersWrapper>
                    <ProjectFilters query={query} onSearch={this.handleSearch} tagValueLoader={this.tagValueLoader}/>
                  </ProjectFiltersWrapper>
                </Feature>

                <ProjectScoreCards organization={organization} isProjectStabilized={isProjectStabilized} selection={selection} hasSessions={hasSessions} hasTransactions={hasTransactions} query={query}/>
                {isProjectStabilized && (<Fragment>
                    {visibleCharts.map(function (id, index) { return (<ProjectCharts location={location} organization={organization} router={router} key={"project-charts-" + id} chartId={id} chartIndex={index} projectId={project === null || project === void 0 ? void 0 : project.id} hasSessions={hasSessions} hasTransactions={!!hasTransactions} visibleCharts={visibleCharts} query={query}/>); })}
                    <ProjectIssues organization={organization} location={location} projectId={selection.projects[0]} query={query} api={this.api}/>
                  </Fragment>)}
              </Layout.Main>
              <Layout.Side>
                <ProjectTeamAccess organization={organization} project={project}/>
                <Feature features={['incidents']} organization={organization}>
                  <ProjectLatestAlerts organization={organization} projectSlug={params.projectId} location={location} isProjectStabilized={isProjectStabilized}/>
                </Feature>
                <ProjectLatestReleases organization={organization} projectSlug={params.projectId} projectId={project === null || project === void 0 ? void 0 : project.id} location={location} isProjectStabilized={isProjectStabilized}/>
                <ProjectQuickLinks organization={organization} project={project} location={location}/>
              </Layout.Side>
            </Layout.Body>
          </StyledPageContent>
        </LightWeightNoProjectMessage>
      </GlobalSelectionHeader>);
    };
    return ProjectDetail;
}(AsyncView));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var ProjectFiltersWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var StyledSdkUpdatesAlert = styled(GlobalSdkUpdateAlert)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
StyledSdkUpdatesAlert.defaultProps = {
    Wrapper: function (p) { return <Layout.Main fullWidth {...p}/>; },
};
var StyledGlobalAppStoreConnectUpdateAlert = styled(GlobalAppStoreConnectUpdateAlert)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
StyledGlobalAppStoreConnectUpdateAlert.defaultProps = {
    Wrapper: function (p) { return <Layout.Main fullWidth {...p}/>; },
};
export default withProjects(withGlobalSelection(ProjectDetail));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=projectDetail.jsx.map