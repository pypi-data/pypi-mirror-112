import { __awaiter, __generator } from "tslib";
var BOOTSTRAP_URL = '/api/client-config/';
var bootApplication = function (data) {
    window.csrfCookieName = data.csrfCookieName;
    return data;
};
function bootWithHydration() {
    return __awaiter(this, void 0, void 0, function () {
        var response, data;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, fetch(BOOTSTRAP_URL)];
                case 1:
                    response = _a.sent();
                    return [4 /*yield*/, response.json()];
                case 2:
                    data = _a.sent();
                    window.__initialData = data;
                    return [2 /*return*/, bootApplication(data)];
            }
        });
    });
}
export function bootstrap() {
    return __awaiter(this, void 0, void 0, function () {
        var bootstrapData;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    bootstrapData = window.__initialData;
                    if (!(bootstrapData === undefined)) return [3 /*break*/, 2];
                    return [4 /*yield*/, bootWithHydration()];
                case 1: return [2 /*return*/, _a.sent()];
                case 2: return [2 /*return*/, bootApplication(bootstrapData)];
            }
        });
    });
}
//# sourceMappingURL=index.jsx.map