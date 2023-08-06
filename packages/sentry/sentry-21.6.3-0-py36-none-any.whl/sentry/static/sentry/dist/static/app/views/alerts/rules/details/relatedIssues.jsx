import { __assign, __extends, __makeTemplateObject } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { SectionHeading } from 'app/components/charts/styles';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import GroupList from 'app/components/issues/groupList';
import { Panel, PanelBody } from 'app/components/panels';
import Tooltip from 'app/components/tooltip';
import { IconInfo } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { DATASET_EVENT_TYPE_FILTERS } from 'app/views/alerts/incidentRules/constants';
var RelatedIssues = /** @class */ (function (_super) {
    __extends(RelatedIssues, _super);
    function RelatedIssues() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderEmptyMessage = function () {
            return (<Panel>
        <PanelBody>
          <EmptyStateWarning small withIcon={false}>
            {t('No issues for this alert rule')}
          </EmptyStateWarning>
        </PanelBody>
      </Panel>);
        };
        return _this;
    }
    RelatedIssues.prototype.render = function () {
        var _a;
        var _b = this.props, rule = _b.rule, projects = _b.projects, organization = _b.organization, timePeriod = _b.timePeriod;
        var start = timePeriod.start, end = timePeriod.end;
        var path = "/organizations/" + organization.slug + "/issues/";
        var queryParams = __assign(__assign({ start: start, end: end, groupStatsPeriod: 'auto', limit: 5 }, (rule.environment ? { environment: rule.environment } : {})), { sort: rule.aggregate === 'count_unique(user)' ? 'user' : 'freq', query: [
                rule.query,
                ((_a = rule.eventTypes) === null || _a === void 0 ? void 0 : _a.length)
                    ? "event.type:[" + rule.eventTypes.join(", ") + "]"
                    : DATASET_EVENT_TYPE_FILTERS[rule.dataset],
            ].join(' '), project: projects.map(function (project) { return project.id; }) });
        var issueSearch = {
            pathname: "/organizations/" + organization.slug + "/issues/",
            query: queryParams,
        };
        return (<Fragment>
        <ControlsWrapper>
          <StyledSectionHeading>
            {t('Related Issues')}
            <Tooltip title={t('Top issues containing events matching the metric.')}>
              <IconInfo size="xs" color="gray200"/>
            </Tooltip>
          </StyledSectionHeading>
          <Button data-test-id="issues-open" size="small" to={issueSearch}>
            {t('Open in Issues')}
          </Button>
        </ControlsWrapper>

        <TableWrapper>
          <GroupList orgId={organization.slug} endpointPath={path} queryParams={queryParams} query={"start=" + start + "&end=" + end + "&groupStatsPeriod=auto"} canSelectGroups={false} renderEmptyMessage={this.renderEmptyMessage} withChart withPagination={false} useFilteredStats customStatsPeriod={timePeriod} useTintRow={false}/>
        </TableWrapper>
      </Fragment>);
    };
    return RelatedIssues;
}(Component));
var StyledSectionHeading = styled(SectionHeading)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var ControlsWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space(1));
var TableWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"], ["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"])), space(4), Panel, space(1));
export default RelatedIssues;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=relatedIssues.jsx.map