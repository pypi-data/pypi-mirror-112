import { __assign, __read } from "tslib";
import { IconFire, IconFix, IconInfo, IconLocation, IconMobile, IconRefresh, IconSpan, IconStack, IconSwitch, IconTerminal, IconUser, IconWarning, } from 'app/icons';
import { t } from 'app/locale';
import { BreadcrumbLevelType, BreadcrumbType } from 'app/types/breadcrumbs';
import { defined } from 'app/utils';
function convertCrumbType(breadcrumb) {
    if (breadcrumb.type === BreadcrumbType.EXCEPTION) {
        return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.ERROR });
    }
    // special case for 'ui.' and `sentry.` category breadcrumbs
    // TODO: find a better way to customize UI around non-schema data
    if (breadcrumb.type === BreadcrumbType.DEFAULT && defined(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.category)) {
        var _a = __read(breadcrumb.category.split('.'), 2), category = _a[0], subcategory = _a[1];
        if (category === 'ui') {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.UI });
        }
        if (category === 'console') {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.DEBUG });
        }
        if (category === 'navigation') {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.NAVIGATION });
        }
        if (category === 'sentry' &&
            (subcategory === 'transaction' || subcategory === 'event')) {
            return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.TRANSACTION });
        }
    }
    if (!Object.values(BreadcrumbType).includes(breadcrumb.type)) {
        return __assign(__assign({}, breadcrumb), { type: BreadcrumbType.DEFAULT });
    }
    return breadcrumb;
}
function getCrumbDetails(type) {
    switch (type) {
        case BreadcrumbType.USER:
        case BreadcrumbType.UI:
            return {
                color: 'purple300',
                icon: IconUser,
                description: t('User Action'),
            };
        case BreadcrumbType.NAVIGATION:
            return {
                color: 'green300',
                icon: IconLocation,
                description: t('Navigation'),
            };
        case BreadcrumbType.DEBUG:
            return {
                color: 'purple300',
                icon: IconFix,
                description: t('Debug'),
            };
        case BreadcrumbType.INFO:
            return {
                color: 'blue300',
                icon: IconInfo,
                description: t('Info'),
            };
        case BreadcrumbType.ERROR:
            return {
                color: 'red300',
                icon: IconFire,
                description: t('Error'),
            };
        case BreadcrumbType.HTTP:
            return {
                color: 'green300',
                icon: IconSwitch,
                description: t('HTTP request'),
            };
        case BreadcrumbType.WARNING:
            return {
                color: 'orange400',
                icon: IconWarning,
                description: t('Warning'),
            };
        case BreadcrumbType.QUERY:
            return {
                color: 'blue300',
                icon: IconStack,
                description: t('Query'),
            };
        case BreadcrumbType.SYSTEM:
            return {
                color: 'pink200',
                icon: IconMobile,
                description: t('System'),
            };
        case BreadcrumbType.SESSION:
            return {
                color: 'orange500',
                icon: IconRefresh,
                description: t('Session'),
            };
        case BreadcrumbType.TRANSACTION:
            return {
                color: 'pink300',
                icon: IconSpan,
                description: t('Transaction'),
            };
        default:
            return {
                icon: IconTerminal,
                description: t('Default'),
            };
    }
}
export function transformCrumbs(breadcrumbs) {
    return breadcrumbs.map(function (breadcrumb, index) {
        var _a;
        var convertedCrumbType = convertCrumbType(breadcrumb);
        var crumbDetails = getCrumbDetails(convertedCrumbType.type);
        return __assign(__assign(__assign({ id: index }, convertedCrumbType), crumbDetails), { level: (_a = convertedCrumbType === null || convertedCrumbType === void 0 ? void 0 : convertedCrumbType.level) !== null && _a !== void 0 ? _a : BreadcrumbLevelType.UNDEFINED });
    });
}
//# sourceMappingURL=utils.jsx.map