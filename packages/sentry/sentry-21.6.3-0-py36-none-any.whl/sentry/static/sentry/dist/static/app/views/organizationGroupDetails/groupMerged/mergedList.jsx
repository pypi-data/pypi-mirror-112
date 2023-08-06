import { Fragment } from 'react';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody } from 'app/components/panels';
import QueryCount from 'app/components/queryCount';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
import MergedItem from './mergedItem';
import MergedToolbar from './mergedToolbar';
function MergedList(_a) {
    var _b = _a.fingerprints, fingerprints = _b === void 0 ? [] : _b, pageLinks = _a.pageLinks, onToggleCollapse = _a.onToggleCollapse, onUnmerge = _a.onUnmerge, organization = _a.organization, groupId = _a.groupId, project = _a.project;
    var fingerprintsWithLatestEvent = fingerprints.filter(function (_a) {
        var latestEvent = _a.latestEvent;
        return !!latestEvent;
    });
    var hasResults = fingerprintsWithLatestEvent.length > 0;
    if (!hasResults) {
        return (<Panel>
        <EmptyStateWarning>
          <p>{t("There don't seem to be any hashes for this issue.")}</p>
        </EmptyStateWarning>
      </Panel>);
    }
    return (<Fragment>
      <h2>
        <span>{t('Merged fingerprints with latest event')}</span>{' '}
        <QueryCount count={fingerprintsWithLatestEvent.length}/>
      </h2>

      <Panel>
        <MergedToolbar onToggleCollapse={onToggleCollapse} onUnmerge={onUnmerge} orgId={organization.slug} project={project} groupId={groupId}/>

        <PanelBody>
          {fingerprintsWithLatestEvent.map(function (fingerprint) { return (<MergedItem key={fingerprint.id} organization={organization} fingerprint={fingerprint}/>); })}
        </PanelBody>
      </Panel>
      {pageLinks && <Pagination pageLinks={pageLinks}/>}
    </Fragment>);
}
export default withOrganization(MergedList);
//# sourceMappingURL=mergedList.jsx.map