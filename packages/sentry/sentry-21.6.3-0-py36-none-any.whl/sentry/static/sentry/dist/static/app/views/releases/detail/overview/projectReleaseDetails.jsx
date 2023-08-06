import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import Count from 'app/components/count';
import DateTime from 'app/components/dateTime';
import { KeyValueTable, KeyValueTableRow } from 'app/components/keyValueTable';
import Link from 'app/components/links/link';
import TextOverflow from 'app/components/textOverflow';
import TimeSince from 'app/components/timeSince';
import Version from 'app/components/version';
import { t, tn } from 'app/locale';
import { SectionHeading, Wrapper } from './styles';
var ProjectReleaseDetails = function (_a) {
    var _b;
    var release = _a.release, releaseMeta = _a.releaseMeta, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug;
    var version = release.version, versionInfo = release.versionInfo, dateCreated = release.dateCreated, firstEvent = release.firstEvent, lastEvent = release.lastEvent;
    return (<Wrapper>
      <SectionHeading>{t('Project Release Details')}</SectionHeading>
      <KeyValueTable>
        <KeyValueTableRow keyName={t('Created')} value={<DateTime date={dateCreated} seconds={false}/>}/>
        <KeyValueTableRow keyName={t('Version')} value={<Version version={version} anchor={false}/>}/>
        <KeyValueTableRow keyName={t('Package')} value={<StyledTextOverflow ellipsisDirection="left">
              {(_b = versionInfo.package) !== null && _b !== void 0 ? _b : '\u2014'}
            </StyledTextOverflow>}/>
        <KeyValueTableRow keyName={t('First Event')} value={firstEvent ? <TimeSince date={firstEvent}/> : '\u2014'}/>
        <KeyValueTableRow keyName={t('Last Event')} value={lastEvent ? <TimeSince date={lastEvent}/> : '\u2014'}/>
        <KeyValueTableRow keyName={t('Source Maps')} value={<Link to={"/settings/" + orgSlug + "/projects/" + projectSlug + "/source-maps/" + encodeURIComponent(version) + "/"}>
              <Count value={releaseMeta.releaseFileCount}/>{' '}
              {tn('artifact', 'artifacts', releaseMeta.releaseFileCount)}
            </Link>}/>
      </KeyValueTable>
    </Wrapper>);
};
var StyledTextOverflow = styled(TextOverflow)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  line-height: inherit;\n  text-align: right;\n"], ["\n  line-height: inherit;\n  text-align: right;\n"])));
export default ProjectReleaseDetails;
var templateObject_1;
//# sourceMappingURL=projectReleaseDetails.jsx.map