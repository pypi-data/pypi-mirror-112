import 'focus-visible';
import { NODE_ENV } from 'app/constants';
import ConfigStore from 'app/stores/configStore';
import { setupColorScheme } from 'app/utils/matchMedia';
export function commonInitialization(config) {
    if (NODE_ENV === 'development') {
        import(/* webpackMode: "eager" */ 'app/utils/silence-react-unsafe-warnings');
    }
    ConfigStore.loadInitialData(config);
    // setup darkmode + favicon
    setupColorScheme();
}
//# sourceMappingURL=commonInitialization.jsx.map