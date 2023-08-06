import { __assign, __makeTemplateObject } from "tslib";
import { Fragment } from 'react';
import { withRouter } from 'react-router';
import { css } from '@emotion/react';
import { getDebugSourceName } from 'app/data/debugFileSources';
import { tct } from 'app/locale';
import FieldFromConfig from 'app/views/settings/components/forms/fieldFromConfig';
import Form from 'app/views/settings/components/forms/form';
import AppStoreConnect from './appStoreConnect';
import { getFormFields, getInitialData } from './utils';
function DebugFileCustomRepository(_a) {
    var Header = _a.Header, Body = _a.Body, Footer = _a.Footer, onSave = _a.onSave, sourceConfig = _a.sourceConfig, sourceType = _a.sourceType, _b = _a.params, orgId = _b.orgId, projectSlug = _b.projectId, location = _a.location, appStoreConnectContext = _a.appStoreConnectContext, closeModal = _a.closeModal;
    function handleSave(data) {
        onSave(__assign(__assign({}, data), { type: sourceType })).then(function () {
            closeModal();
            if (sourceType === 'appStoreConnect' &&
                (appStoreConnectContext === null || appStoreConnectContext === void 0 ? void 0 : appStoreConnectContext.updateAlertMessage)) {
                window.location.reload();
            }
        });
    }
    if (sourceType === 'appStoreConnect') {
        return (<AppStoreConnect Header={Header} Body={Body} Footer={Footer} orgSlug={orgId} projectSlug={projectSlug} onSubmit={handleSave} initialData={sourceConfig} location={location} appStoreConnectContext={appStoreConnectContext}/>);
    }
    var fields = getFormFields(sourceType);
    var initialData = getInitialData(sourceConfig);
    return (<Fragment>
      <Header closeButton>
        {sourceConfig
            ? tct('Update [name] Repository', { name: getDebugSourceName(sourceType) })
            : tct('Add [name] Repository', { name: getDebugSourceName(sourceType) })}
      </Header>
      {fields && (<Form allowUndo requireChanges initialData={initialData} onSubmit={handleSave} footerClass="modal-footer">
          {fields.map(function (field, i) { return (<FieldFromConfig key={field.name || i} field={field} inline={false} stacked/>); })}
        </Form>)}
    </Fragment>);
}
export default withRouter(DebugFileCustomRepository);
export var modalCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n  max-width: 680px;\n"], ["\n  width: 100%;\n  max-width: 680px;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map