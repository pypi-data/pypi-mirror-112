import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import space from 'app/styles/space';
import GroupingComponentChildren from './groupingComponentChildren';
import GroupingComponentStacktrace from './groupingComponentStacktrace';
import { shouldInlineComponentValue } from './utils';
var GroupingComponent = function (_a) {
    var component = _a.component, showNonContributing = _a.showNonContributing;
    var shouldInlineValue = shouldInlineComponentValue(component);
    var GroupingComponentListItems = component.id === 'stacktrace'
        ? GroupingComponentStacktrace
        : GroupingComponentChildren;
    return (<GroupingComponentWrapper isContributing={component.contributes}>
      <span>
        {component.name || component.id}
        {component.hint && <GroupingHint>{" (" + component.hint + ")"}</GroupingHint>}
      </span>

      <GroupingComponentList isInline={shouldInlineValue}>
        <GroupingComponentListItems component={component} showNonContributing={showNonContributing}/>
      </GroupingComponentList>
    </GroupingComponentWrapper>);
};
var GroupingComponentList = styled('ul')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n  margin: 0;\n  list-style: none;\n  &,\n  & > li {\n    display: ", ";\n  }\n"], ["\n  padding: 0;\n  margin: 0;\n  list-style: none;\n  &,\n  & > li {\n    display: ", ";\n  }\n"])), function (p) { return (p.isInline ? 'inline' : 'block'); });
export var GroupingComponentListItem = styled('li')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: 0;\n  margin: ", " 0 ", " ", ";\n\n  ", "\n"], ["\n  padding: 0;\n  margin: ", " 0 ", " ", ";\n\n  ", "\n"])), space(0.25), space(0.25), space(1.5), function (p) {
    return p.isCollapsable &&
        "\n    border-left: 1px solid " + p.theme.innerBorder + ";\n    margin: 0 0 -" + space(0.25) + " " + space(1) + ";\n    padding-left: " + space(0.5) + ";\n  ";
});
export var GroupingValue = styled('code')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: inline-block;\n  margin: ", " ", " ", " 0;\n  font-size: ", ";\n  padding: 0 ", ";\n  background: rgba(112, 163, 214, 0.1);\n  color: ", ";\n\n  ", "\n"], ["\n  display: inline-block;\n  margin: ", " ", " ", " 0;\n  font-size: ", ";\n  padding: 0 ", ";\n  background: rgba(112, 163, 214, 0.1);\n  color: ", ";\n\n  ", "\n"])), space(0.25), space(0.5), space(0.25), function (p) { return p.theme.fontSizeSmall; }, space(0.25), function (p) { return p.theme.textColor; }, function (_a) {
    var valueType = _a.valueType;
    return (valueType === 'function' || valueType === 'symbol') &&
        "\n    font-weight: bold;\n    color: " + function (p) { return p.theme.textColor; } + ";\n  ";
});
var GroupingComponentWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n\n  ", ", button {\n    opacity: 1;\n  }\n"], ["\n  color: ", ";\n\n  ", ", button {\n    opacity: 1;\n  }\n"])), function (p) { return (p.isContributing ? null : p.theme.textColor); }, GroupingValue);
var GroupingHint = styled('small')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: 0.8em;\n"], ["\n  font-size: 0.8em;\n"])));
export default GroupingComponent;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=groupingComponent.jsx.map