import { __makeTemplateObject } from "tslib";
import { useSortable } from '@dnd-kit/sortable';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { IconAdd } from 'app/icons';
import { DisplayType } from './types';
import WidgetWrapper from './widgetWrapper';
export var ADD_WIDGET_BUTTON_DRAG_ID = 'add-widget-button';
var initialStyles = {
    x: 0,
    y: 0,
    scaleX: 1,
    scaleY: 1,
};
function AddWidget(_a) {
    var onAddWidget = _a.onAddWidget, onOpenWidgetBuilder = _a.onOpenWidgetBuilder, orgFeatures = _a.orgFeatures;
    var onClick = orgFeatures.includes('metrics') ? onOpenWidgetBuilder : onAddWidget;
    var _b = useSortable({
        disabled: true,
        id: ADD_WIDGET_BUTTON_DRAG_ID,
        transition: null,
    }), setNodeRef = _b.setNodeRef, transform = _b.transform;
    return (<WidgetWrapper key="add" ref={setNodeRef} displayType={DisplayType.BIG_NUMBER} layoutId={ADD_WIDGET_BUTTON_DRAG_ID} style={{ originX: 0, originY: 0 }} animate={transform
            ? {
                x: transform.x,
                y: transform.y,
                scaleX: (transform === null || transform === void 0 ? void 0 : transform.scaleX) && transform.scaleX <= 1 ? transform.scaleX : 1,
                scaleY: (transform === null || transform === void 0 ? void 0 : transform.scaleY) && transform.scaleY <= 1 ? transform.scaleY : 1,
            }
            : initialStyles} transition={{
            duration: 0.25,
        }}>
      <InnerWrapper onClick={onClick}>
        <AddButton data-test-id="widget-add" onClick={onClick} icon={<IconAdd size="lg" isCircled color="inactive"/>}/>
      </InnerWrapper>
    </WidgetWrapper>);
}
export default AddWidget;
var AddButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border: none;\n  &,\n  &:focus,\n  &:active,\n  &:hover {\n    background: transparent;\n    box-shadow: none;\n  }\n"], ["\n  border: none;\n  &,\n  &:focus,\n  &:active,\n  &:hover {\n    background: transparent;\n    box-shadow: none;\n  }\n"])));
var InnerWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 100%;\n  height: 110px;\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  cursor: ", ";\n"], ["\n  width: 100%;\n  height: 110px;\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  cursor: ", ";\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return (p.onClick ? 'pointer' : ''); });
var templateObject_1, templateObject_2;
//# sourceMappingURL=addWidget.jsx.map