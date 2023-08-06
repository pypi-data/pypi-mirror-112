import { __read } from "tslib";
import * as React from 'react';
import Button from 'app/components/button';
import { t, tn } from 'app/locale';
/**
 * This component is used to show first X items and collapse the rest
 */
var Collapsible = function (_a) {
    var collapseButton = _a.collapseButton, expandButton = _a.expandButton, _b = _a.maxVisibleItems, maxVisibleItems = _b === void 0 ? 5 : _b, children = _a.children;
    var _c = __read(React.useState(true), 2), isCollapsed = _c[0], setCollapsed = _c[1];
    var handleCollapseToggle = function () { return setCollapsed(!isCollapsed); };
    var items = React.Children.toArray(children);
    var canCollapse = items.length > maxVisibleItems;
    if (!canCollapse) {
        return <React.Fragment>{children}</React.Fragment>;
    }
    var visibleItems = isCollapsed ? items.slice(0, maxVisibleItems) : items;
    var numberOfHiddenItems = items.length - visibleItems.length;
    var showDefault = (numberOfHiddenItems > 0 && !expandButton) ||
        (numberOfHiddenItems === 0 && !collapseButton);
    return (<React.Fragment>
      {visibleItems}

      {showDefault && (<Button priority="link" onClick={handleCollapseToggle}>
          {isCollapsed
                ? tn('Show %s hidden item', 'Show %s hidden items', numberOfHiddenItems)
                : t('Collapse')}
        </Button>)}

      {numberOfHiddenItems > 0 &&
            (expandButton === null || expandButton === void 0 ? void 0 : expandButton({ onExpand: handleCollapseToggle, numberOfHiddenItems: numberOfHiddenItems }))}
      {numberOfHiddenItems === 0 && (collapseButton === null || collapseButton === void 0 ? void 0 : collapseButton({ onCollapse: handleCollapseToggle }))}
    </React.Fragment>);
};
export default Collapsible;
//# sourceMappingURL=collapsible.jsx.map