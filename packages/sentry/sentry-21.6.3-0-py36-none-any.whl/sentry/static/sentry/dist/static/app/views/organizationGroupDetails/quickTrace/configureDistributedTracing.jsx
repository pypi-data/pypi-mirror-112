import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { Component } from 'react';
import styled from '@emotion/styled';
import quickTraceExample from 'sentry-images/spot/performance-quick-trace.svg';
import { promptsCheck, promptsUpdate } from 'app/actionCreators/prompts';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Hovercard from 'app/components/hovercard';
import { Panel } from 'app/components/panels';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getConfigureTracingDocsLink } from 'app/utils/docs';
import { promptCanShow, promptIsDismissed } from 'app/utils/promptIsDismissed';
import withApi from 'app/utils/withApi';
var DISTRIBUTED_TRACING_FEATURE = 'distributed_tracing';
var ConfigureDistributedTracing = /** @class */ (function (_super) {
    __extends(ConfigureDistributedTracing, _super);
    function ConfigureDistributedTracing() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            shouldShow: null,
        };
        return _this;
    }
    ConfigureDistributedTracing.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ConfigureDistributedTracing.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, event, project, organization, data;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, event = _a.event, project = _a.project, organization = _a.organization;
                        if (!promptCanShow(DISTRIBUTED_TRACING_FEATURE, event.eventID)) {
                            this.setState({ shouldShow: false });
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, promptsCheck(api, {
                                projectId: project.id,
                                organizationId: organization.id,
                                feature: DISTRIBUTED_TRACING_FEATURE,
                            })];
                    case 1:
                        data = _b.sent();
                        this.setState({ shouldShow: !promptIsDismissed(data !== null && data !== void 0 ? data : {}, 30) });
                        return [2 /*return*/];
                }
            });
        });
    };
    ConfigureDistributedTracing.prototype.trackAnalytics = function (_a) {
        var eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, project = _b.project, organization = _b.organization;
        trackAnalyticsEvent({
            eventKey: eventKey,
            eventName: eventName,
            organization_id: parseInt(organization.id, 10),
            project_id: parseInt(project.id, 10),
            platform: project.platform,
        });
    };
    ConfigureDistributedTracing.prototype.handleClick = function (_a) {
        var _this = this;
        var action = _a.action, eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, api = _b.api, project = _b.project, organization = _b.organization;
        var data = {
            projectId: project.id,
            organizationId: organization.id,
            feature: DISTRIBUTED_TRACING_FEATURE,
            status: action,
        };
        promptsUpdate(api, data).then(function () { return _this.setState({ shouldShow: false }); });
        this.trackAnalytics({ eventKey: eventKey, eventName: eventName });
    };
    ConfigureDistributedTracing.prototype.renderActionButton = function (docsLink) {
        var _this = this;
        var features = ['organizations:performance-view'];
        var noFeatureMessage = t('Requires performance monitoring.');
        var renderDisabled = function (p) { return (<Hovercard body={<FeatureDisabled features={features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
        {p.children(p)}
      </Hovercard>); };
        return (<Feature hookName="feature-disabled:configure-distributed-tracing" features={features} renderDisabled={renderDisabled}>
        {function () { return (<Button size="small" priority="primary" href={docsLink} onClick={function () {
                    return _this.trackAnalytics({
                        eventKey: 'quick_trace.missing_instrumentation.docs',
                        eventName: 'Quick Trace: Missing Instrumentation Docs',
                    });
                }}>
            {t('Read the docs')}
          </Button>); }}
      </Feature>);
    };
    ConfigureDistributedTracing.prototype.render = function () {
        var _this = this;
        var project = this.props.project;
        var shouldShow = this.state.shouldShow;
        if (!shouldShow) {
            return null;
        }
        var docsLink = getConfigureTracingDocsLink(project);
        // if the platform does not support performance, do not show this prompt
        if (docsLink === null) {
            return null;
        }
        return (<ExampleQuickTracePanel dashedBorder>
        <div>
          <Header>{t('Configure Distributed Tracing')}</Header>
          <Description>
            {t('See what happened right before and after this error')}
          </Description>
        </div>
        <Image src={quickTraceExample} alt="configure distributed tracing"/>
        <ActionButtons>
          {this.renderActionButton(docsLink)}
          <ButtonBar merged>
            <Button title={t('Remind me next month')} size="small" onClick={function () {
                return _this.handleClick({
                    action: 'snoozed',
                    eventKey: 'quick_trace.missing_instrumentation.snoozed',
                    eventName: 'Quick Trace: Missing Instrumentation Snoozed',
                });
            }}>
              {t('Snooze')}
            </Button>
            <Button title={t('Dismiss for this project')} size="small" onClick={function () {
                return _this.handleClick({
                    action: 'dismissed',
                    eventKey: 'quick_trace.missing_instrumentation.dismissed',
                    eventName: 'Quick Trace: Missing Instrumentation Dismissed',
                });
            }}>
              {t('Dismiss')}
            </Button>
          </ButtonBar>
        </ActionButtons>
      </ExampleQuickTracePanel>);
    };
    return ConfigureDistributedTracing;
}(Component));
var ExampleQuickTracePanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1.5fr 1fr;\n  grid-template-rows: auto max-content;\n  grid-gap: ", ";\n  background: none;\n  padding: ", ";\n  margin: ", " 0;\n"], ["\n  display: grid;\n  grid-template-columns: 1.5fr 1fr;\n  grid-template-rows: auto max-content;\n  grid-gap: ", ";\n  background: none;\n  padding: ", ";\n  margin: ", " 0;\n"])), space(1), space(2), space(2));
var Header = styled('h3')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  text-transform: uppercase;\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  text-transform: uppercase;\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, space(1));
var Description = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var Image = styled('img')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  grid-row: 1/3;\n  grid-column: 2/3;\n  justify-self: end;\n"], ["\n  grid-row: 1/3;\n  grid-column: 2/3;\n  justify-self: end;\n"])));
var ActionButtons = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content auto;\n  justify-items: start;\n  align-items: end;\n  grid-column-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content auto;\n  justify-items: start;\n  align-items: end;\n  grid-column-gap: ", ";\n"])), space(1));
export default withApi(ConfigureDistributedTracing);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=configureDistributedTracing.jsx.map