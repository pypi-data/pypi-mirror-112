import { __assign, __rest } from "tslib";
import * as React from 'react';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import { beforeFetch, getTraceRequestPayload, makeEventView, } from 'app/utils/performance/quickTrace/utils';
import withApi from 'app/utils/withApi';
function TraceMetaQuery(_a) {
    var traceId = _a.traceId, start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod, children = _a.children, props = __rest(_a, ["traceId", "start", "end", "statsPeriod", "children"]);
    if (!traceId) {
        return (<React.Fragment>
        {children({
                isLoading: false,
                error: null,
                meta: null,
            })}
      </React.Fragment>);
    }
    var eventView = makeEventView({ start: start, end: end, statsPeriod: statsPeriod });
    return (<GenericDiscoverQuery route={"events-trace-meta/" + traceId} beforeFetch={beforeFetch} getRequestPayload={getTraceRequestPayload} eventView={eventView} {...props}>
      {function (_a) {
            var tableData = _a.tableData, rest = __rest(_a, ["tableData"]);
            return children(__assign({ meta: tableData }, rest));
        }}
    </GenericDiscoverQuery>);
}
export default withApi(TraceMetaQuery);
//# sourceMappingURL=traceMetaQuery.jsx.map