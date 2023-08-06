import { __assign, __awaiter, __generator, __makeTemplateObject } from "tslib";
import * as React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import { archiveRelease, restoreRelease } from 'app/actionCreators/release';
import { Client } from 'app/api';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Confirm from 'app/components/confirm';
import DropdownLink from 'app/components/dropdownLink';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import MenuItem from 'app/components/menuItem';
import NavigationButtonGroup from 'app/components/navigationButtonGroup';
import TextOverflow from 'app/components/textOverflow';
import Tooltip from 'app/components/tooltip';
import { IconEllipsis } from 'app/icons';
import { t, tct, tn } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { formatVersion } from 'app/utils/formatters';
import { isReleaseArchived } from '../utils';
function ReleaseActions(_a) {
    var location = _a.location, organization = _a.organization, projectSlug = _a.projectSlug, release = _a.release, releaseMeta = _a.releaseMeta, refetchData = _a.refetchData;
    function handleArchive() {
        return __awaiter(this, void 0, void 0, function () {
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _b.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, archiveRelease(new Client(), {
                                orgSlug: organization.slug,
                                projectSlug: projectSlug,
                                releaseVersion: release.version,
                            })];
                    case 1:
                        _b.sent();
                        browserHistory.push("/organizations/" + organization.slug + "/releases/");
                        return [3 /*break*/, 3];
                    case 2:
                        _a = _b.sent();
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    }
    function handleRestore() {
        return __awaiter(this, void 0, void 0, function () {
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _b.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, restoreRelease(new Client(), {
                                orgSlug: organization.slug,
                                projectSlug: projectSlug,
                                releaseVersion: release.version,
                            })];
                    case 1:
                        _b.sent();
                        refetchData();
                        return [3 /*break*/, 3];
                    case 2:
                        _a = _b.sent();
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    }
    function getProjectList() {
        var maxVisibleProjects = 5;
        var visibleProjects = releaseMeta.projects.slice(0, maxVisibleProjects);
        var numberOfCollapsedProjects = releaseMeta.projects.length - visibleProjects.length;
        return (<React.Fragment>
        {visibleProjects.map(function (project) { return (<ProjectBadge key={project.slug} project={project} avatarSize={18}/>); })}
        {numberOfCollapsedProjects > 0 && (<span>
            <Tooltip title={release.projects
                    .slice(maxVisibleProjects)
                    .map(function (p) { return p.slug; })
                    .join(', ')}>
              + {tn('%s other project', '%s other projects', numberOfCollapsedProjects)}
            </Tooltip>
          </span>)}
      </React.Fragment>);
    }
    function getModalHeader(title) {
        return (<h4>
        <TextOverflow>{title}</TextOverflow>
      </h4>);
    }
    function getModalMessage(message) {
        return (<React.Fragment>
        {message}

        <ProjectsWrapper>{getProjectList()}</ProjectsWrapper>

        {t('Are you sure you want to do this?')}
      </React.Fragment>);
    }
    function replaceReleaseUrl(toRelease) {
        return toRelease
            ? {
                pathname: location.pathname
                    .replace(encodeURIComponent(release.version), toRelease)
                    .replace(release.version, toRelease),
                query: __assign(__assign({}, location.query), { activeRepo: undefined }),
            }
            : '';
    }
    function handleNavigationClick(direction) {
        trackAnalyticsEvent({
            eventKey: "release_detail.pagination",
            eventName: "Release Detail: Pagination",
            organization_id: parseInt(organization.id, 10),
            direction: direction,
        });
    }
    var _b = release.currentProjectMeta, nextReleaseVersion = _b.nextReleaseVersion, prevReleaseVersion = _b.prevReleaseVersion, firstReleaseVersion = _b.firstReleaseVersion, lastReleaseVersion = _b.lastReleaseVersion;
    return (<ButtonBar gap={1}>
      <NavigationButtonGroup hasPrevious={!!prevReleaseVersion} hasNext={!!nextReleaseVersion} links={[
            replaceReleaseUrl(firstReleaseVersion),
            replaceReleaseUrl(prevReleaseVersion),
            replaceReleaseUrl(nextReleaseVersion),
            replaceReleaseUrl(lastReleaseVersion),
        ]} onOldestClick={function () { return handleNavigationClick('oldest'); }} onOlderClick={function () { return handleNavigationClick('older'); }} onNewerClick={function () { return handleNavigationClick('newer'); }} onNewestClick={function () { return handleNavigationClick('newest'); }}/>
      <StyledDropdownLink caret={false} anchorRight={window.innerWidth > 992} title={<ActionsButton icon={<IconEllipsis />} label={t('Actions')}/>}>
        {isReleaseArchived(release) ? (<Confirm onConfirm={handleRestore} header={getModalHeader(tct('Restore Release [release]', {
                release: formatVersion(release.version),
            }))} message={getModalMessage(tn('You are restoring this release for the following project:', 'By restoring this release, you are also restoring it for the following projects:', releaseMeta.projects.length))} cancelText={t('Nevermind')} confirmText={t('Restore')}>
            <MenuItem>{t('Restore')}</MenuItem>
          </Confirm>) : (<Confirm onConfirm={handleArchive} header={getModalHeader(tct('Archive Release [release]', {
                release: formatVersion(release.version),
            }))} message={getModalMessage(tn('You are archiving this release for the following project:', 'By archiving this release, you are also archiving it for the following projects:', releaseMeta.projects.length))} cancelText={t('Nevermind')} confirmText={t('Archive')}>
            <MenuItem>{t('Archive')}</MenuItem>
          </Confirm>)}
      </StyledDropdownLink>
    </ButtonBar>);
}
var ActionsButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 40px;\n  height: 40px;\n  padding: 0;\n"], ["\n  width: 40px;\n  height: 40px;\n  padding: 0;\n"])));
var StyledDropdownLink = styled(DropdownLink)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  & + .dropdown-menu {\n    top: 50px !important;\n  }\n"], ["\n  & + .dropdown-menu {\n    top: 50px !important;\n  }\n"])));
var ProjectsWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: ", " 0 ", " ", ";\n  display: grid;\n  gap: ", ";\n  img {\n    border: none !important;\n    box-shadow: none !important;\n  }\n"], ["\n  margin: ", " 0 ", " ", ";\n  display: grid;\n  gap: ", ";\n  img {\n    border: none !important;\n    box-shadow: none !important;\n  }\n"])), space(2), space(2), space(2), space(0.5));
export default ReleaseActions;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=releaseActions.jsx.map