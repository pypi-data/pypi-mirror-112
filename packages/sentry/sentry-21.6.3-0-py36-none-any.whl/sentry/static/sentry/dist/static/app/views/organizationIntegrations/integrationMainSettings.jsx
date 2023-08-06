import { __extends } from "tslib";
import React from 'react';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
var IntegrationMainSettings = /** @class */ (function (_super) {
    __extends(IntegrationMainSettings, _super);
    function IntegrationMainSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            integration: _this.props.integration,
        };
        _this.handleSubmitSuccess = function (data) {
            addSuccessMessage(t('Integration updated.'));
            _this.props.onUpdate();
            _this.setState({ integration: data });
        };
        return _this;
    }
    Object.defineProperty(IntegrationMainSettings.prototype, "initialData", {
        get: function () {
            var integration = this.props.integration;
            return {
                name: integration.name,
                domain: integration.domainName || '',
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationMainSettings.prototype, "formFields", {
        get: function () {
            var fields = [
                {
                    name: 'name',
                    type: 'string',
                    required: false,
                    label: t('Integration Name'),
                },
                {
                    name: 'domain',
                    type: 'string',
                    required: false,
                    label: t('Full URL'),
                },
            ];
            return fields;
        },
        enumerable: false,
        configurable: true
    });
    IntegrationMainSettings.prototype.render = function () {
        var integration = this.state.integration;
        var organization = this.props.organization;
        return (<Form initialData={this.initialData} apiMethod="PUT" apiEndpoint={"/organizations/" + organization.slug + "/integrations/" + integration.id + "/"} onSubmitSuccess={this.handleSubmitSuccess} submitLabel={t('Save Settings')}>
        <JsonForm fields={this.formFields}/>
      </Form>);
    };
    return IntegrationMainSettings;
}(React.Component));
export default IntegrationMainSettings;
//# sourceMappingURL=integrationMainSettings.jsx.map