import { __assign, __extends } from "tslib";
import * as React from 'react';
import { browserHistory } from 'react-router';
import { decodeScalar } from 'app/utils/queryString';
import { FILTER_OPTIONS } from './constants';
var Histogram = /** @class */ (function (_super) {
    __extends(Histogram, _super);
    function Histogram() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleResetView = function () {
            var _a = _this.props, location = _a.location, zoomKeys = _a.zoomKeys;
            browserHistory.push({
                pathname: location.pathname,
                query: removeHistogramQueryStrings(location, zoomKeys),
            });
        };
        _this.handleFilterChange = function (value) {
            var _a = _this.props, location = _a.location, zoomKeys = _a.zoomKeys;
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, removeHistogramQueryStrings(location, zoomKeys)), { dataFilter: value }),
            });
        };
        return _this;
    }
    Histogram.prototype.isZoomed = function () {
        var _a = this.props, location = _a.location, zoomKeys = _a.zoomKeys;
        return zoomKeys.map(function (key) { return location.query[key]; }).some(function (value) { return value !== undefined; });
    };
    Histogram.prototype.getActiveFilter = function () {
        var location = this.props.location;
        var dataFilter = location.query.dataFilter
            ? decodeScalar(location.query.dataFilter)
            : FILTER_OPTIONS[0].value;
        return FILTER_OPTIONS.find(function (item) { return item.value === dataFilter; }) || FILTER_OPTIONS[0];
    };
    Histogram.prototype.render = function () {
        var childrenProps = {
            isZoomed: this.isZoomed(),
            handleResetView: this.handleResetView,
            activeFilter: this.getActiveFilter(),
            handleFilterChange: this.handleFilterChange,
            filterOptions: FILTER_OPTIONS,
        };
        return this.props.children(childrenProps);
    };
    return Histogram;
}(React.Component));
export function removeHistogramQueryStrings(location, zoomKeys) {
    var query = __assign(__assign({}, location.query), { cursor: undefined });
    delete query.dataFilter;
    // reset all zoom parameters
    zoomKeys.forEach(function (key) { return delete query[key]; });
    return query;
}
export default Histogram;
//# sourceMappingURL=index.jsx.map