import * as React from 'react';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import withApi from 'app/utils/withApi';
export function getRequestFunction(_props) {
    var aggregateColumn = _props.aggregateColumn;
    function getTagExplorerRequestPayload(props) {
        var eventView = props.eventView;
        var apiPayload = eventView.getEventsAPIPayload(props.location);
        apiPayload.aggregateColumn = aggregateColumn;
        apiPayload.sort = _props.sort ? _props.sort : '-sumdelta';
        apiPayload.tagKey = _props.tagKey;
        apiPayload.tagKeyLimit = _props.tagKeyLimit;
        apiPayload.numBucketsPerKey = _props.numBucketsPerKey;
        return apiPayload;
    }
    return getTagExplorerRequestPayload;
}
function shouldRefetchData(prevProps, nextProps) {
    return (prevProps.aggregateColumn !== nextProps.aggregateColumn ||
        prevProps.sort !== nextProps.sort ||
        prevProps.tagKey !== nextProps.tagKey);
}
function TagKeyHistogramQuery(props) {
    return (<GenericDiscoverQuery route="events-facets-performance-histogram" getRequestPayload={getRequestFunction(props)} shouldRefetchData={shouldRefetchData} {...props}/>);
}
export default withApi(TagKeyHistogramQuery);
//# sourceMappingURL=tagKeyHistogramQuery.jsx.map