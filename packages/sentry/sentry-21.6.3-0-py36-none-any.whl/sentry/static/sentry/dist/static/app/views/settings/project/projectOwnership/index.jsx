import { __assign, __extends, __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import styled from '@emotion/styled';
import { openEditOwnershipRules, openModal } from 'app/actionCreators/modal';
import Feature from 'app/components/acl/feature';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
import AddCodeOwnerModal from 'app/views/settings/project/projectOwnership/addCodeOwnerModal';
import CodeOwnersPanel from 'app/views/settings/project/projectOwnership/codeowners';
import RulesPanel from 'app/views/settings/project/projectOwnership/rulesPanel';
var ProjectOwnership = /** @class */ (function (_super) {
    __extends(ProjectOwnership, _super);
    function ProjectOwnership() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleAddCodeOwner = function () {
            var _a = _this.state, codeMappings = _a.codeMappings, integrations = _a.integrations;
            openModal(function (modalProps) { return (<AddCodeOwnerModal {...modalProps} organization={_this.props.organization} project={_this.props.project} codeMappings={codeMappings} integrations={integrations} onSave={_this.handleCodeownerAdded}/>); });
        };
        _this.handleOwnershipSave = function (text) {
            _this.setState(function (prevState) { return ({
                ownership: __assign(__assign({}, prevState.ownership), { raw: text }),
            }); });
        };
        _this.handleCodeownerAdded = function (data) {
            var codeowners = _this.state.codeowners;
            var newCodeowners = codeowners === null || codeowners === void 0 ? void 0 : codeowners.concat(data);
            _this.setState({ codeowners: newCodeowners });
        };
        _this.handleCodeownerDeleted = function (data) {
            var codeowners = _this.state.codeowners;
            var newCodeowners = codeowners === null || codeowners === void 0 ? void 0 : codeowners.filter(function (codeowner) { return codeowner.id !== data.id; });
            _this.setState({ codeowners: newCodeowners });
        };
        return _this;
    }
    ProjectOwnership.prototype.getTitle = function () {
        var project = this.props.project;
        return routeTitleGen(t('Issue Owners'), project.slug, false);
    };
    ProjectOwnership.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        var endpoints = [
            ['ownership', "/projects/" + organization.slug + "/" + project.slug + "/ownership/"],
            [
                'codeMappings',
                "/organizations/" + organization.slug + "/code-mappings/",
                { query: { projectId: project.id } },
            ],
            [
                'integrations',
                "/organizations/" + organization.slug + "/integrations/",
                { query: { features: ['codeowners'] } },
            ],
        ];
        if (organization.features.includes('integrations-codeowners')) {
            endpoints.push([
                'codeowners',
                "/projects/" + organization.slug + "/" + project.slug + "/codeowners/",
                { query: { expand: ['codeMapping', 'ownershipSyntax'] } },
            ]);
        }
        return endpoints;
    };
    ProjectOwnership.prototype.getPlaceholder = function () {
        return "#example usage\npath:src/example/pipeline/* person@sentry.io #infra\nurl:http://example.com/settings/* #product\ntags.sku_class:enterprise #enterprise";
    };
    ProjectOwnership.prototype.getDetail = function () {
        return tct("Automatically assign issues and send alerts to the right people based on issue properties. [link:Learn more].", {
            link: (<ExternalLink href="https://docs.sentry.io/product/error-monitoring/issue-owners/"/>),
        });
    };
    ProjectOwnership.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, project = _a.project, organization = _a.organization;
        var _b = this.state, ownership = _b.ownership, codeowners = _b.codeowners;
        var disabled = !organization.access.includes('project:write');
        return (<Fragment>
        <SettingsPageHeader title={t('Issue Owners')} action={<Fragment>
              <Button to={{
                    pathname: "/organizations/" + organization.slug + "/issues/",
                    query: { project: project.id },
                }} size="small">
                {t('View Issues')}
              </Button>
              <Feature features={['integrations-codeowners']}>
                <CodeOwnerButton onClick={this.handleAddCodeOwner} size="small" priority="primary" data-test-id="add-codeowner-button">
                  {t('Add Codeowner File')}
                </CodeOwnerButton>
              </Feature>
            </Fragment>}/>
        <PermissionAlert />
        <RulesPanel data-test-id="issueowners-panel" type="issueowners" raw={ownership.raw || ''} dateUpdated={ownership.lastUpdated} placeholder={this.getPlaceholder()} detail={this.getDetail()} controls={[
                <Button key="edit" size="small" onClick={function () {
                        return openEditOwnershipRules({
                            organization: organization,
                            project: project,
                            ownership: ownership,
                            onSave: _this.handleOwnershipSave,
                        });
                    }} disabled={disabled}>
              {t('Edit')}
            </Button>,
            ]}/>
        <Feature features={['integrations-codeowners']}>
          <CodeOwnersPanel codeowners={codeowners} onDelete={this.handleCodeownerDeleted} {...this.props}/>
        </Feature>
        <Form apiEndpoint={"/projects/" + organization.slug + "/" + project.slug + "/ownership/"} apiMethod="PUT" saveOnBlur initialData={{
                fallthrough: ownership.fallthrough,
                autoAssignment: ownership.autoAssignment,
            }} hideFooter>
          <JsonForm forms={[
                {
                    title: t('Issue Owners'),
                    fields: [
                        {
                            name: 'autoAssignment',
                            type: 'boolean',
                            label: t('Automatically assign issues'),
                            help: t('Assign issues when a new event matches the rules above.'),
                            disabled: disabled,
                        },
                        {
                            name: 'fallthrough',
                            type: 'boolean',
                            label: t('Send alert to project members if there’s no assigned owner'),
                            help: t('Alerts will be sent to all users who have access to this project.'),
                            disabled: disabled,
                        },
                    ],
                },
            ]}/>
        </Form>
      </Fragment>);
    };
    return ProjectOwnership;
}(AsyncView));
export default ProjectOwnership;
var CodeOwnerButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var templateObject_1;
//# sourceMappingURL=index.jsx.map