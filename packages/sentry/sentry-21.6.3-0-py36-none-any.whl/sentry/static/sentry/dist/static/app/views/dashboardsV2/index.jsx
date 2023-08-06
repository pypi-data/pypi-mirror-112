import { __extends } from "tslib";
import * as React from 'react';
import NotFound from 'app/components/errors/notFound';
import LoadingIndicator from 'app/components/loadingIndicator';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import DashboardDetail from './detail';
import OrgDashboards from './orgDashboards';
import { DashboardState } from './types';
import { DashboardBasicFeature } from './view';
var DashboardsV2Container = /** @class */ (function (_super) {
    __extends(DashboardsV2Container, _super);
    function DashboardsV2Container() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DashboardsV2Container.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, params = _a.params, api = _a.api, location = _a.location, children = _a.children;
        if (organization.features.includes('dashboards-edit')) {
            return children;
        }
        return (<DashboardBasicFeature organization={organization}>
        <OrgDashboards api={api} location={location} params={params} organization={organization}>
          {function (_a) {
                var dashboard = _a.dashboard, dashboards = _a.dashboards, error = _a.error, reloadData = _a.reloadData;
                return error ? (<NotFound />) : dashboard ? (<DashboardDetail {..._this.props} initialState={DashboardState.VIEW} dashboard={dashboard} dashboards={dashboards} reloadData={reloadData}/>) : (<LoadingIndicator />);
            }}
        </OrgDashboards>
      </DashboardBasicFeature>);
    };
    return DashboardsV2Container;
}(React.Component));
export default withApi(withOrganization(DashboardsV2Container));
//# sourceMappingURL=index.jsx.map