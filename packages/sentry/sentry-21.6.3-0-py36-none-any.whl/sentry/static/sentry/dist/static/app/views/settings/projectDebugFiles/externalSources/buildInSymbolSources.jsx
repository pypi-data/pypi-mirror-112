import { __awaiter, __generator } from "tslib";
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import ProjectActions from 'app/actions/projectActions';
import { t } from 'app/locale';
import SelectField from 'app/views/settings/components/forms/selectField';
function BuildInSymbolSources(_a) {
    var api = _a.api, organization = _a.organization, builtinSymbolSourceOptions = _a.builtinSymbolSourceOptions, builtinSymbolSources = _a.builtinSymbolSources, projectSlug = _a.projectSlug;
    function getRequestMessages(builtinSymbolSourcesQuantity) {
        if (builtinSymbolSourcesQuantity > builtinSymbolSources.length) {
            return {
                successMessage: t('Successfully added built-in repository'),
                errorMessage: t('An error occurred while adding new built-in repository'),
            };
        }
        return {
            successMessage: t('Successfully removed built-in repository'),
            errorMessage: t('An error occurred while removing built-in repository'),
        };
    }
    function handleChange(value) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, successMessage, errorMessage, updatedProjectDetails, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = getRequestMessages(value.length), successMessage = _a.successMessage, errorMessage = _a.errorMessage;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + projectSlug + "/", {
                                method: 'PUT',
                                data: {
                                    builtinSymbolSources: value,
                                },
                            })];
                    case 2:
                        updatedProjectDetails = _c.sent();
                        ProjectActions.updateSuccess(updatedProjectDetails);
                        addSuccessMessage(successMessage);
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        addErrorMessage(errorMessage);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    return (<SelectField name="builtinSymbolSources" label={t('Built-in Repositories')} help={t('Configures which built-in repositories Sentry should use to resolve debug files.')} value={builtinSymbolSources} onChange={handleChange} choices={builtinSymbolSourceOptions === null || builtinSymbolSourceOptions === void 0 ? void 0 : builtinSymbolSourceOptions.filter(function (source) { return !source.hidden; }).map(function (source) { return [source.sentry_key, t(source.name)]; })} getValue={function (value) { return (value === null ? [] : value); }} flexibleControlStateSize multiple/>);
}
export default BuildInSymbolSources;
//# sourceMappingURL=buildInSymbolSources.jsx.map