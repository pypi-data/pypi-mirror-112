import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import LoadingIndicator from 'app/components/loadingIndicator';
import { PanelItem } from 'app/components/panels';
import { t, tct } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
var ProjectPerformance = /** @class */ (function (_super) {
    __extends(ProjectPerformance, _super);
    function ProjectPerformance() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function () {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            var organization = _this.props.organization;
            _this.setState({
                loading: true,
            });
            _this.api.request("/projects/" + orgId + "/" + projectId + "/transaction-threshold/configure/", {
                method: 'DELETE',
                success: function () {
                    trackAnalyticsEvent({
                        eventKey: 'performance_views.project_transaction_threshold.clear',
                        eventName: 'Project Transaction Threshold: Cleared',
                        organization_id: organization.id,
                    });
                },
                complete: function () { return _this.fetchData(); },
            });
        };
        return _this;
    }
    ProjectPerformance.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Performance'), projectId, false);
    };
    ProjectPerformance.prototype.getEndpoints = function () {
        var params = this.props.params;
        var orgId = params.orgId, projectId = params.projectId;
        var endpoints = [
            ['threshold', "/projects/" + orgId + "/" + projectId + "/transaction-threshold/configure/"],
        ];
        return endpoints;
    };
    ProjectPerformance.prototype.getEmptyMessage = function () {
        return t('There is no threshold set for this project.');
    };
    ProjectPerformance.prototype.renderLoading = function () {
        return (<LoadingIndicatorContainer>
        <LoadingIndicator />
      </LoadingIndicatorContainer>);
    };
    Object.defineProperty(ProjectPerformance.prototype, "formFields", {
        get: function () {
            var fields = [
                {
                    name: 'metric',
                    type: 'select',
                    label: t('Calculation Method'),
                    choices: [
                        ['duration', t('Transaction Duration')],
                        ['lcp', t('Largest Contentful Paint')],
                    ],
                    help: tct('This determines which duration is used to set your thresholds. By default, we use transaction duration which measures the entire length of the transaction. You can also set this to use a [link:Web Vital].', {
                        link: (<ExternalLink href="https://docs.sentry.io/product/performance/web-vitals/"/>),
                    }),
                },
                {
                    name: 'threshold',
                    type: 'string',
                    label: t('Response Time Threshold (ms)'),
                    placeholder: t('300'),
                    help: tct('Define what a satisfactory response time is based on the calculation method above. This will affect how your [link1:Apdex] and [link2:User Misery] thresholds are calculated. For example, misery will be 4x your satisfactory response time.', {
                        link1: (<ExternalLink href="https://docs.sentry.io/performance-monitoring/performance/metrics/#apdex"/>),
                        link2: (<ExternalLink href="https://docs.sentry.io/product/performance/metrics/#user-misery"/>),
                    }),
                },
            ];
            return fields;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectPerformance.prototype, "initialData", {
        get: function () {
            var threshold = this.state.threshold;
            return {
                threshold: threshold.threshold,
                metric: threshold.metric,
            };
        },
        enumerable: false,
        configurable: true
    });
    ProjectPerformance.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, project = _a.project;
        var endpoint = "/projects/" + organization.slug + "/" + project.slug + "/transaction-threshold/configure/";
        return (<React.Fragment>
        <SettingsPageHeader title={t('Performance')}/>
        <PermissionAlert />
        <Form saveOnBlur allowUndo initialData={this.initialData} apiMethod="POST" apiEndpoint={endpoint} onSubmitSuccess={function (resp) {
                var initial = _this.initialData;
                var changedThreshold = initial.metric === resp.metric;
                trackAnalyticsEvent({
                    eventKey: 'performance_views.project_transaction_threshold.change',
                    eventName: 'Project Transaction Threshold: Changed',
                    organization_id: organization.id,
                    from: changedThreshold ? initial.threshold : initial.metric,
                    to: changedThreshold ? resp.threshold : resp.metric,
                    key: changedThreshold ? 'threshold' : 'metric',
                });
                _this.setState({ threshold: resp });
            }}>
          <JsonForm title={t('General')} fields={this.formFields} renderFooter={function () { return (<Actions>
                <Button onClick={function () { return _this.handleDelete(); }}>{t('Reset All')}</Button>
              </Actions>); }}/>
        </Form>
      </React.Fragment>);
    };
    return ProjectPerformance;
}(AsyncView));
var Actions = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
var LoadingIndicatorContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 18px 18px 0;\n"], ["\n  margin: 18px 18px 0;\n"])));
export default ProjectPerformance;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectPerformance.jsx.map