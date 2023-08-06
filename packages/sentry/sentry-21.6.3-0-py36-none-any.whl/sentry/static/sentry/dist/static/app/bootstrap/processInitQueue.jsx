var _a;
import { __awaiter, __generator } from "tslib";
import exportGlobals from 'app/bootstrap/exportGlobals';
import { SentryInitRenderReactComponent } from 'app/types';
import { renderDom } from './renderDom';
import { renderOnDomReady } from './renderOnDomReady';
var COMPONENT_MAP = (_a = {},
    _a[SentryInitRenderReactComponent.INDICATORS] = function () {
        return import(/* webpackChunkName: "Indicators" */ 'app/components/indicators');
    },
    _a[SentryInitRenderReactComponent.SYSTEM_ALERTS] = function () {
        return import(/* webpackChunkName: "SystemAlerts" */ 'app/views/app/systemAlerts');
    },
    _a[SentryInitRenderReactComponent.SETUP_WIZARD] = function () {
        return import(/* webpackChunkName: "SetupWizard" */ 'app/views/setupWizard');
    },
    _a[SentryInitRenderReactComponent.U2F_SIGN] = function () {
        return import(/* webpackChunkName: "U2fSign" */ 'app/components/u2f/u2fsign');
    },
    _a);
function processItem(initConfig) {
    return __awaiter(this, void 0, void 0, function () {
        var input, element, passwordStrength, Component_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (!(initConfig.name === 'passwordStrength')) return [3 /*break*/, 2];
                    input = initConfig.input, element = initConfig.element;
                    if (!input || !element) {
                        return [2 /*return*/];
                    }
                    return [4 /*yield*/, import(
                        /* webpackChunkName: "PasswordStrength" */ 'app/components/passwordStrength')];
                case 1:
                    passwordStrength = _a.sent();
                    passwordStrength.attachTo({
                        input: document.querySelector(input),
                        element: document.querySelector(element),
                    });
                    return [2 /*return*/];
                case 2:
                    if (!(initConfig.name === 'renderReact')) return [3 /*break*/, 4];
                    if (!COMPONENT_MAP.hasOwnProperty(initConfig.component)) {
                        return [2 /*return*/];
                    }
                    return [4 /*yield*/, COMPONENT_MAP[initConfig.component]()];
                case 3:
                    Component_1 = (_a.sent()).default;
                    renderOnDomReady(function () {
                        // TODO(ts): Unsure how to type this, complains about u2fsign's required props
                        return renderDom(Component_1, initConfig.container, initConfig.props);
                    });
                    _a.label = 4;
                case 4:
                    /**
                     * Callback for when js bundle is loaded. Provide library + component references
                     * for downstream consumers to use.
                     */
                    if (initConfig.name === 'onReady' && typeof initConfig.onReady === 'function') {
                        initConfig.onReady(exportGlobals);
                    }
                    return [2 /*return*/];
            }
        });
    });
}
/**
 * This allows server templates to push "tasks" to be run after application has initialized.
 * The global `window.__onSentryInit` is used for this.
 *
 * Be careful here as we can not guarantee type safety on `__onSentryInit` as
 * these will be defined in server rendered templates
 */
export function processInitQueue() {
    return __awaiter(this, void 0, void 0, function () {
        var queued;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    // Currently, this is run *before* anything is queued in
                    // `window.__onSentryInit`. We want to provide a migration path for potential
                    // custom plugins that rely on `window.SentryApp` so they can start migrating
                    // their plugins ASAP, as `SentryApp` will be loaded async and will require
                    // callbacks to access it, instead of via `window` global.
                    if (typeof window.__onSentryInit !== 'undefined' &&
                        !Array.isArray(window.__onSentryInit)) {
                        return [2 /*return*/];
                    }
                    queued = window.__onSentryInit;
                    // Stub future calls of `window.__onSentryInit.push` so that it is
                    // processed immediately (since bundle is loaded at this point and no
                    // longer needs to act as a queue)
                    //
                    window.__onSentryInit = {
                        push: processItem,
                    };
                    if (!Array.isArray(queued)) return [3 /*break*/, 2];
                    // These are all side-effects, so no need to return a value, but allow consumer to
                    // wait for all initialization to finish
                    return [4 /*yield*/, Promise.all(queued.map(processItem))];
                case 1:
                    // These are all side-effects, so no need to return a value, but allow consumer to
                    // wait for all initialization to finish
                    _a.sent();
                    _a.label = 2;
                case 2: return [2 /*return*/];
            }
        });
    });
}
//# sourceMappingURL=processInitQueue.jsx.map