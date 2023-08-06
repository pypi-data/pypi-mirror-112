import * as React from 'react';
import withApi from 'app/utils/withApi';
import GenericDiscoverQuery from './genericDiscoverQuery';
function shouldRefetchData(prevProps, nextProps) {
    return (prevProps.transactionName !== nextProps.transactionName ||
        prevProps.transactionThreshold !== nextProps.transactionThreshold ||
        prevProps.transactionThresholdMetric !== nextProps.transactionThresholdMetric);
}
function DiscoverQuery(props) {
    return (<GenericDiscoverQuery route="eventsv2" shouldRefetchData={shouldRefetchData} {...props}/>);
}
export default withApi(DiscoverQuery);
//# sourceMappingURL=discoverQuery.jsx.map