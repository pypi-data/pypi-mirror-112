import { __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import styled from '@emotion/styled';
import ExternalLink from 'app/components/links/externalLink';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
function getSdkUpdateSuggestion(_a) {
    var sdk = _a.sdk, suggestion = _a.suggestion, _b = _a.shortStyle, shortStyle = _b === void 0 ? false : _b, _c = _a.capitalized, capitalized = _c === void 0 ? false : _c;
    function getUpdateSdkContent(newSdkVersion) {
        var _a, _b, _c, _d;
        if (capitalized) {
            return sdk
                ? shortStyle
                    ? tct('Update to @v[new-sdk-version]', (_a = {},
                        _a['new-sdk-version'] = newSdkVersion,
                        _a))
                    : tct('Update your SDK from @v[sdk-version] to @v[new-sdk-version]', (_b = {},
                        _b['sdk-version'] = sdk.version,
                        _b['new-sdk-version'] = newSdkVersion,
                        _b))
                : t('Update your SDK version');
        }
        return sdk
            ? shortStyle
                ? tct('update to @v[new-sdk-version]', (_c = {},
                    _c['new-sdk-version'] = newSdkVersion,
                    _c))
                : tct('update your SDK from @v[sdk-version] to @v[new-sdk-version]', (_d = {},
                    _d['sdk-version'] = sdk.version,
                    _d['new-sdk-version'] = newSdkVersion,
                    _d))
            : t('update your SDK version');
    }
    var getTitleData = function () {
        switch (suggestion.type) {
            case 'updateSdk':
                return {
                    href: suggestion === null || suggestion === void 0 ? void 0 : suggestion.sdkUrl,
                    content: getUpdateSdkContent(suggestion.newSdkVersion),
                };
            case 'changeSdk':
                return {
                    href: suggestion === null || suggestion === void 0 ? void 0 : suggestion.sdkUrl,
                    content: tct('migrate to the [sdkName] SDK', {
                        sdkName: <code>{suggestion.newSdkName}</code>,
                    }),
                };
            case 'enableIntegration':
                return {
                    href: suggestion === null || suggestion === void 0 ? void 0 : suggestion.integrationUrl,
                    content: t("enable the '%s' integration", suggestion.integrationName),
                };
            default:
                return null;
        }
    };
    var getTitle = function () {
        var titleData = getTitleData();
        if (!titleData) {
            return null;
        }
        var href = titleData.href, content = titleData.content;
        if (!href) {
            return content;
        }
        return <ExternalLink href={href}>{content}</ExternalLink>;
    };
    var title = <Fragment>{getTitle()}</Fragment>;
    if (!suggestion.enables.length) {
        return title;
    }
    var alertContent = suggestion.enables
        .map(function (subSuggestion, index) {
        var subSuggestionContent = getSdkUpdateSuggestion({
            suggestion: subSuggestion,
            sdk: sdk,
        });
        if (!subSuggestionContent) {
            return null;
        }
        return <Fragment key={index}>{subSuggestionContent}</Fragment>;
    })
        .filter(function (content) { return !!content; });
    if (!alertContent.length) {
        return title;
    }
    return tct('[title] so you can: [suggestion]', {
        title: title,
        suggestion: <AlertUl>{alertContent}</AlertUl>,
    });
}
export default getSdkUpdateSuggestion;
var AlertUl = styled('ul')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n  margin-bottom: ", ";\n  padding-left: 0 !important;\n"], ["\n  margin-top: ", ";\n  margin-bottom: ", ";\n  padding-left: 0 !important;\n"])), space(1), space(1));
var templateObject_1;
//# sourceMappingURL=getSdkUpdateSuggestion.jsx.map