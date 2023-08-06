import { __read, __spreadArray } from "tslib";
import { Fragment } from 'react';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import getUnknownData from '../getUnknownData';
import getAppKnownData from './getAppKnownData';
import { AppKnownDataType } from './types';
var appKnownDataValues = [
    AppKnownDataType.ID,
    AppKnownDataType.START_TIME,
    AppKnownDataType.DEVICE_HASH,
    AppKnownDataType.IDENTIFIER,
    AppKnownDataType.NAME,
    AppKnownDataType.VERSION,
    AppKnownDataType.BUILD,
];
var appIgnoredDataValues = [];
var App = function (_a) {
    var data = _a.data, event = _a.event;
    return (<Fragment>
    <ContextBlock data={getAppKnownData(event, data, appKnownDataValues)}/>
    <ContextBlock data={getUnknownData(data, __spreadArray(__spreadArray([], __read(appKnownDataValues)), __read(appIgnoredDataValues)))}/>
  </Fragment>);
};
export default App;
//# sourceMappingURL=app.jsx.map