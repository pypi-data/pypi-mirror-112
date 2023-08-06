import React from 'react';
import ReactDOM from 'react-dom';
export function renderDom(Component, container, props) {
    if (props === void 0) { props = {}; }
    var rootEl = document.querySelector(container);
    // Note: On pages like `SetupWizard`, we will attempt to mount main App
    // but will fail because the DOM el wasn't found (which is intentional)
    if (!rootEl) {
        return;
    }
    ReactDOM.render(<Component {...props}/>, rootEl);
}
//# sourceMappingURL=renderDom.jsx.map