import { __assign, __extends, __makeTemplateObject } from "tslib";
import { cloneElement, Component, isValidElement } from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { createDashboard, deleteDashboard, updateDashboard, } from 'app/actionCreators/dashboards';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import Breadcrumbs from 'app/components/breadcrumbs';
import HookOrDefault from 'app/components/hookOrDefault';
import * as Layout from 'app/components/layouts/thirds';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import Controls from './controls';
import Dashboard from './dashboard';
import { DEFAULT_STATS_PERIOD, EMPTY_DASHBOARD } from './data';
import DashboardTitle from './title';
import { DashboardState } from './types';
import { cloneDashboard } from './utils';
var UNSAVED_MESSAGE = t('You have unsaved changes, are you sure you want to leave?');
var HookHeader = HookOrDefault({ hookName: 'component:dashboards-header' });
var DashboardDetail = /** @class */ (function (_super) {
    __extends(DashboardDetail, _super);
    function DashboardDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            dashboardState: _this.props.initialState,
            modifiedDashboard: _this.updateModifiedDashboard(_this.props.initialState),
        };
        _this.onEdit = function () {
            var dashboard = _this.props.dashboard;
            trackAnalyticsEvent({
                eventKey: 'dashboards2.edit.start',
                eventName: 'Dashboards2: Edit start',
                organization_id: parseInt(_this.props.organization.id, 10),
            });
            _this.setState({
                dashboardState: DashboardState.EDIT,
                modifiedDashboard: cloneDashboard(dashboard),
            });
        };
        _this.onRouteLeave = function () {
            if (![DashboardState.VIEW, DashboardState.PENDING_DELETE].includes(_this.state.dashboardState)) {
                return UNSAVED_MESSAGE;
            }
            return undefined;
        };
        _this.onUnload = function (event) {
            if ([DashboardState.VIEW, DashboardState.PENDING_DELETE].includes(_this.state.dashboardState)) {
                return;
            }
            event.preventDefault();
            event.returnValue = UNSAVED_MESSAGE;
        };
        _this.onDelete = function (dashboard) { return function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, location = _a.location;
            if (!(dashboard === null || dashboard === void 0 ? void 0 : dashboard.id)) {
                return;
            }
            var previousDashboardState = _this.state.dashboardState;
            _this.setState({ dashboardState: DashboardState.PENDING_DELETE }, function () {
                deleteDashboard(api, organization.slug, dashboard.id)
                    .then(function () {
                    addSuccessMessage(t('Dashboard deleted'));
                    trackAnalyticsEvent({
                        eventKey: 'dashboards2.delete',
                        eventName: 'Dashboards2: Delete',
                        organization_id: parseInt(_this.props.organization.id, 10),
                    });
                    browserHistory.replace({
                        pathname: "/organizations/" + organization.slug + "/dashboards/",
                        query: location.query,
                    });
                })
                    .catch(function () {
                    _this.setState({
                        dashboardState: previousDashboardState,
                    });
                });
            });
        }; };
        _this.onCancel = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location, params = _a.params;
            if (params.dashboardId) {
                trackAnalyticsEvent({
                    eventKey: 'dashboards2.edit.cancel',
                    eventName: 'Dashboards2: Edit cancel',
                    organization_id: parseInt(_this.props.organization.id, 10),
                });
                _this.setState({
                    dashboardState: DashboardState.VIEW,
                    modifiedDashboard: null,
                });
                return;
            }
            trackAnalyticsEvent({
                eventKey: 'dashboards2.create.cancel',
                eventName: 'Dashboards2: Create cancel',
                organization_id: parseInt(_this.props.organization.id, 10),
            });
            browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/dashboards/",
                query: location.query,
            });
        };
        _this.onCommit = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, location = _a.location, dashboard = _a.dashboard, reloadData = _a.reloadData;
            var _b = _this.state, modifiedDashboard = _b.modifiedDashboard, dashboardState = _b.dashboardState;
            switch (dashboardState) {
                case DashboardState.CREATE: {
                    if (modifiedDashboard) {
                        createDashboard(api, organization.slug, modifiedDashboard).then(function (newDashboard) {
                            addSuccessMessage(t('Dashboard created'));
                            trackAnalyticsEvent({
                                eventKey: 'dashboards2.create.complete',
                                eventName: 'Dashboards2: Create complete',
                                organization_id: parseInt(organization.id, 10),
                            });
                            _this.setState({
                                dashboardState: DashboardState.VIEW,
                                modifiedDashboard: null,
                            });
                            // redirect to new dashboard
                            browserHistory.replace({
                                pathname: "/organizations/" + organization.slug + "/dashboard/" + newDashboard.id + "/",
                                query: __assign({}, location.query),
                            });
                        });
                    }
                    break;
                }
                case DashboardState.EDIT: {
                    // only update the dashboard if there are changes
                    if (modifiedDashboard) {
                        if (isEqual(dashboard, modifiedDashboard)) {
                            _this.setState({
                                dashboardState: DashboardState.VIEW,
                                modifiedDashboard: null,
                            });
                            return;
                        }
                        updateDashboard(api, organization.slug, modifiedDashboard).then(function (newDashboard) {
                            addSuccessMessage(t('Dashboard updated'));
                            trackAnalyticsEvent({
                                eventKey: 'dashboards2.edit.complete',
                                eventName: 'Dashboards2: Edit complete',
                                organization_id: parseInt(organization.id, 10),
                            });
                            _this.setState({
                                dashboardState: DashboardState.VIEW,
                                modifiedDashboard: null,
                            });
                            if (dashboard && newDashboard.id !== dashboard.id) {
                                browserHistory.replace({
                                    pathname: "/organizations/" + organization.slug + "/dashboard/" + newDashboard.id + "/",
                                    query: __assign({}, location.query),
                                });
                                return;
                            }
                            if (reloadData) {
                                reloadData();
                            }
                        });
                        return;
                    }
                    _this.setState({
                        dashboardState: DashboardState.VIEW,
                        modifiedDashboard: null,
                    });
                    break;
                }
                case DashboardState.VIEW:
                default: {
                    _this.setState({
                        dashboardState: DashboardState.VIEW,
                        modifiedDashboard: null,
                    });
                    break;
                }
            }
        };
        _this.setModifiedDashboard = function (dashboard) {
            _this.setState({
                modifiedDashboard: dashboard,
            });
        };
        _this.onSetWidgetToBeUpdated = function (widget) {
            _this.setState({ widgetToBeUpdated: widget });
        };
        _this.onUpdateWidget = function (widgets) {
            var modifiedDashboard = _this.state.modifiedDashboard;
            if (modifiedDashboard === null) {
                return;
            }
            _this.setState(function (state) { return (__assign(__assign({}, state), { widgetToBeUpdated: undefined, modifiedDashboard: __assign(__assign({}, state.modifiedDashboard), { widgets: widgets }) })); }, _this.updateRouteAfterSavingWidget);
        };
        return _this;
    }
    DashboardDetail.prototype.componentDidMount = function () {
        var _a = this.props, route = _a.route, router = _a.router;
        this.checkStateRoute();
        router.setRouteLeaveHook(route, this.onRouteLeave);
        window.addEventListener('beforeunload', this.onUnload);
    };
    DashboardDetail.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.location.pathname !== this.props.location.pathname) {
            this.checkStateRoute();
        }
    };
    DashboardDetail.prototype.componentWillUnmount = function () {
        window.removeEventListener('beforeunload', this.onUnload);
    };
    DashboardDetail.prototype.checkStateRoute = function () {
        var _a = this.props, router = _a.router, organization = _a.organization, params = _a.params;
        var dashboardId = params.dashboardId;
        var dashboardDetailsRoute = "/organizations/" + organization.slug + "/dashboard/" + dashboardId + "/";
        if (this.isWidgetBuilderRouter && !this.isEditing) {
            router.replace(dashboardDetailsRoute);
        }
        if (location.pathname === dashboardDetailsRoute && !!this.state.widgetToBeUpdated) {
            this.onSetWidgetToBeUpdated(undefined);
        }
    };
    DashboardDetail.prototype.updateRouteAfterSavingWidget = function () {
        if (this.isWidgetBuilderRouter) {
            var _a = this.props, router = _a.router, organization = _a.organization, params = _a.params;
            var dashboardId = params.dashboardId;
            if (dashboardId) {
                router.replace("/organizations/" + organization.slug + "/dashboard/" + dashboardId + "/");
                return;
            }
            router.replace("/organizations/" + organization.slug + "/dashboards/new/");
        }
    };
    DashboardDetail.prototype.updateModifiedDashboard = function (dashboardState) {
        var dashboard = this.props.dashboard;
        switch (dashboardState) {
            case DashboardState.CREATE:
                return cloneDashboard(EMPTY_DASHBOARD);
            case DashboardState.EDIT:
                return cloneDashboard(dashboard);
            default: {
                return null;
            }
        }
    };
    Object.defineProperty(DashboardDetail.prototype, "isEditing", {
        get: function () {
            var dashboardState = this.state.dashboardState;
            return [
                DashboardState.EDIT,
                DashboardState.CREATE,
                DashboardState.PENDING_DELETE,
            ].includes(dashboardState);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DashboardDetail.prototype, "isWidgetBuilderRouter", {
        get: function () {
            var _a = this.props, location = _a.location, params = _a.params, organization = _a.organization;
            var dashboardId = params.dashboardId;
            var newWidgetRoutes = [
                "/organizations/" + organization.slug + "/dashboards/new/widget/new/",
                "/organizations/" + organization.slug + "/dashboard/" + dashboardId + "/widget/new/",
            ];
            return newWidgetRoutes.includes(location.pathname) || this.isWidgetBuilderEditRouter;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DashboardDetail.prototype, "isWidgetBuilderEditRouter", {
        get: function () {
            var _a = this.props, location = _a.location, params = _a.params, organization = _a.organization;
            var dashboardId = params.dashboardId, widgetId = params.widgetId;
            var widgetEditRoutes = [
                "/organizations/" + organization.slug + "/dashboards/new/widget/" + widgetId + "/edit/",
                "/organizations/" + organization.slug + "/dashboard/" + dashboardId + "/widget/" + widgetId + "/edit/",
            ];
            return widgetEditRoutes.includes(location.pathname);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(DashboardDetail.prototype, "dashboardTitle", {
        get: function () {
            var dashboard = this.props.dashboard;
            var modifiedDashboard = this.state.modifiedDashboard;
            return modifiedDashboard ? modifiedDashboard.title : dashboard.title;
        },
        enumerable: false,
        configurable: true
    });
    DashboardDetail.prototype.renderWidgetBuilder = function (dashboard) {
        var children = this.props.children;
        var _a = this.state, modifiedDashboard = _a.modifiedDashboard, widgetToBeUpdated = _a.widgetToBeUpdated;
        return isValidElement(children)
            ? cloneElement(children, {
                dashboard: modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard,
                onSave: this.onUpdateWidget,
                widget: widgetToBeUpdated,
            })
            : children;
    };
    DashboardDetail.prototype.renderDefaultDashboardDetail = function () {
        var _a = this.props, organization = _a.organization, dashboard = _a.dashboard, dashboards = _a.dashboards, params = _a.params, router = _a.router, location = _a.location;
        var _b = this.state, modifiedDashboard = _b.modifiedDashboard, dashboardState = _b.dashboardState;
        var dashboardId = params.dashboardId;
        return (<GlobalSelectionHeader skipLoadLastUsed={organization.features.includes('global-views')} defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: DEFAULT_STATS_PERIOD,
                },
            }}>
        <PageContent>
          <LightWeightNoProjectMessage organization={organization}>
            <StyledPageHeader>
              <DashboardTitle dashboard={modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard} onUpdate={this.setModifiedDashboard} isEditing={this.isEditing}/>
              <Controls organization={organization} dashboards={dashboards} onEdit={this.onEdit} onCancel={this.onCancel} onCommit={this.onCommit} onDelete={this.onDelete(dashboard)} dashboardState={dashboardState}/>
            </StyledPageHeader>
            <HookHeader organization={organization}/>
            <Dashboard paramDashboardId={dashboardId} dashboard={modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard} organization={organization} isEditing={this.isEditing} onUpdate={this.onUpdateWidget} onSetWidgetToBeUpdated={this.onSetWidgetToBeUpdated} router={router} location={location}/>
          </LightWeightNoProjectMessage>
        </PageContent>
      </GlobalSelectionHeader>);
    };
    DashboardDetail.prototype.renderDashboardDetail = function () {
        var _a = this.props, organization = _a.organization, dashboard = _a.dashboard, dashboards = _a.dashboards, params = _a.params, router = _a.router, location = _a.location;
        var _b = this.state, modifiedDashboard = _b.modifiedDashboard, dashboardState = _b.dashboardState;
        var dashboardId = params.dashboardId;
        return (<GlobalSelectionHeader skipLoadLastUsed={organization.features.includes('global-views')} defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: DEFAULT_STATS_PERIOD,
                },
            }}>
        <LightWeightNoProjectMessage organization={organization}>
          <Layout.Header>
            <Layout.HeaderContent>
              <Breadcrumbs crumbs={[
                {
                    label: t('Dashboards'),
                    to: "/organizations/" + organization.slug + "/dashboards/",
                },
                {
                    label: dashboardState === DashboardState.CREATE
                        ? t('Create Dashboard')
                        : organization.features.includes('dashboards-edit') &&
                            dashboard.id === 'default-overview'
                            ? 'Default Dashboard'
                            : this.dashboardTitle,
                },
            ]}/>
              <Layout.Title>
                <DashboardTitle dashboard={modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard} onUpdate={this.setModifiedDashboard} isEditing={this.isEditing}/>
              </Layout.Title>
            </Layout.HeaderContent>
            <Layout.HeaderActions>
              <Controls organization={organization} dashboards={dashboards} onEdit={this.onEdit} onCancel={this.onCancel} onCommit={this.onCommit} onDelete={this.onDelete(dashboard)} dashboardState={dashboardState}/>
            </Layout.HeaderActions>
          </Layout.Header>
          <Layout.Body>
            <Layout.Main fullWidth>
              <Dashboard paramDashboardId={dashboardId} dashboard={modifiedDashboard !== null && modifiedDashboard !== void 0 ? modifiedDashboard : dashboard} organization={organization} isEditing={this.isEditing} onUpdate={this.onUpdateWidget} onSetWidgetToBeUpdated={this.onSetWidgetToBeUpdated} router={router} location={location}/>
            </Layout.Main>
          </Layout.Body>
        </LightWeightNoProjectMessage>
      </GlobalSelectionHeader>);
    };
    DashboardDetail.prototype.render = function () {
        var _a = this.props, organization = _a.organization, dashboard = _a.dashboard;
        if (this.isEditing && this.isWidgetBuilderRouter) {
            return this.renderWidgetBuilder(dashboard);
        }
        if (organization.features.includes('dashboards-edit')) {
            return this.renderDashboardDetail();
        }
        return this.renderDefaultDashboardDetail();
    };
    return DashboardDetail;
}(Component));
var StyledPageHeader = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n  grid-row-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  color: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(0, 1fr) max-content;\n    grid-column-gap: ", ";\n    height: 40px;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: minmax(0, 1fr);\n  grid-row-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  color: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(0, 1fr) max-content;\n    grid-column-gap: ", ";\n    height: 40px;\n  }\n"])), space(2), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; }, space(2), function (p) { return p.theme.breakpoints[1]; }, space(2));
export default withApi(withOrganization(DashboardDetail));
var templateObject_1;
//# sourceMappingURL=detail.jsx.map