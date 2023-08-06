import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import space from 'app/styles/space';
var GroupListHeader = function (_a) {
    var _b = _a.withChart, withChart = _b === void 0 ? true : _b, _c = _a.narrowGroups, narrowGroups = _c === void 0 ? false : _c;
    return (<PanelHeader disablePadding>
    <IssueWrapper>{t('Issue')}</IssueWrapper>
    {withChart && (<ChartWrapper className={"hidden-xs hidden-sm " + (narrowGroups ? 'hidden-md' : '')}>
        {t('Graph')}
      </ChartWrapper>)}
    <EventUserWrapper>{t('events')}</EventUserWrapper>
    <EventUserWrapper>{t('users')}</EventUserWrapper>
    <AssigneeWrapper className="hidden-xs hidden-sm toolbar-header">
      {t('Assignee')}
    </AssigneeWrapper>
  </PanelHeader>);
};
export default GroupListHeader;
var Heading = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-self: center;\n  margin: 0 ", ";\n"], ["\n  display: flex;\n  align-self: center;\n  margin: 0 ", ";\n"])), space(2));
var IssueWrapper = styled(Heading)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n  width: 66.66%;\n\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n"], ["\n  flex: 1;\n  width: 66.66%;\n\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var EventUserWrapper = styled(Heading)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  justify-content: flex-end;\n  width: 60px;\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"], ["\n  justify-content: flex-end;\n  width: 60px;\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"])), function (p) { return p.theme.breakpoints[3]; });
var ChartWrapper = styled(Heading)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  justify-content: space-between;\n  width: 160px;\n"], ["\n  justify-content: space-between;\n  width: 160px;\n"])));
var AssigneeWrapper = styled(Heading)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  justify-content: flex-end;\n  width: 80px;\n"], ["\n  justify-content: flex-end;\n  width: 80px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=groupListHeader.jsx.map