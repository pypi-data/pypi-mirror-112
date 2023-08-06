import { __assign, __makeTemplateObject, __read, __spreadArray } from "tslib";
import { Fragment, useState } from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { SectionHeading } from 'app/components/charts/styles';
import DiscoverButton from 'app/components/discoverButton';
import GroupList from 'app/components/issues/groupList';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody } from 'app/components/panels';
import { DEFAULT_RELATIVE_PERIODS, DEFAULT_STATS_PERIOD } from 'app/constants';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { decodeScalar } from 'app/utils/queryString';
import NoGroupsHandler from '../issueList/noGroupsHandler';
function ProjectIssues(_a) {
    var organization = _a.organization, location = _a.location, projectId = _a.projectId, query = _a.query, api = _a.api;
    var _b = __read(useState(), 2), pageLinks = _b[0], setPageLinks = _b[1];
    var _c = __read(useState(), 2), onCursor = _c[0], setOnCursor = _c[1];
    function handleOpenInIssuesClick() {
        trackAnalyticsEvent({
            eventKey: 'project_detail.open_issues',
            eventName: 'Project Detail: Open issues from project detail',
            organization_id: parseInt(organization.id, 10),
        });
    }
    function handleOpenInDiscoverClick() {
        trackAnalyticsEvent({
            eventKey: 'project_detail.open_discover',
            eventName: 'Project Detail: Open discover from project detail',
            organization_id: parseInt(organization.id, 10),
        });
    }
    function handleFetchSuccess(groupListState, cursorHandler) {
        setPageLinks(groupListState.pageLinks);
        setOnCursor(function () { return cursorHandler; });
    }
    function getDiscoverUrl() {
        return {
            pathname: "/organizations/" + organization.slug + "/discover/results/",
            query: __assign({ name: t('Frequent Unhandled Issues'), field: ['issue', 'title', 'count()', 'count_unique(user)', 'project'], sort: ['-count'], query: ['event.type:error error.unhandled:true', query].join(' ').trim(), display: 'top5' }, getParams(pick(location.query, __spreadArray([], __read(Object.values(URL_PARAM)))))),
        };
    }
    var endpointPath = "/organizations/" + organization.slug + "/issues/";
    var issueQuery = ['is:unresolved error.unhandled:true ', query].join(' ').trim();
    var queryParams = __assign(__assign({ limit: 5 }, getParams(pick(location.query, __spreadArray(__spreadArray([], __read(Object.values(URL_PARAM))), ['cursor'])))), { query: issueQuery, sort: 'freq' });
    var issueSearch = {
        pathname: endpointPath,
        query: queryParams,
    };
    function renderEmptyMessage() {
        var selectedTimePeriod = location.query.start
            ? null
            : DEFAULT_RELATIVE_PERIODS[decodeScalar(location.query.statsPeriod, DEFAULT_STATS_PERIOD)];
        var displayedPeriod = selectedTimePeriod
            ? selectedTimePeriod.toLowerCase()
            : t('given timeframe');
        return (<Panel>
        <PanelBody>
          <NoGroupsHandler api={api} organization={organization} query={issueQuery} selectedProjectIds={[projectId]} groupIds={[]} emptyMessage={tct('No unhandled issues for the [timePeriod].', {
                timePeriod: displayedPeriod,
            })}/>
        </PanelBody>
      </Panel>);
    }
    return (<Fragment>
      <ControlsWrapper>
        <SectionHeading>{t('Frequent Unhandled Issues')}</SectionHeading>
        <ButtonBar gap={1}>
          <Button data-test-id="issues-open" size="small" to={issueSearch} onClick={handleOpenInIssuesClick}>
            {t('Open in Issues')}
          </Button>
          <DiscoverButton onClick={handleOpenInDiscoverClick} to={getDiscoverUrl()} size="small">
            {t('Open in Discover')}
          </DiscoverButton>
          <StyledPagination pageLinks={pageLinks} onCursor={onCursor}/>
        </ButtonBar>
      </ControlsWrapper>

      <GroupList orgId={organization.slug} endpointPath={endpointPath} queryParams={queryParams} query="" canSelectGroups={false} renderEmptyMessage={renderEmptyMessage} withChart={false} withPagination={false} onFetchSuccess={handleFetchSuccess}/>
    </Fragment>);
}
var ControlsWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  flex-wrap: wrap;\n  @media (max-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  flex-wrap: wrap;\n  @media (max-width: ", ") {\n    display: block;\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[0]; });
var StyledPagination = styled(Pagination)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
export default ProjectIssues;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectIssues.jsx.map