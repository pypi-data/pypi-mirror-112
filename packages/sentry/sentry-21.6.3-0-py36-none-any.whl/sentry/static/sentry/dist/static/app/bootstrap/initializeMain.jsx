import { __awaiter, __generator } from "tslib";
import { initializeLocale } from './initializeLocale';
export function initializeMain(config) {
    return __awaiter(this, void 0, void 0, function () {
        var initializeApp;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: 
                // This needs to be loaded as early as possible, or else the locale library can
                // throw an exception and prevent the application from being loaded.
                //
                // e.g. `app/constants` uses `t()` and is imported quite early
                return [4 /*yield*/, initializeLocale(config)];
                case 1:
                    // This needs to be loaded as early as possible, or else the locale library can
                    // throw an exception and prevent the application from being loaded.
                    //
                    // e.g. `app/constants` uses `t()` and is imported quite early
                    _a.sent();
                    return [4 /*yield*/, import('./initializeApp')];
                case 2:
                    initializeApp = (_a.sent()).initializeApp;
                    return [4 /*yield*/, initializeApp(config)];
                case 3:
                    _a.sent();
                    return [2 /*return*/];
            }
        });
    });
}
//# sourceMappingURL=initializeMain.jsx.map