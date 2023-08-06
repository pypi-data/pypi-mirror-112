import { __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import Badge from 'app/components/badge';
import Breadcrumbs from 'app/components/breadcrumbs';
import Clipboard from 'app/components/clipboard';
import IdBadge from 'app/components/idBadge';
import * as Layout from 'app/components/layouts/thirds';
import ExternalLink from 'app/components/links/externalLink';
import ListLink from 'app/components/links/listLink';
import NavTabs from 'app/components/navTabs';
import Tooltip from 'app/components/tooltip';
import Version from 'app/components/version';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { IconCopy, IconOpen } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { formatAbbreviatedNumber } from 'app/utils/formatters';
import ReleaseActions from './releaseActions';
var ReleaseHeader = function (_a) {
    var location = _a.location, organization = _a.organization, release = _a.release, project = _a.project, releaseMeta = _a.releaseMeta, refetchData = _a.refetchData;
    var version = release.version, url = release.url;
    var commitCount = releaseMeta.commitCount, commitFilesChanged = releaseMeta.commitFilesChanged;
    var releasePath = "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(version) + "/";
    var tabs = [
        { title: t('Overview'), to: '' },
        {
            title: (<Fragment>
          {t('Commits')} <NavTabsBadge text={formatAbbreviatedNumber(commitCount)}/>
        </Fragment>),
            to: "commits/",
        },
        {
            title: (<Fragment>
          {t('Files Changed')}
          <NavTabsBadge text={formatAbbreviatedNumber(commitFilesChanged)}/>
        </Fragment>),
            to: "files-changed/",
        },
    ];
    var getTabUrl = function (path) { return ({
        pathname: releasePath + path,
        query: pick(location.query, Object.values(URL_PARAM)),
    }); };
    var getActiveTabTo = function () {
        // We are not doing strict version check because there would be a tiny page shift when switching between releases with paginator
        var activeTab = tabs
            .filter(function (tab) { return tab.to.length; }) // remove home 'Overview' from consideration
            .find(function (tab) { return location.pathname.endsWith(tab.to); });
        if (activeTab) {
            return activeTab.to;
        }
        return tabs[0].to; // default to 'Overview'
    };
    return (<Layout.Header>
      <Layout.HeaderContent>
        <Breadcrumbs crumbs={[
            {
                to: "/organizations/" + organization.slug + "/releases/",
                label: t('Releases'),
                preserveGlobalSelection: true,
            },
            { label: t('Release Details') },
        ]}/>
        <Layout.Title>
          <ReleaseName>
            <IdBadge project={project} avatarSize={28} hideName/>
            <StyledVersion version={version} anchor={false} truncate/>
            <IconWrapper>
              <Clipboard value={version}>
                <Tooltip title={version} containerDisplayMode="flex">
                  <IconCopy />
                </Tooltip>
              </Clipboard>
            </IconWrapper>
            {!!url && (<IconWrapper>
                <Tooltip title={url}>
                  <ExternalLink href={url}>
                    <IconOpen />
                  </ExternalLink>
                </Tooltip>
              </IconWrapper>)}
          </ReleaseName>
        </Layout.Title>
      </Layout.HeaderContent>

      <Layout.HeaderActions>
        <ReleaseActions organization={organization} projectSlug={project.slug} release={release} releaseMeta={releaseMeta} refetchData={refetchData} location={location}/>
      </Layout.HeaderActions>

      <Fragment>
        <StyledNavTabs>
          {tabs.map(function (tab) { return (<ListLink key={tab.to} to={getTabUrl(tab.to)} isActive={function () { return getActiveTabTo() === tab.to; }}>
              {tab.title}
            </ListLink>); })}
        </StyledNavTabs>
      </Fragment>
    </Layout.Header>);
};
var ReleaseName = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledVersion = styled(Version)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var IconWrapper = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  transition: color 0.3s ease-in-out;\n  margin-left: ", ";\n\n  &,\n  a {\n    color: ", ";\n    display: flex;\n    &:hover {\n      cursor: pointer;\n      color: ", ";\n    }\n  }\n"], ["\n  transition: color 0.3s ease-in-out;\n  margin-left: ", ";\n\n  &,\n  a {\n    color: ", ";\n    display: flex;\n    &:hover {\n      cursor: pointer;\n      color: ", ";\n    }\n  }\n"])), space(1), function (p) { return p.theme.gray300; }, function (p) { return p.theme.textColor; });
var StyledNavTabs = styled(NavTabs)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: 0;\n  /* Makes sure the tabs are pushed into another row */\n  width: 100%;\n"], ["\n  margin-bottom: 0;\n  /* Makes sure the tabs are pushed into another row */\n  width: 100%;\n"])));
var NavTabsBadge = styled(Badge)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
export default ReleaseHeader;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=releaseHeader.jsx.map