import { __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import moment from 'moment';
import Alert from 'app/components/alert';
import ActorAvatar from 'app/components/avatar/actorAvatar';
import { SectionHeading } from 'app/components/charts/styles';
import { getInterval } from 'app/components/charts/utils';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import Duration from 'app/components/duration';
import IdBadge from 'app/components/idBadge';
import { KeyValueTable, KeyValueTableRow } from 'app/components/keyValueTable';
import * as Layout from 'app/components/layouts/thirds';
import { Panel, PanelBody } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import TimeSince from 'app/components/timeSince';
import Tooltip from 'app/components/tooltip';
import { IconCheckmark, IconFire, IconInfo, IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import Projects from 'app/utils/projects';
import { AlertRuleThresholdType, Dataset, } from 'app/views/alerts/incidentRules/types';
import { extractEventTypeFilterFromRule } from 'app/views/alerts/incidentRules/utils/getEventTypeFilter';
import Timeline from 'app/views/alerts/rules/details/timeline';
import AlertBadge from '../../alertBadge';
import { AlertRuleStatus, IncidentStatus } from '../../types';
import { API_INTERVAL_POINTS_LIMIT, TIME_OPTIONS } from './constants';
import MetricChart from './metricChart';
import RelatedIssues from './relatedIssues';
import RelatedTransactions from './relatedTransactions';
var DetailsBody = /** @class */ (function (_super) {
    __extends(DetailsBody, _super);
    function DetailsBody() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DetailsBody.prototype.getMetricText = function () {
        var rule = this.props.rule;
        if (!rule) {
            return '';
        }
        var aggregate = rule.aggregate;
        return tct('[metric]', {
            metric: aggregate,
        });
    };
    DetailsBody.prototype.getTimeWindow = function () {
        var rule = this.props.rule;
        if (!rule) {
            return '';
        }
        var timeWindow = rule.timeWindow;
        return tct('[window]', {
            window: <Duration seconds={timeWindow * 60}/>,
        });
    };
    DetailsBody.prototype.getInterval = function () {
        var _a = this.props, _b = _a.timePeriod, start = _b.start, end = _b.end, rule = _a.rule;
        var startDate = moment.utc(start);
        var endDate = moment.utc(end);
        var timeWindow = rule === null || rule === void 0 ? void 0 : rule.timeWindow;
        if (timeWindow &&
            endDate.diff(startDate) < API_INTERVAL_POINTS_LIMIT * timeWindow * 60 * 1000) {
            return timeWindow + "m";
        }
        return getInterval({ start: start, end: end }, true);
    };
    DetailsBody.prototype.getFilter = function () {
        var rule = this.props.rule;
        if (!rule) {
            return null;
        }
        return (<Filters>
        <code>{extractEventTypeFilterFromRule(rule)}</code>&nbsp;&nbsp;
        {rule.query && <code>{rule.query}</code>}
      </Filters>);
    };
    DetailsBody.prototype.renderTrigger = function (trigger) {
        var rule = this.props.rule;
        if (!rule) {
            return null;
        }
        var status = trigger.label === 'critical' ? (<StatusWrapper>
          <IconFire color="red300" size="sm"/> Critical
        </StatusWrapper>) : trigger.label === 'warning' ? (<StatusWrapper>
          <IconWarning color="yellow300" size="sm"/> Warning
        </StatusWrapper>) : (<StatusWrapper>
          <IconCheckmark color="green300" size="sm" isCircled/> Resolved
        </StatusWrapper>);
        var thresholdTypeText = rule.thresholdType === AlertRuleThresholdType.ABOVE ? t('above') : t('below');
        return (<TriggerCondition>
        {status}
        <TriggerText>{thresholdTypeText + " " + trigger.alertThreshold}</TriggerText>
      </TriggerCondition>);
    };
    DetailsBody.prototype.renderRuleDetails = function () {
        var _a, _b, _c;
        var rule = this.props.rule;
        if (rule === undefined) {
            return <Placeholder height="200px"/>;
        }
        var criticalTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'warning';
        });
        var ownerId = (_a = rule.owner) === null || _a === void 0 ? void 0 : _a.split(':')[1];
        var teamActor = ownerId && { type: 'team', id: ownerId, name: '' };
        return (<React.Fragment>
        <SidebarGroup>
          <Heading>{t('Metric')}</Heading>
          <RuleText>{this.getMetricText()}</RuleText>
        </SidebarGroup>

        <SidebarGroup>
          <Heading>{t('Environment')}</Heading>
          <RuleText>{(_b = rule.environment) !== null && _b !== void 0 ? _b : 'All'}</RuleText>
        </SidebarGroup>

        <SidebarGroup>
          <Heading>{t('Filters')}</Heading>
          {this.getFilter()}
        </SidebarGroup>

        <SidebarGroup>
          <Heading>{t('Conditions')}</Heading>
          {criticalTrigger && this.renderTrigger(criticalTrigger)}
          {warningTrigger && this.renderTrigger(warningTrigger)}
        </SidebarGroup>

        <SidebarGroup>
          <Heading>{t('Other Details')}</Heading>
          <KeyValueTable>
            <KeyValueTableRow keyName={t('Team')} value={teamActor ? <ActorAvatar actor={teamActor} size={24}/> : 'Unassigned'}/>

            {rule.createdBy && (<KeyValueTableRow keyName={t('Created By')} value={<CreatedBy>{(_c = rule.createdBy.name) !== null && _c !== void 0 ? _c : '-'}</CreatedBy>}/>)}

            {rule.dateModified && (<KeyValueTableRow keyName={t('Last Modified')} value={<TimeSince date={rule.dateModified} suffix={t('ago')}/>}/>)}
          </KeyValueTable>
        </SidebarGroup>
      </React.Fragment>);
    };
    DetailsBody.prototype.renderMetricStatus = function () {
        var incidents = this.props.incidents;
        // get current status
        var activeIncident = incidents === null || incidents === void 0 ? void 0 : incidents.find(function (_a) {
            var dateClosed = _a.dateClosed;
            return !dateClosed;
        });
        var status = activeIncident ? activeIncident.status : IncidentStatus.CLOSED;
        var latestIncident = (incidents === null || incidents === void 0 ? void 0 : incidents.length) ? incidents[0] : null;
        // The date at which the alert was triggered or resolved
        var activityDate = activeIncident
            ? activeIncident.dateStarted
            : latestIncident
                ? latestIncident.dateClosed
                : null;
        return (<StatusContainer>
        <HeaderItem>
          <Heading noMargin>{t('Current Status')}</Heading>
          <Status>
            <AlertBadge status={status} hideText/>
            {activeIncident ? t('Triggered') : t('Resolved')}
            {activityDate ? <TimeSince date={activityDate}/> : '-'}
          </Status>
        </HeaderItem>
      </StatusContainer>);
    };
    DetailsBody.prototype.renderLoading = function () {
        return (<Layout.Body>
        <Layout.Main>
          <Placeholder height="38px"/>
          <ChartPanel>
            <PanelBody withPadding>
              <Placeholder height="200px"/>
            </PanelBody>
          </ChartPanel>
        </Layout.Main>
        <Layout.Side>
          <Placeholder height="200px"/>
        </Layout.Side>
      </Layout.Body>);
    };
    DetailsBody.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, rule = _a.rule, incidents = _a.incidents, location = _a.location, organization = _a.organization, timePeriod = _a.timePeriod, selectedIncident = _a.selectedIncident, handleZoom = _a.handleZoom, orgId = _a.params.orgId;
        if (!rule) {
            return this.renderLoading();
        }
        var query = rule.query, projectSlugs = rule.projects;
        var queryWithTypeFilter = (query + " " + extractEventTypeFilterFromRule(rule)).trim();
        return (<Projects orgId={orgId} slugs={projectSlugs}>
        {function (_a) {
                var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
                return initiallyLoaded ? (<React.Fragment>
              {selectedIncident &&
                        selectedIncident.alertRule.status === AlertRuleStatus.SNAPSHOT && (<StyledLayoutBody>
                    <StyledAlert type="warning" icon={<IconInfo size="md"/>}>
                      {t('Alert Rule settings have been updated since this alert was triggered.')}
                    </StyledAlert>
                  </StyledLayoutBody>)}
              <StyledLayoutBodyWrapper>
                <Layout.Main>
                  <HeaderContainer>
                    <HeaderGrid>
                      <HeaderItem>
                        <Heading noMargin>{t('Display')}</Heading>
                        <ChartControls>
                          <DropdownControl label={timePeriod.display}>
                            {TIME_OPTIONS.map(function (_a) {
                        var label = _a.label, value = _a.value;
                        return (<DropdownItem key={value} eventKey={value} onSelect={_this.props.handleTimePeriodChange}>
                                {label}
                              </DropdownItem>);
                    })}
                          </DropdownControl>
                        </ChartControls>
                      </HeaderItem>
                      {projects && projects.length && (<HeaderItem>
                          <Heading noMargin>{t('Project')}</Heading>

                          <IdBadge avatarSize={16} project={projects[0]}/>
                        </HeaderItem>)}
                      <HeaderItem>
                        <Heading noMargin>
                          {t('Time Interval')}
                          <Tooltip title={t('The time window over which the metric is evaluated.')}>
                            <IconInfo size="xs" color="gray200"/>
                          </Tooltip>
                        </Heading>

                        <RuleText>{_this.getTimeWindow()}</RuleText>
                      </HeaderItem>
                    </HeaderGrid>
                  </HeaderContainer>

                  <MetricChart api={api} rule={rule} incidents={incidents} timePeriod={timePeriod} selectedIncident={selectedIncident} organization={organization} projects={projects} interval={_this.getInterval()} filter={_this.getFilter()} query={queryWithTypeFilter} orgId={orgId} handleZoom={handleZoom}/>
                  <DetailWrapper>
                    <ActivityWrapper>
                      {(rule === null || rule === void 0 ? void 0 : rule.dataset) === Dataset.ERRORS && (<RelatedIssues organization={organization} rule={rule} projects={(projects || []).filter(function (project) {
                            return rule.projects.includes(project.slug);
                        })} timePeriod={timePeriod}/>)}
                      {(rule === null || rule === void 0 ? void 0 : rule.dataset) === Dataset.TRANSACTIONS && (<RelatedTransactions organization={organization} location={location} rule={rule} projects={(projects || []).filter(function (project) {
                            return rule.projects.includes(project.slug);
                        })} start={timePeriod.start} end={timePeriod.end} filter={extractEventTypeFilterFromRule(rule)}/>)}
                    </ActivityWrapper>
                  </DetailWrapper>
                </Layout.Main>
                <Layout.Side>
                  {_this.renderMetricStatus()}
                  <Timeline api={api} organization={organization} rule={rule} incidents={incidents}/>
                  {_this.renderRuleDetails()}
                </Layout.Side>
              </StyledLayoutBodyWrapper>
            </React.Fragment>) : (<Placeholder height="200px"/>);
            }}
      </Projects>);
    };
    return DetailsBody;
}(React.Component));
export default DetailsBody;
var SidebarGroup = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var DetailWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n\n  @media (max-width: ", ") {\n    flex-direction: column-reverse;\n  }\n"], ["\n  display: flex;\n  flex: 1;\n\n  @media (max-width: ", ") {\n    flex-direction: column-reverse;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var StatusWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  svg {\n    margin-right: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  svg {\n    margin-right: ", ";\n  }\n"])), space(0.5));
var HeaderContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  height: 60px;\n  display: flex;\n  flex-direction: row;\n  align-content: flex-start;\n"], ["\n  height: 60px;\n  display: flex;\n  flex-direction: row;\n  align-content: flex-start;\n"])));
var HeaderGrid = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto auto auto;\n  align-items: stretch;\n  grid-gap: 60px;\n"], ["\n  display: grid;\n  grid-template-columns: auto auto auto;\n  align-items: stretch;\n  grid-gap: 60px;\n"])));
var HeaderItem = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n\n  > *:nth-child(2) {\n    flex: 1;\n    display: flex;\n    align-items: center;\n  }\n"], ["\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n\n  > *:nth-child(2) {\n    flex: 1;\n    display: flex;\n    align-items: center;\n  }\n"])));
var StyledLayoutBody = styled(Layout.Body)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  flex-grow: 0;\n  padding-bottom: 0 !important;\n  @media (min-width: ", ") {\n    grid-template-columns: auto;\n  }\n"], ["\n  flex-grow: 0;\n  padding-bottom: 0 !important;\n  @media (min-width: ", ") {\n    grid-template-columns: auto;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledLayoutBodyWrapper = styled(Layout.Body)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-bottom: -", ";\n"], ["\n  margin-bottom: -", ";\n"])), space(3));
var StyledAlert = styled(Alert)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var ActivityWrapper = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  width: 100%;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  width: 100%;\n"])));
var Status = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  position: relative;\n  display: grid;\n  grid-template-columns: auto auto auto;\n  grid-gap: ", ";\n  font-size: ", ";\n"], ["\n  position: relative;\n  display: grid;\n  grid-template-columns: auto auto auto;\n  grid-gap: ", ";\n  font-size: ", ";\n"])), space(0.5), function (p) { return p.theme.fontSizeLarge; });
var StatusContainer = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  height: 60px;\n  display: flex;\n  margin-bottom: ", ";\n"], ["\n  height: 60px;\n  display: flex;\n  margin-bottom: ", ";\n"])), space(1.5));
var Heading = styled(SectionHeading)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto auto;\n  justify-content: flex-start;\n  margin-top: ", ";\n  margin-bottom: ", ";\n  line-height: 1;\n  gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto auto;\n  justify-content: flex-start;\n  margin-top: ", ";\n  margin-bottom: ", ";\n  line-height: 1;\n  gap: ", ";\n"])), function (p) { return (p.noMargin ? 0 : space(2)); }, space(0.5), space(1));
var ChartControls = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n"])));
var ChartPanel = styled(Panel)(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(2));
var RuleText = styled('div')(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var Filters = styled('span')(templateObject_17 || (templateObject_17 = __makeTemplateObject(["\n  width: 100%;\n  overflow-wrap: break-word;\n  font-size: ", ";\n  gap: ", ";\n"], ["\n  width: 100%;\n  overflow-wrap: break-word;\n  font-size: ", ";\n  gap: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space(1));
var TriggerCondition = styled('div')(templateObject_18 || (templateObject_18 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var TriggerText = styled('div')(templateObject_19 || (templateObject_19 = __makeTemplateObject(["\n  margin-left: ", ";\n  white-space: nowrap;\n"], ["\n  margin-left: ", ";\n  white-space: nowrap;\n"])), space(0.5));
var CreatedBy = styled('div')(templateObject_20 || (templateObject_20 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17, templateObject_18, templateObject_19, templateObject_20;
//# sourceMappingURL=body.jsx.map