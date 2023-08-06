import { __assign, __rest } from "tslib";
import 'echarts/lib/chart/heatmap';
import 'echarts/lib/component/visualMap';
export default function HeatMapSeries(props) {
    if (props === void 0) { props = {}; }
    var data = props.data, rest = __rest(props, ["data"]);
    return __assign(__assign({ data: data }, rest), { type: 'heatmap' });
}
//# sourceMappingURL=heatMapSeries.jsx.map