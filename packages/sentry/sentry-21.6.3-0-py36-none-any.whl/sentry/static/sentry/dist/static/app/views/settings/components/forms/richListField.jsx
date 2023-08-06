import { __extends, __makeTemplateObject, __read, __rest, __spreadArray } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import Button from 'app/components/button';
import ConfirmDelete from 'app/components/confirmDelete';
import DropdownAutoComplete from 'app/components/dropdownAutoComplete';
import DropdownButton from 'app/components/dropdownButton';
import Tooltip from 'app/components/tooltip';
import { IconAdd, IconDelete, IconSettings, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import InputField from 'app/views/settings/components/forms/inputField';
var RichList = /** @class */ (function (_super) {
    __extends(RichList, _super);
    function RichList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.triggerChange = function (items) {
            var _a, _b, _c, _d;
            if (!_this.props.disabled) {
                (_b = (_a = _this.props).onChange) === null || _b === void 0 ? void 0 : _b.call(_a, items, {});
                (_d = (_c = _this.props).onBlur) === null || _d === void 0 ? void 0 : _d.call(_c, items, {});
            }
        };
        _this.addItem = function (data) {
            var items = __spreadArray(__spreadArray([], __read(_this.props.value)), [data]);
            _this.triggerChange(items);
        };
        _this.updateItem = function (data, index) {
            var items = __spreadArray([], __read(_this.props.value));
            items.splice(index, 1, data);
            _this.triggerChange(items);
        };
        _this.removeItem = function (index) {
            var items = __spreadArray([], __read(_this.props.value));
            items.splice(index, 1);
            _this.triggerChange(items);
        };
        _this.onSelectDropdownItem = function (item) {
            if (!_this.props.disabled && _this.props.onAddItem) {
                _this.props.onAddItem(item, _this.addItem);
            }
        };
        _this.onEditItem = function (item, index) {
            var _a, _b;
            if (!_this.props.disabled) {
                (_b = (_a = _this.props).onEditItem) === null || _b === void 0 ? void 0 : _b.call(_a, omit(item, 'error'), function (data) {
                    return _this.updateItem(data, index);
                });
            }
        };
        _this.onRemoveItem = function (item, index) {
            var _a, _b;
            if (!_this.props.disabled) {
                (_b = (_a = _this.props).onRemoveItem) === null || _b === void 0 ? void 0 : _b.call(_a, item, function () { return _this.removeItem(index); });
            }
        };
        _this.renderItem = function (item, index) {
            var _a = _this.props, disabled = _a.disabled, renderItem = _a.renderItem, onEditItem = _a.onEditItem, removeConfirm = _a.removeConfirm;
            var error = item.error;
            var warning = item.warning;
            return (<Item disabled={!!disabled} key={index} onClick={(error || warning) && onEditItem && !disabled
                    ? function () { return _this.onEditItem(item, index); }
                    : undefined}>
        {renderItem(item)}
        {error ? (<StatusIcon>
            <Tooltip title={error} containerDisplayMode="inline-flex">
              <IconWarning color="red300"/>
            </Tooltip>
          </StatusIcon>) : warning ? (<StatusIcon>
            <Tooltip title={warning} containerDisplayMode="inline-flex">
              <IconWarning color="yellow300"/>
            </Tooltip>
          </StatusIcon>) : (onEditItem && (<SettingsButton onClick={function () { return _this.onEditItem(item, index); }} disabled={disabled} icon={<IconSettings />} size="zero" label={t('Edit Item')} borderless/>))}
        <DeleteButtonWrapper onClick={function (event) {
                    event.preventDefault();
                    event.stopPropagation();
                }}>
          {removeConfirm ? (<ConfirmDelete confirmText={t('Remove')} disabled={disabled} {...removeConfirm} confirmInput={item.name} priority="danger" onConfirm={function () {
                        var _a;
                        _this.onRemoveItem(item, index);
                        (_a = removeConfirm.onConfirm) === null || _a === void 0 ? void 0 : _a.call(removeConfirm, item);
                    }}>
              <DeleteButton disabled={disabled} size="zero" icon={<IconDelete size="xs"/>} label={t('Delete Item')} borderless/>
            </ConfirmDelete>) : (<DeleteButton disabled={disabled} size="zero" icon={<IconDelete size="xs"/>} label={t('Delete Item')} onClick={function () { return _this.onRemoveItem(item, index); }} borderless/>)}
        </DeleteButtonWrapper>
      </Item>);
        };
        _this.renderDropdown = function () {
            var disabled = _this.props.disabled;
            return (<DropdownAutoComplete {..._this.props.addDropdown} disabled={disabled} onSelect={_this.onSelectDropdownItem}>
        {function (_a) {
                    var isOpen = _a.isOpen;
                    return (<DropdownButton disabled={disabled} icon={<IconAdd size="xs" isCircled/>} isOpen={isOpen} size="small">
            {_this.props.addButtonText}
          </DropdownButton>);
                }}
      </DropdownAutoComplete>);
        };
        return _this;
    }
    RichList.prototype.render = function () {
        return (<ItemList>
        {this.props.value.map(this.renderItem)}
        {this.renderDropdown()}
      </ItemList>);
    };
    RichList.defaultProps = {
        addButtonText: t('Add item'),
        onAddItem: function (item, addItem) { return addItem(item); },
        onRemoveItem: function (item, removeItem) { return removeItem(item); },
    };
    return RichList;
}(React.PureComponent));
/**
 * A 'rich' dropdown that provides action hooks for when item
 * are selected/created/removed.
 *
 * An example usage is the debug image selector where each 'source' option
 * requires additional configuration data.
 */
export default function RichListField(props) {
    return (<InputField {...props} field={function (fieldProps) {
            var value = fieldProps.value, otherProps = __rest(fieldProps, ["value"]);
            // We must not render this field until `setValue` has been applied by the
            // model, which is done after the field is mounted for the first time. To
            // check this, we cannot use Array.isArray because the value passed in by
            // the model might actually be an ObservableArray.
            if (typeof value === 'string' || (value === null || value === void 0 ? void 0 : value.length) === undefined) {
                return null;
            }
            return <RichList {...otherProps} value={__spreadArray([], __read(value))}/>;
        }}/>);
}
var ItemList = styled('ul')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  align-items: flex-start;\n  padding: 0;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  align-items: flex-start;\n  padding: 0;\n"])));
var Item = styled('li')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n  align-items: center;\n  border-radius: ", ";\n  font-size: ", ";\n  font-weight: 600;\n  line-height: ", ";\n  text-transform: none;\n  margin: 0 10px 5px 0;\n  white-space: nowrap;\n  padding: ", " 36px ", " ", ";\n  /* match adjacent elements */\n  height: 32px;\n  overflow: hidden;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  opacity: ", ";\n  cursor: ", ";\n"], ["\n  position: relative;\n  display: flex;\n  align-items: center;\n  border-radius: ", ";\n  font-size: ", ";\n  font-weight: 600;\n  line-height: ", ";\n  text-transform: none;\n  margin: 0 10px 5px 0;\n  white-space: nowrap;\n  padding: ", " 36px ", " ", ";\n  /* match adjacent elements */\n  height: 32px;\n  overflow: hidden;\n  background-color: ", ";\n  border: 1px solid ", ";\n  color: ", ";\n  opacity: ", ";\n  cursor: ", ";\n"])), function (p) { return p.theme.button.borderRadius; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.fontSizeSmall; }, space(1), space(1), space(1.5), function (p) { return p.theme.button.default.background; }, function (p) { return p.theme.button.default.border; }, function (p) { return p.theme.button.default.color; }, function (p) { return (p.disabled ? 0.65 : null); }, function (p) { return (p.disabled ? 'not-allowed' : p.onClick ? 'pointer' : 'default'); });
var ItemButton = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  &:hover {\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return (p.disabled ? p.theme.gray300 : p.theme.button.default.color); });
var SettingsButton = styled(ItemButton)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-left: 10px;\n"], ["\n  margin-left: 10px;\n"])));
var DeleteButton = styled(ItemButton)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  height: 100%;\n  width: 100%;\n"], ["\n  height: 100%;\n  width: 100%;\n"])));
var StatusIcon = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-left: 10px;\n  display: inline-flex;\n"], ["\n  margin-left: 10px;\n  display: inline-flex;\n"])));
var DeleteButtonWrapper = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  position: absolute;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  z-index: 1;\n  right: 0;\n  width: 36px;\n  height: 100%;\n"], ["\n  position: absolute;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  z-index: 1;\n  right: 0;\n  width: 36px;\n  height: 100%;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=richListField.jsx.map