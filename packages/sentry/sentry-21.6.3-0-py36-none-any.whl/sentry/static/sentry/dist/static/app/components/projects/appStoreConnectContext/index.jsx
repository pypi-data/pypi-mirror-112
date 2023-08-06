import { __assign, __awaiter, __generator, __read } from "tslib";
import { createContext, useEffect, useState } from 'react';
import withApi from 'app/utils/withApi';
var AppStoreConnectContext = createContext(undefined);
import { getAppConnectStoreUpdateAlertMessage } from './utils';
var Provider = withApi(function (_a) {
    var _b;
    var api = _a.api, children = _a.children, project = _a.project, organization = _a.organization;
    var _c = __read(useState(), 2), projectDetails = _c[0], setProjectDetails = _c[1];
    var _d = __read(useState(undefined), 2), appStoreConnectValidationData = _d[0], setAppStoreConnectValidationData = _d[1];
    var orgSlug = organization.slug;
    var hasAppConnectStoreFeatureFlag = !!((_b = organization.features) === null || _b === void 0 ? void 0 : _b.includes('app-store-connect'));
    useEffect(function () {
        fetchProjectDetails();
    }, [project]);
    useEffect(function () {
        fetchAppStoreConnectValidationData();
    }, [projectDetails]);
    function fetchProjectDetails() {
        return __awaiter(this, void 0, void 0, function () {
            var response, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (!hasAppConnectStoreFeatureFlag || !project || projectDetails) {
                            return [2 /*return*/];
                        }
                        if (project.symbolSources) {
                            setProjectDetails(project);
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + project.slug + "/")];
                    case 2:
                        response = _b.sent();
                        setProjectDetails(response);
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function getAppStoreConnectSymbolSourceId(symbolSources) {
        var _a;
        return (_a = (symbolSources ? JSON.parse(symbolSources) : []).find(function (symbolSource) { return symbolSource.type.toLowerCase() === 'appstoreconnect'; })) === null || _a === void 0 ? void 0 : _a.id;
    }
    function fetchAppStoreConnectValidationData() {
        return __awaiter(this, void 0, void 0, function () {
            var appStoreConnectSymbolSourceId, response, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (!projectDetails) {
                            return [2 /*return*/];
                        }
                        appStoreConnectSymbolSourceId = getAppStoreConnectSymbolSourceId(projectDetails.symbolSources);
                        if (!appStoreConnectSymbolSourceId) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectDetails.slug + "/appstoreconnect/validate/" + appStoreConnectSymbolSourceId + "/")];
                    case 2:
                        response = _b.sent();
                        setAppStoreConnectValidationData(__assign({ id: appStoreConnectSymbolSourceId }, response));
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    return (<AppStoreConnectContext.Provider value={appStoreConnectValidationData
            ? __assign(__assign({}, appStoreConnectValidationData), { updateAlertMessage: getAppConnectStoreUpdateAlertMessage(appStoreConnectValidationData) }) : undefined}>
      {children}
    </AppStoreConnectContext.Provider>);
});
var Consumer = AppStoreConnectContext.Consumer;
export { Provider, Consumer };
export default AppStoreConnectContext;
//# sourceMappingURL=index.jsx.map