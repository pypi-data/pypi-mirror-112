import { __extends } from "tslib";
import { Component } from 'react';
import Checkbox from 'app/components/checkbox';
import { t } from 'app/locale';
import SelectedGroupStore from 'app/stores/selectedGroupStore';
var GroupCheckBox = /** @class */ (function (_super) {
    __extends(GroupCheckBox, _super);
    function GroupCheckBox() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isSelected: SelectedGroupStore.isSelected(_this.props.id),
        };
        _this.unsubscribe = SelectedGroupStore.listen(function () {
            _this.onSelectedGroupChange();
        }, undefined);
        _this.handleSelect = function () {
            var id = _this.props.id;
            SelectedGroupStore.toggleSelect(id);
        };
        return _this;
    }
    GroupCheckBox.prototype.componentWillReceiveProps = function (nextProps) {
        if (nextProps.id !== this.props.id) {
            this.setState({
                isSelected: SelectedGroupStore.isSelected(nextProps.id),
            });
        }
    };
    GroupCheckBox.prototype.shouldComponentUpdate = function (_nextProps, nextState) {
        return nextState.isSelected !== this.state.isSelected;
    };
    GroupCheckBox.prototype.componentWillUnmount = function () {
        this.unsubscribe();
    };
    GroupCheckBox.prototype.onSelectedGroupChange = function () {
        var isSelected = SelectedGroupStore.isSelected(this.props.id);
        if (isSelected !== this.state.isSelected) {
            this.setState({
                isSelected: isSelected,
            });
        }
    };
    GroupCheckBox.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, id = _a.id;
        var isSelected = this.state.isSelected;
        return (<Checkbox aria-label={t('Select Issue')} value={id} checked={isSelected} onChange={this.handleSelect} disabled={disabled}/>);
    };
    return GroupCheckBox;
}(Component));
export default GroupCheckBox;
//# sourceMappingURL=groupCheckBox.jsx.map