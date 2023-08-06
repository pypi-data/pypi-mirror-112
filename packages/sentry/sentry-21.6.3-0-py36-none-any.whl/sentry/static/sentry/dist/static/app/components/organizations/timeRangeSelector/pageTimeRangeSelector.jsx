import { __makeTemplateObject, __read, __rest } from "tslib";
import { useState } from 'react';
import styled from '@emotion/styled';
import TimeRangeSelector from 'app/components/organizations/timeRangeSelector';
import { Panel } from 'app/components/panels';
import { DEFAULT_RELATIVE_PERIODS } from 'app/constants';
import { t } from 'app/locale';
import space from 'app/styles/space';
function PageTimeRangeSelector(_a) {
    var className = _a.className, props = __rest(_a, ["className"]);
    var _b = __read(useState(false), 2), isCalendarOpen = _b[0], setIsCalendarOpen = _b[1];
    return (<DropdownDate className={className} isCalendarOpen={isCalendarOpen}>
      <TimeRangeSelector label={<DropdownLabel>{t('Date Range:')}</DropdownLabel>} onToggleSelector={function (isOpen) { return setIsCalendarOpen(isOpen); }} relativeOptions={DEFAULT_RELATIVE_PERIODS} {...props}/>
    </DropdownDate>);
}
var DropdownDate = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  height: 42px;\n\n  background: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  padding: 0;\n  margin: 0;\n  font-size: ", ";\n  color: ", ";\n\n  /* TimeRangeRoot in TimeRangeSelector */\n  > div {\n    width: 100%;\n    align-self: stretch;\n  }\n\n  /* StyledItemHeader used to show selected value of TimeRangeSelector */\n  > div > div:first-child {\n    padding: 0 ", ";\n  }\n\n  /* Menu that dropdowns from TimeRangeSelector */\n  > div > div:last-child {\n    /* Remove awkward 1px width difference on dropdown due to border */\n    box-sizing: content-box;\n    font-size: 1em;\n  }\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  height: 42px;\n\n  background: ", ";\n  border: 1px solid ", ";\n  border-radius: ", ";\n  padding: 0;\n  margin: 0;\n  font-size: ", ";\n  color: ", ";\n\n  /* TimeRangeRoot in TimeRangeSelector */\n  > div {\n    width: 100%;\n    align-self: stretch;\n  }\n\n  /* StyledItemHeader used to show selected value of TimeRangeSelector */\n  > div > div:first-child {\n    padding: 0 ", ";\n  }\n\n  /* Menu that dropdowns from TimeRangeSelector */\n  > div > div:last-child {\n    /* Remove awkward 1px width difference on dropdown due to border */\n    box-sizing: content-box;\n    font-size: 1em;\n  }\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) {
    return p.isCalendarOpen
        ? p.theme.borderRadius + " " + p.theme.borderRadius + " 0 0"
        : p.theme.borderRadius;
}, function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.textColor; }, space(2));
var DropdownLabel = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: left;\n  font-weight: 600;\n  color: ", ";\n\n  > span:last-child {\n    font-weight: 400;\n  }\n"], ["\n  text-align: left;\n  font-weight: 600;\n  color: ", ";\n\n  > span:last-child {\n    font-weight: 400;\n  }\n"])), function (p) { return p.theme.textColor; });
export default PageTimeRangeSelector;
var templateObject_1, templateObject_2;
//# sourceMappingURL=pageTimeRangeSelector.jsx.map