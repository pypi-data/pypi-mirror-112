import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import { PanelAlert, PanelItem } from 'app/components/panels';
import accountPasswordFields from 'app/data/forms/accountPassword';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
function PasswordForm() {
    function handleSubmitSuccess(_change, model) {
        // Reset form on success
        model.resetForm();
        addSuccessMessage('Password has been changed');
    }
    function handleSubmitError() {
        addErrorMessage('Error changing password');
    }
    var user = ConfigStore.get('user');
    return (<Form apiMethod="PUT" apiEndpoint="/users/me/password/" initialData={{}} onSubmitSuccess={handleSubmitSuccess} onSubmitError={handleSubmitError} hideFooter>
      <JsonForm forms={accountPasswordFields} additionalFieldProps={{ user: user }} renderFooter={function () { return (<Actions>
            <Button type="submit" priority="primary">
              {t('Change password')}
            </Button>
          </Actions>); }} renderHeader={function () { return (<PanelAlert type="info">
            {t('Changing your password will invalidate all logged in sessions.')}
          </PanelAlert>); }}/>
    </Form>);
}
var Actions = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
export default PasswordForm;
var templateObject_1;
//# sourceMappingURL=passwordForm.jsx.map