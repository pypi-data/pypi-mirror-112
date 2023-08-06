import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import ErrorBoundary from 'app/components/errorBoundary';
import Hovercard from 'app/components/hovercard';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import QuickTrace from 'app/components/quickTrace';
import { generateTraceTarget } from 'app/components/quickTrace/utils';
import { t, tct, tn } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getConfigureTracingDocsLink } from 'app/utils/docs';
import { getShortEventId } from 'app/utils/events';
import { MetaData } from './styles';
function handleTraceLink(organization) {
    trackAnalyticsEvent({
        eventKey: 'quick_trace.trace_id.clicked',
        eventName: 'Quick Trace: Trace ID clicked',
        organization_id: parseInt(organization.id, 10),
        source: 'events',
    });
}
export default function QuickTraceMeta(_a) {
    var _b, _c, _d;
    var event = _a.event, location = _a.location, organization = _a.organization, quickTrace = _a.quickTrace, traceMeta = _a.traceMeta, anchor = _a.anchor, errorDest = _a.errorDest, transactionDest = _a.transactionDest, project = _a.project;
    var features = ['performance-view'];
    var noFeatureMessage = t('Requires performance monitoring.');
    var docsLink = getConfigureTracingDocsLink(project);
    var traceId = (_d = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id) !== null && _d !== void 0 ? _d : null;
    var traceTarget = generateTraceTarget(event, organization);
    var body;
    var footer;
    if (!traceId || !quickTrace || quickTrace.trace === null) {
        // this platform doesn't support performance don't show anything here
        if (docsLink === null) {
            return null;
        }
        body = t('Missing Trace');
        // need to configure tracing
        footer = <ExternalLink href={docsLink}>{t('Read the docs')}</ExternalLink>;
    }
    else {
        if (quickTrace.isLoading) {
            body = <Placeholder height="24px"/>;
        }
        else if (quickTrace.error) {
            body = '\u2014';
        }
        else {
            body = (<ErrorBoundary mini>
          <QuickTrace event={event} quickTrace={{
                    type: quickTrace.type,
                    trace: quickTrace.trace,
                }} location={location} organization={organization} anchor={anchor} errorDest={errorDest} transactionDest={transactionDest}/>
        </ErrorBoundary>);
        }
        footer = (<Link to={traceTarget} onClick={function () { return handleTraceLink(organization); }}>
        {tct('View Full Trace: [id][events]', {
                id: getShortEventId(traceId !== null && traceId !== void 0 ? traceId : ''),
                events: traceMeta
                    ? tn(' (%s event)', ' (%s events)', traceMeta.transactions + traceMeta.errors)
                    : '',
            })}
      </Link>);
    }
    return (<Feature hookName="feature-disabled:performance-quick-trace" features={features}>
      {function (_a) {
            var hasFeature = _a.hasFeature;
            // also need to enable the performance feature
            if (!hasFeature) {
                footer = (<Hovercard body={<FeatureDisabled features={features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
              {footer}
            </Hovercard>);
            }
            return <QuickTraceMetaBase body={body} footer={footer}/>;
        }}
    </Feature>);
}
export function QuickTraceMetaBase(_a) {
    var body = _a.body, footer = _a.footer;
    return (<MetaData headingText={t('Trace Navigator')} tooltipText={t('An abbreviated version of the full trace. Related frontend and backend services can be added to provide further visibility.')} bodyText={<div data-test-id="quick-trace-body">{body}</div>} subtext={<div data-test-id="quick-trace-footer">{footer}</div>}/>);
}
//# sourceMappingURL=quickTraceMeta.jsx.map