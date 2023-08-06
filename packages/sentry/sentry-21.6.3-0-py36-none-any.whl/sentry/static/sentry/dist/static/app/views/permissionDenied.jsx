import { __extends } from "tslib";
import { Component } from 'react';
import DocumentTitle from 'react-document-title';
import { withRouter } from 'react-router';
import * as Sentry from '@sentry/react';
import ExternalLink from 'app/components/links/externalLink';
import LoadingError from 'app/components/loadingError';
import { t, tct } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
import withOrganization from 'app/utils/withOrganization';
import withProject from 'app/utils/withProject';
var ERROR_NAME = 'Permission Denied';
var PermissionDenied = /** @class */ (function (_super) {
    __extends(PermissionDenied, _super);
    function PermissionDenied() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PermissionDenied.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, routes = _a.routes;
        var route = getRouteStringFromRoutes(routes);
        Sentry.withScope(function (scope) {
            scope.setFingerprint([ERROR_NAME, route]);
            scope.setExtra('route', route);
            scope.setExtra('orgFeatures', (organization && organization.features) || []);
            scope.setExtra('orgAccess', (organization && organization.access) || []);
            scope.setExtra('projectFeatures', (project && project.features) || []);
            Sentry.captureException(new Error("" + ERROR_NAME + (route ? " : " + route : '')));
        });
    };
    PermissionDenied.prototype.render = function () {
        return (<DocumentTitle title={t('Permission Denied')}>
        <PageContent>
          <LoadingError message={tct("Your role does not have the necessary permissions to access this\n               resource, please read more about [link:organizational roles]", {
                link: (<ExternalLink href="https://docs.sentry.io/product/accounts/membership/"/>),
            })}/>
        </PageContent>
      </DocumentTitle>);
    };
    return PermissionDenied;
}(Component));
export default withRouter(withOrganization(withProject(PermissionDenied)));
//# sourceMappingURL=permissionDenied.jsx.map