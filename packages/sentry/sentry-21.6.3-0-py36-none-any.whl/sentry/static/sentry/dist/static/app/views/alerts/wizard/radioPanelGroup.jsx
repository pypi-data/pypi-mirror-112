import { __makeTemplateObject, __read, __rest } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import Radio from 'app/components/radio';
import space from 'app/styles/space';
var RadioPanelGroup = function (_a) {
    var value = _a.value, choices = _a.choices, label = _a.label, onChange = _a.onChange, props = __rest(_a, ["value", "choices", "label", "onChange"]);
    return (<Container {...props} role="radiogroup" aria-labelledby={label}>
    {(choices || []).map(function (_a, index) {
            var _b = __read(_a, 3), id = _b[0], name = _b[1], extraContent = _b[2];
            return (<RadioPanel key={index}>
        <RadioLineItem role="radio" index={index} aria-checked={value === id}>
          <Radio radioSize="small" aria-label={id} checked={value === id} onChange={function (e) { return onChange(id, e); }}/>
          <div>{name}</div>
          {extraContent}
        </RadioLineItem>
      </RadioPanel>);
        })}
  </Container>);
};
export default RadioPanelGroup;
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: row;\n  grid-auto-rows: max-content;\n  grid-auto-columns: auto;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: row;\n  grid-auto-rows: max-content;\n  grid-auto-columns: auto;\n"])), space(1));
var RadioLineItem = styled('label')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", " ", ";\n  grid-template-columns: max-content auto max-content;\n  align-items: center;\n  cursor: pointer;\n  outline: none;\n  font-weight: normal;\n  margin: 0;\n  color: ", ";\n  transition: color 0.3s ease-in;\n  padding: 0;\n  position: relative;\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n\n  svg {\n    display: none;\n    opacity: 0;\n  }\n\n  &[aria-checked='true'] {\n    color: ", ";\n  }\n"], ["\n  display: grid;\n  grid-gap: ", " ", ";\n  grid-template-columns: max-content auto max-content;\n  align-items: center;\n  cursor: pointer;\n  outline: none;\n  font-weight: normal;\n  margin: 0;\n  color: ", ";\n  transition: color 0.3s ease-in;\n  padding: 0;\n  position: relative;\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n\n  svg {\n    display: none;\n    opacity: 0;\n  }\n\n  &[aria-checked='true'] {\n    color: ", ";\n  }\n"])), space(0.25), space(1), function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
var RadioPanel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=radioPanelGroup.jsx.map