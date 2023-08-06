import { __assign, __makeTemplateObject } from "tslib";
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import Breadcrumbs from 'app/components/breadcrumbs';
import IdBadge from 'app/components/idBadge';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { isActiveSuperuser } from 'app/utils/isActiveSuperuser';
import recreateRoute from 'app/utils/recreateRoute';
import withProjects from 'app/utils/withProjects';
import MenuItem from 'app/views/settings/components/settingsBreadcrumb/menuItem';
function BuilderBreadCrumbs(props) {
    var orgSlug = props.orgSlug, title = props.title, alertName = props.alertName, projectSlug = props.projectSlug, projects = props.projects, routes = props.routes, canChangeProject = props.canChangeProject, location = props.location;
    var project = projects.find(function (_a) {
        var slug = _a.slug;
        return projectSlug === slug;
    });
    var isSuperuser = isActiveSuperuser();
    var projectCrumbLink = {
        to: "/settings/" + orgSlug + "/projects/" + projectSlug + "/",
        label: <IdBadge project={project} avatarSize={18} disableLink/>,
        preserveGlobalSelection: true,
    };
    var projectCrumbDropdown = {
        onSelect: function (_a) {
            var value = _a.value;
            browserHistory.push(recreateRoute('', {
                routes: routes,
                params: { orgId: orgSlug, projectId: value },
                location: location,
            }));
        },
        label: <IdBadge project={project} avatarSize={18} disableLink/>,
        items: projects
            .filter(function (proj) { return proj.isMember || isSuperuser; })
            .map(function (proj, index) { return ({
            index: index,
            value: proj.slug,
            label: (<MenuItem>
            <IdBadge project={proj} avatarProps={{ consistentWidth: true }} avatarSize={18} disableLink/>
          </MenuItem>),
            searchKey: proj.slug,
        }); }),
    };
    var projectCrumb = canChangeProject ? projectCrumbDropdown : projectCrumbLink;
    var crumbs = [
        {
            to: "/organizations/" + orgSlug + "/alerts/rules/",
            label: t('Alerts'),
            preserveGlobalSelection: true,
        },
        projectCrumb,
        __assign({ label: title }, (alertName
            ? {
                to: "/organizations/" + orgSlug + "/alerts/" + projectSlug + "/wizard",
                preserveGlobalSelection: true,
            }
            : {})),
    ];
    if (alertName) {
        crumbs.push({ label: alertName });
    }
    return <StyledBreadcrumbs crumbs={crumbs}/>;
}
var StyledBreadcrumbs = styled(Breadcrumbs)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 18px;\n  margin-bottom: ", ";\n"], ["\n  font-size: 18px;\n  margin-bottom: ", ";\n"])), space(3));
export default withProjects(BuilderBreadCrumbs);
var templateObject_1;
//# sourceMappingURL=builderBreadCrumbs.jsx.map