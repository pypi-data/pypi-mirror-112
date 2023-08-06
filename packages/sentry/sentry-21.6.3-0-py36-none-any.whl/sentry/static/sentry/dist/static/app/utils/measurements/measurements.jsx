import { __assign, __read } from "tslib";
import * as React from 'react';
import { MOBILE_VITAL_DETAILS, WEB_VITAL_DETAILS, } from 'app/utils/performance/vitals/constants';
function measurementsFromDetails(details) {
    return Object.fromEntries(Object.entries(details).map(function (_a) {
        var _b = __read(_a, 2), key = _b[0], value = _b[1];
        var newValue = {
            name: value.name,
            key: key,
        };
        return [key, newValue];
    }));
}
var MOBILE_MEASUREMENTS = measurementsFromDetails(MOBILE_VITAL_DETAILS);
var WEB_MEASUREMENTS = measurementsFromDetails(WEB_VITAL_DETAILS);
function Measurements(_a) {
    var organization = _a.organization, children = _a.children;
    var measurements = organization.features.includes('performance-mobile-vitals')
        ? __assign(__assign({}, WEB_MEASUREMENTS), MOBILE_MEASUREMENTS) : WEB_MEASUREMENTS;
    return <React.Fragment>{children({ measurements: measurements })}</React.Fragment>;
}
export default Measurements;
//# sourceMappingURL=measurements.jsx.map