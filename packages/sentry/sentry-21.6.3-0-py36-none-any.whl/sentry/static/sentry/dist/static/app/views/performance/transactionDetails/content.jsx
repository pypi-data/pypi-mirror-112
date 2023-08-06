import { __assign, __extends } from "tslib";
import { Fragment } from 'react';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import NotFound from 'app/components/errors/notFound';
import { BorderlessEventEntries } from 'app/components/events/eventEntries';
import EventMetadata from 'app/components/events/eventMetadata';
import EventVitals from 'app/components/events/eventVitals';
import * as SpanEntryContext from 'app/components/events/interfaces/spans/context';
import RootSpanStatus from 'app/components/events/rootSpanStatus';
import FileSize from 'app/components/fileSize';
import * as Layout from 'app/components/layouts/thirds';
import LoadingError from 'app/components/loadingError';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import TagsTable from 'app/components/tagsTable';
import { IconOpen } from 'app/icons';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import * as QuickTraceContext from 'app/utils/performance/quickTrace/quickTraceContext';
import QuickTraceQuery from 'app/utils/performance/quickTrace/quickTraceQuery';
import TraceMetaQuery from 'app/utils/performance/quickTrace/traceMetaQuery';
import { getTraceTimeRangeFromEvent } from 'app/utils/performance/quickTrace/utils';
import Projects from 'app/utils/projects';
import { appendTagCondition, decodeScalar } from 'app/utils/queryString';
import Breadcrumb from 'app/views/performance/breadcrumb';
import { transactionSummaryRouteWithQuery } from '../transactionSummary/utils';
import { getTransactionDetailsUrl } from '../utils';
import EventMetas from './eventMetas';
var EventDetailsContent = /** @class */ (function (_super) {
    __extends(EventDetailsContent, _super);
    function EventDetailsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: {},
            event: undefined,
            // local state
            isSidebarVisible: true,
        };
        _this.toggleSidebar = function () {
            _this.setState({ isSidebarVisible: !_this.state.isSidebarVisible });
        };
        _this.generateTagUrl = function (tag) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            var event = _this.state.event;
            if (!event) {
                return '';
            }
            var query = decodeScalar(location.query.query, '');
            var newQuery = __assign(__assign({}, location.query), { query: appendTagCondition(query, tag.key, tag.value) });
            return transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: event.title,
                projectID: decodeScalar(location.query.project),
                query: newQuery,
            });
        };
        return _this;
    }
    EventDetailsContent.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        var eventSlug = params.eventSlug;
        var url = "/organizations/" + organization.slug + "/events/" + eventSlug + "/";
        return [['event', url]];
    };
    Object.defineProperty(EventDetailsContent.prototype, "projectId", {
        get: function () {
            return this.props.eventSlug.split(':')[0];
        },
        enumerable: false,
        configurable: true
    });
    EventDetailsContent.prototype.renderBody = function () {
        var event = this.state.event;
        if (!event) {
            return <NotFound />;
        }
        return this.renderContent(event);
    };
    EventDetailsContent.prototype.renderContent = function (event) {
        var _this = this;
        var _a, _b, _c;
        var _d = this.props, organization = _d.organization, location = _d.location, eventSlug = _d.eventSlug;
        // metrics
        trackAnalyticsEvent({
            eventKey: 'performance.event_details',
            eventName: 'Performance: Opened Event Details',
            event_type: event.type,
            organization_id: parseInt(organization.id, 10),
        });
        var isSidebarVisible = this.state.isSidebarVisible;
        var transactionName = event.title;
        var query = decodeScalar(location.query.query, '');
        var eventJsonUrl = "/api/0/projects/" + organization.slug + "/" + this.projectId + "/events/" + event.eventID + "/json/";
        var traceId = (_c = (_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.trace_id) !== null && _c !== void 0 ? _c : '';
        var _e = getTraceTimeRangeFromEvent(event), start = _e.start, end = _e.end;
        return (<TraceMetaQuery location={location} orgSlug={organization.slug} traceId={traceId} start={start} end={end}>
        {function (metaResults) { return (<QuickTraceQuery event={event} location={location} orgSlug={organization.slug}>
            {function (results) {
                    var _a;
                    return (<Fragment>
                <Layout.Header>
                  <Layout.HeaderContent>
                    <Breadcrumb organization={organization} location={location} transactionName={transactionName} eventSlug={eventSlug}/>
                    <Layout.Title data-test-id="event-header">{event.title}</Layout.Title>
                  </Layout.HeaderContent>
                  <Layout.HeaderActions>
                    <ButtonBar gap={1}>
                      <Button onClick={_this.toggleSidebar}>
                        {isSidebarVisible ? 'Hide Details' : 'Show Details'}
                      </Button>
                      {results && (<Button icon={<IconOpen />} href={eventJsonUrl} external>
                          {t('JSON')} (<FileSize bytes={event.size}/>)
                        </Button>)}
                    </ButtonBar>
                  </Layout.HeaderActions>
                </Layout.Header>
                <Layout.Body>
                  {results && (<Layout.Main fullWidth>
                      <EventMetas quickTrace={results} meta={(_a = metaResults === null || metaResults === void 0 ? void 0 : metaResults.meta) !== null && _a !== void 0 ? _a : null} event={event} organization={organization} projectId={_this.projectId} location={location} errorDest="issue" transactionDest="performance"/>
                    </Layout.Main>)}
                  <Layout.Main fullWidth={!isSidebarVisible}>
                    <Projects orgId={organization.slug} slugs={[_this.projectId]}>
                      {function (_a) {
                            var projects = _a.projects;
                            return (<SpanEntryContext.Provider value={{
                                    getViewChildTransactionTarget: function (childTransactionProps) {
                                        return getTransactionDetailsUrl(organization, childTransactionProps.eventSlug, childTransactionProps.transaction, location.query);
                                    },
                                }}>
                          <QuickTraceContext.Provider value={results}>
                            <BorderlessEventEntries organization={organization} event={event} project={projects[0]} showExampleCommit={false} showTagSummary={false} location={location} api={_this.api}/>
                          </QuickTraceContext.Provider>
                        </SpanEntryContext.Provider>);
                        }}
                    </Projects>
                  </Layout.Main>
                  {isSidebarVisible && (<Layout.Side>
                      {results === undefined && (<Fragment>
                          <EventMetadata event={event} organization={organization} projectId={_this.projectId}/>
                          <RootSpanStatus event={event}/>
                        </Fragment>)}
                      <EventVitals event={event}/>
                      <TagsTable event={event} query={query} generateUrl={_this.generateTagUrl}/>
                    </Layout.Side>)}
                </Layout.Body>
              </Fragment>);
                }}
          </QuickTraceQuery>); }}
      </TraceMetaQuery>);
    };
    EventDetailsContent.prototype.renderError = function (error) {
        var notFound = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 404; });
        var permissionDenied = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 403; });
        if (notFound) {
            return <NotFound />;
        }
        if (permissionDenied) {
            return (<LoadingError message={t('You do not have permission to view that event.')}/>);
        }
        return _super.prototype.renderError.call(this, error, true, true);
    };
    EventDetailsContent.prototype.renderComponent = function () {
        var organization = this.props.organization;
        return (<SentryDocumentTitle title={t('Performance - Event Details')} orgSlug={organization.slug}>
        {_super.prototype.renderComponent.call(this)}
      </SentryDocumentTitle>);
    };
    return EventDetailsContent;
}(AsyncComponent));
export default EventDetailsContent;
//# sourceMappingURL=content.jsx.map