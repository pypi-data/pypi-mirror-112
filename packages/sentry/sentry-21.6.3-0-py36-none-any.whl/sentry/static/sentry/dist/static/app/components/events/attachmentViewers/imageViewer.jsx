import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { getAttachmentUrl, } from 'app/components/events/attachmentViewers/utils';
import { PanelItem } from 'app/components/panels';
export default function ImageViewer(props) {
    return (<Container>
      <img src={getAttachmentUrl(props, true)}/>
    </Container>);
}
var Container = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  justify-content: center;\n"], ["\n  justify-content: center;\n"])));
var templateObject_1;
//# sourceMappingURL=imageViewer.jsx.map