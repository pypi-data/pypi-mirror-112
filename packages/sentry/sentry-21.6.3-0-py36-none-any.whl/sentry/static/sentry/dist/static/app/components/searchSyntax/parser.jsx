var _a, _b;
import { __assign, __read, __spreadArray } from "tslib";
import moment from 'moment';
import { t } from 'app/locale';
import { isMeasurement, isSpanOperationBreakdownField, measurementType, } from 'app/utils/discover/fields';
import grammar from './grammar.pegjs';
import { getKeyName } from './utils';
var listJoiner = function (_a) {
    var _b = __read(_a, 4), s1 = _b[0], comma = _b[1], s2 = _b[2], value = _b[3];
    return ({
        separator: [s1.value, comma, s2.value].join(''),
        value: value,
    });
};
/**
 * A token represents a node in the syntax tree. These are all extrapolated
 * from the grammar and may not be named exactly the same.
 */
export var Token;
(function (Token) {
    Token["Spaces"] = "spaces";
    Token["Filter"] = "filter";
    Token["FreeText"] = "freeText";
    Token["LogicGroup"] = "logicGroup";
    Token["LogicBoolean"] = "logicBoolean";
    Token["KeySimple"] = "keySimple";
    Token["KeyExplicitTag"] = "keyExplicitTag";
    Token["KeyAggregate"] = "keyAggregate";
    Token["KeyAggregateArgs"] = "keyAggregateArgs";
    Token["ValueIso8601Date"] = "valueIso8601Date";
    Token["ValueRelativeDate"] = "valueRelativeDate";
    Token["ValueDuration"] = "valueDuration";
    Token["ValuePercentage"] = "valuePercentage";
    Token["ValueBoolean"] = "valueBoolean";
    Token["ValueNumber"] = "valueNumber";
    Token["ValueText"] = "valueText";
    Token["ValueNumberList"] = "valueNumberList";
    Token["ValueTextList"] = "valueTextList";
})(Token || (Token = {}));
/**
 * An operator in a key value term
 */
export var TermOperator;
(function (TermOperator) {
    TermOperator["Default"] = "";
    TermOperator["GreaterThanEqual"] = ">=";
    TermOperator["LessThanEqual"] = "<=";
    TermOperator["GreaterThan"] = ">";
    TermOperator["LessThan"] = "<";
    TermOperator["Equal"] = "=";
    TermOperator["NotEqual"] = "!=";
})(TermOperator || (TermOperator = {}));
/**
 * Logic operators
 */
export var BooleanOperator;
(function (BooleanOperator) {
    BooleanOperator["And"] = "AND";
    BooleanOperator["Or"] = "OR";
})(BooleanOperator || (BooleanOperator = {}));
/**
 * The Token.Filter may be one of many types of filters. This enum declares the
 * each variant filter type.
 */
export var FilterType;
(function (FilterType) {
    FilterType["Text"] = "text";
    FilterType["TextIn"] = "textIn";
    FilterType["Date"] = "date";
    FilterType["SpecificDate"] = "specificDate";
    FilterType["RelativeDate"] = "relativeDate";
    FilterType["Duration"] = "duration";
    FilterType["Numeric"] = "numeric";
    FilterType["NumericIn"] = "numericIn";
    FilterType["Boolean"] = "boolean";
    FilterType["AggregateDuration"] = "aggregateDuration";
    FilterType["AggregatePercentage"] = "aggregatePercentage";
    FilterType["AggregateNumeric"] = "aggregateNumeric";
    FilterType["AggregateDate"] = "aggregateDate";
    FilterType["AggregateRelativeDate"] = "aggregateRelativeDate";
    FilterType["Has"] = "has";
    FilterType["Is"] = "is";
})(FilterType || (FilterType = {}));
var allOperators = [
    TermOperator.Default,
    TermOperator.GreaterThanEqual,
    TermOperator.LessThanEqual,
    TermOperator.GreaterThan,
    TermOperator.LessThan,
    TermOperator.Equal,
    TermOperator.NotEqual,
];
var basicOperators = [TermOperator.Default, TermOperator.NotEqual];
/**
 * Map of certain filter types to other filter types with applicable operators
 * e.g. SpecificDate can use the operators from Date to become a Date filter.
 */
export var interchangeableFilterOperators = (_a = {},
    _a[FilterType.SpecificDate] = [FilterType.Date],
    _a[FilterType.Date] = [FilterType.SpecificDate],
    _a);
var textKeys = [Token.KeySimple, Token.KeyExplicitTag];
var numberUnits = {
    b: 1000000000,
    m: 1000000,
    k: 1000,
};
/**
 * This constant-type configuration object declares how each filter type
 * operates. Including what types of keys, operators, and values it may
 * recieve.
 *
 * This configuration is used to generate the discriminate Filter type that is
 * returned from the tokenFilter converter.
 */
export var filterTypeConfig = (_b = {},
    _b[FilterType.Text] = {
        validKeys: textKeys,
        validOps: basicOperators,
        validValues: [Token.ValueText],
        canNegate: true,
    },
    _b[FilterType.TextIn] = {
        validKeys: textKeys,
        validOps: [],
        validValues: [Token.ValueTextList],
        canNegate: true,
    },
    _b[FilterType.Date] = {
        validKeys: [Token.KeySimple],
        validOps: allOperators,
        validValues: [Token.ValueIso8601Date],
        canNegate: false,
    },
    _b[FilterType.SpecificDate] = {
        validKeys: [Token.KeySimple],
        validOps: [],
        validValues: [Token.ValueIso8601Date],
        canNegate: false,
    },
    _b[FilterType.RelativeDate] = {
        validKeys: [Token.KeySimple],
        validOps: [],
        validValues: [Token.ValueRelativeDate],
        canNegate: false,
    },
    _b[FilterType.Duration] = {
        validKeys: [Token.KeySimple],
        validOps: allOperators,
        validValues: [Token.ValueDuration],
        canNegate: false,
    },
    _b[FilterType.Numeric] = {
        validKeys: [Token.KeySimple],
        validOps: allOperators,
        validValues: [Token.ValueNumber],
        canNegate: false,
    },
    _b[FilterType.NumericIn] = {
        validKeys: [Token.KeySimple],
        validOps: [],
        validValues: [Token.ValueNumberList],
        canNegate: false,
    },
    _b[FilterType.Boolean] = {
        validKeys: [Token.KeySimple],
        validOps: basicOperators,
        validValues: [Token.ValueBoolean],
        canNegate: true,
    },
    _b[FilterType.AggregateDuration] = {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValueDuration],
        canNegate: true,
    },
    _b[FilterType.AggregateNumeric] = {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValueNumber],
        canNegate: true,
    },
    _b[FilterType.AggregatePercentage] = {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValuePercentage],
        canNegate: true,
    },
    _b[FilterType.AggregateDate] = {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValueIso8601Date],
        canNegate: true,
    },
    _b[FilterType.AggregateRelativeDate] = {
        validKeys: [Token.KeyAggregate],
        validOps: allOperators,
        validValues: [Token.ValueRelativeDate],
        canNegate: true,
    },
    _b[FilterType.Has] = {
        validKeys: [Token.KeySimple],
        validOps: basicOperators,
        validValues: [],
        canNegate: true,
    },
    _b[FilterType.Is] = {
        validKeys: [Token.KeySimple],
        validOps: basicOperators,
        validValues: [Token.ValueText],
        canNegate: true,
    },
    _b);
/**
 * Used to construct token results via the token grammar
 */
var TokenConverter = /** @class */ (function () {
    function TokenConverter(_a) {
        var _this = this;
        var text = _a.text, location = _a.location, config = _a.config;
        /**
         * Validates various types of keys
         */
        this.keyValidation = {
            isNumeric: function (key) { return _this.config.numericKeys.has(key) || isMeasurement(key); },
            isBoolean: function (key) { return _this.config.booleanKeys.has(key); },
            isPercentage: function (key) { return _this.config.percentageKeys.has(key); },
            isDate: function (key) { return _this.config.dateKeys.has(key); },
            isDuration: function (key) {
                return _this.config.durationKeys.has(key) ||
                    isSpanOperationBreakdownField(key) ||
                    measurementType(key) === 'duration';
            },
        };
        /**
         * Creates a token with common `text` and `location` keys.
         */
        this.makeToken = function (args) { return (__assign({ text: _this.text(), location: _this.location() }, args)); };
        this.tokenSpaces = function (value) {
            return _this.makeToken({
                type: Token.Spaces,
                value: value,
            });
        };
        this.tokenFilter = function (filter, key, value, operator, negated) {
            return _this.makeToken({
                type: Token.Filter,
                filter: filter,
                key: key,
                value: value,
                negated: negated,
                operator: operator !== null && operator !== void 0 ? operator : TermOperator.Default,
                invalid: _this.checkInvalidFilter(filter, key, value),
            });
        };
        this.tokenFreeText = function (value, quoted) {
            return _this.makeToken({
                type: Token.FreeText,
                value: value,
                quoted: quoted,
            });
        };
        this.tokenLogicGroup = function (inner) {
            return _this.makeToken({
                type: Token.LogicGroup,
                inner: inner,
            });
        };
        this.tokenLogicBoolean = function (bool) {
            return _this.makeToken({
                type: Token.LogicBoolean,
                value: bool,
            });
        };
        this.tokenKeySimple = function (value, quoted) {
            return _this.makeToken({
                type: Token.KeySimple,
                value: value,
                quoted: quoted,
            });
        };
        this.tokenKeyExplicitTag = function (prefix, key) {
            return _this.makeToken({
                type: Token.KeyExplicitTag,
                prefix: prefix,
                key: key,
            });
        };
        this.tokenKeyAggregate = function (name, args, argsSpaceBefore, argsSpaceAfter) {
            return _this.makeToken({
                type: Token.KeyAggregate,
                name: name,
                args: args,
                argsSpaceBefore: argsSpaceBefore,
                argsSpaceAfter: argsSpaceAfter,
            });
        };
        this.tokenKeyAggregateArgs = function (arg1, args) {
            return _this.makeToken({
                type: Token.KeyAggregateArgs,
                args: __spreadArray([{ separator: '', value: arg1 }], __read(args.map(listJoiner))),
            });
        };
        this.tokenValueIso8601Date = function (value) {
            return _this.makeToken({
                type: Token.ValueIso8601Date,
                value: moment(value),
            });
        };
        this.tokenValueRelativeDate = function (value, sign, unit) {
            return _this.makeToken({
                type: Token.ValueRelativeDate,
                value: Number(value),
                sign: sign,
                unit: unit,
            });
        };
        this.tokenValueDuration = function (value, unit) {
            return _this.makeToken({
                type: Token.ValueDuration,
                value: Number(value),
                unit: unit,
            });
        };
        this.tokenValuePercentage = function (value) {
            return _this.makeToken({
                type: Token.ValuePercentage,
                value: Number(value),
            });
        };
        this.tokenValueBoolean = function (value) {
            return _this.makeToken({
                type: Token.ValueBoolean,
                value: ['1', 'true'].includes(value.toLowerCase()),
            });
        };
        this.tokenValueNumber = function (value, unit) {
            var _a;
            return _this.makeToken({
                type: Token.ValueNumber,
                value: value,
                rawValue: Number(value) * ((_a = numberUnits[unit]) !== null && _a !== void 0 ? _a : 1),
                unit: unit,
            });
        };
        this.tokenValueNumberList = function (item1, items) {
            return _this.makeToken({
                type: Token.ValueNumberList,
                items: __spreadArray([{ separator: '', value: item1 }], __read(items.map(listJoiner))),
            });
        };
        this.tokenValueTextList = function (item1, items) {
            return _this.makeToken({
                type: Token.ValueTextList,
                items: __spreadArray([{ separator: '', value: item1 }], __read(items.map(listJoiner))),
            });
        };
        this.tokenValueText = function (value, quoted) {
            return _this.makeToken({
                type: Token.ValueText,
                value: value,
                quoted: quoted,
            });
        };
        /**
         * This method is used while tokenizing to predicate whether a filter should
         * match or not. We do this because not all keys are valid for specific
         * filter types. For example, boolean filters should only match for keys
         * which can be filtered as booleans.
         *
         * See [0] and look for &{ predicate } to understand how predicates are
         * declared in the grammar
         *
         * [0]:https://pegjs.org/documentation
         */
        this.predicateFilter = function (type, key) {
            var _a, _b, _c;
            var keyName = getKeyName(key);
            var aggregateKey = key;
            var _d = _this.keyValidation, isNumeric = _d.isNumeric, isDuration = _d.isDuration, isBoolean = _d.isBoolean, isDate = _d.isDate, isPercentage = _d.isPercentage;
            switch (type) {
                case FilterType.Numeric:
                case FilterType.NumericIn:
                    return isNumeric(keyName);
                case FilterType.Duration:
                    return isDuration(keyName);
                case FilterType.Boolean:
                    return isBoolean(keyName);
                case FilterType.Date:
                case FilterType.RelativeDate:
                case FilterType.SpecificDate:
                    return isDate(keyName);
                case FilterType.AggregateDuration:
                    return (_a = aggregateKey.args) === null || _a === void 0 ? void 0 : _a.args.some(function (arg) { return isDuration(arg.value.value); });
                case FilterType.AggregateDate:
                    return (_b = aggregateKey.args) === null || _b === void 0 ? void 0 : _b.args.some(function (arg) { return isDate(arg.value.value); });
                case FilterType.AggregatePercentage:
                    return (_c = aggregateKey.args) === null || _c === void 0 ? void 0 : _c.args.some(function (arg) { return isPercentage(arg.value.value); });
                default:
                    return true;
            }
        };
        /**
         * Predicates weather a text filter have operators for specific keys.
         */
        this.predicateTextOperator = function (key) {
            return _this.config.textOperatorKeys.has(getKeyName(key));
        };
        /**
         * Checks a filter against some non-grammar validation rules
         */
        this.checkInvalidFilter = function (filter, key, value) {
            // Only text filters may currently be invalid, since the text filter is the
            // "fall through" filter that will match when other filter predicates fail.
            if (filter !== FilterType.Text) {
                return null;
            }
            return _this.checkInvalidTextFilter(key, value);
        };
        /**
         * Validates text filters which may have failed predication
         */
        this.checkInvalidTextFilter = function (key, value) {
            // Explicit tag keys will always be treated as text filters
            if (key.type === Token.KeyExplicitTag) {
                return _this.checkInvalidTextValue(value);
            }
            var keyName = getKeyName(key);
            if (_this.keyValidation.isDuration(keyName)) {
                return {
                    reason: t('Invalid duration. Expected number followed by duration unit suffix'),
                    expectedType: [FilterType.Duration],
                };
            }
            if (_this.keyValidation.isDate(keyName)) {
                return {
                    reason: t('Invalid date format. Expected +/-duration (e.g. +1h) or ISO 8601-like (e.g. {now})', new Date().toISOString()),
                    expectedType: [FilterType.Date, FilterType.SpecificDate, FilterType.RelativeDate],
                };
            }
            if (_this.keyValidation.isBoolean(keyName)) {
                return {
                    reason: t('Invalid boolean. Expected true, 1, false, or 0.'),
                    expectedType: [FilterType.Boolean],
                };
            }
            if (_this.keyValidation.isNumeric(keyName)) {
                return {
                    reason: t('Invalid number. Expected number then optional k, m, or b suffix (e.g. 500k)'),
                    expectedType: [FilterType.Numeric, FilterType.NumericIn],
                };
            }
            return _this.checkInvalidTextValue(value);
        };
        /**
         * Validates the value of a text filter
         */
        this.checkInvalidTextValue = function (value) {
            if (!value.quoted && /(^|[^\\])"/.test(value.value)) {
                return { reason: t('Quotes must enclose text or be escaped') };
            }
            if (!value.quoted && value.value === '') {
                return { reason: t('Filter must have a value') };
            }
            return null;
        };
        this.text = text;
        this.location = location;
        this.config = config;
    }
    return TokenConverter;
}());
export { TokenConverter };
var defaultConfig = {
    textOperatorKeys: new Set(['sentry.semver']),
    durationKeys: new Set(['transaction.duration']),
    percentageKeys: new Set(['percentage']),
    numericKeys: new Set([
        'project_id',
        'project.id',
        'issue.id',
        'stack.colno',
        'stack.lineno',
        'stack.stack_level',
        'transaction.duration',
        'apdex',
        'p75',
        'p95',
        'p99',
        'failure_rate',
        'count_miserable',
        'user_misery',
        'count_miserable_new',
        'user_miser_new',
    ]),
    dateKeys: new Set([
        'start',
        'end',
        'first_seen',
        'last_seen',
        'time',
        'event.timestamp',
        'timestamp',
        'timestamp.to_hour',
        'timestamp.to_day',
        'transaction.start_time',
        'transaction.end_time',
    ]),
    booleanKeys: new Set([
        'error.handled',
        'error.unhandled',
        'stack.in_app',
        'key_transaction',
        'team_key_transaction',
    ]),
    allowBoolean: true,
};
var options = {
    TokenConverter: TokenConverter,
    TermOperator: TermOperator,
    FilterType: FilterType,
    config: defaultConfig,
};
/**
 * Parse a search query into a ParseResult. Failing to parse the search query
 * will result in null.
 */
export function parseSearch(query) {
    try {
        return grammar.parse(query, options);
    }
    catch (e) {
        // TODO(epurkhiser): Should we capture these errors somewhere?
    }
    return null;
}
//# sourceMappingURL=parser.jsx.map