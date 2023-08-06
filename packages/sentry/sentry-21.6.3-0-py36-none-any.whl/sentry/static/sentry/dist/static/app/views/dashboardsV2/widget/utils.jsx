var _a;
import { t } from 'app/locale';
export var DisplayType;
(function (DisplayType) {
    DisplayType["AREA"] = "area";
    DisplayType["BAR"] = "bar";
    DisplayType["LINE"] = "line";
    DisplayType["TABLE"] = "table";
    DisplayType["WORLD_MAP"] = "world_map";
    DisplayType["BIG_NUMBER"] = "big_number";
    DisplayType["STACKED_AREA"] = "stacked_area";
})(DisplayType || (DisplayType = {}));
export var DataSet;
(function (DataSet) {
    DataSet["EVENTS"] = "events";
    DataSet["METRICS"] = "metrics";
})(DataSet || (DataSet = {}));
export var displayTypes = (_a = {},
    _a[DisplayType.AREA] = t('Area Chart'),
    _a[DisplayType.BAR] = t('Bar Chart'),
    _a[DisplayType.LINE] = t('Line Chart'),
    _a[DisplayType.TABLE] = t('Table'),
    _a[DisplayType.WORLD_MAP] = t('World Map'),
    _a[DisplayType.BIG_NUMBER] = t('Big Number'),
    _a);
//# sourceMappingURL=utils.jsx.map