import { __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import styled from '@emotion/styled';
import Hook from 'app/components/hook';
import ExternalLink from 'app/components/links/externalLink';
import { IconSentry } from 'app/icons';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import space from 'app/styles/space';
import getDynamicText from 'app/utils/getDynamicText';
function Footer(_a) {
    var className = _a.className;
    var config = ConfigStore.getConfig();
    return (<footer className={className}>
      <LeftLinks>
        {config.isOnPremise && (<Fragment>
            {'Sentry '}
            {getDynamicText({
                fixed: 'Acceptance Test',
                value: config.version.current,
            })}
            <Build>
              {getDynamicText({
                fixed: 'test',
                value: config.version.build.substring(0, 7),
            })}
            </Build>
          </Fragment>)}
        {config.privacyUrl && (<FooterLink href={config.privacyUrl}>{t('Privacy Policy')}</FooterLink>)}
        {config.termsUrl && (<FooterLink href={config.termsUrl}>{t('Terms of Use')}</FooterLink>)}
      </LeftLinks>
      <LogoLink />
      <RightLinks>
        <FooterLink href="/api/">{t('API')}</FooterLink>
        <FooterLink href="/docs/">{t('Docs')}</FooterLink>
        <FooterLink href="https://github.com/getsentry/sentry">
          {t('Contribute')}
        </FooterLink>
        {config.isOnPremise && !config.demoMode && (<FooterLink href="/out/">{t('Migrate to SaaS')}</FooterLink>)}
      </RightLinks>
      <Hook name="footer"/>
    </footer>);
}
var LeftLinks = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  justify-self: flex-start;\n  gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  justify-self: flex-start;\n  gap: ", ";\n"])), space(2));
var RightLinks = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  justify-self: flex-end;\n  gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  align-items: center;\n  justify-self: flex-end;\n  gap: ", ";\n"])), space(2));
var FooterLink = styled(ExternalLink)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n"], ["\n  color: ", ";\n  &.focus-visible {\n    outline: none;\n    box-shadow: ", " 0 2px 0;\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.blue300; });
var LogoLink = styled(function (props) { return (<ExternalLink href="https://sentry.io/welcome/" tabIndex={-1} {...props}>
    <IconSentry size="xl"/>
  </ExternalLink>); })(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  display: block;\n  width: 32px;\n  height: 32px;\n  margin: 0 auto;\n"], ["\n  color: ", ";\n  display: block;\n  width: 32px;\n  height: 32px;\n  margin: 0 auto;\n"])), function (p) { return p.theme.subText; });
var Build = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  font-weight: bold;\n  margin-left: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  font-weight: bold;\n  margin-left: ", ";\n"])), function (p) { return p.theme.fontSizeRelativeSmall; }, function (p) { return p.theme.subText; }, space(1));
var StyledFooter = styled(Footer)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  color: ", ";\n  border-top: 1px solid ", ";\n  padding: ", ";\n  margin-top: 20px;\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr 1fr;\n  color: ", ";\n  border-top: 1px solid ", ";\n  padding: ", ";\n  margin-top: 20px;\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.border; }, space(4), function (p) { return p.theme.breakpoints[0]; });
export default StyledFooter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=footer.jsx.map