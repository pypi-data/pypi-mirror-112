var _a, _b;
import { __assign, __read, __spreadArray } from "tslib";
import { assert } from 'app/types/utils';
var CONDITIONS_ARGUMENTS = [
    {
        label: 'equal =',
        value: 'equals',
    },
    {
        label: 'not equal !=',
        value: 'notEquals',
    },
    {
        label: 'less <',
        value: 'less',
    },
    {
        label: 'greater >',
        value: 'greater',
    },
    {
        label: 'less or equals <=',
        value: 'lessOrEquals',
    },
    {
        label: 'greater or equals >=',
        value: 'greaterOrEquals',
    },
];
// Refer to src/sentry/search/events/fields.py
export var AGGREGATIONS = {
    count: {
        parameters: [],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    count_unique: {
        parameters: [
            {
                kind: 'column',
                columnTypes: ['string', 'integer', 'number', 'duration', 'date', 'boolean'],
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'line',
    },
    failure_count: {
        parameters: [],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'line',
    },
    min: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate([
                    'integer',
                    'number',
                    'duration',
                    'date',
                ]),
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    max: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate([
                    'integer',
                    'number',
                    'duration',
                    'date',
                ]),
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    avg: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    sum: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'area',
    },
    any: {
        parameters: [
            {
                kind: 'column',
                columnTypes: ['string', 'integer', 'number', 'duration', 'date', 'boolean'],
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
    },
    last_seen: {
        parameters: [],
        outputType: 'date',
        isSortable: true,
    },
    // Tracing functions.
    p50: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    p75: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    p95: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        type: [],
        isSortable: true,
        multiPlotType: 'line',
    },
    p99: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    p100: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: false,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    percentile: {
        parameters: [
            {
                kind: 'column',
                columnTypes: validateForNumericAggregate(['duration', 'number']),
                defaultValue: 'transaction.duration',
                required: true,
            },
            {
                kind: 'value',
                dataType: 'number',
                defaultValue: '0.5',
                required: true,
            },
        ],
        outputType: null,
        isSortable: true,
        multiPlotType: 'line',
    },
    failure_rate: {
        parameters: [],
        outputType: 'percentage',
        isSortable: true,
        multiPlotType: 'line',
    },
    apdex: {
        getFieldOverrides: function (_a) {
            var _b, _c;
            var parameter = _a.parameter, organization = _a.organization;
            if (organization.features.includes('project-transaction-threshold')) {
                return { required: false, placeholder: 'Automatic', defaultValue: '' };
            }
            return {
                defaultValue: (_c = (_b = organization.apdexThreshold) === null || _b === void 0 ? void 0 : _b.toString()) !== null && _c !== void 0 ? _c : parameter.defaultValue,
            };
        },
        parameters: [
            {
                kind: 'value',
                dataType: 'number',
                defaultValue: '300',
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'line',
    },
    user_misery: {
        getFieldOverrides: function (_a) {
            var _b, _c;
            var parameter = _a.parameter, organization = _a.organization;
            if (organization.features.includes('project-transaction-threshold')) {
                return { required: false, placeholder: 'Automatic', defaultValue: '' };
            }
            return {
                defaultValue: (_c = (_b = organization.apdexThreshold) === null || _b === void 0 ? void 0 : _b.toString()) !== null && _c !== void 0 ? _c : parameter.defaultValue,
            };
        },
        parameters: [
            {
                kind: 'value',
                dataType: 'number',
                defaultValue: '300',
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    eps: {
        parameters: [],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    epm: {
        parameters: [],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    count_miserable: {
        getFieldOverrides: function (_a) {
            var _b, _c;
            var parameter = _a.parameter, organization = _a.organization;
            if (parameter.kind === 'column') {
                return { defaultValue: 'user' };
            }
            if (organization.features.includes('project-transaction-threshold')) {
                return { required: false, placeholder: 'Automatic', defaultValue: '' };
            }
            return {
                defaultValue: (_c = (_b = organization.apdexThreshold) === null || _b === void 0 ? void 0 : _b.toString()) !== null && _c !== void 0 ? _c : parameter.defaultValue,
            };
        },
        parameters: [
            {
                kind: 'column',
                columnTypes: validateAllowedColumns(['user']),
                defaultValue: 'user',
                required: true,
            },
            {
                kind: 'value',
                dataType: 'number',
                defaultValue: '300',
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
    count_if: {
        parameters: [
            {
                kind: 'column',
                columnTypes: ['string', 'duration'],
                defaultValue: 'transaction.duration',
                required: true,
            },
            {
                kind: 'dropdown',
                options: CONDITIONS_ARGUMENTS,
                dataType: 'string',
                defaultValue: CONDITIONS_ARGUMENTS[0].value,
                required: true,
            },
            {
                kind: 'value',
                dataType: 'string',
                defaultValue: '300',
                required: true,
            },
        ],
        outputType: 'number',
        isSortable: true,
        multiPlotType: 'area',
    },
};
// TPM and TPS are aliases that are only used in Performance
export var ALIASES = {
    tpm: 'epm',
    tps: 'eps',
};
assert(AGGREGATIONS);
var FieldKey;
(function (FieldKey) {
    FieldKey["CULPRIT"] = "culprit";
    FieldKey["DEVICE_ARCH"] = "device.arch";
    FieldKey["DEVICE_BATTERY_LEVEL"] = "device.battery_level";
    FieldKey["DEVICE_BRAND"] = "device.brand";
    FieldKey["DEVICE_CHARGING"] = "device.charging";
    FieldKey["DEVICE_LOCALE"] = "device.locale";
    FieldKey["DEVICE_NAME"] = "device.name";
    FieldKey["DEVICE_ONLINE"] = "device.online";
    FieldKey["DEVICE_ORIENTATION"] = "device.orientation";
    FieldKey["DEVICE_SIMULATOR"] = "device.simulator";
    FieldKey["DEVICE_UUID"] = "device.uuid";
    FieldKey["DIST"] = "dist";
    FieldKey["ENVIRONMENT"] = "environment";
    FieldKey["ERROR_HANDLED"] = "error.handled";
    FieldKey["ERROR_UNHANDLED"] = "error.unhandled";
    FieldKey["ERROR_MECHANISM"] = "error.mechanism";
    FieldKey["ERROR_TYPE"] = "error.type";
    FieldKey["ERROR_VALUE"] = "error.value";
    FieldKey["EVENT_TYPE"] = "event.type";
    FieldKey["GEO_CITY"] = "geo.city";
    FieldKey["GEO_COUNTRY_CODE"] = "geo.country_code";
    FieldKey["GEO_REGION"] = "geo.region";
    FieldKey["HTTP_METHOD"] = "http.method";
    FieldKey["HTTP_REFERER"] = "http.referer";
    FieldKey["HTTP_URL"] = "http.url";
    FieldKey["ID"] = "id";
    FieldKey["ISSUE"] = "issue";
    FieldKey["LOCATION"] = "location";
    FieldKey["MESSAGE"] = "message";
    FieldKey["OS_BUILD"] = "os.build";
    FieldKey["OS_KERNEL_VERSION"] = "os.kernel_version";
    FieldKey["PLATFORM_NAME"] = "platform.name";
    FieldKey["PROJECT"] = "project";
    FieldKey["RELEASE"] = "release";
    FieldKey["SDK_NAME"] = "sdk.name";
    FieldKey["SDK_VERSION"] = "sdk.version";
    FieldKey["STACK_ABS_PATH"] = "stack.abs_path";
    FieldKey["STACK_COLNO"] = "stack.colno";
    FieldKey["STACK_FILENAME"] = "stack.filename";
    FieldKey["STACK_FUNCTION"] = "stack.function";
    FieldKey["STACK_IN_APP"] = "stack.in_app";
    FieldKey["STACK_LINENO"] = "stack.lineno";
    FieldKey["STACK_MODULE"] = "stack.module";
    FieldKey["STACK_PACKAGE"] = "stack.package";
    FieldKey["STACK_STACK_LEVEL"] = "stack.stack_level";
    FieldKey["TIMESTAMP"] = "timestamp";
    FieldKey["TIMESTAMP_TO_HOUR"] = "timestamp.to_hour";
    FieldKey["TIMESTAMP_TO_DAY"] = "timestamp.to_day";
    FieldKey["TITLE"] = "title";
    FieldKey["TRACE"] = "trace";
    FieldKey["TRACE_PARENT_SPAN"] = "trace.parent_span";
    FieldKey["TRACE_SPAN"] = "trace.span";
    FieldKey["TRANSACTION"] = "transaction";
    FieldKey["TRANSACTION_DURATION"] = "transaction.duration";
    FieldKey["TRANSACTION_OP"] = "transaction.op";
    FieldKey["TRANSACTION_STATUS"] = "transaction.status";
    FieldKey["USER_EMAIL"] = "user.email";
    FieldKey["USER_ID"] = "user.id";
    FieldKey["USER_IP"] = "user.ip";
    FieldKey["USER_USERNAME"] = "user.username";
    FieldKey["USER_DISPLAY"] = "user.display";
})(FieldKey || (FieldKey = {}));
/**
 * Refer to src/sentry/snuba/events.py, search for Columns
 */
export var FIELDS = (_a = {},
    _a[FieldKey.ID] = 'string',
    // issue.id and project.id are omitted on purpose.
    // Customers should use `issue` and `project` instead.
    _a[FieldKey.TIMESTAMP] = 'date',
    // time is omitted on purpose.
    // Customers should use `timestamp` or `timestamp.to_hour`.
    _a[FieldKey.TIMESTAMP_TO_HOUR] = 'date',
    _a[FieldKey.TIMESTAMP_TO_DAY] = 'date',
    _a[FieldKey.CULPRIT] = 'string',
    _a[FieldKey.LOCATION] = 'string',
    _a[FieldKey.MESSAGE] = 'string',
    _a[FieldKey.PLATFORM_NAME] = 'string',
    _a[FieldKey.ENVIRONMENT] = 'string',
    _a[FieldKey.RELEASE] = 'string',
    _a[FieldKey.DIST] = 'string',
    _a[FieldKey.TITLE] = 'string',
    _a[FieldKey.EVENT_TYPE] = 'string',
    // tags.key and tags.value are omitted on purpose as well.
    _a[FieldKey.TRANSACTION] = 'string',
    _a[FieldKey.USER_ID] = 'string',
    _a[FieldKey.USER_EMAIL] = 'string',
    _a[FieldKey.USER_USERNAME] = 'string',
    _a[FieldKey.USER_IP] = 'string',
    _a[FieldKey.SDK_NAME] = 'string',
    _a[FieldKey.SDK_VERSION] = 'string',
    _a[FieldKey.HTTP_METHOD] = 'string',
    _a[FieldKey.HTTP_REFERER] = 'string',
    _a[FieldKey.HTTP_URL] = 'string',
    _a[FieldKey.OS_BUILD] = 'string',
    _a[FieldKey.OS_KERNEL_VERSION] = 'string',
    _a[FieldKey.DEVICE_NAME] = 'string',
    _a[FieldKey.DEVICE_BRAND] = 'string',
    _a[FieldKey.DEVICE_LOCALE] = 'string',
    _a[FieldKey.DEVICE_UUID] = 'string',
    _a[FieldKey.DEVICE_ARCH] = 'string',
    _a[FieldKey.DEVICE_BATTERY_LEVEL] = 'number',
    _a[FieldKey.DEVICE_ORIENTATION] = 'string',
    _a[FieldKey.DEVICE_SIMULATOR] = 'boolean',
    _a[FieldKey.DEVICE_ONLINE] = 'boolean',
    _a[FieldKey.DEVICE_CHARGING] = 'boolean',
    _a[FieldKey.GEO_COUNTRY_CODE] = 'string',
    _a[FieldKey.GEO_REGION] = 'string',
    _a[FieldKey.GEO_CITY] = 'string',
    _a[FieldKey.ERROR_TYPE] = 'string',
    _a[FieldKey.ERROR_VALUE] = 'string',
    _a[FieldKey.ERROR_MECHANISM] = 'string',
    _a[FieldKey.ERROR_HANDLED] = 'boolean',
    _a[FieldKey.ERROR_UNHANDLED] = 'boolean',
    _a[FieldKey.STACK_ABS_PATH] = 'string',
    _a[FieldKey.STACK_FILENAME] = 'string',
    _a[FieldKey.STACK_PACKAGE] = 'string',
    _a[FieldKey.STACK_MODULE] = 'string',
    _a[FieldKey.STACK_FUNCTION] = 'string',
    _a[FieldKey.STACK_IN_APP] = 'boolean',
    _a[FieldKey.STACK_COLNO] = 'number',
    _a[FieldKey.STACK_LINENO] = 'number',
    _a[FieldKey.STACK_STACK_LEVEL] = 'number',
    // contexts.key and contexts.value omitted on purpose.
    // Transaction event fields.
    _a[FieldKey.TRANSACTION_DURATION] = 'duration',
    _a[FieldKey.TRANSACTION_OP] = 'string',
    _a[FieldKey.TRANSACTION_STATUS] = 'string',
    _a[FieldKey.TRACE] = 'string',
    _a[FieldKey.TRACE_SPAN] = 'string',
    _a[FieldKey.TRACE_PARENT_SPAN] = 'string',
    // Field alises defined in src/sentry/api/event_search.py
    _a[FieldKey.PROJECT] = 'string',
    _a[FieldKey.ISSUE] = 'string',
    _a[FieldKey.USER_DISPLAY] = 'string',
    _a);
export var FIELD_TAGS = Object.freeze(Object.fromEntries(Object.keys(FIELDS).map(function (item) { return [item, { key: item, name: item }]; })));
export var WebVital;
(function (WebVital) {
    WebVital["FP"] = "measurements.fp";
    WebVital["FCP"] = "measurements.fcp";
    WebVital["LCP"] = "measurements.lcp";
    WebVital["FID"] = "measurements.fid";
    WebVital["CLS"] = "measurements.cls";
    WebVital["TTFB"] = "measurements.ttfb";
    WebVital["RequestTime"] = "measurements.ttfb.requesttime";
})(WebVital || (WebVital = {}));
export var MobileVital;
(function (MobileVital) {
    MobileVital["AppStartCold"] = "measurements.app_start_cold";
    MobileVital["AppStartWarm"] = "measurements.app_start_warm";
    MobileVital["FramesTotal"] = "measurements.frames_total";
    MobileVital["FramesSlow"] = "measurements.frames_slow";
    MobileVital["FramesFrozen"] = "measurements.frames_frozen";
})(MobileVital || (MobileVital = {}));
var MEASUREMENTS = (_b = {},
    _b[WebVital.FP] = 'duration',
    _b[WebVital.FCP] = 'duration',
    _b[WebVital.LCP] = 'duration',
    _b[WebVital.FID] = 'duration',
    _b[WebVital.CLS] = 'number',
    _b[WebVital.TTFB] = 'duration',
    _b[WebVital.RequestTime] = 'duration',
    _b[MobileVital.AppStartCold] = 'duration',
    _b[MobileVital.AppStartWarm] = 'duration',
    _b[MobileVital.FramesTotal] = 'number',
    _b[MobileVital.FramesSlow] = 'number',
    _b[MobileVital.FramesFrozen] = 'number',
    _b);
// This list contains fields/functions that are available with performance-view feature.
export var TRACING_FIELDS = __spreadArray([
    'avg',
    'sum',
    'transaction.duration',
    'transaction.op',
    'transaction.status',
    'p50',
    'p75',
    'p95',
    'p99',
    'p100',
    'percentile',
    'failure_rate',
    'apdex',
    'count_miserable',
    'user_misery',
    'eps',
    'epm',
    'key_transaction',
    'team_key_transaction'
], __read(Object.keys(MEASUREMENTS)));
export var MEASUREMENT_PATTERN = /^measurements\.([a-zA-Z0-9-_.]+)$/;
export var SPAN_OP_BREAKDOWN_PATTERN = /^spans\.([a-zA-Z0-9-_.]+)$/;
export function isMeasurement(field) {
    var results = field.match(MEASUREMENT_PATTERN);
    return !!results;
}
export function measurementType(field) {
    if (MEASUREMENTS.hasOwnProperty(field)) {
        return MEASUREMENTS[field];
    }
    return 'number';
}
export function getMeasurementSlug(field) {
    var results = field.match(MEASUREMENT_PATTERN);
    if (results && results.length >= 2) {
        return results[1];
    }
    return null;
}
var AGGREGATE_PATTERN = /^(\w+)\((.*)?\)$/;
// Identical to AGGREGATE_PATTERN, but without the $ for newline, or ^ for start of line
var AGGREGATE_BASE = /(\w+)\((.*)?\)/g;
export function getAggregateArg(field) {
    // only returns the first argument if field is an aggregate
    var result = parseFunction(field);
    if (result && result.arguments.length > 0) {
        return result.arguments[0];
    }
    return null;
}
export function parseFunction(field) {
    var results = field.match(AGGREGATE_PATTERN);
    if (results && results.length === 3) {
        return {
            name: results[1],
            arguments: parseArguments(results[1], results[2]),
        };
    }
    return null;
}
export function parseArguments(functionText, columnText) {
    // Some functions take a quoted string for their arguments that may contain commas
    // This function attempts to be identical with the similarly named parse_arguments
    // found in src/sentry/search/events/fields.py
    if ((functionText !== 'to_other' && functionText !== 'count_if') ||
        columnText.length === 0) {
        return columnText ? columnText.split(',').map(function (result) { return result.trim(); }) : [];
    }
    var args = [];
    var quoted = false;
    var escaped = false;
    var i = 0;
    var j = 0;
    while (j < columnText.length) {
        if (i === j && columnText[j] === '"') {
            // when we see a quote at the beginning of
            // an argument, then this is a quoted string
            quoted = true;
        }
        else if (quoted && !escaped && columnText[j] === '\\') {
            // when we see a slash inside a quoted string,
            // the next character is an escape character
            escaped = true;
        }
        else if (quoted && !escaped && columnText[j] === '"') {
            // when we see a non-escaped quote while inside
            // of a quoted string, we should end it
            quoted = false;
        }
        else if (quoted && escaped) {
            // when we are inside a quoted string and have
            // begun an escape character, we should end it
            escaped = false;
        }
        else if (quoted && columnText[j] === ',') {
            // when we are inside a quoted string and see
            // a comma, it should not be considered an
            // argument separator
        }
        else if (columnText[j] === ',') {
            // when we see a comma outside of a quoted string
            // it is an argument separator
            args.push(columnText.substring(i, j).trim());
            i = j + 1;
        }
        j += 1;
    }
    if (i !== j) {
        // add in the last argument if any
        args.push(columnText.substring(i).trim());
    }
    return args;
}
// `|` is an invalid field character, so it is used to determine whether a field is an equation or not
var EQUATION_PREFIX = 'equation|';
var EQUATION_ALIAS_PATTERN = /^equation\[(\d+)\]$/;
export function isEquation(field) {
    return field.startsWith(EQUATION_PREFIX);
}
export function isEquationAlias(field) {
    return EQUATION_ALIAS_PATTERN.test(field);
}
export function getEquationAliasIndex(field) {
    var results = field.match(EQUATION_ALIAS_PATTERN);
    if (results && results.length === 2) {
        return parseInt(results[1], 10);
    }
    return -1;
}
export function getEquation(field) {
    return field.slice(EQUATION_PREFIX.length);
}
export function isAggregateEquation(field) {
    var results = field.match(AGGREGATE_BASE);
    return isEquation(field) && results !== null && results.length > 0;
}
export function generateAggregateFields(organization, eventFields, excludeFields) {
    if (excludeFields === void 0) { excludeFields = []; }
    var functions = Object.keys(AGGREGATIONS);
    var fields = Object.values(eventFields).map(function (field) { return field.field; });
    functions.forEach(function (func) {
        var parameters = AGGREGATIONS[func].parameters.map(function (param) {
            var overrides = AGGREGATIONS[func].getFieldOverrides;
            if (typeof overrides === 'undefined') {
                return param;
            }
            return __assign(__assign({}, param), overrides({ parameter: param, organization: organization }));
        });
        if (parameters.every(function (param) { return typeof param.defaultValue !== 'undefined'; })) {
            var newField = func + "(" + parameters
                .map(function (param) { return param.defaultValue; })
                .join(',') + ")";
            if (fields.indexOf(newField) === -1 && excludeFields.indexOf(newField) === -1) {
                fields.push(newField);
            }
        }
    });
    return fields.map(function (field) { return ({ field: field }); });
}
export function explodeFieldString(field) {
    var _a;
    if (isEquation(field)) {
        return { kind: 'equation', field: getEquation(field) };
    }
    var results = parseFunction(field);
    if (results) {
        return {
            kind: 'function',
            function: [
                results.name,
                (_a = results.arguments[0]) !== null && _a !== void 0 ? _a : '',
                results.arguments[1],
                results.arguments[2],
            ],
        };
    }
    return { kind: 'field', field: field };
}
export function generateFieldAsString(value) {
    if (value.kind === 'field') {
        return value.field;
    }
    else if (value.kind === 'equation') {
        return "" + EQUATION_PREFIX + value.field;
    }
    var aggregation = value.function[0];
    var parameters = value.function.slice(1).filter(function (i) { return i; });
    return aggregation + "(" + parameters.join(',') + ")";
}
export function explodeField(field) {
    var results = explodeFieldString(field.field);
    return results;
}
/**
 * Get the alias that the API results will have for a given aggregate function name
 */
export function getAggregateAlias(field) {
    var result = parseFunction(field);
    if (!result) {
        return field;
    }
    var alias = result.name;
    if (result.arguments.length > 0) {
        alias += '_' + result.arguments.join('_');
    }
    return alias.replace(/[^\w]/g, '_').replace(/^_+/g, '').replace(/_+$/, '');
}
/**
 * Check if a field name looks like an aggregate function or known aggregate alias.
 */
export function isAggregateField(field) {
    return parseFunction(field) !== null;
}
/**
 * Convert a function string into type it will output.
 * This is useful when you need to format values in tooltips,
 * or in series markers.
 */
export function aggregateOutputType(field) {
    var result = parseFunction(field);
    if (!result) {
        return 'number';
    }
    var outputType = aggregateFunctionOutputType(result.name, result.arguments[0]);
    if (outputType === null) {
        return 'number';
    }
    return outputType;
}
/**
 * Converts a function string and its first argument into its output type.
 * - If the function has a fixed output type, that will be the result.
 * - If the function does not define an output type, the output type will be equal to
 *   the type of its first argument.
 * - If the function has an optional first argument, and it was not defined, make sure
 *   to use the default argument as the first argument.
 * - If the type could not be determined, return null.
 */
export function aggregateFunctionOutputType(funcName, firstArg) {
    var _a;
    var aggregate = AGGREGATIONS[ALIASES[funcName] || funcName];
    // Attempt to use the function's outputType.
    if (aggregate === null || aggregate === void 0 ? void 0 : aggregate.outputType) {
        return aggregate.outputType;
    }
    // If the first argument is undefined and it is not required,
    // then we attempt to get the default value.
    if (!firstArg && ((_a = aggregate === null || aggregate === void 0 ? void 0 : aggregate.parameters) === null || _a === void 0 ? void 0 : _a[0])) {
        if (aggregate.parameters[0].required === false) {
            firstArg = aggregate.parameters[0].defaultValue;
        }
    }
    // If the function is an inherit type it will have a field as
    // the first parameter and we can use that to get the type.
    if (firstArg && FIELDS.hasOwnProperty(firstArg)) {
        return FIELDS[firstArg];
    }
    else if (firstArg && isMeasurement(firstArg)) {
        return measurementType(firstArg);
    }
    else if (firstArg && isSpanOperationBreakdownField(firstArg)) {
        return 'duration';
    }
    return null;
}
/**
 * Get the multi-series chart type for an aggregate function.
 */
export function aggregateMultiPlotType(field) {
    var result = parseFunction(field);
    // Handle invalid data.
    if (!result) {
        return 'area';
    }
    if (!AGGREGATIONS.hasOwnProperty(result.name)) {
        return 'area';
    }
    return AGGREGATIONS[result.name].multiPlotType;
}
function validateForNumericAggregate(validColumnTypes) {
    return function (_a) {
        var name = _a.name, dataType = _a.dataType;
        // these built-in columns cannot be applied to numeric aggregates such as percentile(...)
        if ([
            FieldKey.DEVICE_BATTERY_LEVEL,
            FieldKey.STACK_COLNO,
            FieldKey.STACK_LINENO,
            FieldKey.STACK_STACK_LEVEL,
        ].includes(name)) {
            return false;
        }
        return validColumnTypes.includes(dataType);
    };
}
function validateAllowedColumns(validColumns) {
    return function (_a) {
        var name = _a.name;
        return validColumns.includes(name);
    };
}
var alignedTypes = ['number', 'duration', 'integer', 'percentage'];
export function fieldAlignment(columnName, columnType, metadata) {
    var align = 'left';
    if (columnType) {
        align = alignedTypes.includes(columnType) ? 'right' : 'left';
    }
    if (columnType === undefined || columnType === 'never') {
        // fallback to align the column based on the table metadata
        var maybeType = metadata ? metadata[getAggregateAlias(columnName)] : undefined;
        if (maybeType !== undefined && alignedTypes.includes(maybeType)) {
            align = 'right';
        }
    }
    return align;
}
/**
 * Match on types that are legal to show on a timeseries chart.
 */
export function isLegalYAxisType(match) {
    return ['number', 'integer', 'duration', 'percentage'].includes(match);
}
export function isSpanOperationBreakdownField(field) {
    return field.startsWith('spans.');
}
export var SPAN_OP_RELATIVE_BREAKDOWN_FIELD = 'span_ops_breakdown.relative';
export function isRelativeSpanOperationBreakdownField(field) {
    return field === SPAN_OP_RELATIVE_BREAKDOWN_FIELD;
}
export var SPAN_OP_BREAKDOWN_FIELDS = [
    'spans.http',
    'spans.db',
    'spans.browser',
    'spans.resource',
];
export function getSpanOperationName(field) {
    var results = field.match(SPAN_OP_BREAKDOWN_PATTERN);
    if (results && results.length >= 2) {
        return results[1];
    }
    return null;
}
export function getColumnType(column) {
    if (column.kind === 'function') {
        var outputType = aggregateFunctionOutputType(column.function[0], column.function[1]);
        if (outputType !== null) {
            return outputType;
        }
    }
    else if (column.kind === 'field') {
        if (FIELDS.hasOwnProperty(column.field)) {
            return FIELDS[column.field];
        }
        else if (isMeasurement(column.field)) {
            return measurementType(column.field);
        }
        else if (isSpanOperationBreakdownField(column.field)) {
            return 'duration';
        }
    }
    return 'string';
}
//# sourceMappingURL=fields.jsx.map