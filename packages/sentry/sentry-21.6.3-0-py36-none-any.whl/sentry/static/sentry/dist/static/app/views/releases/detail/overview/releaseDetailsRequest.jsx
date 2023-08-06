import { __assign, __awaiter, __extends, __generator, __read } from "tslib";
import * as React from 'react';
import isEqual from 'lodash/isEqual';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { t } from 'app/locale';
import { getSessionsInterval } from 'app/utils/sessions';
import withApi from 'app/utils/withApi';
import { getReleaseParams } from '../../utils';
var ReleaseDetailsRequest = /** @class */ (function (_super) {
    __extends(ReleaseDetailsRequest, _super);
    function ReleaseDetailsRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            reloading: false,
            errored: false,
            thisRelease: null,
            allReleases: null,
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, disable, promises, _b, thisRelease, allReleases, error_1;
            var _c, _d;
            return __generator(this, function (_e) {
                switch (_e.label) {
                    case 0:
                        _a = this.props, api = _a.api, disable = _a.disable;
                        if (disable) {
                            return [2 /*return*/];
                        }
                        api.clear();
                        this.setState(function (state) { return ({
                            reloading: state.thisRelease !== null && state.allReleases !== null,
                            errored: false,
                        }); });
                        promises = [this.fetchThisRelease(), this.fetchAllReleases()];
                        _e.label = 1;
                    case 1:
                        _e.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, Promise.all(promises)];
                    case 2:
                        _b = __read.apply(void 0, [_e.sent(), 2]), thisRelease = _b[0], allReleases = _b[1];
                        this.setState({
                            reloading: false,
                            thisRelease: thisRelease,
                            allReleases: allReleases,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _e.sent();
                        addErrorMessage((_d = (_c = error_1.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) !== null && _d !== void 0 ? _d : t('Error loading health data'));
                        this.setState({
                            reloading: false,
                            errored: true,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ReleaseDetailsRequest.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ReleaseDetailsRequest.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.version !== this.props.version ||
            !isEqual(prevProps.location, this.props.location)) {
            this.fetchData();
        }
    };
    Object.defineProperty(ReleaseDetailsRequest.prototype, "path", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/sessions/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ReleaseDetailsRequest.prototype, "baseQueryParams", {
        get: function () {
            var _a;
            var _b = this.props, location = _b.location, releaseBounds = _b.releaseBounds, organization = _b.organization;
            var releaseParams = getReleaseParams({
                location: location,
                releaseBounds: releaseBounds,
                defaultStatsPeriod: DEFAULT_STATS_PERIOD,
                allowEmptyPeriod: true,
            });
            return __assign({ field: ['count_unique(user)', 'sum(session)'], groupBy: ['session.status'], interval: getSessionsInterval({
                    start: releaseParams.start,
                    end: releaseParams.end,
                    period: (_a = releaseParams.statsPeriod) !== null && _a !== void 0 ? _a : undefined,
                }, { highFidelity: organization.features.includes('minute-resolution-sessions') }) }, releaseParams);
        },
        enumerable: false,
        configurable: true
    });
    ReleaseDetailsRequest.prototype.fetchThisRelease = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, version, response;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, version = _a.version;
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: __assign(__assign({}, this.baseQueryParams), { query: "release:" + version }),
                            })];
                    case 1:
                        response = _b.sent();
                        return [2 /*return*/, response];
                }
            });
        });
    };
    ReleaseDetailsRequest.prototype.fetchAllReleases = function () {
        return __awaiter(this, void 0, void 0, function () {
            var api, response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        api = this.props.api;
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: this.baseQueryParams,
                            })];
                    case 1:
                        response = _a.sent();
                        return [2 /*return*/, response];
                }
            });
        });
    };
    ReleaseDetailsRequest.prototype.render = function () {
        var _a = this.state, reloading = _a.reloading, errored = _a.errored, thisRelease = _a.thisRelease, allReleases = _a.allReleases;
        var children = this.props.children;
        var loading = thisRelease === null && allReleases === null;
        return children({
            loading: loading,
            reloading: reloading,
            errored: errored,
            thisRelease: thisRelease,
            allReleases: allReleases,
        });
    };
    return ReleaseDetailsRequest;
}(React.Component));
export default withApi(ReleaseDetailsRequest);
//# sourceMappingURL=releaseDetailsRequest.jsx.map