import * as React from 'react';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import Hovercard from 'app/components/hovercard';
import { t } from 'app/locale';
/**
 * Provide a component that passes a prop to indicate if the current
 * organization doesn't have access to discover results.
 */
function DiscoverFeature(_a) {
    var children = _a.children;
    var noFeatureMessage = t('Requires discover feature.');
    var renderDisabled = function (p) { return (<Hovercard body={<FeatureDisabled features={p.features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
      {p.children(p)}
    </Hovercard>); };
    return (<Feature hookName="feature-disabled:open-discover" features={['organizations:discover-basic']} renderDisabled={renderDisabled}>
      {function (_a) {
        var hasFeature = _a.hasFeature;
        return children({ hasFeature: hasFeature });
    }}
    </Feature>);
}
export default DiscoverFeature;
//# sourceMappingURL=discoverFeature.jsx.map