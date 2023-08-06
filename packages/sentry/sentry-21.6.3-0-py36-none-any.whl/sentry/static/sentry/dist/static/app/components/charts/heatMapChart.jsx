import { __assign, __rest } from "tslib";
import './components/visualMap';
import * as React from 'react';
import HeatMapSeries from './series/heatMapSeries';
import BaseChart from './baseChart';
export default React.forwardRef(function (props, ref) {
    var series = props.series, seriesOptions = props.seriesOptions, visualMaps = props.visualMaps, otherProps = __rest(props, ["series", "seriesOptions", "visualMaps"]);
    return (<BaseChart ref={ref} options={{
            visualMap: visualMaps,
        }} {...otherProps} series={series.map(function (_a) {
            var seriesName = _a.seriesName, data = _a.data, dataArray = _a.dataArray, options = __rest(_a, ["seriesName", "data", "dataArray"]);
            return HeatMapSeries(__assign(__assign(__assign({}, seriesOptions), options), { name: seriesName, data: dataArray || data.map(function (_a) {
                    var value = _a.value, name = _a.name;
                    return [name, value];
                }) }));
        })}/>);
});
//# sourceMappingURL=heatMapChart.jsx.map