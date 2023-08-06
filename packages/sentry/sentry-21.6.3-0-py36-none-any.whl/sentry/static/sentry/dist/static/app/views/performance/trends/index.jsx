import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import { generatePerformanceEventView } from '../data';
import TrendsContent from './content';
var TrendsSummary = /** @class */ (function (_super) {
    __extends(TrendsSummary, _super);
    function TrendsSummary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: generatePerformanceEventView(_this.props.organization, _this.props.location, _this.props.projects, true),
            error: undefined,
        };
        _this.setError = function (error) {
            _this.setState({ error: error });
        };
        return _this;
    }
    TrendsSummary.getDerivedStateFromProps = function (nextProps, prevState) {
        return __assign(__assign({}, prevState), { eventView: generatePerformanceEventView(nextProps.organization, nextProps.location, nextProps.projects, true) });
    };
    TrendsSummary.prototype.getDocumentTitle = function () {
        return [t('Trends'), t('Performance')].join(' - ');
    };
    TrendsSummary.prototype.renderContent = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var eventView = this.state.eventView;
        return (<TrendsContent organization={organization} location={location} eventView={eventView}/>);
    };
    TrendsSummary.prototype.render = function () {
        var organization = this.props.organization;
        return (<SentryDocumentTitle title={this.getDocumentTitle()} orgSlug={organization.slug}>
        <StyledPageContent>
          <LightWeightNoProjectMessage organization={organization}>
            {this.renderContent()}
          </LightWeightNoProjectMessage>
        </StyledPageContent>
      </SentryDocumentTitle>);
    };
    return TrendsSummary;
}(React.Component));
export default withOrganization(withProjects(withGlobalSelection(withApi(TrendsSummary))));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map