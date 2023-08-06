import { __extends } from "tslib";
import React from 'react';
import { IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import { FieldFromConfig } from 'app/views/settings/components/forms';
import Form from 'app/views/settings/components/forms/form';
import Alert from './alert';
var RepositoryEditForm = /** @class */ (function (_super) {
    __extends(RepositoryEditForm, _super);
    function RepositoryEditForm() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(RepositoryEditForm.prototype, "initialData", {
        get: function () {
            var repository = this.props.repository;
            return {
                name: repository.name,
                url: repository.url || '',
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(RepositoryEditForm.prototype, "formFields", {
        get: function () {
            var fields = [
                {
                    name: 'name',
                    type: 'string',
                    required: true,
                    label: t('Name of your repository.'),
                },
                {
                    name: 'url',
                    type: 'string',
                    required: false,
                    label: t('Full URL to your repository.'),
                    placeholder: t('https://github.com/my-org/my-repo/'),
                },
            ];
            return fields;
        },
        enumerable: false,
        configurable: true
    });
    RepositoryEditForm.prototype.render = function () {
        var _this = this;
        var _a = this.props, onCancel = _a.onCancel, orgSlug = _a.orgSlug, repository = _a.repository;
        var endpoint = "/organizations/" + orgSlug + "/repos/" + repository.id + "/";
        return (<Form initialData={this.initialData} onSubmitSuccess={function (data) {
                _this.props.onSubmitSuccess(data);
                _this.props.closeModal();
            }} apiEndpoint={endpoint} apiMethod="PUT" onCancel={onCancel}>
        <Alert type="warning" icon={<IconWarning />}>
          {tct('Changing the [name:repo name] may have consequences if it no longer matches the repo name used when [link:sending commits with releases].', {
                link: (<a href="https://docs.sentry.io/product/cli/releases/#sentry-cli-commit-integration"/>),
                name: <strong>repo name</strong>,
            })}
        </Alert>
        {this.formFields.map(function (field) { return (<FieldFromConfig key={field.name} field={field} inline={false} stacked flexibleControlStateSize/>); })}
      </Form>);
    };
    return RepositoryEditForm;
}(React.Component));
export default RepositoryEditForm;
//# sourceMappingURL=repositoryEditForm.jsx.map