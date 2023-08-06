import { __assign, __read, __spreadArray, __values } from "tslib";
import isEqual from 'lodash/isEqual';
import { aggregateOutputType, isAggregateField, isLegalYAxisType, } from 'app/utils/discover/fields';
import { DisplayType } from '../utils';
export function mapErrors(data, update) {
    Object.keys(data).forEach(function (key) {
        var value = data[key];
        // Recurse into nested objects.
        if (Array.isArray(value) && typeof value[0] === 'string') {
            update[key] = value[0];
            return;
        }
        else if (Array.isArray(value) && typeof value[0] === 'object') {
            update[key] = value.map(function (item) { return mapErrors(item, {}); });
        }
        else {
            update[key] = mapErrors(value, {});
        }
    });
    return update;
}
export function normalizeQueries(displayType, queries) {
    var e_1, _a, e_2, _b;
    var isTimeseriesChart = [
        DisplayType.LINE,
        DisplayType.AREA,
        DisplayType.STACKED_AREA,
        DisplayType.BAR,
    ].includes(displayType);
    if ([DisplayType.TABLE, DisplayType.WORLD_MAP, DisplayType.BIG_NUMBER].includes(displayType)) {
        // Some display types may only support at most 1 query.
        queries = queries.slice(0, 1);
    }
    else if (isTimeseriesChart) {
        // Timeseries charts supports at most 3 queries.
        queries = queries.slice(0, 3);
    }
    if (displayType === DisplayType.TABLE) {
        return queries;
    }
    // Filter out non-aggregate fields
    queries = queries.map(function (query) {
        var fields = query.fields.filter(isAggregateField);
        if (isTimeseriesChart || displayType === DisplayType.WORLD_MAP) {
            // Filter out fields that will not generate numeric output types
            fields = fields.filter(function (field) { return isLegalYAxisType(aggregateOutputType(field)); });
        }
        if (isTimeseriesChart && fields.length && fields.length > 3) {
            // Timeseries charts supports at most 3 fields.
            fields = fields.slice(0, 3);
        }
        return __assign(__assign({}, query), { fields: fields.length ? fields : ['count()'] });
    });
    if (isTimeseriesChart) {
        // For timeseries widget, all queries must share identical set of fields.
        var referenceFields_1 = __spreadArray([], __read(queries[0].fields));
        try {
            queryLoop: for (var queries_1 = __values(queries), queries_1_1 = queries_1.next(); !queries_1_1.done; queries_1_1 = queries_1.next()) {
                var query = queries_1_1.value;
                if (referenceFields_1.length >= 3) {
                    break;
                }
                if (isEqual(referenceFields_1, query.fields)) {
                    continue;
                }
                try {
                    for (var _c = (e_2 = void 0, __values(query.fields)), _d = _c.next(); !_d.done; _d = _c.next()) {
                        var field = _d.value;
                        if (referenceFields_1.length >= 3) {
                            break queryLoop;
                        }
                        if (!referenceFields_1.includes(field)) {
                            referenceFields_1.push(field);
                        }
                    }
                }
                catch (e_2_1) { e_2 = { error: e_2_1 }; }
                finally {
                    try {
                        if (_d && !_d.done && (_b = _c.return)) _b.call(_c);
                    }
                    finally { if (e_2) throw e_2.error; }
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (queries_1_1 && !queries_1_1.done && (_a = queries_1.return)) _a.call(queries_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        queries = queries.map(function (query) {
            return __assign(__assign({}, query), { fields: referenceFields_1 });
        });
    }
    if ([DisplayType.WORLD_MAP, DisplayType.BIG_NUMBER].includes(displayType)) {
        // For world map chart, cap fields of the queries to only one field.
        queries = queries.map(function (query) {
            return __assign(__assign({}, query), { fields: query.fields.slice(0, 1) });
        });
    }
    return queries;
}
//# sourceMappingURL=utils.jsx.map