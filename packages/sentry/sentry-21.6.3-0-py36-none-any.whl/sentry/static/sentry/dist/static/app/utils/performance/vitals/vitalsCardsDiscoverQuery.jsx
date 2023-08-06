import { __assign, __read, __rest, __spreadArray } from "tslib";
import * as React from 'react';
import pick from 'lodash/pick';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import { PERFORMANCE_URL_PARAM } from 'app/utils/performance/constants';
import withApi from 'app/utils/withApi';
function getRequestPayload(props) {
    var eventView = props.eventView, vitals = props.vitals;
    var apiPayload = eventView === null || eventView === void 0 ? void 0 : eventView.getEventsAPIPayload(props.location);
    return __assign({ vital: vitals }, pick(apiPayload, __spreadArray(['query'], __read(Object.values(PERFORMANCE_URL_PARAM)))));
}
function VitalsCardsDiscoverQuery(props) {
    return (<GenericDiscoverQuery getRequestPayload={getRequestPayload} route="events-vitals" {...props}>
      {function (_a) {
            var tableData = _a.tableData, rest = __rest(_a, ["tableData"]);
            return props.children(__assign({ vitalsData: tableData }, rest));
        }}
    </GenericDiscoverQuery>);
}
export default withApi(VitalsCardsDiscoverQuery);
//# sourceMappingURL=vitalsCardsDiscoverQuery.jsx.map