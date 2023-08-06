import { __read, __spreadArray } from "tslib";
import { Fragment } from 'react';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import getUnknownData from '../getUnknownData';
import getOperatingSystemKnownData from './getGPUKnownData';
import { GPUKnownDataType } from './types';
var gpuKnownDataValues = [
    GPUKnownDataType.NAME,
    GPUKnownDataType.VERSION,
    GPUKnownDataType.VENDOR_NAME,
    GPUKnownDataType.MEMORY,
    GPUKnownDataType.NPOT_SUPPORT,
    GPUKnownDataType.MULTI_THREAD_RENDERING,
    GPUKnownDataType.API_TYPE,
];
var gpuIgnoredDataValues = [];
var GPU = function (_a) {
    var data = _a.data;
    if (data.vendor_id > 0) {
        gpuKnownDataValues.unshift[GPUKnownDataType.VENDOR_ID];
    }
    if (data.id > 0) {
        gpuKnownDataValues.unshift[GPUKnownDataType.ID];
    }
    return (<Fragment>
      <ContextBlock data={getOperatingSystemKnownData(data, gpuKnownDataValues)}/>
      <ContextBlock data={getUnknownData(data, __spreadArray(__spreadArray([], __read(gpuKnownDataValues)), __read(gpuIgnoredDataValues)))}/>
    </Fragment>);
};
export default GPU;
//# sourceMappingURL=gpu.jsx.map