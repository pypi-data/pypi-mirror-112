import { __assign, __extends, __makeTemplateObject, __read, __rest } from "tslib";
import { Fragment } from 'react';
import styled from '@emotion/styled';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { fields } from 'app/data/forms/accountNotificationSettings';
import { t } from 'app/locale';
import withOrganizations from 'app/utils/withOrganizations';
import AsyncView from 'app/views/asyncView';
import { ACCOUNT_NOTIFICATION_FIELDS, } from 'app/views/settings/account/notifications/fields';
import NotificationSettingsByType from 'app/views/settings/account/notifications/notificationSettingsByType';
import { groupByOrganization, isGroupedByProject, } from 'app/views/settings/account/notifications/utils';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SelectField from 'app/views/settings/components/forms/selectField';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
var PanelBodyLineItem = styled(PanelBody)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 1.4rem;\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"], ["\n  font-size: 1.4rem;\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n"])), function (p) { return p.theme.innerBorder; });
var AccountNotificationsByProject = function (_a) {
    var projects = _a.projects, field = _a.field;
    var projectsByOrg = groupByOrganization(projects);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    var title = field.title, description = field.description, fieldConfig = __rest(field, ["title", "description"]);
    // Display as select box in this view regardless of the type specified in the config
    var data = Object.values(projectsByOrg).map(function (org) { return ({
        name: org.organization.name,
        projects: org.projects.map(function (project) { return (__assign(__assign({}, fieldConfig), { 
            // `name` key refers to field name
            // we use project.id because slugs are not unique across orgs
            name: project.id, label: project.slug })); }),
    }); });
    return (<Fragment>
      {data.map(function (_a) {
            var name = _a.name, projectFields = _a.projects;
            return (<div key={name}>
          <PanelHeader>{name}</PanelHeader>
          {projectFields.map(function (f) { return (<PanelBodyLineItem key={f.name}>
              <SelectField defaultValue={f.defaultValue} name={f.name} choices={f.choices} label={f.label}/>
            </PanelBodyLineItem>); })}
        </div>);
        })}
    </Fragment>);
};
var AccountNotificationsByOrganization = function (_a) {
    var organizations = _a.organizations, field = _a.field;
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    var title = field.title, description = field.description, fieldConfig = __rest(field, ["title", "description"]);
    // Display as select box in this view regardless of the type specified in the config
    var data = organizations.map(function (org) { return (__assign(__assign({}, fieldConfig), { 
        // `name` key refers to field name
        // we use org.id to remain consistent project.id use (which is required because slugs are not unique across orgs)
        name: org.id, label: org.slug })); });
    return (<Fragment>
      {data.map(function (f) { return (<PanelBodyLineItem key={f.name}>
          <SelectField defaultValue={f.defaultValue} name={f.name} choices={f.choices} label={f.label}/>
        </PanelBodyLineItem>); })}
    </Fragment>);
};
var AccountNotificationsByOrganizationContainer = withOrganizations(AccountNotificationsByOrganization);
var AccountNotificationFineTuning = /** @class */ (function (_super) {
    __extends(AccountNotificationFineTuning, _super);
    function AccountNotificationFineTuning() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AccountNotificationFineTuning.prototype.getEndpoints = function () {
        var fineTuneType = this.props.params.fineTuneType;
        var endpoints = [
            ['notifications', '/users/me/notifications/'],
            ['fineTuneData', "/users/me/notifications/" + fineTuneType + "/"],
        ];
        if (isGroupedByProject(fineTuneType)) {
            endpoints.push(['projects', '/projects/']);
        }
        endpoints.push(['emails', '/users/me/emails/']);
        if (fineTuneType === 'email') {
            endpoints.push(['emails', '/users/me/emails/']);
        }
        return endpoints;
    };
    Object.defineProperty(AccountNotificationFineTuning.prototype, "emailChoices", {
        // Return a sorted list of user's verified emails
        get: function () {
            var _a, _b, _c;
            return ((_c = (_b = (_a = this.state.emails) === null || _a === void 0 ? void 0 : _a.filter(function (_a) {
                var isVerified = _a.isVerified;
                return isVerified;
            })) === null || _b === void 0 ? void 0 : _b.sort(function (a, b) {
                // Sort by primary -> email
                if (a.isPrimary) {
                    return -1;
                }
                else if (b.isPrimary) {
                    return 1;
                }
                return a.email < b.email ? -1 : 1;
            })) !== null && _c !== void 0 ? _c : []);
        },
        enumerable: false,
        configurable: true
    });
    AccountNotificationFineTuning.prototype.renderBody = function () {
        var _a = this.props, params = _a.params, organizations = _a.organizations;
        var fineTuneType = params.fineTuneType;
        if (['alerts', 'deploy', 'workflow'].includes(fineTuneType) &&
            organizations.some(function (organization) {
                return organization.features.includes('notification-platform');
            })) {
            return <NotificationSettingsByType notificationType={fineTuneType}/>;
        }
        var _b = this.state, notifications = _b.notifications, projects = _b.projects, fineTuneData = _b.fineTuneData, projectsPageLinks = _b.projectsPageLinks;
        var isProject = isGroupedByProject(fineTuneType);
        var field = ACCOUNT_NOTIFICATION_FIELDS[fineTuneType];
        var title = field.title, description = field.description;
        var _c = __read(isProject ? this.getEndpoints()[2] : [], 2), stateKey = _c[0], url = _c[1];
        var hasProjects = !!(projects === null || projects === void 0 ? void 0 : projects.length);
        if (fineTuneType === 'email') {
            // Fetch verified email addresses
            field.choices = this.emailChoices.map(function (_a) {
                var email = _a.email;
                return [email, email];
            });
        }
        if (!notifications || !fineTuneData) {
            return null;
        }
        return (<div>
        <SettingsPageHeader title={title}/>
        {description && <TextBlock>{description}</TextBlock>}

        {field &&
                field.defaultFieldName &&
                // not implemented yet
                field.defaultFieldName !== 'weeklyReports' && (<Form saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notifications/" initialData={notifications}>
              <JsonForm title={"Default " + title} fields={[fields[field.defaultFieldName]]}/>
            </Form>)}
        <Panel>
          <PanelBody>
            <PanelHeader hasButtons={isProject}>
              <Heading>{isProject ? t('Projects') : t('Organizations')}</Heading>
              <div>
                {isProject &&
                this.renderSearchInput({
                    placeholder: t('Search Projects'),
                    url: url,
                    stateKey: stateKey,
                })}
              </div>
            </PanelHeader>

            <Form saveOnBlur apiMethod="PUT" apiEndpoint={"/users/me/notifications/" + fineTuneType + "/"} initialData={fineTuneData}>
              {isProject && hasProjects && (<AccountNotificationsByProject projects={projects} field={field}/>)}

              {isProject && !hasProjects && (<EmptyMessage>{t('No projects found')}</EmptyMessage>)}

              {!isProject && (<AccountNotificationsByOrganizationContainer field={field}/>)}
            </Form>
          </PanelBody>
        </Panel>

        {projects && <Pagination pageLinks={projectsPageLinks} {...this.props}/>}
      </div>);
    };
    return AccountNotificationFineTuning;
}(AsyncView));
var Heading = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
export default withOrganizations(AccountNotificationFineTuning);
var templateObject_1, templateObject_2;
//# sourceMappingURL=accountNotificationFineTuning.jsx.map