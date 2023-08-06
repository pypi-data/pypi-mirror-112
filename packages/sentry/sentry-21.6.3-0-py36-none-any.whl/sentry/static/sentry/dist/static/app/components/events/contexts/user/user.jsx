import { __read, __spreadArray } from "tslib";
import UserAvatar from 'app/components/avatar/userAvatar';
import ErrorBoundary from 'app/components/errorBoundary';
import ContextBlock from 'app/components/events/contexts/contextBlock';
import KeyValueList from 'app/components/events/interfaces/keyValueList';
import { removeFilterMaskedEntries } from 'app/components/events/interfaces/utils';
import { getMeta } from 'app/components/events/meta/metaProxy';
import { defined } from 'app/utils';
import getUnknownData from '../getUnknownData';
import getUserKnownData from './getUserKnownData';
import { UserIgnoredDataType, UserKnownDataType } from './types';
var userKnownDataValues = [
    UserKnownDataType.ID,
    UserKnownDataType.EMAIL,
    UserKnownDataType.USERNAME,
    UserKnownDataType.IP_ADDRESS,
    UserKnownDataType.NAME,
];
var userIgnoredDataValues = [UserIgnoredDataType.DATA];
function User(_a) {
    var data = _a.data;
    return (<div className="user-widget">
      <div className="pull-left">
        <UserAvatar user={removeFilterMaskedEntries(data)} size={48} gravatar={false}/>
      </div>
      <ContextBlock data={getUserKnownData(data, userKnownDataValues)}/>
      <ContextBlock data={getUnknownData(data, __spreadArray(__spreadArray([], __read(userKnownDataValues)), __read(userIgnoredDataValues)))}/>
      {defined(data === null || data === void 0 ? void 0 : data.data) && (<ErrorBoundary mini>
          <KeyValueList data={Object.entries(data.data).map(function (_a) {
                var _b = __read(_a, 2), key = _b[0], value = _b[1];
                return ({
                    key: key,
                    value: value,
                    subject: key,
                    meta: getMeta(data.data, key),
                });
            })} isContextData/>
        </ErrorBoundary>)}
    </div>);
}
export default User;
//# sourceMappingURL=user.jsx.map