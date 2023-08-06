import { __awaiter, __generator, __read } from "tslib";
import * as Sentry from '@sentry/react';
import * as moment from 'moment';
import * as qs from 'query-string';
import { DEFAULT_LOCALE_DATA, setLocale } from 'app/locale';
// zh-cn => zh_CN
function convertToDjangoLocaleFormat(language) {
    var _a = __read(language.split('-'), 2), left = _a[0], right = _a[1];
    return left + (right ? '_' + right.toUpperCase() : '');
}
function getTranslations(language) {
    return __awaiter(this, void 0, void 0, function () {
        var e_1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    language = convertToDjangoLocaleFormat(language);
                    // No need to load the english locale
                    if (language === 'en') {
                        return [2 /*return*/, DEFAULT_LOCALE_DATA];
                    }
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, import("sentry-locale/" + language + "/LC_MESSAGES/django.po")];
                case 2: return [2 /*return*/, _a.sent()];
                case 3:
                    e_1 = _a.sent();
                    Sentry.withScope(function (scope) {
                        scope.setLevel(Sentry.Severity.Warning);
                        scope.setFingerprint(['sentry-locale-not-found']);
                        scope.setExtra('locale', language);
                        Sentry.captureException(e_1);
                    });
                    // Default locale if not found
                    return [2 /*return*/, DEFAULT_LOCALE_DATA];
                case 4: return [2 /*return*/];
            }
        });
    });
}
/**
 * Initialize locale
 *
 * This *needs* to be initialized as early as possible (e.g. before `app/locale` is used),
 * otherwise the rest of the application will fail to load.
 *
 * Priority:
 *
 * - URL params (`?lang=en`)
 * - User configuration options
 * - User's system language code (from request)
 * - "en" as default
 */
export function initializeLocale(config) {
    var _a, _b;
    return __awaiter(this, void 0, void 0, function () {
        var queryString, queryStringLang, languageCode, translations, err_1;
        return __generator(this, function (_c) {
            switch (_c.label) {
                case 0:
                    queryString = {};
                    // Parse query string for `lang`
                    try {
                        queryString = qs.parse(window.location.search) || {};
                    }
                    catch (_d) {
                        // ignore if this fails to parse
                        // this can happen if we have an invalid query string
                        // e.g. unencoded "%"
                    }
                    queryStringLang = Array.isArray(queryString.lang)
                        ? queryString.lang[0]
                        : queryString.lang;
                    languageCode = queryStringLang || ((_b = (_a = config.user) === null || _a === void 0 ? void 0 : _a.options) === null || _b === void 0 ? void 0 : _b.language) || config.languageCode || 'en';
                    _c.label = 1;
                case 1:
                    _c.trys.push([1, 5, , 6]);
                    return [4 /*yield*/, getTranslations(languageCode)];
                case 2:
                    translations = _c.sent();
                    setLocale(translations);
                    if (!(languageCode !== 'en')) return [3 /*break*/, 4];
                    return [4 /*yield*/, import("moment/locale/" + languageCode)];
                case 3:
                    _c.sent();
                    moment.locale(languageCode);
                    _c.label = 4;
                case 4: return [3 /*break*/, 6];
                case 5:
                    err_1 = _c.sent();
                    Sentry.captureException(err_1);
                    return [3 /*break*/, 6];
                case 6: return [2 /*return*/];
            }
        });
    });
}
//# sourceMappingURL=initializeLocale.jsx.map