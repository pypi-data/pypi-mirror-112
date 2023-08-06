import { __awaiter, __generator, __read, __spreadArray } from "tslib";
import isEqual from 'lodash/isEqual';
import pick from 'lodash/pick';
import { action, computed, makeObservable, observable } from 'mobx';
import { Client } from 'app/api';
import { createFuzzySearch } from 'app/utils/createFuzzySearch';
import { noFilter, toggleAllFilters, toggleFilter } from './filter';
import SpanTreeModel from './spanTreeModel';
import { boundsGenerator, generateRootSpan, getSpanID, parseTrace } from './utils';
var WaterfallModel = /** @class */ (function () {
    function WaterfallModel(event) {
        var _this = this;
        this.api = new Client();
        this.fuse = undefined;
        // readable/writable state
        this.operationNameFilters = noFilter;
        this.filterSpans = undefined;
        this.searchQuery = undefined;
        this.toggleOperationNameFilter = function (operationName) {
            _this.operationNameFilters = toggleFilter(_this.operationNameFilters, operationName);
        };
        this.toggleAllOperationNameFilters = function () {
            var operationNames = Array.from(_this.operationNameCounts.keys());
            _this.operationNameFilters = toggleAllFilters(_this.operationNameFilters, operationNames);
        };
        this.toggleSpanGroup = function (spanID) {
            if (_this.hiddenSpanGroups.has(spanID)) {
                _this.hiddenSpanGroups.delete(spanID);
                return;
            }
            _this.hiddenSpanGroups.add(spanID);
        };
        this.generateBounds = function (_a) {
            var viewStart = _a.viewStart, viewEnd = _a.viewEnd;
            return boundsGenerator({
                traceStartTimestamp: _this.parsedTrace.traceStartTimestamp,
                traceEndTimestamp: _this.parsedTrace.traceEndTimestamp,
                viewStart: viewStart,
                viewEnd: viewEnd,
            });
        };
        this.getWaterfall = function (_a) {
            var viewStart = _a.viewStart, viewEnd = _a.viewEnd;
            var generateBounds = _this.generateBounds({
                viewStart: viewStart,
                viewEnd: viewEnd,
            });
            return _this.rootSpan.getSpansList({
                operationNameFilters: _this.operationNameFilters,
                generateBounds: generateBounds,
                treeDepth: 0,
                isLastSibling: true,
                continuingTreeDepths: [],
                hiddenSpanGroups: _this.hiddenSpanGroups,
                spanGroups: new Set(),
                filterSpans: _this.filterSpans,
                previousSiblingEndTimestamp: undefined,
                event: _this.event,
            });
        };
        this.event = event;
        this.parsedTrace = parseTrace(event);
        var rootSpan = generateRootSpan(this.parsedTrace);
        this.rootSpan = new SpanTreeModel(rootSpan, this.parsedTrace.childSpans, this.api, true);
        this.indexSearch(this.parsedTrace, rootSpan);
        // Set of span IDs whose sub-trees should be hidden. This is used for the
        // span tree toggling product feature.
        this.hiddenSpanGroups = new Set();
        makeObservable(this, {
            rootSpan: observable,
            // operation names filtering
            operationNameFilters: observable,
            toggleOperationNameFilter: action,
            toggleAllOperationNameFilters: action,
            operationNameCounts: computed.struct,
            // span search
            filterSpans: observable,
            searchQuery: observable,
            querySpanSearch: action,
            // span group toggling
            hiddenSpanGroups: observable,
            toggleSpanGroup: action,
        });
    }
    WaterfallModel.prototype.isEvent = function (otherEvent) {
        return isEqual(this.event, otherEvent);
    };
    Object.defineProperty(WaterfallModel.prototype, "operationNameCounts", {
        get: function () {
            return this.rootSpan.operationNameCounts;
        },
        enumerable: false,
        configurable: true
    });
    WaterfallModel.prototype.indexSearch = function (parsedTrace, rootSpan) {
        return __awaiter(this, void 0, void 0, function () {
            var spans, transformed, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.filterSpans = undefined;
                        this.searchQuery = undefined;
                        spans = parsedTrace.spans;
                        transformed = __spreadArray([rootSpan], __read(spans)).map(function (span) {
                            var _a;
                            var indexed = [];
                            // basic properties
                            var pickedSpan = pick(span, [
                                // TODO: do we want this?
                                // 'trace_id',
                                'span_id',
                                'start_timestamp',
                                'timestamp',
                                'op',
                                'description',
                            ]);
                            var basicValues = Object.values(pickedSpan)
                                .filter(function (value) { return !!value; })
                                .map(function (value) { return String(value); });
                            indexed.push.apply(indexed, __spreadArray([], __read(basicValues)));
                            // tags
                            var tagKeys = [];
                            var tagValues = [];
                            var tags = span === null || span === void 0 ? void 0 : span.tags;
                            if (tags) {
                                tagKeys = Object.keys(tags);
                                tagValues = Object.values(tags);
                            }
                            var data = (_a = span === null || span === void 0 ? void 0 : span.data) !== null && _a !== void 0 ? _a : {};
                            var dataKeys = [];
                            var dataValues = [];
                            if (data) {
                                dataKeys = Object.keys(data);
                                dataValues = Object.values(data).map(function (value) { return JSON.stringify(value, null, 4) || ''; });
                            }
                            return {
                                span: span,
                                indexed: indexed,
                                tagKeys: tagKeys,
                                tagValues: tagValues,
                                dataKeys: dataKeys,
                                dataValues: dataValues,
                            };
                        });
                        _a = this;
                        return [4 /*yield*/, createFuzzySearch(transformed, {
                                keys: ['indexed', 'tagKeys', 'tagValues', 'dataKeys', 'dataValues'],
                                includeMatches: false,
                                threshold: 0.6,
                                location: 0,
                                distance: 100,
                                maxPatternLength: 32,
                            })];
                    case 1:
                        _a.fuse = _b.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    WaterfallModel.prototype.querySpanSearch = function (searchQuery) {
        if (!searchQuery) {
            // reset
            if (this.filterSpans !== undefined) {
                this.filterSpans = undefined;
                this.searchQuery = undefined;
            }
            return;
        }
        if (!this.fuse) {
            return;
        }
        var results = this.fuse.search(searchQuery);
        var spanIDs = results.reduce(function (setOfSpanIDs, result) {
            var spanID = getSpanID(result.item.span);
            if (spanID) {
                setOfSpanIDs.add(spanID);
            }
            return setOfSpanIDs;
        }, new Set());
        this.searchQuery = searchQuery;
        this.filterSpans = {
            results: results,
            spanIDs: spanIDs,
        };
    };
    return WaterfallModel;
}());
export default WaterfallModel;
//# sourceMappingURL=waterfallModel.jsx.map