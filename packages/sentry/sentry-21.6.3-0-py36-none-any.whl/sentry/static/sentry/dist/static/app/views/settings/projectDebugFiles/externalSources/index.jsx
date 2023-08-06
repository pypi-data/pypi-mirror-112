import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import BuildInSymbolSources from './buildInSymbolSources';
import SymbolSources from './symbolSources';
function ExternalSources(_a) {
    var api = _a.api, organization = _a.organization, symbolSources = _a.symbolSources, builtinSymbolSources = _a.builtinSymbolSources, builtinSymbolSourceOptions = _a.builtinSymbolSourceOptions, projectSlug = _a.projectSlug, location = _a.location, router = _a.router;
    return (<Panel>
      <PanelHeader>{t('External Sources')}</PanelHeader>
      <PanelBody>
        <SymbolSources api={api} location={location} router={router} organization={organization} symbolSources={symbolSources} projectSlug={projectSlug}/>
        <BuildInSymbolSources api={api} organization={organization} builtinSymbolSources={builtinSymbolSources} builtinSymbolSourceOptions={builtinSymbolSourceOptions} projectSlug={projectSlug}/>
      </PanelBody>
    </Panel>);
}
export default ExternalSources;
//# sourceMappingURL=index.jsx.map