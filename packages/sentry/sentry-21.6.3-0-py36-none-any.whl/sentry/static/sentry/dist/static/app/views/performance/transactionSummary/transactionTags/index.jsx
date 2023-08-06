import { __assign, __extends, __makeTemplateObject } from "tslib";
import { Component } from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import EventView from 'app/utils/discover/eventView';
import { decodeScalar } from 'app/utils/queryString';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import { getTransactionName } from '../../utils';
import TagsPageContent from './content';
var TransactionTags = /** @class */ (function (_super) {
    __extends(TransactionTags, _super);
    function TransactionTags() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: generateTagsEventView(_this.props.location, getTransactionName(_this.props.location)),
        };
        _this.renderNoAccess = function () {
            return <Alert type="warning">{t("You don't have access to this feature")}</Alert>;
        };
        return _this;
    }
    TransactionTags.getDerivedStateFromProps = function (nextProps, prevState) {
        return __assign(__assign({}, prevState), { eventView: generateTagsEventView(nextProps.location, getTransactionName(nextProps.location)) });
    };
    TransactionTags.prototype.getDocumentTitle = function () {
        var name = getTransactionName(this.props.location);
        var hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), t('Tags')].join(' \u2014 ');
        }
        return [t('Summary'), t('Tags')].join(' \u2014 ');
    };
    TransactionTags.prototype.render = function () {
        var _a = this.props, organization = _a.organization, projects = _a.projects, location = _a.location;
        var eventView = this.state.eventView;
        var transactionName = getTransactionName(location);
        if (!eventView || transactionName === undefined) {
            // If there is no transaction name, redirect to the Performance landing page
            browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: __assign({}, location.query),
            });
            return null;
        }
        var shouldForceProject = eventView.project.length === 1;
        var forceProject = shouldForceProject
            ? projects.find(function (p) { return parseInt(p.id, 10) === eventView.project[0]; })
            : undefined;
        var projectSlugs = eventView.project
            .map(function (projectId) { return projects.find(function (p) { return parseInt(p.id, 10) === projectId; }); })
            .filter(function (p) { return p !== undefined; })
            .map(function (p) { return p.slug; });
        return (<SentryDocumentTitle title={this.getDocumentTitle()} orgSlug={organization.slug} projectSlug={forceProject === null || forceProject === void 0 ? void 0 : forceProject.slug}>
        <Feature features={['performance-tag-page']} organization={organization} renderDisabled={this.renderNoAccess}>
          <GlobalSelectionHeader lockedMessageSubject={t('transaction')} shouldForceProject={shouldForceProject} forceProject={forceProject} specificProjectSlugs={projectSlugs} disableMultipleProjectSelection showProjectSettingsLink>
            <StyledPageContent>
              <LightWeightNoProjectMessage organization={organization}>
                <TagsPageContent location={location} eventView={eventView} transactionName={transactionName} organization={organization} projects={projects}/>
              </LightWeightNoProjectMessage>
            </StyledPageContent>
          </GlobalSelectionHeader>
        </Feature>
      </SentryDocumentTitle>);
    };
    return TransactionTags;
}(Component));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
function generateTagsEventView(location, transactionName) {
    if (transactionName === undefined) {
        return undefined;
    }
    var query = decodeScalar(location.query.query, '');
    var conditions = tokenizeSearch(query);
    var eventView = EventView.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields: ['transaction.duration'],
        query: conditions.formatString(),
        projects: [],
    }, location);
    eventView.additionalConditions.setTagValues('event.type', ['transaction']);
    eventView.additionalConditions.setTagValues('transaction', [transactionName]);
    return eventView;
}
export default withGlobalSelection(withProjects(withOrganization(TransactionTags)));
var templateObject_1;
//# sourceMappingURL=index.jsx.map