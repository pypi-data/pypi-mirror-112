import { __assign, __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import WidgetArea from 'sentry-images/dashboard/widget-area.svg';
import WidgetBar from 'sentry-images/dashboard/widget-bar.svg';
import WidgetBigNumber from 'sentry-images/dashboard/widget-big-number.svg';
import WidgetLine from 'sentry-images/dashboard/widget-line-1.svg';
import WidgetTable from 'sentry-images/dashboard/widget-table.svg';
import WidgetWorldMap from 'sentry-images/dashboard/widget-world-map.svg';
import { createDashboard, deleteDashboard, fetchDashboard, } from 'app/actionCreators/dashboards';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import MenuItem from 'app/components/menuItem';
import Pagination from 'app/components/pagination';
import TimeSince from 'app/components/timeSince';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import { DisplayType } from 'app/views/dashboardsV2/types';
import ContextMenu from '../contextMenu';
import { cloneDashboard } from '../utils';
import DashboardCard from './dashboardCard';
function DashboardList(_a) {
    var api = _a.api, organization = _a.organization, location = _a.location, dashboards = _a.dashboards, pageLinks = _a.pageLinks, onDashboardsChange = _a.onDashboardsChange;
    function miniWidget(displayType) {
        switch (displayType) {
            case DisplayType.BAR:
                return WidgetBar;
            case DisplayType.AREA:
                return WidgetArea;
            case DisplayType.BIG_NUMBER:
                return WidgetBigNumber;
            case DisplayType.TABLE:
                return WidgetTable;
            case DisplayType.WORLD_MAP:
                return WidgetWorldMap;
            case DisplayType.LINE:
            default:
                return WidgetLine;
        }
    }
    function handleDelete(dashboard) {
        deleteDashboard(api, organization.slug, dashboard.id)
            .then(function () {
            trackAnalyticsEvent({
                eventKey: 'dashboards_manage.delete',
                eventName: 'Dashboards Manager: Dashboard Deleted',
                organization_id: parseInt(organization.id, 10),
                dashboard_id: parseInt(dashboard.id, 10),
            });
            onDashboardsChange();
            addSuccessMessage(t('Dashboard deleted'));
        })
            .catch(function () {
            addErrorMessage(t('Error deleting Dashboard'));
        });
    }
    function handleDuplicate(dashboard) {
        fetchDashboard(api, organization.slug, dashboard.id)
            .then(function (dashboardDetail) {
            var newDashboard = cloneDashboard(dashboardDetail);
            newDashboard.widgets.map(function (widget) { return (widget.id = undefined); });
            createDashboard(api, organization.slug, newDashboard, true).then(function () {
                trackAnalyticsEvent({
                    eventKey: 'dashboards_manage.duplicate',
                    eventName: 'Dashboards Manager: Dashboard Duplicated',
                    organization_id: parseInt(organization.id, 10),
                    dashboard_id: parseInt(dashboard.id, 10),
                });
                onDashboardsChange();
                addSuccessMessage(t('Dashboard duplicated'));
            });
        })
            .catch(function () { return addErrorMessage(t('Error duplicating Dashboard')); });
    }
    function renderMiniDashboards() {
        return dashboards === null || dashboards === void 0 ? void 0 : dashboards.map(function (dashboard, index) {
            return (<DashboardCard key={index + "-" + dashboard.id} title={dashboard.id === 'default-overview' ? 'Default Dashboard' : dashboard.title} to={{
                    pathname: "/organizations/" + organization.slug + "/dashboard/" + dashboard.id + "/",
                    query: __assign({}, location.query),
                }} detail={tn('%s widget', '%s widgets', dashboard.widgetDisplay.length)} dateStatus={dashboard.dateCreated ? <TimeSince date={dashboard.dateCreated}/> : undefined} createdBy={dashboard.createdBy} renderWidgets={function () { return (<WidgetGrid>
              {dashboard.widgetDisplay.map(function (displayType, i) {
                        return displayType === DisplayType.BIG_NUMBER ? (<BigNumberWidgetWrapper key={i + "-" + displayType}>
                    <WidgetImage src={miniWidget(displayType)}/>
                  </BigNumberWidgetWrapper>) : (<MiniWidgetWrapper key={i + "-" + displayType}>
                    <WidgetImage src={miniWidget(displayType)}/>
                  </MiniWidgetWrapper>);
                    })}
            </WidgetGrid>); }} renderContextMenu={function () { return (<ContextMenu>
              <MenuItem data-test-id="dashboard-delete" onClick={function (event) {
                        event.preventDefault();
                        handleDelete(dashboard);
                    }} disabled={dashboards.length <= 1}>
                {t('Delete')}
              </MenuItem>
              <MenuItem data-test-id="dashboard-duplicate" onClick={function (event) {
                        event.preventDefault();
                        handleDuplicate(dashboard);
                    }}>
                {t('Duplicate')}
              </MenuItem>
            </ContextMenu>); }}/>);
        });
    }
    function renderDashboardGrid() {
        if (!(dashboards === null || dashboards === void 0 ? void 0 : dashboards.length)) {
            return (<EmptyStateWarning>
          <p>{t('Sorry, no Dashboards match your filters.')}</p>
        </EmptyStateWarning>);
        }
        return <DashboardGrid>{renderMiniDashboards()}</DashboardGrid>;
    }
    return (<Fragment>
      {renderDashboardGrid()}
      <PaginationRow pageLinks={pageLinks} onCursor={function (cursor, path, query, direction) {
            var offset = Number(cursor.split(':')[1]);
            var newQuery = __assign(__assign({}, query), { cursor: cursor });
            var isPrevious = direction === -1;
            if (offset <= 0 && isPrevious) {
                delete newQuery.cursor;
            }
            trackAnalyticsEvent({
                eventKey: 'dashboards_manage.paginate',
                eventName: 'Dashboards Manager: Paginate',
                organization_id: parseInt(organization.id, 10),
            });
            browserHistory.push({
                pathname: path,
                query: newQuery,
            });
        }}/>
    </Fragment>);
}
var DashboardGrid = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-template-rows: repeat(3, max-content);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-template-rows: repeat(3, max-content);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, minmax(100px, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(3, minmax(100px, 1fr));\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; });
var WidgetGrid = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n  grid-auto-flow: row dense;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(6, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(8, minmax(0, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n  grid-auto-flow: row dense;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(6, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(8, minmax(0, 1fr));\n  }\n"])), space(0.25), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[3]; }, function (p) { return p.theme.breakpoints[4]; });
var BigNumberWidgetWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  width: 100%;\n  height: 100%;\n\n  /* 2 cols */\n  grid-area: span 1 / span 2;\n\n  @media (min-width: ", ") {\n    /* 4 cols */\n    grid-area: span 1 / span 1;\n  }\n\n  @media (min-width: ", ") {\n    /* 6 and 8 cols */\n    grid-area: span 1 / span 2;\n  }\n"], ["\n  display: flex;\n  align-items: flex-start;\n  width: 100%;\n  height: 100%;\n\n  /* 2 cols */\n  grid-area: span 1 / span 2;\n\n  @media (min-width: ", ") {\n    /* 4 cols */\n    grid-area: span 1 / span 1;\n  }\n\n  @media (min-width: ", ") {\n    /* 6 and 8 cols */\n    grid-area: span 1 / span 2;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[3]; });
var MiniWidgetWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  width: 100%;\n  height: 100%;\n  grid-area: span 2 / span 2;\n"], ["\n  display: flex;\n  align-items: flex-start;\n  width: 100%;\n  height: 100%;\n  grid-area: span 2 / span 2;\n"])));
var WidgetImage = styled('img')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  width: 100%;\n  height: 100%;\n"], ["\n  width: 100%;\n  height: 100%;\n"])));
var PaginationRow = styled(Pagination)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
export default withApi(DashboardList);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=dashboardList.jsx.map