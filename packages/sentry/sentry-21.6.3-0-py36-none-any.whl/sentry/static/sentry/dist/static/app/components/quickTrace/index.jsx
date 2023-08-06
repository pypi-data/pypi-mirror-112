import { __extends, __read, __spreadArray } from "tslib";
import * as React from 'react';
import DropdownLink from 'app/components/dropdownLink';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import { generateSingleErrorTarget, generateSingleTransactionTarget, generateTraceTarget, isQuickTraceEvent, } from 'app/components/quickTrace/utils';
import Tooltip from 'app/components/tooltip';
import { backend, frontend, mobile, serverless } from 'app/data/platformCategories';
import { IconFire } from 'app/icons';
import { t, tct, tn } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getDocsPlatform } from 'app/utils/docs';
import { getDuration } from 'app/utils/formatters';
import localStorage from 'app/utils/localStorage';
import { parseQuickTrace } from 'app/utils/performance/quickTrace/utils';
import Projects from 'app/utils/projects';
var FRONTEND_PLATFORMS = __spreadArray(__spreadArray([], __read(frontend)), __read(mobile));
var BACKEND_PLATFORMS = __spreadArray(__spreadArray([], __read(backend)), __read(serverless));
import { DropdownContainer, DropdownItem, DropdownItemSubContainer, DropdownMenuHeader, ErrorNodeContent, EventNode, ExternalDropdownLink, QuickTraceContainer, SectionSubtext, SingleEventHoverText, StyledTruncate, TraceConnector, } from './styles';
var TOOLTIP_PREFIX = {
    root: 'root',
    ancestors: 'ancestor',
    parent: 'parent',
    current: '',
    children: 'child',
    descendants: 'descendant',
};
export default function QuickTrace(_a) {
    var event = _a.event, quickTrace = _a.quickTrace, location = _a.location, organization = _a.organization, anchor = _a.anchor, errorDest = _a.errorDest, transactionDest = _a.transactionDest;
    var parsedQuickTrace;
    try {
        parsedQuickTrace = parseQuickTrace(quickTrace, event, organization);
    }
    catch (error) {
        return <React.Fragment>{'\u2014'}</React.Fragment>;
    }
    var traceLength = quickTrace.trace && quickTrace.trace.length;
    var root = parsedQuickTrace.root, ancestors = parsedQuickTrace.ancestors, parent = parsedQuickTrace.parent, children = parsedQuickTrace.children, descendants = parsedQuickTrace.descendants, current = parsedQuickTrace.current;
    var nodes = [];
    if (root) {
        nodes.push(<EventNodeSelector key="root-node" location={location} organization={organization} events={[root]} currentEvent={event} text={t('Root')} anchor={anchor} nodeKey="root" errorDest={errorDest} transactionDest={transactionDest}/>);
        nodes.push(<TraceConnector key="root-connector"/>);
    }
    if (ancestors === null || ancestors === void 0 ? void 0 : ancestors.length) {
        nodes.push(<EventNodeSelector key="ancestors-node" location={location} organization={organization} events={ancestors} currentEvent={event} text={tn('%s Ancestor', '%s Ancestors', ancestors.length)} anchor={anchor} nodeKey="ancestors" errorDest={errorDest} transactionDest={transactionDest}/>);
        nodes.push(<TraceConnector key="ancestors-connector"/>);
    }
    if (parent) {
        nodes.push(<EventNodeSelector key="parent-node" location={location} organization={organization} events={[parent]} currentEvent={event} text={t('Parent')} anchor={anchor} nodeKey="parent" errorDest={errorDest} transactionDest={transactionDest}/>);
        nodes.push(<TraceConnector key="parent-connector"/>);
    }
    var currentNode = (<EventNodeSelector key="current-node" location={location} organization={organization} text={t('This Event')} events={[current]} currentEvent={event} anchor={anchor} nodeKey="current" errorDest={errorDest} transactionDest={transactionDest}/>);
    if (traceLength === 1) {
        nodes.push(<Projects key="missing-services" orgId={organization.slug} slugs={[current.project_slug]}>
        {function (_a) {
                var projects = _a.projects;
                var project = projects.find(function (p) { return p.slug === current.project_slug; });
                if (project === null || project === void 0 ? void 0 : project.platform) {
                    if (BACKEND_PLATFORMS.includes(project.platform)) {
                        return (<React.Fragment>
                  <MissingServiceNode anchor={anchor} organization={organization} platform={project.platform} connectorSide="right"/>
                  {currentNode}
                </React.Fragment>);
                    }
                    else if (FRONTEND_PLATFORMS.includes(project.platform)) {
                        return (<React.Fragment>
                  {currentNode}
                  <MissingServiceNode anchor={anchor} organization={organization} platform={project.platform} connectorSide="left"/>
                </React.Fragment>);
                    }
                }
                return currentNode;
            }}
      </Projects>);
    }
    else {
        nodes.push(currentNode);
    }
    if (children.length) {
        nodes.push(<TraceConnector key="children-connector"/>);
        nodes.push(<EventNodeSelector key="children-node" location={location} organization={organization} events={children} currentEvent={event} text={tn('%s Child', '%s Children', children.length)} anchor={anchor} nodeKey="children" errorDest={errorDest} transactionDest={transactionDest}/>);
    }
    if (descendants === null || descendants === void 0 ? void 0 : descendants.length) {
        nodes.push(<TraceConnector key="descendants-connector"/>);
        nodes.push(<EventNodeSelector key="descendants-node" location={location} organization={organization} events={descendants} currentEvent={event} text={tn('%s Descendant', '%s Descendants', descendants.length)} anchor={anchor} nodeKey="descendants" errorDest={errorDest} transactionDest={transactionDest}/>);
    }
    return <QuickTraceContainer>{nodes}</QuickTraceContainer>;
}
function handleNode(key, organization) {
    trackAnalyticsEvent({
        eventKey: 'quick_trace.node.clicked',
        eventName: 'Quick Trace: Node clicked',
        organization_id: parseInt(organization.id, 10),
        node_key: key,
    });
}
function handleDropdownItem(key, organization, extra) {
    trackAnalyticsEvent({
        eventKey: 'quick_trace.dropdown.clicked' + (extra ? '_extra' : ''),
        eventName: 'Quick Trace: Dropdown clicked',
        organization_id: parseInt(organization.id, 10),
        node_key: key,
    });
}
function EventNodeSelector(_a) {
    var location = _a.location, organization = _a.organization, _b = _a.events, events = _b === void 0 ? [] : _b, text = _a.text, currentEvent = _a.currentEvent, nodeKey = _a.nodeKey, anchor = _a.anchor, errorDest = _a.errorDest, transactionDest = _a.transactionDest, _c = _a.numEvents, numEvents = _c === void 0 ? 5 : _c;
    var errors = events.flatMap(function (event) { var _a; return (_a = event.errors) !== null && _a !== void 0 ? _a : []; });
    var type = nodeKey === 'current' ? 'black' : 'white';
    if (errors.length > 0) {
        type = nodeKey === 'current' ? 'error' : 'warning';
        text = (<ErrorNodeContent>
        <IconFire size="xs"/>
        {text}
      </ErrorNodeContent>);
    }
    // make sure to exclude the current event from the dropdown
    events = events.filter(function (event) { return event.event_id !== currentEvent.id; });
    errors = errors.filter(function (error) { return error.event_id !== currentEvent.id; });
    if (events.length + errors.length === 0) {
        return <EventNode type={type}>{text}</EventNode>;
    }
    else if (events.length + errors.length === 1) {
        /**
         * When there is only 1 event, clicking the node should take the user directly to
         * the event without additional steps.
         */
        var hoverText = errors.length ? (t('View the error for this Transaction')) : (<SingleEventHoverText event={events[0]}/>);
        var target = errors.length
            ? generateSingleErrorTarget(errors[0], organization, location, errorDest)
            : generateSingleTransactionTarget(events[0], organization, location, transactionDest);
        return (<StyledEventNode text={text} hoverText={hoverText} to={target} onClick={function () { return handleNode(nodeKey, organization); }} type={type}/>);
    }
    else {
        /**
         * When there is more than 1 event, clicking the node should expand a dropdown to
         * allow the user to select which event to go to.
         */
        var hoverText = tct('View [eventPrefix] [eventType]', {
            eventPrefix: TOOLTIP_PREFIX[nodeKey],
            eventType: errors.length && events.length
                ? 'events'
                : events.length
                    ? 'transactions'
                    : 'errors',
        });
        return (<DropdownContainer>
        <DropdownLink caret={false} title={<StyledEventNode text={text} hoverText={hoverText} type={type}/>} anchorRight={anchor === 'right'}>
          {errors.length > 0 && (<DropdownMenuHeader first>
              {tn('Related Error', 'Related Errors', errors.length)}
            </DropdownMenuHeader>)}
          {errors.slice(0, numEvents).map(function (error) {
                var target = generateSingleErrorTarget(error, organization, location, errorDest);
                return (<DropdownNodeItem key={error.event_id} event={error} to={target} allowDefaultEvent onSelect={function () { return handleDropdownItem(nodeKey, organization, false); }} organization={organization} anchor={anchor}/>);
            })}
          {events.length > 0 && (<DropdownMenuHeader first={errors.length === 0}>
              {tn('Transaction', 'Transactions', events.length)}
            </DropdownMenuHeader>)}
          {events.slice(0, numEvents).map(function (event) {
                var target = generateSingleTransactionTarget(event, organization, location, transactionDest);
                return (<DropdownNodeItem key={event.event_id} event={event} to={target} onSelect={function () { return handleDropdownItem(nodeKey, organization, false); }} allowDefaultEvent organization={organization} subtext={getDuration(event['transaction.duration'] / 1000, event['transaction.duration'] < 1000 ? 0 : 2, true)} anchor={anchor}/>);
            })}
          {(errors.length > numEvents || events.length > numEvents) && (<DropdownItem to={generateTraceTarget(currentEvent, organization)} allowDefaultEvent onSelect={function () { return handleDropdownItem(nodeKey, organization, true); }}>
              {t('View all events')}
            </DropdownItem>)}
        </DropdownLink>
      </DropdownContainer>);
    }
}
function DropdownNodeItem(_a) {
    var event = _a.event, onSelect = _a.onSelect, to = _a.to, allowDefaultEvent = _a.allowDefaultEvent, organization = _a.organization, subtext = _a.subtext, anchor = _a.anchor;
    return (<DropdownItem to={to} onSelect={onSelect} allowDefaultEvent={allowDefaultEvent}>
      <DropdownItemSubContainer>
        <Projects orgId={organization.slug} slugs={[event.project_slug]}>
          {function (_a) {
            var projects = _a.projects;
            var project = projects.find(function (p) { return p.slug === event.project_slug; });
            return (<ProjectBadge disableLink hideName project={project ? project : { slug: event.project_slug }} avatarSize={16}/>);
        }}
        </Projects>
        {isQuickTraceEvent(event) ? (<StyledTruncate value={event.transaction} 
        // expand in the opposite direction of the anchor
        expandDirection={anchor === 'left' ? 'right' : 'left'} maxLength={35} leftTrim trimRegex={/\.|\//g}/>) : (<StyledTruncate value={event.title} 
        // expand in the opposite direction of the anchor
        expandDirection={anchor === 'left' ? 'right' : 'left'} maxLength={45}/>)}
      </DropdownItemSubContainer>
      {subtext && <SectionSubtext>{subtext}</SectionSubtext>}
    </DropdownItem>);
}
function StyledEventNode(_a) {
    var text = _a.text, hoverText = _a.hoverText, to = _a.to, onClick = _a.onClick, _b = _a.type, type = _b === void 0 ? 'white' : _b;
    return (<Tooltip position="top" containerDisplayMode="inline-flex" title={hoverText}>
      <EventNode type={type} icon={null} to={to} onClick={onClick}>
        {text}
      </EventNode>
    </Tooltip>);
}
var HIDE_MISSING_SERVICE_KEY = 'quick-trace:hide-missing-services';
// 30 days
var HIDE_MISSING_EXPIRES = 1000 * 60 * 60 * 24 * 30;
function readHideMissingServiceState() {
    var value = localStorage.getItem(HIDE_MISSING_SERVICE_KEY);
    if (value === null) {
        return false;
    }
    var expires = parseInt(value, 10);
    var now = new Date().getTime();
    return expires > now;
}
var MissingServiceNode = /** @class */ (function (_super) {
    __extends(MissingServiceNode, _super);
    function MissingServiceNode() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            hideMissing: readHideMissingServiceState(),
        };
        _this.dismissMissingService = function () {
            var _a = _this.props, organization = _a.organization, platform = _a.platform;
            var now = new Date().getTime();
            localStorage.setItem(HIDE_MISSING_SERVICE_KEY, (now + HIDE_MISSING_EXPIRES).toString());
            _this.setState({ hideMissing: true });
            trackAnalyticsEvent({
                eventKey: 'quick_trace.missing_service.dismiss',
                eventName: 'Quick Trace: Missing Service Dismissed',
                organization_id: parseInt(organization.id, 10),
                platform: platform,
            });
        };
        _this.trackExternalLink = function () {
            var _a = _this.props, organization = _a.organization, platform = _a.platform;
            trackAnalyticsEvent({
                eventKey: 'quick_trace.missing_service.docs',
                eventName: 'Quick Trace: Missing Service Clicked',
                organization_id: parseInt(organization.id, 10),
                platform: platform,
            });
        };
        return _this;
    }
    MissingServiceNode.prototype.render = function () {
        var hideMissing = this.state.hideMissing;
        var _a = this.props, anchor = _a.anchor, connectorSide = _a.connectorSide, platform = _a.platform;
        if (hideMissing) {
            return null;
        }
        var docPlatform = getDocsPlatform(platform, true);
        var docsHref = docPlatform === null || docPlatform === 'javascript'
            ? 'https://docs.sentry.io/platforms/javascript/performance/connect-services/'
            : "https://docs.sentry.io/platforms/" + docPlatform + "/performance#connecting-services";
        return (<React.Fragment>
        {connectorSide === 'left' && <TraceConnector />}
        <DropdownContainer>
          <DropdownLink caret={false} title={<StyledEventNode type="white" hoverText={t('No services connected')} text="???"/>} anchorRight={anchor === 'right'}>
            <DropdownItem width="small">
              <ExternalDropdownLink href={docsHref} onClick={this.trackExternalLink}>
                {t('Connect to a service')}
              </ExternalDropdownLink>
            </DropdownItem>
            <DropdownItem onSelect={this.dismissMissingService} width="small">
              {t('Dismiss')}
            </DropdownItem>
          </DropdownLink>
        </DropdownContainer>
        {connectorSide === 'right' && <TraceConnector />}
      </React.Fragment>);
    };
    return MissingServiceNode;
}(React.Component));
//# sourceMappingURL=index.jsx.map