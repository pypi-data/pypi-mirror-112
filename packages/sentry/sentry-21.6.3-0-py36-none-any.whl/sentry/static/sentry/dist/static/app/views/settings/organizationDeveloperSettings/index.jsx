import { __extends } from "tslib";
import { removeSentryApp } from 'app/actionCreators/sentryApps';
import Access from 'app/components/acl/access';
import AlertLink from 'app/components/alertLink';
import Button from 'app/components/button';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { IconAdd } from 'app/icons';
import { t } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import SentryApplicationRow from 'app/views/settings/organizationDeveloperSettings/sentryApplicationRow';
var OrganizationDeveloperSettings = /** @class */ (function (_super) {
    __extends(OrganizationDeveloperSettings, _super);
    function OrganizationDeveloperSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.removeApp = function (app) {
            var apps = _this.state.applications.filter(function (a) { return a.slug !== app.slug; });
            removeSentryApp(_this.api, app).then(function () {
                _this.setState({ applications: apps });
            }, function () { });
        };
        _this.renderApplicationRow = function (app) {
            var organization = _this.props.organization;
            return (<SentryApplicationRow key={app.uuid} app={app} organization={organization} onRemoveApp={_this.removeApp}/>);
        };
        return _this;
    }
    OrganizationDeveloperSettings.prototype.getTitle = function () {
        var orgId = this.props.params.orgId;
        return routeTitleGen(t('Developer Settings'), orgId, false);
    };
    OrganizationDeveloperSettings.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        return [['applications', "/organizations/" + orgId + "/sentry-apps/"]];
    };
    OrganizationDeveloperSettings.prototype.renderInternalIntegrations = function () {
        var orgId = this.props.params.orgId;
        var organization = this.props.organization;
        var integrations = this.state.applications.filter(function (app) { return app.status === 'internal'; });
        var isEmpty = integrations.length === 0;
        var permissionTooltipText = t('Manager or Owner permissions required to add an internal integration.');
        var action = (<Access organization={organization} access={['org:write']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<Button priority="primary" disabled={!hasAccess} title={!hasAccess ? permissionTooltipText : undefined} size="small" to={"/settings/" + orgId + "/developer-settings/new-internal/"} icon={<IconAdd size="xs" isCircled/>}>
            {t('New Internal Integration')}
          </Button>);
            }}
      </Access>);
        return (<Panel>
        <PanelHeader hasButtons>
          {t('Internal Integrations')}
          {action}
        </PanelHeader>
        <PanelBody>
          {!isEmpty ? (integrations.map(this.renderApplicationRow)) : (<EmptyMessage>
              {t('No internal integrations have been created yet.')}
            </EmptyMessage>)}
        </PanelBody>
      </Panel>);
    };
    OrganizationDeveloperSettings.prototype.renderExernalIntegrations = function () {
        var orgId = this.props.params.orgId;
        var organization = this.props.organization;
        var integrations = this.state.applications.filter(function (app) { return app.status !== 'internal'; });
        var isEmpty = integrations.length === 0;
        var permissionTooltipText = t('Manager or Owner permissions required to add a public integration.');
        var action = (<Access organization={organization} access={['org:write']}>
        {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<Button priority="primary" disabled={!hasAccess} title={!hasAccess ? permissionTooltipText : undefined} size="small" to={"/settings/" + orgId + "/developer-settings/new-public/"} icon={<IconAdd size="xs" isCircled/>}>
            {t('New Public Integration')}
          </Button>);
            }}
      </Access>);
        return (<Panel>
        <PanelHeader hasButtons>
          {t('Public Integrations')}
          {action}
        </PanelHeader>
        <PanelBody>
          {!isEmpty ? (integrations.map(this.renderApplicationRow)) : (<EmptyMessage>
              {t('No public integrations have been created yet.')}
            </EmptyMessage>)}
        </PanelBody>
      </Panel>);
    };
    OrganizationDeveloperSettings.prototype.renderBody = function () {
        return (<div>
        <SettingsPageHeader title={t('Developer Settings')}/>
        <AlertLink href="https://docs.sentry.io/product/integrations/integration-platform/">
          {t('Have questions about the Integration Platform? Learn more about it in our docs.')}
        </AlertLink>
        {this.renderExernalIntegrations()}
        {this.renderInternalIntegrations()}
      </div>);
    };
    return OrganizationDeveloperSettings;
}(AsyncView));
export default withOrganization(OrganizationDeveloperSettings);
//# sourceMappingURL=index.jsx.map