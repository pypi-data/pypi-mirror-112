import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import DropdownButton from 'app/components/dropdownButton';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
function DropDownButton(_a) {
    var isOpen = _a.isOpen, getActorProps = _a.getActorProps, checkedQuantity = _a.checkedQuantity;
    if (checkedQuantity > 0) {
        return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} size="small" hideBottomBorder={false} priority="primary">
        {tn('%s Active Filter', '%s Active Filters', checkedQuantity)}
      </StyledDropdownButton>);
    }
    return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} size="small" hideBottomBorder={false}>
      {t('Filter By')}
    </StyledDropdownButton>);
}
export default DropDownButton;
var StyledDropdownButton = styled(DropdownButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  z-index: ", ";\n  border-radius: ", ";\n  max-width: 200px;\n  white-space: nowrap;\n\n  ", "\n\n  @media (min-width: ", ") {\n    border-right: 0;\n    border-top-right-radius: 0;\n    border-bottom-right-radius: 0;\n  }\n"], ["\n  z-index: ", ";\n  border-radius: ", ";\n  max-width: 200px;\n  white-space: nowrap;\n\n  ", "\n\n  @media (min-width: ", ") {\n    border-right: 0;\n    border-top-right-radius: 0;\n    border-bottom-right-radius: 0;\n  }\n"])), function (p) { return p.theme.zIndex.dropdownAutocomplete.actor; }, function (p) { return p.theme.borderRadius; }, function (p) {
    return p.isOpen &&
        "\n      :before,\n      :after {\n        position: absolute;\n        bottom: calc(" + space(0.5) + " + 1px);\n        right: 32px;\n        content: '';\n        width: 16px;\n        border: 8px solid transparent;\n        transform: translateY(calc(50% + 2px));\n        right: 9px;\n        border-bottom-color: " + p.theme.backgroundSecondary + ";\n      }\n\n      :before {\n        transform: translateY(calc(50% + 1px));\n        border-bottom-color: " + p.theme.border + ";\n      }\n    ";
}, function (p) { return p.theme.breakpoints[0]; });
var templateObject_1;
//# sourceMappingURL=dropDownButton.jsx.map