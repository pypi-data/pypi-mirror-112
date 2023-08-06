import { __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import { css } from '@emotion/react';
import styled from '@emotion/styled';
import memoize from 'lodash/memoize';
import Access from 'app/components/acl/access';
import MenuItemActionLink from 'app/components/actions/menuItemActionLink';
import ActorAvatar from 'app/components/avatar/actorAvatar';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Confirm from 'app/components/confirm';
import DateTime from 'app/components/dateTime';
import DropdownLink from 'app/components/dropdownLink';
import ErrorBoundary from 'app/components/errorBoundary';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import TimeSince from 'app/components/timeSince';
import Tooltip from 'app/components/tooltip';
import { IconArrow, IconDelete, IconEllipsis, IconSettings } from 'app/icons';
import { t, tct } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import getDynamicText from 'app/utils/getDynamicText';
import { AlertRuleThresholdType } from 'app/views/alerts/incidentRules/types';
import AlertBadge from '../alertBadge';
import { IncidentStatus } from '../types';
import { isIssueAlert } from '../utils';
var RuleListRow = /** @class */ (function (_super) {
    __extends(RuleListRow, _super);
    function RuleListRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Memoized function to find a project from a list of projects
         */
        _this.getProject = memoize(function (slug, projects) {
            return projects.find(function (project) { return project.slug === slug; });
        });
        return _this;
    }
    RuleListRow.prototype.activeIncident = function () {
        var _a;
        var rule = this.props.rule;
        return (((_a = rule.latestIncident) === null || _a === void 0 ? void 0 : _a.status) !== undefined &&
            [IncidentStatus.CRITICAL, IncidentStatus.WARNING].includes(rule.latestIncident.status));
    };
    RuleListRow.prototype.renderLastIncidentDate = function () {
        var rule = this.props.rule;
        if (isIssueAlert(rule)) {
            return null;
        }
        if (!rule.latestIncident) {
            return '-';
        }
        if (this.activeIncident()) {
            return (<div>
          {t('Triggered ')}
          <TimeSince date={rule.latestIncident.dateCreated}/>
        </div>);
        }
        return (<div>
        {t('Resolved ')}
        <TimeSince date={rule.latestIncident.dateClosed}/>
      </div>);
    };
    RuleListRow.prototype.renderAlertRuleStatus = function () {
        var _a, _b;
        var rule = this.props.rule;
        if (isIssueAlert(rule)) {
            return null;
        }
        var activeIncident = this.activeIncident();
        var criticalTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'warning';
        });
        var trigger = activeIncident && ((_a = rule.latestIncident) === null || _a === void 0 ? void 0 : _a.status) === IncidentStatus.CRITICAL
            ? criticalTrigger
            : warningTrigger !== null && warningTrigger !== void 0 ? warningTrigger : criticalTrigger;
        var iconColor = 'green300';
        if (activeIncident) {
            iconColor =
                (trigger === null || trigger === void 0 ? void 0 : trigger.label) === 'critical'
                    ? 'red300'
                    : (trigger === null || trigger === void 0 ? void 0 : trigger.label) === 'warning'
                        ? 'yellow300'
                        : 'green300';
        }
        var thresholdTypeText = activeIncident && rule.thresholdType === AlertRuleThresholdType.ABOVE
            ? t('Above')
            : t('Below');
        return (<FlexCenter>
        <IconArrow color={iconColor} direction={activeIncident && rule.thresholdType === AlertRuleThresholdType.ABOVE
                ? 'up'
                : 'down'}/>
        <TriggerText>{thresholdTypeText + " " + ((_b = trigger === null || trigger === void 0 ? void 0 : trigger.alertThreshold) === null || _b === void 0 ? void 0 : _b.toLocaleString())}</TriggerText>
      </FlexCenter>);
    };
    RuleListRow.prototype.render = function () {
        var _a;
        var _b, _c, _d, _e, _f, _g;
        var _h = this.props, rule = _h.rule, projectsLoaded = _h.projectsLoaded, projects = _h.projects, organization = _h.organization, orgId = _h.orgId, onDelete = _h.onDelete, userTeams = _h.userTeams;
        var slug = rule.projects[0];
        var editLink = "/organizations/" + orgId + "/alerts/" + (isIssueAlert(rule) ? 'rules' : 'metric-rules') + "/" + slug + "/" + rule.id + "/";
        var hasRedesign = !isIssueAlert(rule) && organization.features.includes('alert-details-redesign');
        var detailsLink = "/organizations/" + orgId + "/alerts/rules/details/" + rule.id + "/";
        var ownerId = (_b = rule.owner) === null || _b === void 0 ? void 0 : _b.split(':')[1];
        var teamActor = ownerId
            ? { type: 'team', id: ownerId, name: '' }
            : null;
        var canEdit = ownerId ? userTeams.has(ownerId) : true;
        var hasAlertList = organization.features.includes('alert-details-redesign');
        var alertLink = isIssueAlert(rule) ? (rule.name) : (<TitleLink to={hasRedesign ? detailsLink : editLink}>{rule.name}</TitleLink>);
        var IssueStatusText = (_a = {},
            _a[IncidentStatus.CRITICAL] = t('Critical'),
            _a[IncidentStatus.WARNING] = t('Warning'),
            _a[IncidentStatus.CLOSED] = t('Resolved'),
            _a[IncidentStatus.OPENED] = t('Resolved'),
            _a);
        return (<ErrorBoundary>
        {!hasAlertList ? (<React.Fragment>
            <RuleType>{isIssueAlert(rule) ? t('Issue') : t('Metric')}</RuleType>
            <Title>{alertLink}</Title>
          </React.Fragment>) : (<React.Fragment>
            <AlertNameWrapper isIncident={isIssueAlert(rule)}>
              <FlexCenter>
                <Tooltip title={isIssueAlert(rule)
                    ? t('Issue Alert')
                    : tct('Metric Alert Status: [status]', {
                        status: IssueStatusText[(_d = (_c = rule === null || rule === void 0 ? void 0 : rule.latestIncident) === null || _c === void 0 ? void 0 : _c.status) !== null && _d !== void 0 ? _d : IncidentStatus.CLOSED],
                    })}>
                  <AlertBadge status={(_e = rule === null || rule === void 0 ? void 0 : rule.latestIncident) === null || _e === void 0 ? void 0 : _e.status} isIssue={isIssueAlert(rule)} hideText/>
                </Tooltip>
              </FlexCenter>
              <AlertNameAndStatus>
                <AlertName>{alertLink}</AlertName>
                {!isIssueAlert(rule) && this.renderLastIncidentDate()}
              </AlertNameAndStatus>
            </AlertNameWrapper>
            <FlexCenter>{this.renderAlertRuleStatus()}</FlexCenter>
          </React.Fragment>)}

        <FlexCenter>
          <ProjectBadgeContainer>
            <ProjectBadge avatarSize={18} project={!projectsLoaded ? { slug: slug } : this.getProject(slug, projects)}/>
          </ProjectBadgeContainer>
        </FlexCenter>

        <FlexCenter>
          {teamActor ? <ActorAvatar actor={teamActor} size={24}/> : '-'}
        </FlexCenter>

        {!hasAlertList && <CreatedBy>{(_g = (_f = rule === null || rule === void 0 ? void 0 : rule.createdBy) === null || _f === void 0 ? void 0 : _f.name) !== null && _g !== void 0 ? _g : '-'}</CreatedBy>}
        <FlexCenter>
          <DateTime date={getDynamicText({
                value: rule.dateCreated,
                fixed: new Date('2021-04-20'),
            })} format="ll"/>
        </FlexCenter>
        <ActionsRow>
          <Access access={['alerts:write']}>
            {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<React.Fragment>
                <StyledDropdownLink>
                  <DropdownLink anchorRight caret={false} title={<Button tooltipProps={{
                            containerDisplayMode: 'flex',
                        }} size="small" type="button" aria-label={t('Show more')} icon={<IconEllipsis size="xs"/>}/>}>
                    <li>
                      <Link to={editLink}>{t('Edit')}</Link>
                    </li>
                    <Confirm disabled={!hasAccess || !canEdit} message={tct("Are you sure you want to delete [name]? You won't be able to view the history of this alert once it's deleted.", {
                        name: rule.name,
                    })} header={t('Delete Alert Rule?')} priority="danger" confirmText={t('Delete Rule')} onConfirm={function () { return onDelete(slug, rule); }}>
                      <MenuItemActionLink title={t('Delete')}>
                        {t('Delete')}
                      </MenuItemActionLink>
                    </Confirm>
                  </DropdownLink>
                </StyledDropdownLink>

                {/* Small screen actions */}
                <StyledButtonBar gap={1}>
                  <Confirm disabled={!hasAccess || !canEdit} message={tct("Are you sure you want to delete [name]? You won't be able to view the history of this alert once it's deleted.", {
                        name: rule.name,
                    })} header={t('Delete Alert Rule?')} priority="danger" confirmText={t('Delete Rule')} onConfirm={function () { return onDelete(slug, rule); }}>
                    <Button type="button" icon={<IconDelete />} size="small" title={t('Delete')}/>
                  </Confirm>
                  <Tooltip title={t('Edit')}>
                    <Button size="small" type="button" icon={<IconSettings />} to={editLink}/>
                  </Tooltip>
                </StyledButtonBar>
              </React.Fragment>);
            }}
          </Access>
        </ActionsRow>
      </ErrorBoundary>);
    };
    return RuleListRow;
}(React.Component));
var columnCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  height: 100%;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  height: 100%;\n"])));
var RuleType = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 400;\n  color: ", ";\n  text-transform: uppercase;\n  ", "\n"], ["\n  font-size: ", ";\n  font-weight: 400;\n  color: ", ";\n  text-transform: uppercase;\n  ", "\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, columnCss);
var Title = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), columnCss);
var TitleLink = styled(Link)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
var CreatedBy = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", "\n  ", "\n"], ["\n  ", "\n  ", "\n"])), overflowEllipsis, columnCss);
var FlexCenter = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var AlertNameWrapper = styled(FlexCenter)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) { return p.isIncident && "padding: " + space(3) + " " + space(2) + "; line-height: 2.4;"; });
var AlertNameAndStatus = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  ", "\n  margin-left: ", ";\n  line-height: 1.35;\n"], ["\n  ", "\n  margin-left: ", ";\n  line-height: 1.35;\n"])), overflowEllipsis, space(1.5));
var AlertName = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  ", "\n  font-size: ", ";\n\n  @media (max-width: ", ") {\n    max-width: 300px;\n  }\n  @media (max-width: ", ") {\n    max-width: 165px;\n  }\n  @media (max-width: ", ") {\n    max-width: 100px;\n  }\n"], ["\n  ", "\n  font-size: ", ";\n\n  @media (max-width: ", ") {\n    max-width: 300px;\n  }\n  @media (max-width: ", ") {\n    max-width: 165px;\n  }\n  @media (max-width: ", ") {\n    max-width: 100px;\n  }\n"])), overflowEllipsis, function (p) { return p.theme.fontSizeLarge; }, function (p) { return p.theme.breakpoints[3]; }, function (p) { return p.theme.breakpoints[2]; }, function (p) { return p.theme.breakpoints[1]; });
var ProjectBadgeContainer = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
var ProjectBadge = styled(IdBadge)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var TriggerText = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  margin-left: ", ";\n  white-space: nowrap;\n"], ["\n  margin-left: ", ";\n  white-space: nowrap;\n"])), space(1));
var StyledButtonBar = styled(ButtonBar)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  display: none;\n  justify-content: flex-start;\n  align-items: center;\n\n  @media (max-width: ", ") {\n    display: flex;\n  }\n"], ["\n  display: none;\n  justify-content: flex-start;\n  align-items: center;\n\n  @media (max-width: ", ") {\n    display: flex;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledDropdownLink = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var ActionsRow = styled(FlexCenter)(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  justify-content: center;\n  padding: ", ";\n"], ["\n  justify-content: center;\n  padding: ", ";\n"])), space(1));
export default RuleListRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15;
//# sourceMappingURL=row.jsx.map