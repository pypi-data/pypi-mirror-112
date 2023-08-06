import { __makeTemplateObject, __read } from "tslib";
import { useEffect, useState } from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import ExternalLink from 'app/components/links/externalLink';
import LogoSentry from 'app/components/logoSentry';
import { t } from 'app/locale';
import PreferencesStore from 'app/stores/preferencesStore';
import space from 'app/styles/space';
import { trackAdvancedAnalyticsEvent } from 'app/utils/advancedAnalytics';
import getCookie from 'app/utils/getCookie';
export default function DemoHeader() {
    // if the user came from a SaaS org, we should send them back to upgrade when they leave the sandbox
    var saasOrgSlug = getCookie('saas_org_slug');
    var email = localStorage.getItem('email');
    var queryParameter = email ? "?email=" + email : '';
    var getStartedText = saasOrgSlug ? t('Upgrade Now') : t('Sign Up for Free');
    var getStartedUrl = saasOrgSlug
        ? "https://sentry.io/settings/" + saasOrgSlug + "/billing/checkout/"
        : "https://sentry.io/signup/" + queryParameter;
    var _a = __read(useState(PreferencesStore.prefs.collapsed), 2), collapsed = _a[0], setCollapsed = _a[1];
    var preferenceUnsubscribe = PreferencesStore.listen(function (preferences) { return onPreferenceChange(preferences); }, undefined);
    function onPreferenceChange(preferences) {
        if (preferences.collapsed === collapsed) {
            return;
        }
        setCollapsed(!collapsed);
    }
    useEffect(function () {
        return function () {
            preferenceUnsubscribe();
        };
    });
    return (<Wrapper collapsed={collapsed}>
      <StyledLogoSentry />
      <ButtonBar gap={4}>
        <StyledExternalLink onClick={function () { return trackAdvancedAnalyticsEvent('growth.demo_click_docs', {}, null); }} href="https://docs.sentry.io">
          {t('Documentation')}
        </StyledExternalLink>
        <BaseButton priority="form" onClick={function () {
            return trackAdvancedAnalyticsEvent('growth.demo_click_request_demo', {}, null);
        }} href="https://sentry.io/_/demo/">
          {t('Request a Demo')}
        </BaseButton>
        <GetStarted onClick={function () {
            return trackAdvancedAnalyticsEvent('growth.demo_click_get_started', {
                is_upgrade: !!saasOrgSlug,
            }, null);
        }} href={getStartedUrl}>
          {getStartedText}
        </GetStarted>
      </ButtonBar>
    </Wrapper>);
}
// Note many of the colors don't come from the theme as they come from the marketing site
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-right: ", ";\n  background-color: ", ";\n  height: ", ";\n  display: flex;\n  justify-content: space-between;\n  text-transform: uppercase;\n\n  margin-left: calc(\n    -1 * ", "\n  );\n\n  position: fixed;\n  width: 100%;\n  border-bottom: 1px solid ", ";\n  z-index: ", ";\n\n  @media (max-width: ", ") {\n    height: ", ";\n    margin-left: 0;\n  }\n"], ["\n  padding-right: ", ";\n  background-color: ", ";\n  height: ", ";\n  display: flex;\n  justify-content: space-between;\n  text-transform: uppercase;\n\n  margin-left: calc(\n    -1 * ", "\n  );\n\n  position: fixed;\n  width: 100%;\n  border-bottom: 1px solid ", ";\n  z-index: ", ";\n\n  @media (max-width: ", ") {\n    height: ", ";\n    margin-left: 0;\n  }\n"])), space(3), function (p) { return p.theme.white; }, function (p) { return p.theme.demo.headerSize; }, function (p) { return (p.collapsed ? p.theme.sidebar.collapsedWidth : p.theme.sidebar.expandedWidth); }, function (p) { return p.theme.border; }, function (p) { return p.theme.zIndex.settingsSidebarNav; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.sidebar.mobileHeight; });
var StyledLogoSentry = styled(LogoSentry)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: auto;\n  margin-bottom: auto;\n  margin-left: 20px;\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"], ["\n  margin-top: auto;\n  margin-bottom: auto;\n  margin-left: 20px;\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var BaseButton = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  border-radius: 2rem;\n  text-transform: uppercase;\n"], ["\n  border-radius: 2rem;\n  text-transform: uppercase;\n"])));
// Note many of the colors don't come from the theme as they come from the marketing site
var GetStarted = styled(BaseButton)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  border-color: transparent;\n  box-shadow: 0 2px 0 rgb(54 45 89 / 10%);\n  background-color: #e1567c;\n  color: #fff;\n"], ["\n  border-color: transparent;\n  box-shadow: 0 2px 0 rgb(54 45 89 / 10%);\n  background-color: #e1567c;\n  color: #fff;\n"])));
var StyledExternalLink = styled(ExternalLink)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: #584774;\n"], ["\n  color: #584774;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=demoHeader.jsx.map