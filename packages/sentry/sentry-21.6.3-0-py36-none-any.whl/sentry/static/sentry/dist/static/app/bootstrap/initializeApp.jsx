import { __awaiter, __generator } from "tslib";
import 'bootstrap/js/alert';
import 'bootstrap/js/tab';
import 'bootstrap/js/dropdown';
import './exportGlobals';
import routes from 'app/routes';
import { metric } from 'app/utils/analytics';
import { commonInitialization } from './commonInitialization';
import { initializeSdk } from './initializeSdk';
import { processInitQueue } from './processInitQueue';
import { renderMain } from './renderMain';
import { renderOnDomReady } from './renderOnDomReady';
export function initializeApp(config) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            commonInitialization(config);
            initializeSdk(config, { routes: routes });
            // Used for operational metrics to determine that the application js
            // bundle was loaded by browser.
            metric.mark({ name: 'sentry-app-init' });
            renderOnDomReady(renderMain);
            processInitQueue();
            return [2 /*return*/];
        });
    });
}
//# sourceMappingURL=initializeApp.jsx.map