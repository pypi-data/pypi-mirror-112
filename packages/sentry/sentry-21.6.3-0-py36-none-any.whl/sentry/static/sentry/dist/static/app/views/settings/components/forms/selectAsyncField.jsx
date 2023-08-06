import { __extends, __rest } from "tslib";
import * as React from 'react';
import SelectAsyncControl from 'app/components/forms/selectAsyncControl';
import InputField from 'app/views/settings/components/forms/inputField';
var SelectAsyncField = /** @class */ (function (_super) {
    __extends(SelectAsyncField, _super);
    function SelectAsyncField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            results: [],
        };
        // need to map the option object to the value
        // this is essentially the same code from ./selectField handleChange()
        _this.handleChange = function (onBlur, onChange, optionObj, event) {
            var value = optionObj.value;
            if (!optionObj) {
                value = optionObj;
            }
            else if (_this.props.multiple && Array.isArray(optionObj)) {
                // List of optionObjs
                value = optionObj.map(function (_a) {
                    var val = _a.value;
                    return val;
                });
            }
            else if (!Array.isArray(optionObj)) {
                value = optionObj.value;
            }
            onChange === null || onChange === void 0 ? void 0 : onChange(value, event);
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(value, event);
        };
        return _this;
    }
    SelectAsyncField.prototype.findValue = function (propsValue) {
        /**
         * The propsValue is the `id` of the object (user, team, etc), and
         * react-select expects a full value object: {value: "id", label: "name"}
         *
         * Returning {} here will show the user a dropdown with "No options".
         **/
        return this.state.results.find(function (_a) {
            var value = _a.value;
            return value === propsValue;
        }) || {};
    };
    SelectAsyncField.prototype.render = function () {
        var _this = this;
        var otherProps = __rest(this.props, []);
        return (<InputField {...otherProps} field={function (_a) {
                var onChange = _a.onChange, onBlur = _a.onBlur, _required = _a.required, onResults = _a.onResults, value = _a.value, props = __rest(_a, ["onChange", "onBlur", "required", "onResults", "value"]);
                return (<SelectAsyncControl {...props} onChange={_this.handleChange.bind(_this, onBlur, onChange)} onResults={function (data) {
                        var results = onResults(data);
                        _this.setState({ results: results });
                        return results;
                    }} onSelectResetsInput onCloseResetsInput={false} onBlurResetsInput={false} value={_this.findValue(value)}/>);
            }}/>);
    };
    return SelectAsyncField;
}(React.Component));
export default SelectAsyncField;
//# sourceMappingURL=selectAsyncField.jsx.map