import { __assign, __extends, __makeTemplateObject } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import CreateAlertButton from 'app/components/createAlertButton';
import Hovercard from 'app/components/hovercard';
import * as Layout from 'app/components/layouts/thirds';
import ExternalLink from 'app/components/links/externalLink';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import BuilderBreadCrumbs from 'app/views/alerts/builder/builderBreadCrumbs';
import { Dataset } from 'app/views/alerts/incidentRules/types';
import { AlertWizardAlertNames, AlertWizardOptions, AlertWizardPanelContent, AlertWizardRuleTemplates, } from './options';
import RadioPanelGroup from './radioPanelGroup';
var DEFAULT_ALERT_OPTION = 'issues';
var AlertWizard = /** @class */ (function (_super) {
    __extends(AlertWizard, _super);
    function AlertWizard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            alertOption: DEFAULT_ALERT_OPTION,
        };
        _this.handleChangeAlertOption = function (alertOption) {
            var organization = _this.props.organization;
            _this.setState({ alertOption: alertOption });
            trackAnalyticsEvent({
                eventKey: 'alert_wizard.option_viewed',
                eventName: 'Alert Wizard: Option Viewed',
                organization_id: organization.id,
                alert_type: alertOption,
            });
        };
        return _this;
    }
    AlertWizard.prototype.componentDidMount = function () {
        // capture landing on the alert wizard page and viewing the issue alert by default
        var organization = this.props.organization;
        trackAnalyticsEvent({
            eventKey: 'alert_wizard.option_viewed',
            eventName: 'Alert Wizard: Option Viewed',
            organization_id: organization.id,
            alert_type: DEFAULT_ALERT_OPTION,
        });
    };
    AlertWizard.prototype.renderCreateAlertButton = function () {
        var _a;
        var _b = this.props, organization = _b.organization, location = _b.location, projectId = _b.params.projectId;
        var alertOption = this.state.alertOption;
        var metricRuleTemplate = AlertWizardRuleTemplates[alertOption];
        var isMetricAlert = !!metricRuleTemplate;
        var isTransactionDataset = (metricRuleTemplate === null || metricRuleTemplate === void 0 ? void 0 : metricRuleTemplate.dataset) === Dataset.TRANSACTIONS;
        var to = {
            pathname: "/organizations/" + organization.slug + "/alerts/" + projectId + "/new/",
            query: __assign(__assign({}, (metricRuleTemplate && metricRuleTemplate)), { createFromWizard: true, referrer: (_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.referrer }),
        };
        var noFeatureMessage = t('Requires incidents feature.');
        var renderNoAccess = function (p) { return (<Hovercard body={<FeatureDisabled features={p.features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
        {p.children(p)}
      </Hovercard>); };
        return (<Feature features={isTransactionDataset
                ? ['incidents', 'performance-view']
                : isMetricAlert
                    ? ['incidents']
                    : []} requireAll organization={organization} hookName="feature-disabled:alert-wizard-performance" renderDisabled={renderNoAccess}>
        {function (_a) {
                var hasFeature = _a.hasFeature;
                return (<WizardButtonContainer onClick={function () {
                        return trackAnalyticsEvent({
                            eventKey: 'alert_wizard.option_selected',
                            eventName: 'Alert Wizard: Option Selected',
                            organization_id: organization.id,
                            alert_type: alertOption,
                        });
                    }}>
            <CreateAlertButton organization={organization} projectSlug={projectId} disabled={!hasFeature} priority="primary" to={to} hideIcon>
              {t('Set Conditions')}
            </CreateAlertButton>
          </WizardButtonContainer>);
            }}
      </Feature>);
    };
    AlertWizard.prototype.render = function () {
        var _this = this;
        var _a = this.props, hasMetricAlerts = _a.hasMetricAlerts, organization = _a.organization, projectId = _a.params.projectId, routes = _a.routes, location = _a.location;
        var alertOption = this.state.alertOption;
        var title = t('Alert Creation Wizard');
        var panelContent = AlertWizardPanelContent[alertOption];
        return (<Fragment>
        <SentryDocumentTitle title={title} projectSlug={projectId}/>

        <Layout.Header>
          <StyledHeaderContent>
            <BuilderBreadCrumbs hasMetricAlerts={hasMetricAlerts} orgSlug={organization.slug} projectSlug={projectId} title={t('Select Alert')} routes={routes} location={location} canChangeProject/>
            <Layout.Title>{t('Select Alert')}</Layout.Title>
          </StyledHeaderContent>
        </Layout.Header>
        <StyledLayoutBody>
          <Layout.Main fullWidth>
            <WizardBody>
              <WizardOptions>
                <Styledh2>{t('Errors')}</Styledh2>
                {AlertWizardOptions.map(function (_a, i) {
                var categoryHeading = _a.categoryHeading, options = _a.options;
                return (<OptionsWrapper key={categoryHeading}>
                    {i > 0 && <Styledh2>{categoryHeading}</Styledh2>}
                    <RadioPanelGroup choices={options.map(function (alertType) {
                        return [alertType, AlertWizardAlertNames[alertType]];
                    })} onChange={_this.handleChangeAlertOption} value={alertOption} label="alert-option"/>
                  </OptionsWrapper>);
            })}
              </WizardOptions>
              <WizardPanel visible={!!panelContent && !!alertOption}>
                <WizardPanelBody>
                  <div>
                    <PanelHeader>{AlertWizardAlertNames[alertOption]}</PanelHeader>
                    <PanelBody withPadding>
                      <PanelDescription>
                        {panelContent.description}{' '}
                        {panelContent.docsLink && (<ExternalLink href={panelContent.docsLink}>
                            {t('Learn more')}
                          </ExternalLink>)}
                      </PanelDescription>
                      <WizardImage src={panelContent.illustration}/>
                      <ExampleHeader>{t('Examples')}</ExampleHeader>
                      <ExampleList symbol="bullet">
                        {panelContent.examples.map(function (example, i) { return (<ExampleItem key={i}>{example}</ExampleItem>); })}
                      </ExampleList>
                    </PanelBody>
                  </div>
                  <WizardFooter>{this.renderCreateAlertButton()}</WizardFooter>
                </WizardPanelBody>
              </WizardPanel>
            </WizardBody>
          </Layout.Main>
        </StyledLayoutBody>
      </Fragment>);
    };
    return AlertWizard;
}(Component));
var StyledLayoutBody = styled(Layout.Body)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: -", ";\n"], ["\n  margin-bottom: -", ";\n"])), space(3));
var StyledHeaderContent = styled(Layout.HeaderContent)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  overflow: visible;\n"], ["\n  overflow: visible;\n"])));
var Styledh2 = styled('h2')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-weight: normal;\n  font-size: ", ";\n  margin-bottom: ", " !important;\n"], ["\n  font-weight: normal;\n  font-size: ", ";\n  margin-bottom: ", " !important;\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(1));
var WizardBody = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  padding-top: ", ";\n"], ["\n  display: flex;\n  padding-top: ", ";\n"])), space(1));
var WizardOptions = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex: 3;\n  margin-right: ", ";\n  padding-right: ", ";\n  max-width: 300px;\n"], ["\n  flex: 3;\n  margin-right: ", ";\n  padding-right: ", ";\n  max-width: 300px;\n"])), space(3), space(3));
var WizardImage = styled('img')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  max-height: 300px;\n"], ["\n  max-height: 300px;\n"])));
var WizardPanel = styled(Panel)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  max-width: 700px;\n  position: sticky;\n  top: 20px;\n  flex: 5;\n  display: flex;\n  ", ";\n  flex-direction: column;\n  align-items: start;\n  align-self: flex-start;\n  ", ";\n\n  @keyframes pop {\n    0% {\n      transform: translateY(30px);\n      opacity: 0;\n    }\n    100% {\n      transform: translateY(0);\n      opacity: 1;\n    }\n  }\n"], ["\n  max-width: 700px;\n  position: sticky;\n  top: 20px;\n  flex: 5;\n  display: flex;\n  ", ";\n  flex-direction: column;\n  align-items: start;\n  align-self: flex-start;\n  ", ";\n\n  @keyframes pop {\n    0% {\n      transform: translateY(30px);\n      opacity: 0;\n    }\n    100% {\n      transform: translateY(0);\n      opacity: 1;\n    }\n  }\n"])), function (p) { return !p.visible && 'visibility: hidden'; }, function (p) { return p.visible && 'animation: 0.6s pop ease forwards'; });
var ExampleList = styled(List)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-bottom: ", " !important;\n"], ["\n  margin-bottom: ", " !important;\n"])), space(2));
var WizardPanelBody = styled(PanelBody)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  flex: 1;\n  min-width: 100%;\n"], ["\n  flex: 1;\n  min-width: 100%;\n"])));
var PanelDescription = styled('p')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var ExampleHeader = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin: 0 0 ", " 0;\n  font-size: ", ";\n"], ["\n  margin: 0 0 ", " 0;\n  font-size: ", ";\n"])), space(1), function (p) { return p.theme.fontSizeLarge; });
var ExampleItem = styled(ListItem)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var OptionsWrapper = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  margin-bottom: ", ";\n\n  &:last-child {\n    margin-bottom: 0;\n  }\n"], ["\n  margin-bottom: ", ";\n\n  &:last-child {\n    margin-bottom: 0;\n  }\n"])), space(4));
var WizardFooter = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  padding: ", " ", " ", " ", ";\n"], ["\n  border-top: 1px solid ", ";\n  padding: ", " ", " ", " ", ";\n"])), function (p) { return p.theme.border; }, space(1.5), space(1.5), space(1.5), space(1.5));
var WizardButtonContainer = styled('div')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
export default AlertWizard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15;
//# sourceMappingURL=index.jsx.map