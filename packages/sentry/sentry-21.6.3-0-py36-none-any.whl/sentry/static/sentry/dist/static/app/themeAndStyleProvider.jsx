import { __extends } from "tslib";
import { Component } from 'react';
import ReactDOM from 'react-dom';
import { cache } from '@emotion/css'; // eslint-disable-line emotion/no-vanilla
import { CacheProvider, ThemeProvider } from '@emotion/react'; // This is needed to set "speedy" = false (for percy)
import { loadPreferencesState } from 'app/actionCreators/preferences';
import ConfigStore from 'app/stores/configStore';
import GlobalStyles from 'app/styles/global';
import { darkTheme, lightTheme } from 'app/utils/theme';
import withConfig from 'app/utils/withConfig';
var Main = /** @class */ (function (_super) {
    __extends(Main, _super);
    function Main() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            theme: _this.themeName === 'dark' ? darkTheme : lightTheme,
        };
        return _this;
    }
    Main.prototype.componentDidMount = function () {
        loadPreferencesState();
    };
    Main.prototype.componentDidUpdate = function (prevProps) {
        var config = this.props.config;
        if (config.theme !== prevProps.config.theme) {
            // eslint-disable-next-line
            this.setState({
                theme: config.theme === 'dark' ? darkTheme : lightTheme,
            });
        }
    };
    Object.defineProperty(Main.prototype, "themeName", {
        get: function () {
            return ConfigStore.get('theme');
        },
        enumerable: false,
        configurable: true
    });
    Main.prototype.render = function () {
        return (<ThemeProvider theme={this.state.theme}>
        <GlobalStyles isDark={this.props.config.theme === 'dark'} theme={this.state.theme}/>
        <CacheProvider value={cache}>{this.props.children}</CacheProvider>
        {ReactDOM.createPortal(<meta name="color-scheme" content={this.themeName}/>, document.head)}
      </ThemeProvider>);
    };
    return Main;
}(Component));
export default withConfig(Main);
//# sourceMappingURL=themeAndStyleProvider.jsx.map