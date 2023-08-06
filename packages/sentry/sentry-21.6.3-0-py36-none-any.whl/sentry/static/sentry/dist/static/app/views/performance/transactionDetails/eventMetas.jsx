import { __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import Clipboard from 'app/components/clipboard';
import DateTime from 'app/components/dateTime';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import TimeSince from 'app/components/timeSince';
import Tooltip from 'app/components/tooltip';
import { IconCopy } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { getShortEventId } from 'app/utils/events';
import { getDuration } from 'app/utils/formatters';
import getDynamicText from 'app/utils/getDynamicText';
import { isTransaction } from 'app/utils/performance/quickTrace/utils';
import Projects from 'app/utils/projects';
import theme from 'app/utils/theme';
import QuickTraceMeta from './quickTraceMeta';
import { MetaData } from './styles';
/**
 * This should match the breakpoint chosen for the `EventDetailHeader` below
 */
var BREAKPOINT_MEDIA_QUERY = "(min-width: " + theme.breakpoints[2] + ")";
var EventMetas = /** @class */ (function (_super) {
    __extends(EventMetas, _super);
    function EventMetas() {
        var _a, _b, _c;
        var _this = _super.apply(this, __spreadArray([], __read(arguments))) || this;
        _this.state = {
            isLargeScreen: (_b = (_a = window.matchMedia) === null || _a === void 0 ? void 0 : _a.call(window, BREAKPOINT_MEDIA_QUERY)) === null || _b === void 0 ? void 0 : _b.matches,
        };
        _this.mq = (_c = window.matchMedia) === null || _c === void 0 ? void 0 : _c.call(window, BREAKPOINT_MEDIA_QUERY);
        _this.handleMediaQueryChange = function (changed) {
            _this.setState({
                isLargeScreen: changed.matches,
            });
        };
        return _this;
    }
    EventMetas.prototype.componentDidMount = function () {
        if (this.mq) {
            this.mq.addListener(this.handleMediaQueryChange);
        }
    };
    EventMetas.prototype.componentWillUnmount = function () {
        if (this.mq) {
            this.mq.removeListener(this.handleMediaQueryChange);
        }
    };
    EventMetas.prototype.render = function () {
        var _a = this.props, event = _a.event, organization = _a.organization, projectId = _a.projectId, location = _a.location, quickTrace = _a.quickTrace, meta = _a.meta, errorDest = _a.errorDest, transactionDest = _a.transactionDest;
        var isLargeScreen = this.state.isLargeScreen;
        var type = isTransaction(event) ? 'transaction' : 'event';
        var timestamp = (<TimeSince date={event.dateCreated || (event.endTimestamp || 0) * 1000}/>);
        var httpStatus = <HttpStatus event={event}/>;
        return (<Projects orgId={organization.slug} slugs={[projectId]}>
        {function (_a) {
                var _b, _c, _d;
                var projects = _a.projects;
                var project = projects.find(function (p) { return p.slug === projectId; });
                return (<EventDetailHeader type={type}>
              <MetaData headingText={t('Event ID')} tooltipText={t('The unique ID assigned to this %s.', type)} bodyText={<EventID event={event}/>} subtext={<ProjectBadge project={project ? project : { slug: projectId }} avatarSize={16}/>}/>
              {isTransaction(event) ? (<MetaData headingText={t('Event Duration')} tooltipText={t('The time elapsed between the start and end of this transaction.')} bodyText={getDuration(event.endTimestamp - event.startTimestamp, 2, true)} subtext={timestamp}/>) : (<MetaData headingText={t('Created')} tooltipText={t('The time at which this event was created.')} bodyText={timestamp} subtext={getDynamicText({
                            value: <DateTime date={event.dateCreated}/>,
                            fixed: 'May 6, 2021 3:27:01 UTC',
                        })}/>)}
              {isTransaction(event) && (<MetaData headingText={t('Status')} tooltipText={t('The status of this transaction indicating if it succeeded or otherwise.')} bodyText={(_d = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.status) !== null && _d !== void 0 ? _d : '\u2014'} subtext={httpStatus}/>)}
              <QuickTraceContainer>
                <QuickTraceMeta event={event} project={project} organization={organization} location={location} quickTrace={quickTrace} traceMeta={meta} anchor={isLargeScreen ? 'right' : 'left'} errorDest={errorDest} transactionDest={transactionDest}/>
              </QuickTraceContainer>
            </EventDetailHeader>);
            }}
      </Projects>);
    };
    return EventMetas;
}(React.Component));
var EventDetailHeader = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(", ", 1fr);\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n\n  /* This should match the breakpoint chosen for BREAKPOINT_MEDIA_QUERY above. */\n  @media (min-width: ", ") {\n    ", ";\n    grid-row-gap: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(", ", 1fr);\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n\n  /* This should match the breakpoint chosen for BREAKPOINT_MEDIA_QUERY above. */\n  @media (min-width: ", ") {\n    ", ";\n    grid-row-gap: 0;\n  }\n"])), function (p) { return (p.type === 'transaction' ? 3 : 2); }, space(2), space(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[2]; }, function (p) {
    return p.type === 'transaction'
        ? 'grid-template-columns: minmax(160px, 1fr) minmax(160px, 1fr) minmax(160px, 1fr) 6fr;'
        : 'grid-template-columns: minmax(160px, 1fr) minmax(200px, 1fr) 6fr;';
});
var QuickTraceContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-column: 1/4;\n\n  @media (min-width: ", ") {\n    justify-self: flex-end;\n    min-width: 325px;\n    grid-column: unset;\n  }\n"], ["\n  grid-column: 1/4;\n\n  @media (min-width: ", ") {\n    justify-self: flex-end;\n    min-width: 325px;\n    grid-column: unset;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
function EventID(_a) {
    var event = _a.event;
    return (<Clipboard value={event.eventID}>
      <EventIDContainer>
        <EventIDWrapper>{getShortEventId(event.eventID)}</EventIDWrapper>
        <Tooltip title={event.eventID} position="top">
          <IconCopy color="subText"/>
        </Tooltip>
      </EventIDContainer>
    </Clipboard>);
}
var EventIDContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  cursor: pointer;\n"], ["\n  display: flex;\n  align-items: center;\n  cursor: pointer;\n"])));
var EventIDWrapper = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
function HttpStatus(_a) {
    var event = _a.event;
    var tags = event.tags;
    var emptyStatus = <React.Fragment>{'\u2014'}</React.Fragment>;
    if (!Array.isArray(tags)) {
        return emptyStatus;
    }
    var tag = tags.find(function (tagObject) { return tagObject.key === 'http.status_code'; });
    if (!tag) {
        return emptyStatus;
    }
    return <React.Fragment>HTTP {tag.value}</React.Fragment>;
}
export default EventMetas;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=eventMetas.jsx.map