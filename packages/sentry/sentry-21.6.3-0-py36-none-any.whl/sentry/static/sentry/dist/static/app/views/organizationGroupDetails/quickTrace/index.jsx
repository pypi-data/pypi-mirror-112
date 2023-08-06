import { Fragment } from 'react';
import DistributedTracingPrompt from './configureDistributedTracing';
import IssueQuickTrace from './issueQuickTrace';
export default function QuickTrace(_a) {
    var _b, _c;
    var event = _a.event, group = _a.group, organization = _a.organization, location = _a.location;
    var hasPerformanceView = organization.features.includes('performance-view');
    var hasTraceContext = Boolean((_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id);
    return (<Fragment>
      {!hasTraceContext && (<DistributedTracingPrompt event={event} project={group.project} organization={organization}/>)}
      {hasPerformanceView && hasTraceContext && (<IssueQuickTrace organization={organization} event={event} location={location}/>)}
    </Fragment>);
}
//# sourceMappingURL=index.jsx.map