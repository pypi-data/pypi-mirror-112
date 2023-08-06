import { __makeTemplateObject, __read, __spreadArray } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import CheckboxFancy from 'app/components/checkboxFancy/checkboxFancy';
import DropdownAutoComplete from 'app/components/dropdownAutoComplete';
import Highlight from 'app/components/highlight';
import TextOverflow from 'app/components/textOverflow';
import { IconChevron, IconClose } from 'app/icons';
import { t } from 'app/locale';
import { inputStyles } from 'app/styles/input';
import space from 'app/styles/space';
function GroupByField(_a) {
    var metricTags = _a.metricTags, _b = _a.groupBy, groupBy = _b === void 0 ? [] : _b, onChange = _a.onChange;
    var hasSelected = !!groupBy.length;
    function handleClick(tag) {
        if (groupBy.includes(tag)) {
            var filteredGroupBy = groupBy.filter(function (groupByOption) { return groupByOption !== tag; });
            onChange(filteredGroupBy);
            return;
        }
        onChange(__spreadArray([], __read(new Set(__spreadArray(__spreadArray([], __read(groupBy)), [tag])))));
    }
    function handleUnselectAll(event) {
        event.stopPropagation();
        onChange([]);
    }
    return (<DropdownAutoComplete searchPlaceholder={t('Search tag')} items={metricTags.map(function (metricTag) { return ({
            value: metricTag,
            searchKey: metricTag,
            label: function (_a) {
                var inputValue = _a.inputValue;
                return (<Item onClick={function () { return handleClick(metricTag); }}>
            <div>
              <Highlight text={inputValue}>{metricTag}</Highlight>
            </div>
            <CheckboxFancy isChecked={groupBy.includes(metricTag)}/>
          </Item>);
            },
        }); })} style={{
            width: '100%',
            borderRadius: 0,
        }} maxHeight={110}>
      {function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<Field {...getActorProps()} hasSelected={hasSelected} isOpen={isOpen}>
          {!hasSelected ? (<Placeholder>{t('Group by')}</Placeholder>) : (<React.Fragment>
              <StyledTextOverflow>
                {groupBy.map(function (groupByOption) { return groupByOption; }).join(',')}
              </StyledTextOverflow>
              <StyledClose color={hasSelected ? 'textColor' : 'gray300'} onClick={handleUnselectAll}/>
            </React.Fragment>)}
          <ChevronWrapper>
            <IconChevron direction={isOpen ? 'up' : 'down'} size="sm" color={isOpen ? 'textColor' : 'gray300'}/>
          </ChevronWrapper>
        </Field>);
        }}
    </DropdownAutoComplete>);
}
export default GroupByField;
var Field = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  padding: 0 10px;\n  min-width: 250px;\n  display: grid;\n  grid-template-columns: ", ";\n  resize: none;\n  overflow: hidden;\n  align-items: center;\n  ", "\n"], ["\n  ", ";\n  padding: 0 10px;\n  min-width: 250px;\n  display: grid;\n  grid-template-columns: ", ";\n  resize: none;\n  overflow: hidden;\n  align-items: center;\n  ", "\n"])), function (p) { return inputStyles(p); }, function (p) {
    return p.hasSelected ? '1fr max-content max-content' : '1fr  max-content';
}, function (p) {
    return p.isOpen &&
        "\n      border-bottom-left-radius: 0;\n      border-bottom-right-radius: 0;\n    ";
});
var Item = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  word-break: break-all;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  word-break: break-all;\n"])), space(1.5));
var ChevronWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: 14px;\n  height: 14px;\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  margin-left: ", ";\n"], ["\n  width: 14px;\n  height: 14px;\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  margin-left: ", ";\n"])), space(1));
var StyledClose = styled(IconClose)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  height: 100%;\n  width: 10px;\n  padding: ", " 0;\n  stroke-width: 1.5;\n  margin-left: ", ";\n  box-sizing: content-box;\n"], ["\n  height: 100%;\n  width: 10px;\n  padding: ", " 0;\n  stroke-width: 1.5;\n  margin-left: ", ";\n  box-sizing: content-box;\n"])), space(1), space(1));
var Placeholder = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex: 1;\n  color: ", ";\n  padding: 0 ", ";\n"], ["\n  flex: 1;\n  color: ", ";\n  padding: 0 ", ";\n"])), function (p) { return p.theme.gray200; }, space(0.25));
var StyledTextOverflow = styled(TextOverflow)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=groupByField.jsx.map