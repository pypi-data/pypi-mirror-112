import { Fragment } from 'react';
import isObject from 'lodash/isObject';
import GroupingComponent, { GroupingComponentListItem, GroupingValue, } from './groupingComponent';
import { groupingComponentFilter } from './utils';
var GroupingComponentChildren = function (_a) {
    var component = _a.component, showNonContributing = _a.showNonContributing;
    return (<Fragment>
      {component.values
            .filter(function (value) { return groupingComponentFilter(value, showNonContributing); })
            .map(function (value, idx) { return (<GroupingComponentListItem key={idx}>
            {isObject(value) ? (<GroupingComponent component={value} showNonContributing={showNonContributing}/>) : (<GroupingValue valueType={component.name || component.id}>
                {typeof value === 'string' || typeof value === 'number'
                    ? value
                    : JSON.stringify(value, null, 2)}
              </GroupingValue>)}
          </GroupingComponentListItem>); })}
    </Fragment>);
};
export default GroupingComponentChildren;
//# sourceMappingURL=groupingComponentChildren.jsx.map