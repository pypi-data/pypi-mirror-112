import { __assign, __read, __spreadArray, __values } from "tslib";
import { action, computed, makeObservable, observable } from 'mobx';
import { t } from 'app/locale';
import { generateRootSpan, getSpanID, getSpanOperation, isEventFromBrowserJavaScriptSDK, isOrphanSpan, parseTrace, } from './utils';
var SpanTreeModel = /** @class */ (function () {
    function SpanTreeModel(parentSpan, childSpans, api, isRoot) {
        var _this = this;
        if (isRoot === void 0) { isRoot = false; }
        var _a;
        this.children = [];
        // readable/writable state
        this.fetchEmbeddedChildrenState = 'idle';
        this.showEmbeddedChildren = false;
        this.embeddedChildren = [];
        this.isSpanFilteredOut = function (props) {
            var operationNameFilters = props.operationNameFilters, filterSpans = props.filterSpans;
            if (operationNameFilters.type === 'active_filter') {
                var operationName = getSpanOperation(_this.span);
                if (typeof operationName === 'string' &&
                    !operationNameFilters.operationNames.has(operationName)) {
                    return true;
                }
            }
            if (!filterSpans) {
                return false;
            }
            return !filterSpans.spanIDs.has(getSpanID(_this.span));
        };
        this.getSpansList = function (props) {
            var e_1, _a;
            var operationNameFilters = props.operationNameFilters, generateBounds = props.generateBounds, treeDepth = props.treeDepth, isLastSibling = props.isLastSibling, continuingTreeDepths = props.continuingTreeDepths, hiddenSpanGroups = props.hiddenSpanGroups, 
            // The set of ancestor span IDs whose sub-tree that the span belongs to
            spanGroups = props.spanGroups, filterSpans = props.filterSpans, previousSiblingEndTimestamp = props.previousSiblingEndTimestamp, event = props.event;
            var treeDepthEntry = isOrphanSpan(_this.span)
                ? { type: 'orphan', depth: treeDepth }
                : treeDepth;
            var descendantContinuingTreeDepths = isLastSibling
                ? continuingTreeDepths
                : __spreadArray(__spreadArray([], __read(continuingTreeDepths)), [treeDepthEntry]);
            var parentSpanID = getSpanID(_this.span);
            var childSpanGroup = new Set(spanGroups);
            childSpanGroup.add(parentSpanID);
            var descendantsSource = _this.showEmbeddedChildren
                ? __spreadArray(__spreadArray([], __read(_this.embeddedChildren)), __read(_this.children)) : _this.children;
            var lastIndex = descendantsSource.length - 1;
            var descendants = descendantsSource.reduce(function (acc, span, index) {
                var _a;
                (_a = acc.descendants).push.apply(_a, __spreadArray([], __read(span.getSpansList({
                    operationNameFilters: operationNameFilters,
                    generateBounds: generateBounds,
                    treeDepth: treeDepth + 1,
                    isLastSibling: index === lastIndex,
                    continuingTreeDepths: descendantContinuingTreeDepths,
                    hiddenSpanGroups: hiddenSpanGroups,
                    spanGroups: new Set(childSpanGroup),
                    filterSpans: filterSpans,
                    previousSiblingEndTimestamp: acc.previousSiblingEndTimestamp,
                    event: event,
                }))));
                acc.previousSiblingEndTimestamp = span.span.timestamp;
                return acc;
            }, {
                descendants: [],
                previousSiblingEndTimestamp: undefined,
            }).descendants;
            try {
                for (var hiddenSpanGroups_1 = __values(hiddenSpanGroups), hiddenSpanGroups_1_1 = hiddenSpanGroups_1.next(); !hiddenSpanGroups_1_1.done; hiddenSpanGroups_1_1 = hiddenSpanGroups_1.next()) {
                    var hiddenSpanGroup = hiddenSpanGroups_1_1.value;
                    if (spanGroups.has(hiddenSpanGroup)) {
                        return descendants;
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (hiddenSpanGroups_1_1 && !hiddenSpanGroups_1_1.done && (_a = hiddenSpanGroups_1.return)) _a.call(hiddenSpanGroups_1);
                }
                finally { if (e_1) throw e_1.error; }
            }
            if (_this.isSpanFilteredOut(props)) {
                return __spreadArray([
                    {
                        type: 'filtered_out',
                        span: _this.span,
                    }
                ], __read(descendants));
            }
            var bounds = generateBounds({
                startTimestamp: _this.span.start_timestamp,
                endTimestamp: _this.span.timestamp,
            });
            var isCurrentSpanOutOfView = !bounds.isSpanVisibleInView;
            if (isCurrentSpanOutOfView) {
                return __spreadArray([
                    {
                        type: 'out_of_view',
                        span: _this.span,
                    }
                ], __read(descendants));
            }
            var wrappedSpan = {
                type: _this.isRoot ? 'root_span' : 'span',
                span: _this.span,
                numOfSpanChildren: descendantsSource.length,
                treeDepth: treeDepth,
                isLastSibling: isLastSibling,
                continuingTreeDepths: continuingTreeDepths,
                fetchEmbeddedChildrenState: _this.fetchEmbeddedChildrenState,
                showEmbeddedChildren: _this.showEmbeddedChildren,
                toggleEmbeddedChildren: _this.toggleEmbeddedChildren,
            };
            var gapSpan = _this.generateSpanGap(event, previousSiblingEndTimestamp, treeDepth, continuingTreeDepths);
            if (gapSpan) {
                return __spreadArray([gapSpan, wrappedSpan], __read(descendants));
            }
            return __spreadArray([wrappedSpan], __read(descendants));
        };
        this.toggleEmbeddedChildren = function (props) {
            _this.showEmbeddedChildren = !_this.showEmbeddedChildren;
            _this.fetchEmbeddedChildrenState = 'idle';
            if (_this.showEmbeddedChildren && _this.embeddedChildren.length === 0) {
                return _this.fetchEmbeddedTransactions(props);
            }
            return Promise.resolve(undefined);
        };
        this.api = api;
        this.span = parentSpan;
        this.isRoot = isRoot;
        var spanID = getSpanID(parentSpan);
        var spanChildren = (_a = childSpans === null || childSpans === void 0 ? void 0 : childSpans[spanID]) !== null && _a !== void 0 ? _a : [];
        // Mark descendents as being rendered. This is to address potential recursion issues due to malformed data.
        // For example if a span has a span_id that's identical to its parent_span_id.
        childSpans = __assign({}, childSpans);
        delete childSpans[spanID];
        this.children = spanChildren.map(function (span) {
            return new SpanTreeModel(span, childSpans, api);
        });
        makeObservable(this, {
            operationNameCounts: computed.struct,
            showEmbeddedChildren: observable,
            embeddedChildren: observable,
            fetchEmbeddedChildrenState: observable,
            toggleEmbeddedChildren: action,
            fetchEmbeddedTransactions: action,
        });
    }
    Object.defineProperty(SpanTreeModel.prototype, "operationNameCounts", {
        get: function () {
            var e_2, _a, e_3, _b;
            var _c;
            var result = new Map();
            var operationName = this.span.op;
            if (typeof operationName === 'string' && operationName.length > 0) {
                result.set(operationName, 1);
            }
            try {
                for (var _d = __values(this.children), _e = _d.next(); !_e.done; _e = _d.next()) {
                    var directChild = _e.value;
                    var operationNameCounts = directChild.operationNameCounts;
                    try {
                        for (var operationNameCounts_1 = (e_3 = void 0, __values(operationNameCounts)), operationNameCounts_1_1 = operationNameCounts_1.next(); !operationNameCounts_1_1.done; operationNameCounts_1_1 = operationNameCounts_1.next()) {
                            var _f = __read(operationNameCounts_1_1.value, 2), key = _f[0], count = _f[1];
                            result.set(key, ((_c = result.get(key)) !== null && _c !== void 0 ? _c : 0) + count);
                        }
                    }
                    catch (e_3_1) { e_3 = { error: e_3_1 }; }
                    finally {
                        try {
                            if (operationNameCounts_1_1 && !operationNameCounts_1_1.done && (_b = operationNameCounts_1.return)) _b.call(operationNameCounts_1);
                        }
                        finally { if (e_3) throw e_3.error; }
                    }
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (_e && !_e.done && (_a = _d.return)) _a.call(_d);
                }
                finally { if (e_2) throw e_2.error; }
            }
            // sort alphabetically using case insensitive comparison
            return new Map(__spreadArray([], __read(result)).sort(function (a, b) {
                return String(a[0]).localeCompare(b[0], undefined, { sensitivity: 'base' });
            }));
        },
        enumerable: false,
        configurable: true
    });
    SpanTreeModel.prototype.generateSpanGap = function (event, previousSiblingEndTimestamp, treeDepth, continuingTreeDepths) {
        // hide gap spans (i.e. "missing instrumentation" spans) for browser js transactions,
        // since they're not useful to indicate
        var shouldIncludeGap = !isEventFromBrowserJavaScriptSDK(event);
        var isValidGap = shouldIncludeGap &&
            typeof previousSiblingEndTimestamp === 'number' &&
            previousSiblingEndTimestamp < this.span.start_timestamp &&
            // gap is at least 100 ms
            this.span.start_timestamp - previousSiblingEndTimestamp >= 0.1;
        if (!isValidGap) {
            return undefined;
        }
        var gapSpan = {
            type: 'gap',
            span: {
                type: 'gap',
                start_timestamp: previousSiblingEndTimestamp || this.span.start_timestamp,
                timestamp: this.span.start_timestamp,
                description: t('Missing instrumentation'),
                isOrphan: isOrphanSpan(this.span),
            },
            numOfSpanChildren: 0,
            treeDepth: treeDepth,
            isLastSibling: false,
            continuingTreeDepths: continuingTreeDepths,
            fetchEmbeddedChildrenState: 'idle',
            showEmbeddedChildren: false,
            toggleEmbeddedChildren: undefined,
        };
        return gapSpan;
    };
    SpanTreeModel.prototype.fetchEmbeddedTransactions = function (_a) {
        var _this = this;
        var orgSlug = _a.orgSlug, eventSlug = _a.eventSlug;
        var url = "/organizations/" + orgSlug + "/events/" + eventSlug + "/";
        this.fetchEmbeddedChildrenState = 'loading_embedded_transactions';
        return this.api
            .requestPromise(url, {
            method: 'GET',
            query: {},
        })
            .then(action('fetchEmbeddedTransactionsSuccess', function (event) {
            if (!event) {
                return;
            }
            var parsedTrace = parseTrace(event);
            var rootSpan = generateRootSpan(parsedTrace);
            var parsedRootSpan = new SpanTreeModel(rootSpan, parsedTrace.childSpans, _this.api, false);
            _this.embeddedChildren = [parsedRootSpan];
            _this.fetchEmbeddedChildrenState = 'idle';
        }))
            .catch(action('fetchEmbeddedTransactionsError', function () {
            _this.embeddedChildren = [];
            _this.fetchEmbeddedChildrenState = 'error_fetching_embedded_transactions';
        }));
    };
    return SpanTreeModel;
}());
export default SpanTreeModel;
//# sourceMappingURL=spanTreeModel.jsx.map