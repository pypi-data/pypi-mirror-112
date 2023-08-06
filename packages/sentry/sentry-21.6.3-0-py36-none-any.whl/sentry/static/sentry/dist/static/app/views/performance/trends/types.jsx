export var TrendChangeType;
(function (TrendChangeType) {
    TrendChangeType["IMPROVED"] = "improved";
    TrendChangeType["REGRESSION"] = "regression";
})(TrendChangeType || (TrendChangeType = {}));
export var TrendFunctionField;
(function (TrendFunctionField) {
    TrendFunctionField["P50"] = "p50";
    TrendFunctionField["P75"] = "p75";
    TrendFunctionField["P95"] = "p95";
    TrendFunctionField["P99"] = "p99";
    TrendFunctionField["AVG"] = "avg";
})(TrendFunctionField || (TrendFunctionField = {}));
export var TrendColumnField;
(function (TrendColumnField) {
    TrendColumnField["DURATION"] = "transaction.duration";
    TrendColumnField["LCP"] = "measurements.lcp";
    TrendColumnField["FCP"] = "measurements.fcp";
    TrendColumnField["FID"] = "measurements.fid";
    TrendColumnField["CLS"] = "measurements.cls";
    TrendColumnField["SPANS_DB"] = "spans.db";
    TrendColumnField["SPANS_HTTP"] = "spans.http";
    TrendColumnField["SPANS_BROWSER"] = "spans.browser";
    TrendColumnField["SPANS_RESOURCE"] = "spans.resource";
})(TrendColumnField || (TrendColumnField = {}));
//# sourceMappingURL=types.jsx.map