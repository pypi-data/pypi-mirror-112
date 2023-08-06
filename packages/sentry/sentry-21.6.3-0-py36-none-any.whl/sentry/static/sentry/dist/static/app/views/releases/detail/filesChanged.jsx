import { __assign, __extends, __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import styled from '@emotion/styled';
import FileChange from 'app/components/fileChange';
import { Body, Main } from 'app/components/layouts/thirds';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t, tn } from 'app/locale';
import { formatVersion } from 'app/utils/formatters';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import EmptyState from './emptyState';
import RepositorySwitcher from './repositorySwitcher';
import { getFilesByRepository, getQuery, getReposToRender } from './utils';
import withReleaseRepos from './withReleaseRepos';
var FilesChanged = /** @class */ (function (_super) {
    __extends(FilesChanged, _super);
    function FilesChanged() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    FilesChanged.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, projectSlug = _a.projectSlug;
        var orgId = params.orgId;
        return routeTitleGen(t('Files Changed - Release %s', formatVersion(params.release)), orgId, false, projectSlug);
    };
    FilesChanged.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { fileList: [] });
    };
    FilesChanged.prototype.componentDidUpdate = function (prevProps, prevContext) {
        var _a, _b;
        if (((_a = prevProps.activeReleaseRepo) === null || _a === void 0 ? void 0 : _a.name) !== ((_b = this.props.activeReleaseRepo) === null || _b === void 0 ? void 0 : _b.name)) {
            this.remountComponent();
            return;
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevContext);
    };
    FilesChanged.prototype.getEndpoints = function () {
        var _a = this.props, activeRepository = _a.activeReleaseRepo, location = _a.location, release = _a.release, orgSlug = _a.orgSlug;
        var query = getQuery({ location: location, activeRepository: activeRepository });
        return [
            [
                'fileList',
                "/organizations/" + orgSlug + "/releases/" + encodeURIComponent(release) + "/commitfiles/",
                { query: query },
            ],
        ];
    };
    FilesChanged.prototype.renderLoading = function () {
        return this.renderBody();
    };
    FilesChanged.prototype.renderContent = function () {
        var _a = this.state, fileList = _a.fileList, fileListPageLinks = _a.fileListPageLinks, loading = _a.loading;
        var activeReleaseRepo = this.props.activeReleaseRepo;
        if (loading) {
            return <LoadingIndicator />;
        }
        if (!fileList.length) {
            return (<EmptyState>
          {!activeReleaseRepo
                    ? t('There are no changed files associated with this release.')
                    : t('There are no changed files associated with this release in the %s repository.', activeReleaseRepo.name)}
        </EmptyState>);
        }
        var filesByRepository = getFilesByRepository(fileList);
        var reposToRender = getReposToRender(Object.keys(filesByRepository));
        return (<Fragment>
        {reposToRender.map(function (repoName) {
                var repoData = filesByRepository[repoName];
                var files = Object.keys(repoData);
                var fileCount = files.length;
                return (<Panel key={repoName}>
              <PanelHeader>
                <span>{repoName}</span>
                <span>{tn('%s file changed', '%s files changed', fileCount)}</span>
              </PanelHeader>
              <PanelBody>
                {files.map(function (filename) {
                        var authors = repoData[filename].authors;
                        return (<StyledFileChange key={filename} filename={filename} authors={Object.values(authors)}/>);
                    })}
              </PanelBody>
            </Panel>);
            })}
        <Pagination pageLinks={fileListPageLinks}/>
      </Fragment>);
    };
    FilesChanged.prototype.renderBody = function () {
        var _a = this.props, activeReleaseRepo = _a.activeReleaseRepo, releaseRepos = _a.releaseRepos, router = _a.router, location = _a.location;
        return (<Fragment>
        {releaseRepos.length > 1 && (<RepositorySwitcher repositories={releaseRepos} activeRepository={activeReleaseRepo} location={location} router={router}/>)}
        {this.renderContent()}
      </Fragment>);
    };
    FilesChanged.prototype.renderComponent = function () {
        return (<Body>
        <Main fullWidth>{_super.prototype.renderComponent.call(this)}</Main>
      </Body>);
    };
    return FilesChanged;
}(AsyncView));
export default withReleaseRepos(FilesChanged);
var StyledFileChange = styled(FileChange)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-radius: 0;\n  border-left: none;\n  border-right: none;\n  border-top: none;\n  :last-child {\n    border: none;\n    border-radius: 0;\n  }\n"], ["\n  border-radius: 0;\n  border-left: none;\n  border-right: none;\n  border-top: none;\n  :last-child {\n    border: none;\n    border-radius: 0;\n  }\n"])));
var templateObject_1;
//# sourceMappingURL=filesChanged.jsx.map