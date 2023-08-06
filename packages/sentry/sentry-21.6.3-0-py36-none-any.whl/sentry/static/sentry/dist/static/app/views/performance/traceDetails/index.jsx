import { __extends, __makeTemplateObject } from "tslib";
import { Component } from 'react';
import styled from '@emotion/styled';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import EventView from 'app/utils/discover/eventView';
import { TraceFullDetailedQuery } from 'app/utils/performance/quickTrace/traceFullQuery';
import TraceMetaQuery from 'app/utils/performance/quickTrace/traceMetaQuery';
import { decodeScalar } from 'app/utils/queryString';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import TraceDetailsContent from './content';
var TraceSummary = /** @class */ (function (_super) {
    __extends(TraceSummary, _super);
    function TraceSummary() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TraceSummary.prototype.getDocumentTitle = function () {
        return [t('Trace Details'), t('Performance')].join(' - ');
    };
    TraceSummary.prototype.getTraceSlug = function () {
        var traceSlug = this.props.params.traceSlug;
        return typeof traceSlug === 'string' ? traceSlug.trim() : '';
    };
    TraceSummary.prototype.getDateSelection = function () {
        var location = this.props.location;
        var queryParams = getParams(location.query, {
            allowAbsolutePageDatetime: true,
        });
        var start = decodeScalar(queryParams.start);
        var end = decodeScalar(queryParams.end);
        var statsPeriod = decodeScalar(queryParams.statsPeriod);
        return { start: start, end: end, statsPeriod: statsPeriod };
    };
    TraceSummary.prototype.getTraceEventView = function () {
        var traceSlug = this.getTraceSlug();
        var _a = this.getDateSelection(), start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod;
        return EventView.fromSavedQuery({
            id: undefined,
            name: "Events with Trace ID " + traceSlug,
            fields: ['title', 'event.type', 'project', 'timestamp'],
            orderby: '-timestamp',
            query: "trace:" + traceSlug,
            projects: [ALL_ACCESS_PROJECTS],
            version: 2,
            start: start,
            end: end,
            range: statsPeriod,
        });
    };
    TraceSummary.prototype.renderContent = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, params = _a.params;
        var traceSlug = this.getTraceSlug();
        var _b = this.getDateSelection(), start = _b.start, end = _b.end, statsPeriod = _b.statsPeriod;
        var dateSelected = Boolean(statsPeriod || (start && end));
        var content = function (_a) {
            var isLoading = _a.isLoading, error = _a.error, traces = _a.traces, meta = _a.meta;
            return (<TraceDetailsContent location={location} organization={organization} params={params} traceSlug={traceSlug} traceEventView={_this.getTraceEventView()} dateSelected={dateSelected} isLoading={isLoading} error={error} traces={traces} meta={meta}/>);
        };
        if (!dateSelected) {
            return content({
                isLoading: false,
                error: 'date selection not specified',
                traces: null,
                meta: null,
            });
        }
        return (<TraceFullDetailedQuery location={location} orgSlug={organization.slug} traceId={traceSlug} start={start} end={end} statsPeriod={statsPeriod}>
        {function (traceResults) { return (<TraceMetaQuery location={location} orgSlug={organization.slug} traceId={traceSlug} start={start} end={end} statsPeriod={statsPeriod}>
            {function (metaResults) {
                    return content({
                        isLoading: traceResults.isLoading || metaResults.isLoading,
                        error: traceResults.error || metaResults.error,
                        traces: traceResults.traces,
                        meta: metaResults.meta,
                    });
                }}
          </TraceMetaQuery>); }}
      </TraceFullDetailedQuery>);
    };
    TraceSummary.prototype.render = function () {
        var organization = this.props.organization;
        return (<SentryDocumentTitle title={this.getDocumentTitle()} orgSlug={organization.slug}>
        <StyledPageContent>
          <LightWeightNoProjectMessage organization={organization}>
            {this.renderContent()}
          </LightWeightNoProjectMessage>
        </StyledPageContent>
      </SentryDocumentTitle>);
    };
    return TraceSummary;
}(Component));
export default withOrganization(withApi(TraceSummary));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map