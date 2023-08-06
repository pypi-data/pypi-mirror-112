import { __makeTemplateObject, __read } from "tslib";
import * as React from 'react';
import { css } from '@emotion/react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { IconClose } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
var makeKey = function (prefix) { return prefix + "-banner-dismissed"; };
function dismissBanner(bannerKey) {
    localStorage.setItem(makeKey(bannerKey), 'true');
}
function useDismissable(bannerKey) {
    var key = makeKey(bannerKey);
    var _a = __read(React.useState(localStorage.getItem(key)), 2), value = _a[0], setValue = _a[1];
    var dismiss = function () {
        setValue('true');
        dismissBanner(bannerKey);
    };
    return [value === 'true', dismiss];
}
var Banner = function (_a) {
    var title = _a.title, subtitle = _a.subtitle, _b = _a.isDismissable, isDismissable = _b === void 0 ? true : _b, _c = _a.dismissKey, dismissKey = _c === void 0 ? 'generic-banner' : _c, className = _a.className, backgroundImg = _a.backgroundImg, backgroundComponent = _a.backgroundComponent, children = _a.children;
    var _d = __read(useDismissable(dismissKey), 2), dismissed = _d[0], dismiss = _d[1];
    if (dismissed) {
        return null;
    }
    return (<BannerWrapper backgroundImg={backgroundImg} className={className}>
      {backgroundComponent}
      {isDismissable ? <CloseButton onClick={dismiss}/> : null}
      <BannerContent>
        <BannerTitle>{title}</BannerTitle>
        <BannerSubtitle>{subtitle}</BannerSubtitle>
        <StyledButtonBar gap={1}>{children}</StyledButtonBar>
      </BannerContent>
    </BannerWrapper>);
};
Banner.dismiss = dismissBanner;
var BannerWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", "\n  display: flex;\n  overflow: hidden;\n  align-items: center;\n  justify-content: center;\n  position: relative;\n  margin-bottom: ", ";\n  box-shadow: ", ";\n  border-radius: ", ";\n  height: 180px;\n  color: ", ";\n\n  @media (min-width: ", ") {\n    height: 220px;\n  }\n"], ["\n  ", "\n  display: flex;\n  overflow: hidden;\n  align-items: center;\n  justify-content: center;\n  position: relative;\n  margin-bottom: ", ";\n  box-shadow: ", ";\n  border-radius: ", ";\n  height: 180px;\n  color: ", ";\n\n  @media (min-width: ", ") {\n    height: 220px;\n  }\n"])), function (p) {
    return p.backgroundImg
        ? css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n          background: url(", ");\n          background-repeat: no-repeat;\n          background-size: cover;\n          background-position: center center;\n        "], ["\n          background: url(", ");\n          background-repeat: no-repeat;\n          background-size: cover;\n          background-position: center center;\n        "])), p.backgroundImg) : css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n          background-color: ", ";\n        "], ["\n          background-color: ", ";\n        "])), p.theme.gray500);
}, space(2), function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.white; }, function (p) { return p.theme.breakpoints[0]; });
var BannerContent = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: absolute;\n  display: grid;\n  justify-items: center;\n  grid-template-rows: repeat(3, max-content);\n  text-align: center;\n  padding: ", ";\n"], ["\n  position: absolute;\n  display: grid;\n  justify-items: center;\n  grid-template-rows: repeat(3, max-content);\n  text-align: center;\n  padding: ", ";\n"])), space(4));
var BannerTitle = styled('h1')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin: 0;\n\n  @media (min-width: ", ") {\n    font-size: 40px;\n  }\n"], ["\n  margin: 0;\n\n  @media (min-width: ", ") {\n    font-size: 40px;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var BannerSubtitle = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: 0;\n\n  @media (min-width: ", ") {\n    font-size: ", ";\n  }\n"], ["\n  margin: 0;\n\n  @media (min-width: ", ") {\n    font-size: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.fontSizeExtraLarge; });
var StyledButtonBar = styled(ButtonBar)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-top: ", ";\n  width: fit-content;\n"], ["\n  margin-top: ", ";\n  width: fit-content;\n"])), space(2));
var CloseButton = styled(Button)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  position: absolute;\n  display: block;\n  top: ", ";\n  right: ", ";\n  color: ", ";\n  cursor: pointer;\n  z-index: 1;\n"], ["\n  position: absolute;\n  display: block;\n  top: ", ";\n  right: ", ";\n  color: ", ";\n  cursor: pointer;\n  z-index: 1;\n"])), space(2), space(2), function (p) { return p.theme.white; });
CloseButton.defaultProps = {
    icon: <IconClose />,
    label: t('Close'),
    priority: 'link',
    borderless: true,
    size: 'xsmall',
};
export default Banner;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=banner.jsx.map