import { __assign, __extends } from "tslib";
import { Fragment } from 'react';
import CommitRow from 'app/components/commitRow';
import { Body, Main } from 'app/components/layouts/thirds';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import { formatVersion } from 'app/utils/formatters';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import EmptyState from './emptyState';
import RepositorySwitcher from './repositorySwitcher';
import { getCommitsByRepository, getQuery, getReposToRender } from './utils';
import withReleaseRepos from './withReleaseRepos';
var Commits = /** @class */ (function (_super) {
    __extends(Commits, _super);
    function Commits() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Commits.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, projectSlug = _a.projectSlug;
        var orgId = params.orgId;
        return routeTitleGen(t('Commits - Release %s', formatVersion(params.release)), orgId, false, projectSlug);
    };
    Commits.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { commits: [] });
    };
    Commits.prototype.componentDidUpdate = function (prevProps, prevContext) {
        var _a, _b;
        if (((_a = prevProps.activeReleaseRepo) === null || _a === void 0 ? void 0 : _a.name) !== ((_b = this.props.activeReleaseRepo) === null || _b === void 0 ? void 0 : _b.name)) {
            this.remountComponent();
            return;
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevContext);
    };
    Commits.prototype.getEndpoints = function () {
        var _a = this.props, projectSlug = _a.projectSlug, activeRepository = _a.activeReleaseRepo, location = _a.location, orgSlug = _a.orgSlug, release = _a.release;
        var query = getQuery({ location: location, activeRepository: activeRepository });
        return [
            [
                'commits',
                "/projects/" + orgSlug + "/" + projectSlug + "/releases/" + encodeURIComponent(release) + "/commits/",
                { query: query },
            ],
        ];
    };
    Commits.prototype.renderLoading = function () {
        return this.renderBody();
    };
    Commits.prototype.renderContent = function () {
        var _a = this.state, commits = _a.commits, commitsPageLinks = _a.commitsPageLinks, loading = _a.loading;
        var activeReleaseRepo = this.props.activeReleaseRepo;
        if (loading) {
            return <LoadingIndicator />;
        }
        if (!commits.length) {
            return (<EmptyState>
          {!activeReleaseRepo
                    ? t('There are no commits associated with this release.')
                    : t('There are no commits associated with this release in the %s repository.', activeReleaseRepo.name)}
        </EmptyState>);
        }
        var commitsByRepository = getCommitsByRepository(commits);
        var reposToRender = getReposToRender(Object.keys(commitsByRepository));
        return (<Fragment>
        {reposToRender.map(function (repoName) {
                var _a;
                return (<Panel key={repoName}>
            <PanelHeader>{repoName}</PanelHeader>
            <PanelBody>
              {(_a = commitsByRepository[repoName]) === null || _a === void 0 ? void 0 : _a.map(function (commit) { return (<CommitRow key={commit.id} commit={commit}/>); })}
            </PanelBody>
          </Panel>);
            })}
        <Pagination pageLinks={commitsPageLinks}/>
      </Fragment>);
    };
    Commits.prototype.renderBody = function () {
        var _a = this.props, location = _a.location, router = _a.router, activeReleaseRepo = _a.activeReleaseRepo, releaseRepos = _a.releaseRepos;
        return (<Fragment>
        {releaseRepos.length > 1 && (<RepositorySwitcher repositories={releaseRepos} activeRepository={activeReleaseRepo} location={location} router={router}/>)}
        {this.renderContent()}
      </Fragment>);
    };
    Commits.prototype.renderComponent = function () {
        return (<Body>
        <Main fullWidth>{_super.prototype.renderComponent.call(this)}</Main>
      </Body>);
    };
    return Commits;
}(AsyncView));
export default withReleaseRepos(Commits);
//# sourceMappingURL=commits.jsx.map