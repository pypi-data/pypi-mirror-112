import { __extends, __makeTemplateObject } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import * as Layout from 'app/components/layouts/thirds';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import space from 'app/styles/space';
import BuilderBreadCrumbs from 'app/views/alerts/builder/builderBreadCrumbs';
import IncidentRulesDetails from 'app/views/alerts/incidentRules/details';
import IssueEditor from 'app/views/alerts/issueRuleEditor';
var ProjectAlertsEditor = /** @class */ (function (_super) {
    __extends(ProjectAlertsEditor, _super);
    function ProjectAlertsEditor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            alertType: '',
            ruleName: '',
        };
        _this.handleChangeTitle = function (ruleName) {
            _this.setState({ ruleName: ruleName });
        };
        return _this;
    }
    ProjectAlertsEditor.prototype.getTitle = function () {
        var ruleName = this.state.ruleName;
        return "" + ruleName;
    };
    ProjectAlertsEditor.prototype.render = function () {
        var _a = this.props, hasMetricAlerts = _a.hasMetricAlerts, location = _a.location, organization = _a.organization, project = _a.project, routes = _a.routes;
        var alertType = location.pathname.includes('/alerts/metric-rules/')
            ? 'metric'
            : 'issue';
        return (<Fragment>
        <SentryDocumentTitle title={this.getTitle()} orgSlug={organization.slug} projectSlug={project.slug}/>
        <Layout.Header>
          <Layout.HeaderContent>
            <BuilderBreadCrumbs hasMetricAlerts={hasMetricAlerts} orgSlug={organization.slug} title={t('Edit Alert Rule')} projectSlug={project.slug} routes={routes} location={location}/>
            <Layout.Title>{this.getTitle()}</Layout.Title>
          </Layout.HeaderContent>
        </Layout.Header>
        <EditConditionsBody>
          <Layout.Main fullWidth>
            {(!hasMetricAlerts || alertType === 'issue') && (<IssueEditor {...this.props} project={project} onChangeTitle={this.handleChangeTitle}/>)}
            {hasMetricAlerts && alertType === 'metric' && (<IncidentRulesDetails {...this.props} project={project} onChangeTitle={this.handleChangeTitle}/>)}
          </Layout.Main>
        </EditConditionsBody>
      </Fragment>);
    };
    return ProjectAlertsEditor;
}(Component));
var EditConditionsBody = styled(Layout.Body)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: -", ";\n\n  *:not(img) {\n    max-width: 1000px;\n  }\n"], ["\n  margin-bottom: -", ";\n\n  *:not(img) {\n    max-width: 1000px;\n  }\n"])), space(3));
export default ProjectAlertsEditor;
var templateObject_1;
//# sourceMappingURL=edit.jsx.map