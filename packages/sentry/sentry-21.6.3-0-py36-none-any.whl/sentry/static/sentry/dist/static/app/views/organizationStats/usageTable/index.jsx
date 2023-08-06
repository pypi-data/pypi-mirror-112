import { __extends, __makeTemplateObject } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import ErrorPanel from 'app/components/charts/errorPanel';
import IdBadge from 'app/components/idBadge';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
import { SettingsIconLink } from 'app/components/organizations/headerItem';
import { Panel } from 'app/components/panels';
import PanelTable from 'app/components/panels/panelTable';
import { IconSettings, IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import { DataCategory } from 'app/types';
import theme from 'app/utils/theme';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { formatUsageWithUnits } from '../utils';
var DOCS_URL = 'https://docs.sentry.io/product/accounts/membership/#restricting-access';
var UsageTable = /** @class */ (function (_super) {
    __extends(UsageTable, _super);
    function UsageTable() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getErrorMessage = function (errorMessage) {
            if (errorMessage.projectStats.responseJSON.detail === 'No projects available') {
                return (<EmptyMessage icon={<IconWarning color="gray300" size="48"/>} title={t("You don't have access to any projects, or your organization has no projects.")} description={tct('Learn more about [link:Project Access]', {
                        link: <ExternalLink href={DOCS_URL}/>,
                    })}/>);
            }
            return <IconWarning color="gray300" size="48"/>;
        };
        return _this;
    }
    Object.defineProperty(UsageTable.prototype, "formatUsageOptions", {
        get: function () {
            var dataCategory = this.props.dataCategory;
            return {
                isAbbreviated: dataCategory !== DataCategory.ATTACHMENTS,
                useUnitScaling: dataCategory === DataCategory.ATTACHMENTS,
            };
        },
        enumerable: false,
        configurable: true
    });
    UsageTable.prototype.renderTableRow = function (stat) {
        var dataCategory = this.props.dataCategory;
        var project = stat.project, total = stat.total, accepted = stat.accepted, filtered = stat.filtered, dropped = stat.dropped;
        return [
            <CellProject key={0}>
        <Link to={stat.projectLink}>
          <StyledIdBadge avatarSize={16} disableLink hideOverflow project={project} displayName={project.slug}/>
        </Link>
        <SettingsIconLink to={stat.projectSettingsLink}>
          <IconSettings size={theme.iconSizes.sm}/>
        </SettingsIconLink>
      </CellProject>,
            <CellStat key={1}>
        {formatUsageWithUnits(total, dataCategory, this.formatUsageOptions)}
      </CellStat>,
            <CellStat key={2}>
        {formatUsageWithUnits(accepted, dataCategory, this.formatUsageOptions)}
      </CellStat>,
            <CellStat key={3}>
        {formatUsageWithUnits(filtered, dataCategory, this.formatUsageOptions)}
      </CellStat>,
            <CellStat key={4}>
        {formatUsageWithUnits(dropped, dataCategory, this.formatUsageOptions)}
      </CellStat>,
        ];
    };
    UsageTable.prototype.render = function () {
        var _this = this;
        var _a = this.props, isEmpty = _a.isEmpty, isLoading = _a.isLoading, isError = _a.isError, errors = _a.errors, headers = _a.headers, usageStats = _a.usageStats;
        if (isError) {
            return (<Panel>
          <ErrorPanel height="256px">{this.getErrorMessage(errors)}</ErrorPanel>
        </Panel>);
        }
        return (<StyledPanelTable isLoading={isLoading} isEmpty={isEmpty} headers={headers}>
        {usageStats.map(function (s) { return _this.renderTableRow(s); })}
      </StyledPanelTable>);
    };
    return UsageTable;
}(React.Component));
export default UsageTable;
export var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: repeat(5, auto);\n\n  @media (min-width: ", ") {\n    grid-template-columns: auto repeat(4, 100px);\n  }\n"], ["\n  grid-template-columns: repeat(5, auto);\n\n  @media (min-width: ", ") {\n    grid-template-columns: auto repeat(4, 100px);\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
export var CellStat = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-shrink: 1;\n  text-align: right;\n"], ["\n  flex-shrink: 1;\n  text-align: right;\n"])));
export var CellProject = styled(CellStat)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  text-align: left;\n"], ["\n  display: flex;\n  align-items: center;\n  text-align: left;\n"])));
export var CellSetting = styled(CellStat)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  padding: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  padding: 0;\n"])));
var StyledIdBadge = styled(IdBadge)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  overflow: hidden;\n  white-space: nowrap;\n  flex-shrink: 1;\n"], ["\n  overflow: hidden;\n  white-space: nowrap;\n  flex-shrink: 1;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map