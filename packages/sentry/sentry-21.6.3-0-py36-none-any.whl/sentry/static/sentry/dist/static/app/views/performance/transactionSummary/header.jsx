import { __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import { openModal } from 'app/actionCreators/modal';
import Feature from 'app/components/acl/feature';
import { GuideAnchor } from 'app/components/assistant/guideAnchor';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { CreateAlertFromViewButton } from 'app/components/createAlertButton';
import FeatureBadge from 'app/components/featureBadge';
import * as Layout from 'app/components/layouts/thirds';
import ListLink from 'app/components/links/listLink';
import NavTabs from 'app/components/navTabs';
import { IconSettings } from 'app/icons';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { decodeScalar } from 'app/utils/queryString';
import Breadcrumb from 'app/views/performance/breadcrumb';
import { eventsRouteWithQuery } from './transactionEvents/utils';
import { tagsRouteWithQuery } from './transactionTags/utils';
import { vitalsRouteWithQuery } from './transactionVitals/utils';
import KeyTransactionButton from './keyTransactionButton';
import TeamKeyTransactionButton from './teamKeyTransactionButton';
import TransactionThresholdModal, { modalCss, } from './transactionThresholdModal';
import { transactionSummaryRouteWithQuery } from './utils';
export var Tab;
(function (Tab) {
    Tab[Tab["TransactionSummary"] = 0] = "TransactionSummary";
    Tab[Tab["RealUserMonitoring"] = 1] = "RealUserMonitoring";
    Tab[Tab["Tags"] = 2] = "Tags";
    Tab[Tab["Events"] = 3] = "Events";
})(Tab || (Tab = {}));
var TransactionHeader = /** @class */ (function (_super) {
    __extends(TransactionHeader, _super);
    function TransactionHeader() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.trackVitalsTabClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.vitals.vitals_tab_clicked',
                eventName: 'Performance Views: Vitals tab clicked',
                organization_id: organization.id,
            });
        };
        _this.trackTagsTabClick = function () {
            // TODO(k-fish): Add analytics for tags
        };
        _this.trackEventsTabClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.events.events_tab_clicked',
                eventName: 'Performance Views: Events tab clicked',
                organization_id: organization.id,
            });
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, errors) {
            var _a, _b;
            _this.trackAlertClick(errors);
            (_b = (_a = _this.props).handleIncompatibleQuery) === null || _b === void 0 ? void 0 : _b.call(_a, incompatibleAlertNoticeFn, errors);
        };
        _this.handleCreateAlertSuccess = function () {
            _this.trackAlertClick();
        };
        return _this;
    }
    TransactionHeader.prototype.trackAlertClick = function (errors) {
        var organization = this.props.organization;
        trackAnalyticsEvent({
            eventKey: 'performance_views.summary.create_alert_clicked',
            eventName: 'Performance Views: Create alert clicked',
            organization_id: organization.id,
            status: errors ? 'error' : 'success',
            errors: errors,
            url: window.location.href,
        });
    };
    TransactionHeader.prototype.renderCreateAlertButton = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects;
        return (<CreateAlertFromViewButton eventView={eventView} organization={organization} projects={projects} onIncompatibleQuery={this.handleIncompatibleQuery} onSuccess={this.handleCreateAlertSuccess} referrer="performance"/>);
    };
    TransactionHeader.prototype.renderKeyTransactionButton = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, transactionName = _a.transactionName;
        return (<Feature organization={organization} features={['team-key-transactions']}>
        {function (_a) {
                var hasFeature = _a.hasFeature;
                return hasFeature ? (<TeamKeyTransactionButton transactionName={transactionName} eventView={eventView} organization={organization}/>) : (<KeyTransactionButton transactionName={transactionName} eventView={eventView} organization={organization}/>);
            }}
      </Feature>);
    };
    TransactionHeader.prototype.openModal = function () {
        var _a = this.props, organization = _a.organization, transactionName = _a.transactionName, eventView = _a.eventView, transactionThreshold = _a.transactionThreshold, transactionThresholdMetric = _a.transactionThresholdMetric, onChangeThreshold = _a.onChangeThreshold;
        openModal(function (modalProps) { return (<TransactionThresholdModal {...modalProps} organization={organization} transactionName={transactionName} eventView={eventView} transactionThreshold={transactionThreshold} transactionThresholdMetric={transactionThresholdMetric} onApply={onChangeThreshold}/>); }, { modalCss: modalCss, backdrop: 'static' });
    };
    TransactionHeader.prototype.renderSettingsButton = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, loadingThreshold = _a.loadingThreshold;
        return (<Feature organization={organization} features={['project-transaction-threshold-override']}>
        {function (_a) {
                var hasFeature = _a.hasFeature;
                return hasFeature ? (<GuideAnchor target="project_transaction_threshold_override" position="bottom">
              <Button onClick={function () { return _this.openModal(); }} data-test-id="set-transaction-threshold" icon={<IconSettings />} disabled={loadingThreshold} aria-label={t('Settings')}/>
            </GuideAnchor>) : (<Button href={"/settings/" + organization.slug + "/performance/"} icon={<IconSettings />} aria-label={t('Settings')}/>);
            }}
      </Feature>);
    };
    TransactionHeader.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location, transactionName = _a.transactionName, currentTab = _a.currentTab, hasWebVitals = _a.hasWebVitals;
        var summaryTarget = transactionSummaryRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transactionName,
            projectID: decodeScalar(location.query.project),
            query: location.query,
        });
        var vitalsTarget = vitalsRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transactionName,
            projectID: decodeScalar(location.query.project),
            query: location.query,
        });
        var tagsTarget = tagsRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transactionName,
            projectID: decodeScalar(location.query.project),
            query: location.query,
        });
        var eventsTarget = eventsRouteWithQuery({
            orgSlug: organization.slug,
            transaction: transactionName,
            projectID: decodeScalar(location.query.project),
            query: location.query,
        });
        return (<Layout.Header>
        <Layout.HeaderContent>
          <Breadcrumb organization={organization} location={location} transactionName={transactionName} realUserMonitoring={currentTab === Tab.RealUserMonitoring}/>
          <Layout.Title>{transactionName}</Layout.Title>
        </Layout.HeaderContent>
        <Layout.HeaderActions>
          <ButtonBar gap={1}>
            <Feature organization={organization} features={['incidents']}>
              {function (_a) {
            var hasFeature = _a.hasFeature;
            return hasFeature && _this.renderCreateAlertButton();
        }}
            </Feature>
            {this.renderKeyTransactionButton()}
            {this.renderSettingsButton()}
          </ButtonBar>
        </Layout.HeaderActions>
        <React.Fragment>
          <StyledNavTabs>
            <ListLink to={summaryTarget} isActive={function () { return currentTab === Tab.TransactionSummary; }}>
              {t('Overview')}
            </ListLink>
            {hasWebVitals && (<ListLink to={vitalsTarget} isActive={function () { return currentTab === Tab.RealUserMonitoring; }} onClick={this.trackVitalsTabClick}>
                {t('Web Vitals')}
              </ListLink>)}
            <Feature features={['organizations:performance-tag-page']}>
              <ListLink to={tagsTarget} isActive={function () { return currentTab === Tab.Tags; }} onClick={this.trackTagsTabClick}>
                {t('Tags')}
                <FeatureBadge type="alpha" noTooltip/>
              </ListLink>
            </Feature>
            <Feature features={['organizations:performance-events-page']}>
              <ListLink to={eventsTarget} isActive={function () { return currentTab === Tab.Events; }} onClick={this.trackEventsTabClick}>
                {t('All Events')}
                <FeatureBadge type="beta" noTooltip/>
              </ListLink>
            </Feature>
          </StyledNavTabs>
        </React.Fragment>
      </Layout.Header>);
    };
    return TransactionHeader;
}(React.Component));
var StyledNavTabs = styled(NavTabs)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 0;\n  /* Makes sure the tabs are pushed into another row */\n  width: 100%;\n"], ["\n  margin-bottom: 0;\n  /* Makes sure the tabs are pushed into another row */\n  width: 100%;\n"])));
export default TransactionHeader;
var templateObject_1;
//# sourceMappingURL=header.jsx.map