import { __rest } from "tslib";
import * as React from 'react';
import Button from 'app/components/button';
import DiscoverFeature from 'app/components/discover/discoverFeature';
/**
 * Provide a button that turns itself off if the current organization
 * doesn't have access to discover results.
 */
function DiscoverButton(_a) {
    var children = _a.children, buttonProps = __rest(_a, ["children"]);
    return (<DiscoverFeature>
      {function (_a) {
            var hasFeature = _a.hasFeature;
            return (<Button disabled={!hasFeature} {...buttonProps}>
          {children}
        </Button>);
        }}
    </DiscoverFeature>);
}
export default DiscoverButton;
//# sourceMappingURL=discoverButton.jsx.map