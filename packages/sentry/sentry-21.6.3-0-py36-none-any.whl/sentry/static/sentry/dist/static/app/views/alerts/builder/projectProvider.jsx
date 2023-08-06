import { __assign, __rest } from "tslib";
import * as React from 'react';
import { fetchOrgMembers } from 'app/actionCreators/members';
import Alert from 'app/components/alert';
import LoadingIndicator from 'app/components/loadingIndicator';
import { t } from 'app/locale';
import Projects from 'app/utils/projects';
import withApi from 'app/utils/withApi';
import ScrollToTop from 'app/views/settings/components/scrollToTop';
function AlertBuilderProjectProvider(props) {
    var children = props.children, params = props.params, organization = props.organization, api = props.api, other = __rest(props, ["children", "params", "organization", "api"]);
    var projectId = params.projectId;
    return (<Projects orgId={organization.slug} allProjects>
      {function (_a) {
            var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, isIncomplete = _a.isIncomplete;
            if (!initiallyLoaded) {
                return <LoadingIndicator />;
            }
            var project = projects.find(function (_a) {
                var slug = _a.slug;
                return slug === projectId;
            });
            // if loaded, but project fetching states incomplete or project can't be found, project doesn't exist
            if (isIncomplete || !project) {
                return (<Alert type="warning">
              {t('The project you were looking for was not found.')}
            </Alert>);
            }
            // fetch members list for mail action fields
            fetchOrgMembers(api, organization.slug, [project.id]);
            return (<ScrollToTop location={props.location} disable={function () { return false; }}>
            {children && React.isValidElement(children)
                    ? React.cloneElement(children, __assign(__assign(__assign({}, other), children.props), { project: project, organization: organization }))
                    : children}
          </ScrollToTop>);
        }}
    </Projects>);
}
export default withApi(AlertBuilderProjectProvider);
//# sourceMappingURL=projectProvider.jsx.map