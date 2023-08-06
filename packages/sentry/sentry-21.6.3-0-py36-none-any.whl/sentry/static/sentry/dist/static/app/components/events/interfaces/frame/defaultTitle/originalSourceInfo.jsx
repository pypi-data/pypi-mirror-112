import { Fragment } from 'react';
import { t } from 'app/locale';
import { defined } from 'app/utils';
// TODO(Priscila): Remove BR tags
// mapUrl not always present; e.g. uploaded source maps
var OriginalSourceInfo = function (_a) {
    var mapUrl = _a.mapUrl, map = _a.map;
    if (!defined(map) && !defined(mapUrl)) {
        return null;
    }
    return (<Fragment>
      <strong>{t('Source Map')}</strong>
      <br />
      {mapUrl !== null && mapUrl !== void 0 ? mapUrl : map}
      <br />
    </Fragment>);
};
export default OriginalSourceInfo;
//# sourceMappingURL=originalSourceInfo.jsx.map