import { __assign } from "tslib";
import moment from 'moment-timezone';
import Reflux from 'reflux';
var configStoreConfig = {
    // When the app is booted we will _immediately_ hydrate the config store,
    // effecively ensureing this is not empty.
    config: {},
    init: function () {
        this.config = {};
    },
    get: function (key) {
        return this.config[key];
    },
    set: function (key, value) {
        var _a, _b;
        this.config = __assign(__assign({}, this.config), (_a = {}, _a[key] = value, _a));
        this.trigger((_b = {}, _b[key] = value, _b));
    },
    /**
     * This is only called by media query listener so that we can control
     * the auto switching of color schemes without affecting manual toggle
     */
    updateTheme: function (theme) {
        var _a;
        if (((_a = this.config.user) === null || _a === void 0 ? void 0 : _a.options.theme) !== 'system') {
            return;
        }
        this.set('theme', theme);
    },
    getConfig: function () {
        return this.config;
    },
    loadInitialData: function (config) {
        var _a;
        var shouldUseDarkMode = ((_a = config.user) === null || _a === void 0 ? void 0 : _a.options.theme) === 'dark';
        this.config = __assign(__assign({}, config), { features: new Set(config.features || []), theme: shouldUseDarkMode ? 'dark' : 'light' });
        // TODO(dcramer): abstract this out of ConfigStore
        if (config.user) {
            config.user.permissions = new Set(config.user.permissions);
            moment.tz.setDefault(config.user.options.timezone);
        }
        this.trigger(config);
    },
};
var ConfigStore = Reflux.createStore(configStoreConfig);
export default ConfigStore;
//# sourceMappingURL=configStore.jsx.map