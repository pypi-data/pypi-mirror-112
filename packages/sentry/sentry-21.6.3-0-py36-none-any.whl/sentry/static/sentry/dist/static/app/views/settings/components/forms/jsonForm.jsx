import { __assign, __extends, __read, __rest, __spreadArray } from "tslib";
import * as React from 'react';
import { withRouter } from 'react-router';
import * as Sentry from '@sentry/react';
import scrollToElement from 'scroll-to-element';
import { defined } from 'app/utils';
import { sanitizeQuerySelector } from 'app/utils/sanitizeQuerySelector';
import FormPanel from './formPanel';
var JsonForm = /** @class */ (function (_super) {
    __extends(JsonForm, _super);
    function JsonForm() {
        var _a;
        var _this = _super.apply(this, __spreadArray([], __read(arguments))) || this;
        _this.state = {
            // location.hash is optional because of tests.
            highlighted: (_a = _this.props.location) === null || _a === void 0 ? void 0 : _a.hash,
        };
        return _this;
    }
    JsonForm.prototype.componentDidMount = function () {
        this.scrollToHash();
    };
    JsonForm.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (this.props.location.hash !== nextProps.location.hash) {
            var hash = nextProps.location.hash;
            this.scrollToHash(hash);
            this.setState({ highlighted: hash });
        }
    };
    JsonForm.prototype.scrollToHash = function (toHash) {
        var _a;
        // location.hash is optional because of tests.
        var hash = toHash || ((_a = this.props.location) === null || _a === void 0 ? void 0 : _a.hash);
        if (!hash) {
            return;
        }
        // Push onto callback queue so it runs after the DOM is updated,
        // this is required when navigating from a different page so that
        // the element is rendered on the page before trying to getElementById.
        try {
            scrollToElement(sanitizeQuerySelector(decodeURIComponent(hash)), {
                align: 'middle',
                offset: -100,
            });
        }
        catch (err) {
            Sentry.captureException(err);
        }
    };
    JsonForm.prototype.shouldDisplayForm = function (fields) {
        var fieldsWithVisibleProp = fields.filter(function (field) { return typeof field !== 'function' && defined(field === null || field === void 0 ? void 0 : field.visible); });
        if (fields.length === fieldsWithVisibleProp.length) {
            var _a = this.props, additionalFieldProps_1 = _a.additionalFieldProps, props_1 = __rest(_a, ["additionalFieldProps"]);
            var areAllFieldsHidden = fieldsWithVisibleProp.every(function (field) {
                if (typeof field.visible === 'function') {
                    return !field.visible(__assign(__assign({}, props_1), additionalFieldProps_1));
                }
                return !field.visible;
            });
            return !areAllFieldsHidden;
        }
        return true;
    };
    JsonForm.prototype.renderForm = function (_a) {
        var fields = _a.fields, formPanelProps = _a.formPanelProps, title = _a.title;
        var shouldDisplayForm = this.shouldDisplayForm(fields);
        if (!shouldDisplayForm &&
            !(formPanelProps === null || formPanelProps === void 0 ? void 0 : formPanelProps.renderFooter) &&
            !(formPanelProps === null || formPanelProps === void 0 ? void 0 : formPanelProps.renderHeader)) {
            return null;
        }
        return <FormPanel title={title} fields={fields} {...formPanelProps}/>;
    };
    JsonForm.prototype.render = function () {
        var _this = this;
        var _a = this.props, access = _a.access, fields = _a.fields, title = _a.title, forms = _a.forms, disabled = _a.disabled, features = _a.features, additionalFieldProps = _a.additionalFieldProps, renderFooter = _a.renderFooter, renderHeader = _a.renderHeader, _location = _a.location, otherProps = __rest(_a, ["access", "fields", "title", "forms", "disabled", "features", "additionalFieldProps", "renderFooter", "renderHeader", "location"]);
        var formPanelProps = {
            access: access,
            disabled: disabled,
            features: features,
            additionalFieldProps: additionalFieldProps,
            renderFooter: renderFooter,
            renderHeader: renderHeader,
            highlighted: this.state.highlighted,
        };
        return (<div {...otherProps}>
        {typeof forms !== 'undefined' &&
                forms.map(function (formGroup, i) { return (<React.Fragment key={i}>
              {_this.renderForm(__assign({ formPanelProps: formPanelProps }, formGroup))}
            </React.Fragment>); })}
        {typeof forms === 'undefined' &&
                typeof fields !== 'undefined' &&
                this.renderForm({ fields: fields, formPanelProps: formPanelProps, title: title })}
      </div>);
    };
    return JsonForm;
}(React.Component));
export default withRouter(JsonForm);
//# sourceMappingURL=jsonForm.jsx.map