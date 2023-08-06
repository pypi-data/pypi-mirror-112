import { __extends, __makeTemplateObject } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import TextBlock from 'app/views/settings/components/text/textBlock';
import OwnerInput from 'app/views/settings/project/projectOwnership/ownerInput';
var EditOwnershipRulesModal = /** @class */ (function (_super) {
    __extends(EditOwnershipRulesModal, _super);
    function EditOwnershipRulesModal() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EditOwnershipRulesModal.prototype.render = function () {
        var ownership = this.props.ownership;
        return (<Fragment>
        <Block>
          {t('Rules follow the pattern: ')} <code>type:glob owner owner</code>
        </Block>
        <Block>
          {t('Owners can be team identifiers starting with #, or user emails')}
        </Block>
        <Block>
          {t('Globbing Syntax:')}
          <CodeBlock>{'* matches everything\n? matches any single character'}</CodeBlock>
        </Block>
        <Block>
          {t('Examples')}
          <CodeBlock>
            path:src/example/pipeline/* person@sentry.io #infrastructure
            {'\n'}
            url:http://example.com/settings/* #product
            {'\n'}
            tags.sku_class:enterprise #enterprise
          </CodeBlock>
        </Block>
        {ownership && <OwnerInput {...this.props} initialText={ownership.raw || ''}/>}
      </Fragment>);
    };
    return EditOwnershipRulesModal;
}(Component));
var Block = styled(TextBlock)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 16px;\n"], ["\n  margin-bottom: 16px;\n"])));
var CodeBlock = styled('pre')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  word-break: break-all;\n  white-space: pre-wrap;\n"], ["\n  word-break: break-all;\n  white-space: pre-wrap;\n"])));
export default EditOwnershipRulesModal;
var templateObject_1, templateObject_2;
//# sourceMappingURL=editRulesModal.jsx.map