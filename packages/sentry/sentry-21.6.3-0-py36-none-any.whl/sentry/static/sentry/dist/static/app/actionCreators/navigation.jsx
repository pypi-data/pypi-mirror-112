import { openModal } from 'app/actionCreators/modal';
import NavigationActions from 'app/actions/navigationActions';
import ContextPickerModal from 'app/components/contextPickerModal';
import ProjectsStore from 'app/stores/projectsStore';
// TODO(ts): figure out better typing for react-router here
export function navigateTo(to, router, configUrl) {
    var _a, _b;
    // Check for placeholder params
    var needOrg = to.indexOf(':orgId') > -1;
    var needProject = to.indexOf(':projectId') > -1;
    var comingFromProjectId = (_b = (_a = router === null || router === void 0 ? void 0 : router.location) === null || _a === void 0 ? void 0 : _a.query) === null || _b === void 0 ? void 0 : _b.project;
    var needProjectId = !comingFromProjectId || Array.isArray(comingFromProjectId);
    var projectById = ProjectsStore.getById(comingFromProjectId);
    if (needOrg || (needProject && (needProjectId || !projectById)) || configUrl) {
        openModal(function (modalProps) { return (<ContextPickerModal {...modalProps} nextPath={to} needOrg={needOrg} needProject={needProject} configUrl={configUrl} comingFromProjectId={Array.isArray(comingFromProjectId) ? '' : comingFromProjectId || ''} onFinish={function (path) {
                modalProps.closeModal();
                setTimeout(function () { return router.push(path); }, 0);
            }}/>); }, {});
    }
    else {
        projectById
            ? router.push(to.replace(':projectId', projectById.slug))
            : router.push(to);
    }
}
export function setLastRoute(route) {
    NavigationActions.setLastRoute(route);
}
//# sourceMappingURL=navigation.jsx.map