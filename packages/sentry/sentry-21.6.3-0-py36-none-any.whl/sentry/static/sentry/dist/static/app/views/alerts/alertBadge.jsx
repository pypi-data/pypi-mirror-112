import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { IconCheckmark, IconFire, IconIssues, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { IncidentStatus } from './types';
function AlertBadge(_a) {
    var status = _a.status, _b = _a.hideText, hideText = _b === void 0 ? false : _b, isIssue = _a.isIssue;
    var statusText = t('Resolved');
    var Icon = IconCheckmark;
    var color = 'green300';
    if (isIssue) {
        statusText = t('Issue');
        Icon = IconIssues;
        color = 'gray300';
    }
    else if (status === IncidentStatus.CRITICAL) {
        statusText = t('Critical');
        Icon = IconFire;
        color = 'red300';
    }
    else if (status === IncidentStatus.WARNING) {
        statusText = t('Warning');
        Icon = IconWarning;
        color = 'yellow300';
    }
    return (<Wrapper displayFlex={!hideText}>
      <AlertIconWrapper color={color} icon={Icon}>
        <Icon color="white"/>
      </AlertIconWrapper>

      {!hideText && <IncidentStatusValue color={color}>{statusText}</IncidentStatusValue>}
    </Wrapper>);
}
export default AlertBadge;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: ", ";\n  align-items: center;\n"], ["\n  display: ", ";\n  align-items: center;\n"])), function (p) { return (p.displayFlex ? "flex" : "block"); });
var AlertIconWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n  left: 3px;\n  min-width: 30px;\n\n  &:before {\n    content: '';\n    position: absolute;\n    width: 22px;\n    height: 22px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n\n  svg {\n    width: ", ";\n    z-index: 1;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n  left: 3px;\n  min-width: 30px;\n\n  &:before {\n    content: '';\n    position: absolute;\n    width: 22px;\n    height: 22px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n\n  svg {\n    width: ", ";\n    z-index: 1;\n  }\n"])), function (p) { return (p.icon === IconWarning ? undefined : 1); }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme[p.color]; }, function (p) { return (p.icon === IconIssues ? '11px' : '13px'); });
var IncidentStatusValue = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-left: ", ";\n  color: ", ";\n"], ["\n  margin-left: ", ";\n  color: ", ";\n"])), space(1), function (p) { return p.theme[p.color]; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=alertBadge.jsx.map