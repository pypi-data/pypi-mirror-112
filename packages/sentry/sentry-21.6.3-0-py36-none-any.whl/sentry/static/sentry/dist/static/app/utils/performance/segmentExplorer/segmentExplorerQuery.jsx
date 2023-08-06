import * as React from 'react';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import withApi from 'app/utils/withApi';
export function getRequestFunction(_props) {
    var aggregateColumn = _props.aggregateColumn;
    function getTagExplorerRequestPayload(props) {
        var eventView = props.eventView;
        var apiPayload = eventView.getEventsAPIPayload(props.location);
        apiPayload.aggregateColumn = aggregateColumn;
        apiPayload.sort = _props.sort ? _props.sort : apiPayload.sort;
        if (_props.allTagKeys) {
            apiPayload.allTagKeys = _props.allTagKeys;
        }
        if (_props.tagKey) {
            apiPayload.tagKey = _props.tagKey;
        }
        return apiPayload;
    }
    return getTagExplorerRequestPayload;
}
function shouldRefetchData(prevProps, nextProps) {
    return (prevProps.aggregateColumn !== nextProps.aggregateColumn ||
        prevProps.sort !== nextProps.sort ||
        prevProps.allTagKeys !== nextProps.allTagKeys ||
        prevProps.tagKey !== nextProps.tagKey);
}
function SegmentExplorerQuery(props) {
    return (<GenericDiscoverQuery route="events-facets-performance" getRequestPayload={getRequestFunction(props)} shouldRefetchData={shouldRefetchData} {...props}/>);
}
export default withApi(SegmentExplorerQuery);
//# sourceMappingURL=segmentExplorerQuery.jsx.map