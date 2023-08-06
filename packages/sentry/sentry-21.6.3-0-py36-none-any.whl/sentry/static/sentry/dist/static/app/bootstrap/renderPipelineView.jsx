import ReactDOM from 'react-dom';
import { ROOT_ELEMENT } from 'app/constants';
import PipelineView from 'app/views/integrationPipeline/pipelineView';
function render(pipelineName, props) {
    var rootEl = document.getElementById(ROOT_ELEMENT);
    ReactDOM.render(<PipelineView pipelineName={pipelineName} {...props}/>, rootEl);
}
export function renderPipelineView() {
    var _a = window.__pipelineInitialData, name = _a.name, props = _a.props;
    render(name, props);
}
//# sourceMappingURL=renderPipelineView.jsx.map