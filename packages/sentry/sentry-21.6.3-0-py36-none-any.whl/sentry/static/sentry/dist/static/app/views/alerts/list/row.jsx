import { __extends, __makeTemplateObject } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import memoize from 'lodash/memoize';
import moment from 'moment';
import ActorAvatar from 'app/components/avatar/actorAvatar';
import Duration from 'app/components/duration';
import ErrorBoundary from 'app/components/errorBoundary';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import Tag from 'app/components/tag';
import TimeSince from 'app/components/timeSince';
import { t } from 'app/locale';
import TeamStore from 'app/stores/teamStore';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { getUtcDateString } from 'app/utils/dates';
import getDynamicText from 'app/utils/getDynamicText';
import { alertDetailsLink } from 'app/views/alerts/details';
import { API_INTERVAL_POINTS_LIMIT, API_INTERVAL_POINTS_MIN, } from '../rules/details/constants';
import { IncidentStatus } from '../types';
import { getIncidentMetricPreset, isIssueAlert } from '../utils';
/**
 * Retrieve the start/end for showing the graph of the metric
 * Will show at least 150 and no more than 10,000 data points
 */
export var makeRuleDetailsQuery = function (incident) {
    var timeWindow = incident.alertRule.timeWindow;
    var timeWindowMillis = timeWindow * 60 * 1000;
    var minRange = timeWindowMillis * API_INTERVAL_POINTS_MIN;
    var maxRange = timeWindowMillis * API_INTERVAL_POINTS_LIMIT;
    var now = moment.utc();
    var startDate = moment.utc(incident.dateStarted);
    // make a copy of now since we will modify endDate and use now for comparing
    var endDate = incident.dateClosed ? moment.utc(incident.dateClosed) : moment(now);
    var incidentRange = Math.max(endDate.diff(startDate), 3 * timeWindowMillis);
    var range = Math.min(maxRange, Math.max(minRange, incidentRange));
    var halfRange = moment.duration(range / 2);
    return {
        start: getUtcDateString(startDate.subtract(halfRange)),
        end: getUtcDateString(moment.min(endDate.add(halfRange), now)),
    };
};
var AlertListRow = /** @class */ (function (_super) {
    __extends(AlertListRow, _super);
    function AlertListRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Memoized function to find a project from a list of projects
         */
        _this.getProject = memoize(function (slug, projects) {
            return projects.find(function (project) { return project.slug === slug; });
        });
        return _this;
    }
    Object.defineProperty(AlertListRow.prototype, "metricPreset", {
        get: function () {
            var incident = this.props.incident;
            return incident ? getIncidentMetricPreset(incident) : undefined;
        },
        enumerable: false,
        configurable: true
    });
    AlertListRow.prototype.render = function () {
        var _a, _b, _c;
        var _d = this.props, incident = _d.incident, orgId = _d.orgId, projectsLoaded = _d.projectsLoaded, projects = _d.projects, organization = _d.organization;
        var slug = incident.projects[0];
        var started = moment(incident.dateStarted);
        var duration = moment
            .duration(moment(incident.dateClosed || new Date()).diff(started))
            .as('seconds');
        var hasRedesign = !isIssueAlert(incident.alertRule) &&
            organization.features.includes('alert-details-redesign');
        var alertLink = hasRedesign
            ? {
                pathname: alertDetailsLink(organization, incident),
                query: { alert: incident.identifier },
            }
            : {
                pathname: "/organizations/" + orgId + "/alerts/" + incident.identifier + "/",
            };
        var ownerId = (_a = incident.alertRule.owner) === null || _a === void 0 ? void 0 : _a.split(':')[1];
        var teamName = '';
        if (ownerId) {
            teamName = (_c = (_b = TeamStore.getById(ownerId)) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '';
        }
        var teamActor = ownerId
            ? { type: 'team', id: ownerId, name: teamName }
            : null;
        return (<ErrorBoundary>
        <Title>
          <Link to={alertLink}>{incident.title}</Link>
        </Title>

        <NoWrap>
          {getDynamicText({
                value: <TimeSince date={incident.dateStarted} extraShort/>,
                fixed: '1w ago',
            })}
        </NoWrap>
        <NoWrap>
          {incident.status === IncidentStatus.CLOSED ? (<Duration seconds={getDynamicText({ value: duration, fixed: 1200 })}/>) : (<Tag type="warning">{t('Still Active')}</Tag>)}
        </NoWrap>

        <ProjectBadge avatarSize={18} project={!projectsLoaded ? { slug: slug } : this.getProject(slug, projects)}/>
        <div>#{incident.id}</div>

        <FlexCenter>
          {teamActor ? (<Fragment>
              <StyledActorAvatar actor={teamActor} size={24} hasTooltip={false}/>{' '}
              <TeamWrapper>{teamActor.name}</TeamWrapper>
            </Fragment>) : ('-')}
        </FlexCenter>
      </ErrorBoundary>);
    };
    return AlertListRow;
}(Component));
var Title = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", "\n  min-width: 130px;\n"], ["\n  ", "\n  min-width: 130px;\n"])), overflowEllipsis);
var NoWrap = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
var ProjectBadge = styled(IdBadge)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var FlexCenter = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", "\n  display: flex;\n  align-items: center;\n"], ["\n  ", "\n  display: flex;\n  align-items: center;\n"])), overflowEllipsis);
var TeamWrapper = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
var StyledActorAvatar = styled(ActorAvatar)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
export default AlertListRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=row.jsx.map