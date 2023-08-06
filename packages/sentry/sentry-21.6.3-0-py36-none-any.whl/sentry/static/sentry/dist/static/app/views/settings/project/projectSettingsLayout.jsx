import { __rest } from "tslib";
import * as React from 'react';
import * as AppStoreConnectContext from 'app/components/projects/appStoreConnectContext';
import withOrganization from 'app/utils/withOrganization';
import ProjectContext from 'app/views/projects/projectContext';
import SettingsLayout from 'app/views/settings/components/settingsLayout';
import ProjectSettingsNavigation from 'app/views/settings/project/projectSettingsNavigation';
function ProjectSettingsLayout(_a) {
    var params = _a.params, organization = _a.organization, children = _a.children, routes = _a.routes, props = __rest(_a, ["params", "organization", "children", "routes"]);
    var orgId = params.orgId, projectId = params.projectId;
    return (<ProjectContext orgId={orgId} projectId={projectId}>
      {function (_a) {
            var project = _a.project;
            return (<AppStoreConnectContext.Provider project={project} organization={organization}>
          <SettingsLayout params={params} routes={routes} {...props} renderNavigation={function () { return (<ProjectSettingsNavigation organization={organization}/>); }}>
            {children && React.isValidElement(children)
                    ? React.cloneElement(children, {
                        organization: organization,
                    })
                    : children}
          </SettingsLayout>
        </AppStoreConnectContext.Provider>);
        }}
    </ProjectContext>);
}
export default withOrganization(ProjectSettingsLayout);
//# sourceMappingURL=projectSettingsLayout.jsx.map