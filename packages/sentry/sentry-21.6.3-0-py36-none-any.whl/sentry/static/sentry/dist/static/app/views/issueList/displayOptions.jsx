import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import { getDisplayLabel, IssueDisplayOptions } from 'app/views/issueList/utils';
var IssueListDisplayOptions = function (_a) {
    var onDisplayChange = _a.onDisplayChange, display = _a.display, hasSessions = _a.hasSessions, hasMultipleProjectsSelected = _a.hasMultipleProjectsSelected;
    var getMenuItem = function (key) {
        var tooltipText;
        var disabled = false;
        if (key === IssueDisplayOptions.SESSIONS) {
            if (hasMultipleProjectsSelected) {
                tooltipText = t('This option is not available when multiple projects are selected.');
                disabled = true;
            }
            else if (!hasSessions) {
                tooltipText = t('This option is not available because there is no session data in the selected time period.');
                disabled = true;
            }
        }
        return (<DropdownItem onSelect={onDisplayChange} eventKey={key} isActive={key === display} disabled={disabled}>
        <StyledTooltip containerDisplayMode="block" position="top" title={tooltipText} disabled={!tooltipText}>
          {getDisplayLabel(key)}
        </StyledTooltip>
      </DropdownItem>);
    };
    return (<DropdownControl buttonProps={{ prefix: t('Display') }} buttonTooltipTitle={display === IssueDisplayOptions.SESSIONS
            ? t('This shows the event count as a percent of sessions in the same time period.')
            : null} label={getDisplayLabel(display)}>
      <React.Fragment>
        {getMenuItem(IssueDisplayOptions.EVENTS)}
        {getMenuItem(IssueDisplayOptions.SESSIONS)}
      </React.Fragment>
    </DropdownControl>);
};
var StyledTooltip = styled(Tooltip)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
export default IssueListDisplayOptions;
var templateObject_1;
//# sourceMappingURL=displayOptions.jsx.map