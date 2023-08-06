import * as React from 'react';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import withApi from 'app/utils/withApi';
function VitalsCardsDiscoverQuery(props) {
    return <GenericDiscoverQuery route="eventsv2" {...props}/>;
}
export default withApi(VitalsCardsDiscoverQuery);
//# sourceMappingURL=vitalsDetailsTableQuery.jsx.map