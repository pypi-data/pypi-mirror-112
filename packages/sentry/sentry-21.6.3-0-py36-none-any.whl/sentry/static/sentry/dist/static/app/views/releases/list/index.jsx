import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spreadArray } from "tslib";
import { Fragment } from 'react';
import { forceCheck } from 'react-lazyload';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import { fetchTagValues } from 'app/actionCreators/tags';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import ExternalLink from 'app/components/links/externalLink';
import LoadingIndicator from 'app/components/loadingIndicator';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { getRelativeSummary } from 'app/components/organizations/timeRangeSelector/utils';
import PageHeading from 'app/components/pageHeading';
import Pagination from 'app/components/pagination';
import SearchBar from 'app/components/searchBar';
import SmartSearchBar from 'app/components/smartSearchBar';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { desktop, mobile, releaseHealth } from 'app/data/platformCategories';
import { IconInfo } from 'app/icons';
import { t } from 'app/locale';
import { PageContent, PageHeader } from 'app/styles/organization';
import space from 'app/styles/space';
import { ReleaseStatus, } from 'app/types';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import Projects from 'app/utils/projects';
import routeTitleGen from 'app/utils/routeTitle';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import ReleaseArchivedNotice from '../detail/overview/releaseArchivedNotice';
import ReleaseHealthRequest from '../utils/releaseHealthRequest';
import ReleaseAdoptionChart from './releaseAdoptionChart';
import ReleaseCard from './releaseCard';
import ReleaseDisplayOptions from './releaseDisplayOptions';
import ReleaseListSortOptions from './releaseListSortOptions';
import ReleaseListStatusOptions from './releaseListStatusOptions';
import ReleasePromo from './releasePromo';
import { DisplayOption, SortOption, StatusOption } from './utils';
var supportedTags = {
    'sentry.semver': {
        key: 'sentry.semver',
        name: 'sentry.semver',
    },
    release: {
        key: 'release',
        name: 'release',
    },
};
var ReleasesList = /** @class */ (function (_super) {
    __extends(ReleasesList, _super);
    function ReleasesList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        _this.shouldRenderBadRequests = true;
        _this.handleSearch = function (query) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, query: query }) }));
        };
        _this.handleSortBy = function (sort) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, sort: sort }) }));
        };
        _this.handleDisplay = function (display) {
            var _a = _this.props, location = _a.location, router = _a.router;
            var sort = location.query.sort;
            if (sort === SortOption.USERS_24_HOURS && display === DisplayOption.SESSIONS)
                sort = SortOption.SESSIONS_24_HOURS;
            else if (sort === SortOption.SESSIONS_24_HOURS && display === DisplayOption.USERS)
                sort = SortOption.USERS_24_HOURS;
            else if (sort === SortOption.CRASH_FREE_USERS && display === DisplayOption.SESSIONS)
                sort = SortOption.CRASH_FREE_SESSIONS;
            else if (sort === SortOption.CRASH_FREE_SESSIONS && display === DisplayOption.USERS)
                sort = SortOption.CRASH_FREE_USERS;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, display: display, sort: sort }) }));
        };
        _this.handleStatus = function (status) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, status: status }) }));
        };
        _this.trackAddReleaseHealth = function () {
            var _a = _this.props, organization = _a.organization, selection = _a.selection;
            if (organization.id && selection.projects[0]) {
                trackAnalyticsEvent({
                    eventKey: "releases_list.click_add_release_health",
                    eventName: "Releases List: Click Add Release Health",
                    organization_id: parseInt(organization.id, 10),
                    project_id: selection.projects[0],
                });
            }
        };
        _this.tagValueLoader = function (key, search) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            var projectId = location.query.project;
            return fetchTagValues(_this.api, organization.slug, key, search, projectId ? [projectId] : null, location.query);
        };
        _this.getTagValues = function (tag, currentQuery) { return __awaiter(_this, void 0, void 0, function () {
            var values;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.tagValueLoader(tag.key, currentQuery)];
                    case 1:
                        values = _a.sent();
                        return [2 /*return*/, values.map(function (_a) {
                                var value = _a.value;
                                return value;
                            })];
                }
            });
        }); };
        return _this;
    }
    ReleasesList.prototype.getTitle = function () {
        return routeTitleGen(t('Releases'), this.props.organization.slug, false);
    };
    ReleasesList.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var statsPeriod = location.query.statsPeriod;
        var activeSort = this.getSort();
        var activeStatus = this.getStatus();
        var query = __assign(__assign({}, pick(location.query, ['project', 'environment', 'cursor', 'query', 'sort'])), { summaryStatsPeriod: statsPeriod, per_page: 20, flatten: activeSort === SortOption.DATE ? 0 : 1, adoptionStages: 1, status: activeStatus === StatusOption.ARCHIVED
                ? ReleaseStatus.Archived
                : ReleaseStatus.Active });
        var endpoints = [
            [
                'releases',
                "/organizations/" + organization.slug + "/releases/",
                { query: query },
                { disableEntireQuery: true },
            ],
        ];
        return endpoints;
    };
    ReleasesList.prototype.componentDidMount = function () {
        if (this.props.location.query.project) {
            this.fetchSessionsExistence();
        }
    };
    ReleasesList.prototype.componentDidUpdate = function (prevProps, prevState) {
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
        if (prevProps.location.query.project !== this.props.location.query.project) {
            this.fetchSessionsExistence();
        }
        if (prevState.releases !== this.state.releases) {
            /**
             * Manually trigger checking for elements in viewport.
             * Helpful when LazyLoad components enter the viewport without resize or scroll events,
             * https://github.com/twobin/react-lazyload#forcecheck
             *
             * HealthStatsCharts are being rendered only when they are scrolled into viewport.
             * This is how we re-check them without scrolling once releases change as this view
             * uses shouldReload=true and there is no reloading happening.
             */
            forceCheck();
        }
    };
    ReleasesList.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return typeof query === 'string' ? query : undefined;
    };
    ReleasesList.prototype.getSort = function () {
        var sort = this.props.location.query.sort;
        switch (sort) {
            case SortOption.CRASH_FREE_USERS:
                return SortOption.CRASH_FREE_USERS;
            case SortOption.CRASH_FREE_SESSIONS:
                return SortOption.CRASH_FREE_SESSIONS;
            case SortOption.SESSIONS:
                return SortOption.SESSIONS;
            case SortOption.USERS_24_HOURS:
                return SortOption.USERS_24_HOURS;
            case SortOption.SESSIONS_24_HOURS:
                return SortOption.SESSIONS_24_HOURS;
            case SortOption.BUILD:
                return SortOption.BUILD;
            case SortOption.SEMVER:
                return SortOption.SEMVER;
            case SortOption.ADOPTION:
                return SortOption.ADOPTION;
            default:
                return SortOption.DATE;
        }
    };
    ReleasesList.prototype.getDisplay = function () {
        var display = this.props.location.query.display;
        switch (display) {
            case DisplayOption.USERS:
                return DisplayOption.USERS;
            default:
                return DisplayOption.SESSIONS;
        }
    };
    ReleasesList.prototype.getStatus = function () {
        var status = this.props.location.query.status;
        switch (status) {
            case StatusOption.ARCHIVED:
                return StatusOption.ARCHIVED;
            default:
                return StatusOption.ACTIVE;
        }
    };
    ReleasesList.prototype.getSelectedProject = function () {
        var _a;
        var _b = this.props, selection = _b.selection, organization = _b.organization;
        var selectedProjectId = selection.projects && selection.projects.length === 1 && selection.projects[0];
        return (_a = organization.projects) === null || _a === void 0 ? void 0 : _a.find(function (p) { return p.id === "" + selectedProjectId; });
    };
    ReleasesList.prototype.fetchSessionsExistence = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, organization, location, projectId, response, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, location = _a.location;
                        projectId = location.query.project;
                        if (!projectId) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            hasSessions: null,
                        });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + organization.slug + "/sessions/", {
                                query: {
                                    project: projectId,
                                    field: 'sum(session)',
                                    statsPeriod: '90d',
                                    interval: '1d',
                                },
                            })];
                    case 2:
                        response = _c.sent();
                        this.setState({
                            hasSessions: response.groups[0].totals['sum(session)'] > 0,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ReleasesList.prototype.shouldShowLoadingIndicator = function () {
        var _a = this.state, loading = _a.loading, releases = _a.releases, reloading = _a.reloading;
        return (loading && !reloading) || (loading && !(releases === null || releases === void 0 ? void 0 : releases.length));
    };
    ReleasesList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ReleasesList.prototype.renderError = function () {
        return this.renderBody();
    };
    ReleasesList.prototype.renderEmptyMessage = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, selection = _a.selection;
        var statsPeriod = location.query.statsPeriod;
        var searchQuery = this.getQuery();
        var activeSort = this.getSort();
        var activeStatus = this.getStatus();
        if (searchQuery && searchQuery.length) {
            return (<EmptyStateWarning small>{t('There are no releases that match') + ": '" + searchQuery + "'."}</EmptyStateWarning>);
        }
        if (activeSort === SortOption.USERS_24_HOURS) {
            return (<EmptyStateWarning small>
          {t('There are no releases with active user data (users in the last 24 hours).')}
        </EmptyStateWarning>);
        }
        if (activeSort === SortOption.SESSIONS_24_HOURS) {
            return (<EmptyStateWarning small>
          {t('There are no releases with active session data (sessions in the last 24 hours).')}
        </EmptyStateWarning>);
        }
        if (activeSort === SortOption.BUILD || activeSort === SortOption.SEMVER) {
            return (<EmptyStateWarning small>
          {t('There are no releases with semantic versioning.')}
        </EmptyStateWarning>);
        }
        if (activeSort !== SortOption.DATE) {
            var relativePeriod = getRelativeSummary(statsPeriod || DEFAULT_STATS_PERIOD).toLowerCase();
            return (<EmptyStateWarning small>
          {t('There are no releases with data in the') + " " + relativePeriod + "."}
        </EmptyStateWarning>);
        }
        if (activeStatus === StatusOption.ARCHIVED) {
            return (<EmptyStateWarning small>
          {t('There are no archived releases.')}
        </EmptyStateWarning>);
        }
        return (<ReleasePromo organization={organization} projectId={selection.projects.filter(function (p) { return p !== ALL_ACCESS_PROJECTS; })[0]}/>);
    };
    ReleasesList.prototype.renderHealthCta = function () {
        var _this = this;
        var organization = this.props.organization;
        var _a = this.state, hasSessions = _a.hasSessions, releases = _a.releases;
        var selectedProject = this.getSelectedProject();
        if (!selectedProject || hasSessions !== false || !(releases === null || releases === void 0 ? void 0 : releases.length)) {
            return null;
        }
        return (<Projects orgId={organization.slug} slugs={[selectedProject.slug]}>
        {function (_a) {
                var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetchError = _a.fetchError;
                var project = projects && projects.length === 1 && projects[0];
                var projectCanHaveReleases = project && project.platform && releaseHealth.includes(project.platform);
                if (!initiallyLoaded || fetchError || !projectCanHaveReleases) {
                    return null;
                }
                return (<Alert type="info" icon={<IconInfo size="md"/>}>
              <AlertText>
                <div>
                  {t('To track user adoption, crash rates, session data and more, add Release Health to your current setup.')}
                </div>
                <ExternalLink href="https://docs.sentry.io/product/releases/health/setup/" onClick={_this.trackAddReleaseHealth}>
                  {t('Add Release Health')}
                </ExternalLink>
              </AlertText>
            </Alert>);
            }}
      </Projects>);
    };
    ReleasesList.prototype.renderInnerBody = function (activeDisplay) {
        var _this = this;
        var _a = this.props, location = _a.location, selection = _a.selection, organization = _a.organization, router = _a.router;
        var _b = this.state, hasSessions = _b.hasSessions, releases = _b.releases, reloading = _b.reloading, releasesPageLinks = _b.releasesPageLinks;
        if (this.shouldShowLoadingIndicator()) {
            return <LoadingIndicator />;
        }
        if (!(releases === null || releases === void 0 ? void 0 : releases.length)) {
            return this.renderEmptyMessage();
        }
        return (<ReleaseHealthRequest releases={releases.map(function (_a) {
            var version = _a.version;
            return version;
        })} organization={organization} selection={selection} location={location} display={[this.getDisplay()]} releasesReloading={reloading} healthStatsPeriod={location.query.healthStatsPeriod}>
        {function (_a) {
                var _b;
                var isHealthLoading = _a.isHealthLoading, getHealthData = _a.getHealthData;
                var singleProjectSelected = ((_b = selection.projects) === null || _b === void 0 ? void 0 : _b.length) === 1 &&
                    selection.projects[0] !== ALL_ACCESS_PROJECTS;
                var selectedProject = _this.getSelectedProject();
                var isMobileProject = selectedProject &&
                    selectedProject.platform &&
                    __spreadArray(__spreadArray(__spreadArray([], __read(mobile)), __read(desktop)), [
                        'java-android',
                        'cocoa-objc',
                        'cocoa-swift',
                    ]).includes(selectedProject.platform);
                return (<Fragment>
              {singleProjectSelected && hasSessions && isMobileProject && (<Feature features={['organizations:release-adoption-chart']}>
                  <ReleaseAdoptionChart organization={organization} selection={selection} location={location} router={router} activeDisplay={activeDisplay}/>
                </Feature>)}

              {releases.map(function (release, index) { return (<ReleaseCard key={release.version + "-" + release.projects[0].slug} activeDisplay={activeDisplay} release={release} organization={organization} location={location} selection={selection} reloading={reloading} showHealthPlaceholders={isHealthLoading} isTopRelease={index === 0} getHealthData={getHealthData}/>); })}
              <Pagination pageLinks={releasesPageLinks}/>
            </Fragment>);
            }}
      </ReleaseHealthRequest>);
    };
    ReleasesList.prototype.renderBody = function () {
        var organization = this.props.organization;
        var _a = this.state, releases = _a.releases, reloading = _a.reloading, error = _a.error;
        var activeSort = this.getSort();
        var activeStatus = this.getStatus();
        var activeDisplay = this.getDisplay();
        var hasSemver = organization.features.includes('semver');
        return (<GlobalSelectionHeader showAbsolute={false} timeRangeHint={t('Changing this date range will recalculate the release metrics.')}>
        <PageContent>
          <LightWeightNoProjectMessage organization={organization}>
            <PageHeader>
              <PageHeading>{t('Releases')}</PageHeading>
            </PageHeader>

            {this.renderHealthCta()}

            <SortAndFilterWrapper>
              {hasSemver ? (<SmartSearchBar query={this.getQuery()} placeholder={t('Search by release version')} maxSearchItems={5} hasRecentSearches={false} supportedTags={supportedTags} onSearch={this.handleSearch} onGetTagValues={this.getTagValues}/>) : (<SearchBar placeholder={t('Search')} onSearch={this.handleSearch} query={this.getQuery()}/>)}
              <ReleaseListStatusOptions selected={activeStatus} onSelect={this.handleStatus}/>
              <ReleaseListSortOptions selected={activeSort} selectedDisplay={activeDisplay} onSelect={this.handleSortBy} organization={organization}/>
              <ReleaseDisplayOptions selected={activeDisplay} onSelect={this.handleDisplay}/>
            </SortAndFilterWrapper>

            {!reloading &&
                activeStatus === StatusOption.ARCHIVED &&
                !!(releases === null || releases === void 0 ? void 0 : releases.length) && <ReleaseArchivedNotice multi/>}

            {error
                ? _super.prototype.renderError.call(this, new Error('Unable to load all required endpoints'))
                : this.renderInnerBody(activeDisplay)}
          </LightWeightNoProjectMessage>
        </PageContent>
      </GlobalSelectionHeader>);
    };
    return ReleasesList;
}(AsyncView));
var AlertText = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  justify-content: flex-start;\n  gap: ", ";\n\n  > *:nth-child(1) {\n    flex: 1;\n  }\n  flex-direction: column;\n  @media (min-width: ", ") {\n    flex-direction: row;\n  }\n"], ["\n  display: flex;\n  align-items: flex-start;\n  justify-content: flex-start;\n  gap: ", ";\n\n  > *:nth-child(1) {\n    flex: 1;\n  }\n  flex-direction: column;\n  @media (min-width: ", ") {\n    flex-direction: row;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[1]; });
var SortAndFilterWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr repeat(3, auto);\n  }\n"], ["\n  display: inline-grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr repeat(3, auto);\n  }\n"])), space(2), space(2), function (p) { return p.theme.breakpoints[1]; });
export default withOrganization(withGlobalSelection(ReleasesList));
export { ReleasesList };
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map