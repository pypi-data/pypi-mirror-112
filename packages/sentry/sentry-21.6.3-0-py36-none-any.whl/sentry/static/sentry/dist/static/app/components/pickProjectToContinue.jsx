import { __makeTemplateObject, __read, __spreadArray } from "tslib";
import styled from '@emotion/styled';
import { openModal } from 'app/actionCreators/modal';
import ContextPickerModal from 'app/components/contextPickerModal';
function PickProjectToContinue(_a) {
    var noProjectRedirectPath = _a.noProjectRedirectPath, nextPath = _a.nextPath, router = _a.router, projects = _a.projects;
    var nextPathQuery = nextPath.query;
    var navigating = false;
    var path = nextPath.pathname + "?project=";
    if (nextPathQuery) {
        var filteredQuery = Object.entries(nextPathQuery)
            .filter(function (_a) {
            var _b = __read(_a, 2), key = _b[0], _value = _b[1];
            return key !== 'project';
        })
            .map(function (_a) {
            var _b = __read(_a, 2), key = _b[0], value = _b[1];
            return key + "=" + value;
        });
        var newPathQuery = __spreadArray(__spreadArray([], __read(filteredQuery)), ['project=']).join('&');
        path = nextPath.pathname + "?" + newPathQuery;
    }
    // if the project in URL is missing, but this release belongs to only one project, redirect there
    if (projects.length === 1) {
        router.replace(path + projects[0].id);
        return null;
    }
    openModal(function (modalProps) { return (<ContextPickerModal {...modalProps} needOrg={false} needProject nextPath={path + ":project"} onFinish={function (pathname) {
            navigating = true;
            router.replace(pathname);
        }} projectSlugs={projects.map(function (p) { return p.slug; })}/>); }, {
        onClose: function () {
            // we want this to be executed only if the user didn't select any project
            // (closed modal either via button, Esc, clicking outside, ...)
            if (!navigating) {
                router.push(noProjectRedirectPath);
            }
        },
    });
    return <ContextPickerBackground />;
}
var ContextPickerBackground = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 100vh;\n  width: 100%;\n"], ["\n  height: 100vh;\n  width: 100%;\n"])));
export default PickProjectToContinue;
var templateObject_1;
//# sourceMappingURL=pickProjectToContinue.jsx.map