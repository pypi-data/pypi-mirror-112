import * as React from 'react';
import Breadcrumbs from 'app/components/breadcrumbs';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Confirm from 'app/components/confirm';
import EditableText from 'app/components/editableText';
import * as Layout from 'app/components/layouts/thirds';
import { t } from 'app/locale';
function Header(_a) {
    var title = _a.title, orgSlug = _a.orgSlug, goBackLocation = _a.goBackLocation, dashboardTitle = _a.dashboardTitle, onChangeTitle = _a.onChangeTitle, onSave = _a.onSave, onDelete = _a.onDelete, isEditing = _a.isEditing;
    return (<Layout.Header>
      <Layout.HeaderContent>
        <Breadcrumbs crumbs={[
            {
                to: "/organizations/" + orgSlug + "/dashboards/",
                label: t('Dashboards'),
            },
            {
                to: goBackLocation,
                label: dashboardTitle,
            },
            { label: t('Widget Builder') },
        ]}/>
        <Layout.Title>
          <EditableText value={title} onChange={onChangeTitle} errorMessage={t('Please set a title for this widget')} successMessage={t('Widget title updated successfully')}/>
        </Layout.Title>
      </Layout.HeaderContent>

      <Layout.HeaderActions>
        <ButtonBar gap={1}>
          <Button title={t("You’re seeing the metrics project because you have the feature flag 'organizations:metrics' enabled. Send us feedback via email.")} href="mailto:metrics-feedback@sentry.io?subject=Metrics Feedback">
            {t('Give Feedback')}
          </Button>
          <Button to={goBackLocation}>{t('Cancel')}</Button>
          {isEditing && onDelete && (<Confirm priority="danger" message={t('Are you sure you want to delete this widget?')} onConfirm={onDelete}>
              <Button priority="danger">{t('Delete')}</Button>
            </Confirm>)}
          <Button priority="primary" onClick={onSave} disabled={!onSave} title={!onSave ? t('This feature is not yet available') : undefined}>
            {isEditing ? t('Update Widget') : t('Add Widget')}
          </Button>
        </ButtonBar>
      </Layout.HeaderActions>
    </Layout.Header>);
}
export default Header;
//# sourceMappingURL=header.jsx.map