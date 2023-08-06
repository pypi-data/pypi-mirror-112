import { __assign, __extends, __rest } from "tslib";
import { Component, Fragment } from 'react';
import { cache } from '@emotion/css';
import { CacheProvider, ThemeProvider } from '@emotion/react';
import { render } from '@testing-library/react';
import { lightTheme } from 'app/utils/theme';
function createProvider(contextDefs) {
    var _a;
    return _a = /** @class */ (function (_super) {
            __extends(ContextProvider, _super);
            function ContextProvider() {
                return _super !== null && _super.apply(this, arguments) || this;
            }
            ContextProvider.prototype.getChildContext = function () {
                return contextDefs.context;
            };
            ContextProvider.prototype.render = function () {
                return this.props.children;
            };
            return ContextProvider;
        }(Component)),
        _a.childContextTypes = contextDefs.childContextTypes,
        _a;
}
function makeAllTheProviders(context) {
    return function (_a) {
        var children = _a.children;
        var ContextProvider = context ? createProvider(context) : Fragment;
        return (<ContextProvider>
        <CacheProvider value={cache}>
          <ThemeProvider theme={lightTheme}>{children}</ThemeProvider>
        </CacheProvider>
      </ContextProvider>);
    };
}
/**
 * Migrating from enzyme? Pass context via the options object
 * Before
 * mountWithTheme(<Something />, routerContext);
 * After
 * mountWithTheme(<Something />, {context: routerContext});
 */
var mountWithTheme = function (ui, options) {
    var _a = options !== null && options !== void 0 ? options : {}, context = _a.context, otherOptions = __rest(_a, ["context"]);
    var AllTheProviders = makeAllTheProviders(context);
    return render(ui, __assign({ wrapper: AllTheProviders }, otherOptions));
};
export * from '@testing-library/react';
export { mountWithTheme };
//# sourceMappingURL=reactTestingLibrary.jsx.map