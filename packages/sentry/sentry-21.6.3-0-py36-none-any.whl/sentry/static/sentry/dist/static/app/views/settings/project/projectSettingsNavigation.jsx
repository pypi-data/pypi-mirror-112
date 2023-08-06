import { useContext } from 'react';
import AppStoreConnectContext from 'app/components/projects/appStoreConnectContext';
import withProject from 'app/utils/withProject';
import SettingsNavigation from 'app/views/settings/components/settingsNavigation';
import getConfiguration from 'app/views/settings/project/navigationConfiguration';
var ProjectSettingsNavigation = function (_a) {
    var organization = _a.organization, project = _a.project;
    var appStoreConnectContext = useContext(AppStoreConnectContext);
    var debugFilesNeedsReview = !!(appStoreConnectContext === null || appStoreConnectContext === void 0 ? void 0 : appStoreConnectContext.updateAlertMessage);
    return (<SettingsNavigation navigationObjects={getConfiguration({ project: project, organization: organization, debugFilesNeedsReview: debugFilesNeedsReview })} access={new Set(organization.access)} features={new Set(organization.features)} organization={organization} project={project}/>);
};
export default withProject(ProjectSettingsNavigation);
//# sourceMappingURL=projectSettingsNavigation.jsx.map