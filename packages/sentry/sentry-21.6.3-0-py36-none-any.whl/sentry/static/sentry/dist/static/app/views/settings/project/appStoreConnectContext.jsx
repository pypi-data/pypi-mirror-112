import { __assign, __awaiter, __generator, __read } from "tslib";
import { createContext, useEffect, useState } from 'react';
import withApi from 'app/utils/withApi';
import withProject from 'app/utils/withProject';
var AppStoreConnectContext = createContext(undefined);
var Provider = withApi(withProject(function (_a) {
    var api = _a.api, children = _a.children, project = _a.project, orgSlug = _a.orgSlug;
    var _b = __read(useState(), 2), appStoreConnectValidationData = _b[0], setAppStoreConnectValidationData = _b[1];
    useEffect(function () {
        fetchAppStoreConnectValidationData();
    }, [project]);
    function getAppStoreConnectSymbolSourceId() {
        var _a;
        return (_a = (project.symbolSources ? JSON.parse(project.symbolSources) : []).find(function (symbolSource) { return symbolSource.type.toLowerCase() === 'appstoreconnect'; })) === null || _a === void 0 ? void 0 : _a.id;
    }
    function fetchAppStoreConnectValidationData() {
        return __awaiter(this, void 0, void 0, function () {
            var appStoreConnectSymbolSourceId, response, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        appStoreConnectSymbolSourceId = getAppStoreConnectSymbolSourceId();
                        if (!appStoreConnectSymbolSourceId) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + project.slug + "/appstoreconnect/validate/" + appStoreConnectSymbolSourceId + "/")];
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
    return (<AppStoreConnectContext.Provider value={appStoreConnectValidationData}>
        {children}
      </AppStoreConnectContext.Provider>);
}));
var Consumer = AppStoreConnectContext.Consumer;
export { Provider, Consumer };
export default AppStoreConnectContext;
//# sourceMappingURL=appStoreConnectContext.jsx.map