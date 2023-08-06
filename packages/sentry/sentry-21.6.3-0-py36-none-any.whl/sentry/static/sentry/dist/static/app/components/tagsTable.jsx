import { __makeTemplateObject } from "tslib";
import * as React from 'react';
import styled from '@emotion/styled';
import capitalize from 'lodash/capitalize';
import { SectionHeading } from 'app/components/charts/styles';
import { getMeta, withMeta } from 'app/components/events/meta/metaProxy';
import { KeyValueTable, KeyValueTableRow } from 'app/components/keyValueTable';
import Link from 'app/components/links/link';
import Tooltip from 'app/components/tooltip';
import Version from 'app/components/version';
import { t } from 'app/locale';
import space from 'app/styles/space';
var TagsTable = function (_a) {
    var event = _a.event, query = _a.query, generateUrl = _a.generateUrl, _b = _a.title, title = _b === void 0 ? t('Tag Details') : _b;
    var eventWithMeta = withMeta(event);
    var tags = eventWithMeta.tags;
    var formatErrorKind = function (kind) {
        return capitalize(kind.replace(/_/g, ' '));
    };
    var getErrorMessage = function (error) {
        var _a;
        if (Array.isArray(error)) {
            if ((_a = error[1]) === null || _a === void 0 ? void 0 : _a.reason) {
                return formatErrorKind(error[1].reason);
            }
            else {
                return formatErrorKind(error[0]);
            }
        }
        return formatErrorKind(error);
    };
    var getTooltipTitle = function (errors) {
        return <TooltipTitle>{getErrorMessage(errors[0])}</TooltipTitle>;
    };
    return (<StyledTagsTable>
      <SectionHeading>{title}</SectionHeading>
      <KeyValueTable>
        {tags.map(function (tag) {
            var _a, _b, _c;
            var tagInQuery = query.includes(tag.key + ":");
            var target = tagInQuery ? undefined : generateUrl(tag);
            var keyMetaData = getMeta(tag, 'key');
            var valueMetaData = getMeta(tag, 'value');
            var renderTagValue = function () {
                switch (tag.key) {
                    case 'release':
                        return <Version version={tag.value} anchor={false} withPackage/>;
                    default:
                        return tag.value;
                }
            };
            return (<KeyValueTableRow key={tag.key} keyName={((_a = keyMetaData === null || keyMetaData === void 0 ? void 0 : keyMetaData.err) === null || _a === void 0 ? void 0 : _a.length) ? (<Tooltip title={getTooltipTitle(keyMetaData.err)}>
                    <i>{"<" + t('invalid') + ">"}</i>
                  </Tooltip>) : (tag.key)} value={((_b = valueMetaData === null || valueMetaData === void 0 ? void 0 : valueMetaData.err) === null || _b === void 0 ? void 0 : _b.length) ? (<Tooltip title={getTooltipTitle(valueMetaData.err)}>
                    <i>{"<" + t('invalid') + ">"}</i>
                  </Tooltip>) : ((_c = keyMetaData === null || keyMetaData === void 0 ? void 0 : keyMetaData.err) === null || _c === void 0 ? void 0 : _c.length) ? (<span>{renderTagValue()}</span>) : tagInQuery ? (<Tooltip title={t('This tag is in the current filter conditions')}>
                    <span>{renderTagValue()}</span>
                  </Tooltip>) : (<Link to={target || ''}>{renderTagValue()}</Link>)}/>);
        })}
      </KeyValueTable>
    </StyledTagsTable>);
};
export default TagsTable;
var StyledTagsTable = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var TooltipTitle = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=tagsTable.jsx.map