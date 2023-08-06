import React from 'react';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import NotFound from 'app/components/errors/notFound';
import LoadingIndicator from 'app/components/loadingIndicator';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import DashboardDetail from './detail';
import OrgDashboards from './orgDashboards';
import { DashboardState } from './types';
function ViewEditDashboard(props) {
    var organization = props.organization, params = props.params, api = props.api, location = props.location;
    return (<DashboardBasicFeature organization={organization}>
      <OrgDashboards api={api} location={location} params={params} organization={organization}>
        {function (_a) {
            var dashboard = _a.dashboard, dashboards = _a.dashboards, error = _a.error, reloadData = _a.reloadData;
            return error ? (<NotFound />) : dashboard ? (<DashboardDetail {...props} initialState={DashboardState.VIEW} dashboard={dashboard} dashboards={dashboards} reloadData={reloadData}/>) : (<LoadingIndicator />);
        }}
      </OrgDashboards>
    </DashboardBasicFeature>);
}
export default withApi(withOrganization(ViewEditDashboard));
export var DashboardBasicFeature = function (_a) {
    var organization = _a.organization, children = _a.children;
    var renderDisabled = function () { return (<PageContent>
      <Alert type="warning">{t("You don't have access to this feature")}</Alert>
    </PageContent>); };
    return (<Feature hookName="feature-disabled:dashboards-page" features={['organizations:dashboards-basic']} organization={organization} renderDisabled={renderDisabled}>
      {children}
    </Feature>);
};
//# sourceMappingURL=view.jsx.map