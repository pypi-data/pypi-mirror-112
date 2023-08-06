import { __assign, __extends } from "tslib";
import { Fragment } from 'react';
import ProjectActions from 'app/actions/projectActions';
import Feature from 'app/components/acl/feature';
import ExternalLink from 'app/components/links/externalLink';
import { fields } from 'app/data/forms/projectIssueGrouping';
import { t, tct } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import UpgradeGrouping from './upgradeGrouping';
var ProjectDebugSymbols = /** @class */ (function (_super) {
    __extends(ProjectDebugSymbols, _super);
    function ProjectDebugSymbols() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function (response) {
            // This will update our project context
            ProjectActions.updateSuccess(response);
        };
        return _this;
    }
    ProjectDebugSymbols.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Issue Grouping'), projectId, false);
    };
    ProjectDebugSymbols.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { groupingConfigs: [] });
    };
    ProjectDebugSymbols.prototype.getEndpoints = function () {
        return [['groupingConfigs', '/grouping-configs/']];
    };
    ProjectDebugSymbols.prototype.renderBody = function () {
        var groupingConfigs = this.state.groupingConfigs;
        var _a = this.props, organization = _a.organization, project = _a.project, params = _a.params;
        var orgId = params.orgId, projectId = params.projectId;
        var endpoint = "/projects/" + orgId + "/" + projectId + "/";
        var access = new Set(organization.access);
        var jsonFormProps = {
            additionalFieldProps: {
                organization: organization,
                groupingConfigs: groupingConfigs,
            },
            features: new Set(organization.features),
            access: access,
            disabled: !access.has('project:write'),
        };
        return (<Fragment>
        <SettingsPageHeader title={t('Issue Grouping')}/>

        <TextBlock>
          {tct("All events have a fingerprint. Events with the same fingerprint are grouped together into an issue. To learn more about issue grouping, [link: read the docs].", {
                link: (<ExternalLink href="https://docs.sentry.io/product/data-management-settings/event-grouping/"/>),
            })}
        </TextBlock>

        <Form saveOnBlur allowUndo initialData={project} apiMethod="PUT" apiEndpoint={endpoint} onSubmitSuccess={this.handleSubmit}>
          <JsonForm {...jsonFormProps} title={t('Fingerprint Rules')} fields={[fields.fingerprintingRules]}/>

          <JsonForm {...jsonFormProps} title={t('Stack Trace Rules')} fields={[fields.groupingEnhancements]}/>

          <Feature features={['set-grouping-config']} organization={organization}>
            <JsonForm {...jsonFormProps} title={t('Change defaults')} fields={[
                fields.groupingConfig,
                fields.secondaryGroupingConfig,
                fields.secondaryGroupingExpiry,
            ]}/>
          </Feature>

          <UpgradeGrouping groupingConfigs={groupingConfigs !== null && groupingConfigs !== void 0 ? groupingConfigs : []} organization={organization} projectId={params.projectId} project={project} api={this.api} onUpgrade={this.fetchData}/>
        </Form>
      </Fragment>);
    };
    return ProjectDebugSymbols;
}(AsyncView));
export default ProjectDebugSymbols;
//# sourceMappingURL=index.jsx.map