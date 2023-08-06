import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import { Component, Fragment } from 'react';
import { Link } from 'react-router';
import styled from '@emotion/styled';
import { promptsCheck, promptsUpdate } from 'app/actionCreators/prompts';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import ErrorBoundary from 'app/components/errorBoundary';
import ExternalLink from 'app/components/links/externalLink';
import Placeholder from 'app/components/placeholder';
import QuickTrace from 'app/components/quickTrace';
import { generateTraceTarget } from 'app/components/quickTrace/utils';
import { IconClose, IconInfo } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import QuickTraceQuery from 'app/utils/performance/quickTrace/quickTraceQuery';
import { promptIsDismissed } from 'app/utils/promptIsDismissed';
import withApi from 'app/utils/withApi';
var IssueQuickTrace = /** @class */ (function (_super) {
    __extends(IssueQuickTrace, _super);
    function IssueQuickTrace() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            shouldShow: null,
        };
        _this.snoozePrompt = function () {
            var _a = _this.props, api = _a.api, event = _a.event, organization = _a.organization;
            var data = {
                projectId: event.projectID,
                organizationId: organization.id,
                feature: 'quick_trace_missing',
                status: 'snoozed',
            };
            promptsUpdate(api, data).then(function () { return _this.setState({ shouldShow: false }); });
        };
        return _this;
    }
    IssueQuickTrace.prototype.componentDidMount = function () {
        this.promptsCheck();
    };
    IssueQuickTrace.prototype.shouldComponentUpdate = function (nextProps) {
        return this.props.event !== nextProps.event;
    };
    IssueQuickTrace.prototype.promptsCheck = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, event, organization, data;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, event = _a.event, organization = _a.organization;
                        return [4 /*yield*/, promptsCheck(api, {
                                organizationId: organization.id,
                                projectId: event.projectID,
                                feature: 'quick_trace_missing',
                            })];
                    case 1:
                        data = _b.sent();
                        this.setState({ shouldShow: !promptIsDismissed(data !== null && data !== void 0 ? data : {}, 30) });
                        return [2 /*return*/];
                }
            });
        });
    };
    IssueQuickTrace.prototype.handleTraceLink = function (organization) {
        trackAnalyticsEvent({
            eventKey: 'quick_trace.trace_id.clicked',
            eventName: 'Quick Trace: Trace ID clicked',
            organization_id: parseInt(organization.id, 10),
            source: 'issues',
        });
    };
    IssueQuickTrace.prototype.renderTraceLink = function (_a) {
        var _this = this;
        var isLoading = _a.isLoading, error = _a.error, trace = _a.trace, type = _a.type;
        var _b = this.props, event = _b.event, organization = _b.organization;
        if (isLoading || error !== null || trace === null || type === 'empty') {
            return null;
        }
        return (<LinkContainer>
        <Link to={generateTraceTarget(event, organization)} onClick={function () { return _this.handleTraceLink(organization); }}>
          {t('View Full Trace')}
        </Link>
      </LinkContainer>);
    };
    IssueQuickTrace.prototype.renderQuickTrace = function (results) {
        var _a = this.props, event = _a.event, location = _a.location, organization = _a.organization;
        var shouldShow = this.state.shouldShow;
        var isLoading = results.isLoading, error = results.error, trace = results.trace, type = results.type;
        if (isLoading) {
            return <Placeholder height="24px"/>;
        }
        if (error || trace === null || trace.length === 0) {
            if (!shouldShow) {
                return null;
            }
            return (<StyledAlert type="info" icon={<IconInfo size="sm"/>}>
          <AlertContent>
            {tct('The [type] for this error cannot be found. [link]', {
                    type: type === 'missing' ? t('transaction') : t('trace'),
                    link: (<ExternalLink href="https://docs.sentry.io/product/performance/trace-view/#troubleshooting">
                  {t('Read the docs to understand why.')}
                </ExternalLink>),
                })}
            <Button priority="link" title={t('Dismiss for a month')} onClick={this.snoozePrompt}>
              <IconClose />
            </Button>
          </AlertContent>
        </StyledAlert>);
        }
        return (<QuickTrace event={event} quickTrace={results} location={location} organization={organization} anchor="left" errorDest="issue" transactionDest="performance"/>);
    };
    IssueQuickTrace.prototype.render = function () {
        var _this = this;
        var _a = this.props, event = _a.event, organization = _a.organization, location = _a.location;
        return (<ErrorBoundary mini>
        <QuickTraceQuery event={event} location={location} orgSlug={organization.slug}>
          {function (results) {
                return (<Fragment>
                {_this.renderTraceLink(results)}
                <QuickTraceWrapper>{_this.renderQuickTrace(results)}</QuickTraceWrapper>
              </Fragment>);
            }}
        </QuickTraceQuery>
      </ErrorBoundary>);
    };
    return IssueQuickTrace;
}(Component));
var LinkContainer = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n  padding-left: ", ";\n  position: relative;\n\n  &:before {\n    display: block;\n    position: absolute;\n    content: '';\n    left: 0;\n    top: 2px;\n    height: 14px;\n    border-left: 1px solid ", ";\n  }\n"], ["\n  margin-left: ", ";\n  padding-left: ", ";\n  position: relative;\n\n  &:before {\n    display: block;\n    position: absolute;\n    content: '';\n    left: 0;\n    top: 2px;\n    height: 14px;\n    border-left: 1px solid ", ";\n  }\n"])), space(1), space(1), function (p) { return p.theme.border; });
var QuickTraceWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(0.5));
var StyledAlert = styled(Alert)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var AlertContent = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n\n  @media (min-width: ", ") {\n    justify-content: space-between;\n  }\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n\n  @media (min-width: ", ") {\n    justify-content: space-between;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
export default withApi(IssueQuickTrace);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=issueQuickTrace.jsx.map