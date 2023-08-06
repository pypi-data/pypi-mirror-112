import { __extends, __makeTemplateObject } from "tslib";
import { Component, Fragment } from 'react';
import styled from '@emotion/styled';
import { addErrorMessage } from 'app/actionCreators/indicator';
import ExternalLink from 'app/components/links/externalLink';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import Form from 'app/views/settings/components/forms/form';
import NumberField from 'app/views/settings/components/forms/numberField';
import RadioField from 'app/views/settings/components/forms/radioField';
var impacts = [
    tct("[strong:Quota applies.] Every event you choose to reprocess counts against your plan's quota. Rate limits and spike protection do not apply.", { strong: <strong /> }),
    tct('[strong:Attachment storage required.] If your events come from minidumps or unreal crash reports, you must have [link:attachment storage] enabled.', {
        strong: <strong />,
        link: (<ExternalLink href="https://docs.sentry.io/platforms/native/enriching-events/attachments/#crash-reports-and-privacy"/>),
    }),
    t('Please wait one hour after upload before attempting to reprocess missing debug files.'),
];
var remainingEventsChoices = [
    ['keep', t('Keep')],
    ['delete', t('Delete')],
];
var ReprocessingEventModal = /** @class */ (function (_super) {
    __extends(ReprocessingEventModal, _super);
    function ReprocessingEventModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { maxEvents: undefined };
        _this.handleSuccess = function () {
            var closeModal = _this.props.closeModal;
            closeModal();
            window.location.reload();
        };
        _this.handleMaxEventsChange = function (maxEvents) {
            _this.setState({ maxEvents: Number(maxEvents) || undefined });
        };
        return _this;
    }
    ReprocessingEventModal.prototype.handleError = function () {
        addErrorMessage(t('Failed to reprocess. Please check your input.'));
    };
    ReprocessingEventModal.prototype.render = function () {
        var _a = this.props, organization = _a.organization, Header = _a.Header, Body = _a.Body, closeModal = _a.closeModal, groupId = _a.groupId;
        var maxEvents = this.state.maxEvents;
        var orgSlug = organization.slug;
        var endpoint = "/organizations/" + orgSlug + "/issues/" + groupId + "/reprocessing/";
        var title = t('Reprocess Events');
        return (<Fragment>
        <Header closeButton>{title}</Header>
        <Body>
          <Introduction>
            {t('Reprocessing applies new debug files and grouping enhancements to this Issue. Please consider these impacts:')}
          </Introduction>
          <StyledList symbol="bullet">
            {impacts.map(function (impact, index) { return (<ListItem key={index}>{impact}</ListItem>); })}
          </StyledList>
          <Introduction>
            {tct('For more information, please refer to [link:the documentation.]', {
                link: (<ExternalLink href="https://docs.sentry.io/product/error-monitoring/reprocessing/"/>),
            })}
          </Introduction>
          <Form submitLabel={title} apiEndpoint={endpoint} apiMethod="POST" initialData={{ maxEvents: undefined, remainingEvents: 'keep' }} onSubmitSuccess={this.handleSuccess} onSubmitError={this.handleError} onCancel={closeModal} footerClass="modal-footer">
            <NumberField name="maxEvents" label={t('Number of events to be reprocessed')} help={t('If you set a limit, we will reprocess your most recent events.')} placeholder={t('Reprocess all events')} onChange={this.handleMaxEventsChange} min={1}/>

            <RadioField orientInline label={t('Remaining events')} help={t('What to do with the events that are not reprocessed.')} name="remainingEvents" choices={remainingEventsChoices} disabled={maxEvents === undefined}/>
          </Form>
        </Body>
      </Fragment>);
    };
    return ReprocessingEventModal;
}(Component));
export default ReprocessingEventModal;
var Introduction = styled('p')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var StyledList = styled(List)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  font-size: ", ";\n"], ["\n  grid-gap: ", ";\n  margin-bottom: ", ";\n  font-size: ", ";\n"])), space(1), space(4), function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=reprocessEventModal.jsx.map