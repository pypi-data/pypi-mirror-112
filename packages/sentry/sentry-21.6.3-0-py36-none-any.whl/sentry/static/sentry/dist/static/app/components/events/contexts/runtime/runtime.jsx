import { __read, __spreadArray } from "tslib";
import { Fragment } from 'react';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import getUnknownData from '../getUnknownData';
import getRuntimeKnownData from './getRuntimeKnownData';
import { RuntimeIgnoredDataType, RuntimeKnownDataType } from './types';
var runtimeKnownDataValues = [RuntimeKnownDataType.NAME, RuntimeKnownDataType.VERSION];
var runtimeIgnoredDataValues = [RuntimeIgnoredDataType.BUILD];
var Runtime = function (_a) {
    var data = _a.data;
    return (<Fragment>
      <ContextBlock data={getRuntimeKnownData(data, runtimeKnownDataValues)}/>
      <ContextBlock data={getUnknownData(data, __spreadArray(__spreadArray([], __read(runtimeKnownDataValues)), __read(runtimeIgnoredDataValues)))}/>
    </Fragment>);
};
export default Runtime;
//# sourceMappingURL=runtime.jsx.map