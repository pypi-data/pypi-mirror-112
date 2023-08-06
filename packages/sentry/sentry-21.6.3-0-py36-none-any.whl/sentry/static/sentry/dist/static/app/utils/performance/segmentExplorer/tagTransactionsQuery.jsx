import * as React from 'react';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import withApi from 'app/utils/withApi';
function shouldRefetchData(prevProps, nextProps) {
    return prevProps.query !== nextProps.query;
}
function TagTransactionsQuery(props) {
    return (<GenericDiscoverQuery route="eventsv2" shouldRefetchData={shouldRefetchData} {...props}/>);
}
export default withApi(TagTransactionsQuery);
//# sourceMappingURL=tagTransactionsQuery.jsx.map