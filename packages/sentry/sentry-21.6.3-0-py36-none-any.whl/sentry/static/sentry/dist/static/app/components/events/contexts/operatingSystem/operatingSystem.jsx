import { __read, __spreadArray } from "tslib";
import { Fragment } from 'react';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import getUnknownData from '../getUnknownData';
import getOperatingSystemKnownData from './getOperatingSystemKnownData';
import { OperatingSystemIgnoredDataType, OperatingSystemKnownDataType, } from './types';
var operatingSystemKnownDataValues = [
    OperatingSystemKnownDataType.NAME,
    OperatingSystemKnownDataType.VERSION,
    OperatingSystemKnownDataType.KERNEL_VERSION,
    OperatingSystemKnownDataType.ROOTED,
];
var operatingSystemIgnoredDataValues = [OperatingSystemIgnoredDataType.BUILD];
var OperatingSystem = function (_a) {
    var data = _a.data;
    return (<Fragment>
    <ContextBlock data={getOperatingSystemKnownData(data, operatingSystemKnownDataValues)}/>
    <ContextBlock data={getUnknownData(data, __spreadArray(__spreadArray([], __read(operatingSystemKnownDataValues)), __read(operatingSystemIgnoredDataValues)))}/>
  </Fragment>);
};
export default OperatingSystem;
//# sourceMappingURL=operatingSystem.jsx.map