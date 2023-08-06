import { __extends } from "tslib";
import { PureComponent } from 'react';
import { Panel, PanelBody } from 'app/components/panels';
import SelectMembers from 'app/components/selectMembers';
import { t } from 'app/locale';
import FormField from 'app/views/settings/components/forms/formField';
import TextField from 'app/views/settings/components/forms/textField';
var RuleNameOwnerForm = /** @class */ (function (_super) {
    __extends(RuleNameOwnerForm, _super);
    function RuleNameOwnerForm() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RuleNameOwnerForm.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, project = _a.project, organization = _a.organization, userTeamIds = _a.userTeamIds;
        return (<Panel>
        <PanelBody>
          <TextField disabled={disabled} name="name" label={t('Rule Name')} help={t('Add a name so it’s easy to find later.')} placeholder={t('Something really bad happened')} required/>

          <FormField name="owner" label={t('Team')} help={t('The team that can edit this alert.')} disabled={disabled}>
            {function (_a) {
                var model = _a.model;
                var owner = model.getValue('owner');
                var ownerId = owner && owner.split(':')[1];
                var filteredTeamIds = new Set(userTeamIds);
                // Add the current team that owns the alert
                if (ownerId) {
                    filteredTeamIds.add(ownerId);
                }
                return (<SelectMembers showTeam project={project} organization={organization} value={ownerId} onChange={function (_a) {
                        var value = _a.value;
                        var ownerValue = value && "team:" + value;
                        model.setValue('owner', ownerValue);
                    }} filteredTeamIds={filteredTeamIds} includeUnassigned disabled={disabled}/>);
            }}
          </FormField>
        </PanelBody>
      </Panel>);
    };
    return RuleNameOwnerForm;
}(PureComponent));
export default RuleNameOwnerForm;
//# sourceMappingURL=ruleNameOwnerForm.jsx.map