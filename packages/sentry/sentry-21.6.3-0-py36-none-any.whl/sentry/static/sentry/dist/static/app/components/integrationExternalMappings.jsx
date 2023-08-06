import { __extends, __makeTemplateObject } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import capitalize from 'lodash/capitalize';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import Tooltip from 'app/components/tooltip';
import { IconAdd, IconDelete, IconEdit } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { getIntegrationIcon } from 'app/utils/integrationUtil';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
var IntegrationExternalMappings = /** @class */ (function (_super) {
    __extends(IntegrationExternalMappings, _super);
    function IntegrationExternalMappings() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IntegrationExternalMappings.prototype.render = function () {
        var _a = this.props, integration = _a.integration, mappings = _a.mappings, type = _a.type, onCreateOrEdit = _a.onCreateOrEdit, onDelete = _a.onDelete;
        return (<Fragment>
        <Panel>
          <PanelHeader disablePadding hasButtons>
            <HeaderLayout>
              <ExternalNameColumn>{tct('External [type]', { type: type })}</ExternalNameColumn>
              <SentryNameColumn>{tct('Sentry [type]', { type: type })}</SentryNameColumn>
              <ButtonColumn>
                <AddButton data-test-id="add-mapping-button" onClick={function () { return onCreateOrEdit(); }} size="xsmall" icon={<IconAdd size="xs" isCircled/>}>
                  {tct('Add [type] Mapping', { type: type })}
                </AddButton>
              </ButtonColumn>
            </HeaderLayout>
          </PanelHeader>
          <PanelBody>
            {!mappings.length && (<EmptyMessage icon={getIntegrationIcon(integration.provider.key, 'lg')}>
                {tct('Set up External [type] Mappings.', { type: capitalize(type) })}
              </EmptyMessage>)}
            {mappings.map(function (item) { return (<Access access={['org:integrations']} key={item.id}>
                {function (_a) {
                    var hasAccess = _a.hasAccess;
                    return (<ConfigPanelItem>
                    <Layout>
                      <ExternalNameColumn>{item.externalName}</ExternalNameColumn>
                      <SentryNameColumn>{item.sentryName}</SentryNameColumn>
                      <ButtonColumn>
                        <Tooltip title={t('You must be an organization owner, manager or admin to edit or remove an external user mapping.')} disabled={hasAccess}>
                          <StyledButton size="small" icon={<IconEdit size="sm"/>} label={t('edit')} disabled={!hasAccess} onClick={function () { return onCreateOrEdit(item); }}/>
                          <Confirm disabled={!hasAccess} onConfirm={function () { return onDelete(item); }} message={t('Are you sure you want to remove this external user mapping?')}>
                            <StyledButton size="small" icon={<IconDelete size="sm"/>} label={t('delete')} disabled={!hasAccess}/>
                          </Confirm>
                        </Tooltip>
                      </ButtonColumn>
                    </Layout>
                  </ConfigPanelItem>);
                }}
              </Access>); })}
          </PanelBody>
        </Panel>
      </Fragment>);
    };
    return IntegrationExternalMappings;
}(Component));
export default IntegrationExternalMappings;
var AddButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  text-transform: capitalize;\n"], ["\n  text-transform: capitalize;\n"])));
var Layout = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  grid-template-columns: 2.5fr 2.5fr 1fr;\n  grid-template-areas: 'external-name sentry-name button';\n"], ["\n  display: grid;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  grid-template-columns: 2.5fr 2.5fr 1fr;\n  grid-template-areas: 'external-name sentry-name button';\n"])), space(1));
var HeaderLayout = styled(Layout)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  align-items: center;\n  margin: 0;\n  margin-left: ", ";\n  text-transform: uppercase;\n"], ["\n  align-items: center;\n  margin: 0;\n  margin-left: ", ";\n  text-transform: uppercase;\n"])), space(2));
var ConfigPanelItem = styled(PanelItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject([""], [""])));
var StyledButton = styled(Button)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space(0.5));
// Columns below
var Column = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  overflow: hidden;\n  overflow-wrap: break-word;\n"], ["\n  overflow: hidden;\n  overflow-wrap: break-word;\n"])));
var ExternalNameColumn = styled(Column)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  grid-area: external-name;\n"], ["\n  grid-area: external-name;\n"])));
var SentryNameColumn = styled(Column)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  grid-area: sentry-name;\n"], ["\n  grid-area: sentry-name;\n"])));
var ButtonColumn = styled(Column)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  grid-area: button;\n  text-align: right;\n"], ["\n  grid-area: button;\n  text-align: right;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=integrationExternalMappings.jsx.map